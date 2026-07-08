"""Normalized multi-source literature search (Europe PMC / OpenAlex / Semantic Scholar).

Each `*_search` returns a list of normalized records:
  {source, id, title, abstract, year, doi, venue, citations, url, authors}
`search_all` merges + de-duplicates across sources by DOI/title. Cached via lbd._http.
Keyless where possible; uses .env keys (OpenAlex, Semantic Scholar, NCBI) when present.
"""
from __future__ import annotations

import re

from ..lbd import _http

_ENV = _http.load_env()

EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OPENALEX = "https://api.openalex.org/works"
SEMANTICSCHOLAR = "https://api.semanticscholar.org/graph/v1/paper/search"


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


# --- Europe PMC (biomedical; rich abstracts) --------------------------------------
def europepmc_search(query: str, n: int = 50) -> list[dict]:
    data = _http.get(EUROPEPMC, params={"query": query, "format": "json",
                                        "resultType": "core", "pageSize": min(n, 100)})
    out = []
    for r in (data.get("resultList", {}) or {}).get("result", []) or []:
        out.append({
            "source": "europepmc", "id": r.get("id"),
            "title": r.get("title"), "abstract": r.get("abstractText"),
            "year": r.get("pubYear"), "doi": (r.get("doi") or "").lower() or None,
            "venue": r.get("journalTitle"), "citations": r.get("citedByCount"),
            "url": f"https://europepmc.org/article/{r.get('source')}/{r.get('id')}"
                   if r.get("source") and r.get("id") else None,
            "authors": r.get("authorString"),
        })
    return out


# --- OpenAlex (breadth + citation counts; abstract via inverted index) -------------
def _deinvert(inv: dict | None) -> str | None:
    if not inv:
        return None
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos)) if pos else None


def openalex_search(query: str, n: int = 50) -> list[dict]:
    params = {"search": query, "per-page": min(n, 100),
              "select": "id,title,publication_year,doi,cited_by_count,"
                        "abstract_inverted_index,primary_location,authorships"}
    key = _ENV.get("OPENALEX_API_KEY")
    if key:
        params["api_key"] = key
    data = _http.get(OPENALEX, params=params)
    out = []
    for r in data.get("results", []) or []:
        loc = (r.get("primary_location") or {}).get("source") or {}
        auth = [a.get("author", {}).get("display_name") for a in r.get("authorships", [])[:6]]
        out.append({
            "source": "openalex", "id": r.get("id"), "title": r.get("title"),
            "abstract": _deinvert(r.get("abstract_inverted_index")),
            "year": r.get("publication_year"),
            "doi": (r.get("doi") or "").replace("https://doi.org/", "").lower() or None,
            "venue": loc.get("display_name"), "citations": r.get("cited_by_count"),
            "url": r.get("id"), "authors": ", ".join(a for a in auth if a),
        })
    return out


# --- Semantic Scholar (abstracts + TLDR + citation counts) -------------------------
def semanticscholar_search(query: str, n: int = 50) -> list[dict]:
    headers = {}
    key = _ENV.get("SEMANTIC_SCHOLAR_API_KEY")
    if key:
        headers["x-api-key"] = key
    data = _http.get(SEMANTICSCHOLAR, params={
        "query": query, "limit": min(n, 100),
        "fields": "title,abstract,year,externalIds,venue,citationCount,tldr,authors"},
        headers=headers or None)
    out = []
    for r in data.get("data", []) or []:
        doi = (r.get("externalIds") or {}).get("DOI")
        tldr = (r.get("tldr") or {}).get("text")
        out.append({
            "source": "semanticscholar", "id": r.get("paperId"), "title": r.get("title"),
            "abstract": r.get("abstract") or tldr, "tldr": tldr,
            "year": r.get("year"), "doi": (doi or "").lower() or None,
            "venue": r.get("venue"), "citations": r.get("citationCount"),
            "url": f"https://www.semanticscholar.org/paper/{r.get('paperId')}",
            "authors": ", ".join(a.get("name") for a in (r.get("authors") or [])[:6]),
        })
    return out


def search_all(query: str, n: int = 50) -> list[dict]:
    """Query all sources, merge + de-dup by DOI then normalized title."""
    recs = []
    for fn in (europepmc_search, openalex_search, semanticscholar_search):
        try:
            recs += fn(query, n)
        except Exception as e:  # one source down must not sink the search
            recs.append({"source": fn.__name__, "error": str(e)[:120]})
    seen, merged = {}, []
    for r in recs:
        if r.get("error"):
            continue
        key = r.get("doi") or _norm_title(r.get("title", ""))
        if not key:
            continue
        if key in seen:
            # keep the record with the longer abstract / more citations
            cur = merged[seen[key]]
            if (len(r.get("abstract") or "") > len(cur.get("abstract") or "")):
                cur["abstract"] = r["abstract"]
            cur["citations"] = max(cur.get("citations") or 0, r.get("citations") or 0)
            cur.setdefault("also_in", []).append(r["source"])
            continue
        seen[key] = len(merged)
        merged.append(r)
    merged.sort(key=lambda x: (x.get("citations") or 0), reverse=True)
    return merged
