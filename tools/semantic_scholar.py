"""Semantic Scholar (S2) lookup tool — search, paper details + TLDR, and related-work recommendations.

Rounds out the citation stack (CrossRef / PubMed / OpenAlex) with S2's unique signals: TLDR one-line
summaries, influential-citation counts, and a recommendations endpoint for discovering related work.
Reads SEMANTIC_SCHOLAR_API_KEY from .env (optional; raises rate limits).

Usage:
    python semantic_scholar.py search <query> [--n 8]     Top papers (title/year/DOI/cites/TLDR)
    python semantic_scholar.py paper <doi|s2id|arxiv>     One paper's details + TLDR
    python semantic_scholar.py recommend <doi|s2id> [--n 8]   Recommended related papers
    python semantic_scholar.py bibkey <doi>              Print a suggested bibtex key for a DOI

Dependencies: pip install requests python-dotenv
"""
from __future__ import annotations
import os, sys
import requests
try:
    from dotenv import load_dotenv
    # load .env from cwd or nearest parent
    from pathlib import Path
    p = Path.cwd()
    for cand in [p, *p.parents]:
        if (cand / ".env").exists():
            load_dotenv(cand / ".env"); break
except Exception:
    pass

S2 = "https://api.semanticscholar.org/graph/v1"
REC = "https://api.semanticscholar.org/recommendations/v1"
KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
HDR = {"x-api-key": KEY} if KEY else {}
FIELDS = "title,year,authors,externalIds,citationCount,influentialCitationCount,venue,tldr"


def _pid(ident: str) -> str:
    ident = ident.strip()
    if ident.lower().startswith("10."):
        return f"DOI:{ident}"
    if ident.lower().startswith(("arxiv:", "pmid:", "pmcid:", "corpusid:")):
        return ident
    return ident  # assume S2 paper id


def _fmt(p: dict) -> str:
    au = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:4])
    if p.get("authors") and len(p["authors"]) > 4:
        au += ", et al."
    doi = (p.get("externalIds") or {}).get("DOI", "")
    tldr = (p.get("tldr") or {}).get("text", "") if p.get("tldr") else ""
    lines = [f"  {p.get('title','(no title)')}",
             f"    {au}  |  {p.get('venue','')}  {p.get('year','')}",
             f"    DOI: {doi or '(none)'}  |  cites: {p.get('citationCount','?')} "
             f"(influential: {p.get('influentialCitationCount','?')})"]
    if tldr:
        lines.append(f"    TLDR: {tldr}")
    return "\n".join(lines)


def search(query: str, n: int = 8) -> None:
    r = requests.get(f"{S2}/paper/search", headers=HDR,
                     params={"query": query, "limit": n, "fields": FIELDS}, timeout=30)
    r.raise_for_status()
    data = r.json().get("data", [])
    print(f"S2 SEARCH: {query!r}  ({r.json().get('total','?')} total, showing {len(data)})\n")
    for p in data:
        print(_fmt(p) + "\n")


def paper(ident: str) -> None:
    r = requests.get(f"{S2}/paper/{_pid(ident)}", headers=HDR, params={"fields": FIELDS}, timeout=30)
    r.raise_for_status()
    print(_fmt(r.json()))


def recommend(ident: str, n: int = 8) -> None:
    r = requests.get(f"{REC}/papers/forpaper/{_pid(ident)}", headers=HDR,
                     params={"limit": n, "fields": FIELDS}, timeout=30)
    r.raise_for_status()
    recs = r.json().get("recommendedPapers", [])
    print(f"S2 RECOMMENDATIONS for {ident}  ({len(recs)}):\n")
    for p in recs:
        print(_fmt(p) + "\n")


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__); return 1
    n = 8
    if "--n" in a:
        i = a.index("--n"); n = int(a[i + 1]); a = a[:i] + a[i + 2:]
    cmd = a[0]
    if cmd == "search" and len(a) > 1:
        search(" ".join(a[1:]), n)
    elif cmd == "paper" and len(a) > 1:
        paper(a[1])
    elif cmd == "recommend" and len(a) > 1:
        recommend(a[1], n)
    else:
        print(__doc__); return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
