#!/usr/bin/env python3
"""
PubMed Fetch Tool — single-paper lookup, batch search, PMC full text, .bib enrichment.

Reads NCBI_API_KEY from .env in the project root.

Usage:
    python tools/pubmed_fetch.py lookup  <PMID>                Single PMID -> abstract + PMC status
    python tools/pubmed_fetch.py search  "<query>" [--max N]   Batch search -> results with abstracts
    python tools/pubmed_fetch.py fulltext <PMCID>              Fetch + summarize PMC full text
    python tools/pubmed_fetch.py enrich  [--bib <path>]        Add PMCIDs to .bib entries

Output includes:
  - Full abstract (not just title)
  - PMCID and PMC URL when open-access full text is available
  - Ready-to-paste SOURCES.md table row
  - Ready-to-paste BibTeX block
  - Plain-language "what this paper is about" summary block for NOTEBOOK.md

Lesson enforced: never characterise a paper from its title alone.
Every identified paper goes through `lookup` before any description is written.
"""

import argparse
import json
import os
import re
import sys
import textwrap
import time
import xml.etree.ElementTree as ET
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    sys.exit("requests not installed.  Run: pip install requests")

try:
    from dotenv import load_dotenv
except ImportError:
    sys.exit("python-dotenv not installed.  Run: pip install python-dotenv")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# Force UTF-8 output on Windows (cp1252 default cannot encode box-drawing chars)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf_8"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_KEY   = os.getenv("NCBI_API_KEY", "")
BASE      = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PMC_BASE  = "https://www.ncbi.nlm.nih.gov/pmc/articles"
DELAY     = 0.12   # ≤ 10 req/s with API key (NCBI limit)

# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _get(url: str, params: dict = None, timeout: int = 20) -> requests.Response:
    """GET with rate limiting and retries."""
    p = params or {}
    if API_KEY:
        p["api_key"] = API_KEY
    for attempt in range(3):
        try:
            r = requests.get(url, params=p, timeout=timeout)
            r.raise_for_status()
            time.sleep(DELAY)
            return r
        except requests.RequestException as e:
            if attempt == 2:
                raise
            time.sleep(1.0)
    raise RuntimeError("Should not reach here")


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def _text(elem, path: str, default: str = "") -> str:
    """Safe text extraction from XML element."""
    if elem is None:
        return default
    node = elem.find(path)
    return (node.text or "").strip() if node is not None else default


def _all_text(elem) -> str:
    """Concatenate all text content in an element tree (handles mixed content)."""
    if elem is None:
        return ""
    parts = []
    if elem.text:
        parts.append(elem.text.strip())
    for child in elem:
        parts.append(_all_text(child))
        if child.tail:
            parts.append(child.tail.strip())
    return " ".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Core API: PubMed record fetch
# ---------------------------------------------------------------------------

def fetch_pubmed_record(pmid: str) -> dict:
    """
    Fetch full PubMed XML for a single PMID.
    Returns a dict with: pmid, title, authors, journal, year, doi, pmcid,
                         pmc_url, abstract, abstract_structured, open_access
    """
    pmid = str(pmid).strip()
    url  = f"{BASE}/efetch.fcgi"
    r    = _get(url, {"db": "pubmed", "id": pmid, "rettype": "abstract", "retmode": "xml"})

    try:
        root = ET.fromstring(r.content)
    except ET.ParseError as e:
        return {"pmid": pmid, "error": f"XML parse error: {e}"}

    article = root.find(".//PubmedArticle")
    if article is None:
        return {"pmid": pmid, "error": "No article found for this PMID"}

    med  = article.find("MedlineCitation")
    art  = med.find("Article") if med is not None else None
    data = article.find("PubmedData")

    # --- Title ---
    title = _all_text(art.find("ArticleTitle")) if art is not None else ""

    # --- Authors ---
    authors = []
    if art is not None:
        for auth in art.findall(".//Author"):
            last  = _text(auth, "LastName")
            init  = _text(auth, "Initials")
            coll  = _text(auth, "CollectiveName")
            if coll:
                authors.append(coll)
            elif last:
                authors.append(f"{last} {init}".strip())
    authors_str = ", ".join(authors)

    # --- Journal ---
    journal = ""
    year    = ""
    if art is not None:
        j = art.find("Journal")
        if j is not None:
            journal = _text(j, "ISOAbbreviation") or _text(j, "Title")
            ji = j.find("JournalIssue/PubDate")
            if ji is not None:
                year = _text(ji, "Year") or _text(ji, "MedlineDate", "")[:4]

    # --- DOI, PMCID from ArticleIdList ---
    doi   = ""
    pmcid = ""
    if data is not None:
        for aid in data.findall(".//ArticleId"):
            id_type = aid.get("IdType", "")
            val     = (aid.text or "").strip()
            if id_type == "doi":
                doi = val
            elif id_type == "pmc":
                pmcid = val  # e.g. "PMC12345678"

    # If PMCID not in data, try MedlineCitation OtherID
    if not pmcid and med is not None:
        for oid in med.findall("OtherID"):
            if oid.get("Source") == "NLM" and (oid.text or "").startswith("PMC"):
                pmcid = (oid.text or "").strip()
                break

    pmc_url      = f"{PMC_BASE}/{pmcid}/" if pmcid else ""
    open_access  = bool(pmcid)

    # --- Abstract ---
    abstract_structured = {}
    abstract_plain      = ""
    if art is not None:
        abs_elem = art.find("Abstract")
        if abs_elem is not None:
            parts = []
            for at in abs_elem.findall("AbstractText"):
                label = at.get("Label", "")
                text  = _all_text(at)
                if label:
                    abstract_structured[label] = text
                    parts.append(f"{label}: {text}")
                else:
                    parts.append(text)
            abstract_plain = "\n".join(parts)

    return {
        "pmid":                pmid,
        "title":               title,
        "authors":             authors_str,
        "author_list":         authors,
        "journal":             journal,
        "year":                year,
        "doi":                 doi,
        "pmcid":               pmcid,
        "pmc_url":             pmc_url,
        "open_access":         open_access,
        "abstract":            abstract_plain,
        "abstract_structured": abstract_structured,
        "error":               None,
    }


# ---------------------------------------------------------------------------
# Core API: PubMed search
# ---------------------------------------------------------------------------

def search_pubmed(query: str, max_results: int = 20) -> list[dict]:
    """
    Search PubMed and return a list of record dicts (with abstracts).
    """
    # Step 1: esearch -> list of PMIDs
    r = _get(f"{BASE}/esearch.fcgi", {
        "db": "pubmed", "term": query,
        "retmax": max_results, "retmode": "json",
        "sort": "relevance",
    })
    data = r.json()
    pmids = data.get("esearchresult", {}).get("idlist", [])
    total = int(data.get("esearchresult", {}).get("count", 0))

    if not pmids:
        return []

    # Step 2: batch efetch XML for all PMIDs at once
    url = f"{BASE}/efetch.fcgi"
    r2  = _get(url, {
        "db": "pubmed", "id": ",".join(pmids),
        "rettype": "abstract", "retmode": "xml",
    })

    try:
        root = ET.fromstring(r2.content)
    except ET.ParseError:
        # Fall back to individual lookups
        records = []
        for pmid in pmids:
            records.append(fetch_pubmed_record(pmid))
            time.sleep(DELAY)
        return records

    records = []
    for article in root.findall(".//PubmedArticle"):
        med  = article.find("MedlineCitation")
        pmid = _text(med, "PMID") if med is not None else ""
        rec  = fetch_pubmed_record(pmid) if pmid else {}
        rec["_total_results"] = total
        records.append(rec)

    return records


# ---------------------------------------------------------------------------
# Core API: PMC full text
# ---------------------------------------------------------------------------

def fetch_pmc_fulltext(pmcid: str) -> dict:
    """
    Fetch PMC full text XML and extract abstract, methods, results sections.
    pmcid should be like 'PMC12345678' or just '12345678'.
    """
    # Normalise: strip 'PMC' prefix for the API call
    numeric_id = pmcid.replace("PMC", "").strip()

    r = _get(f"{BASE}/efetch.fcgi", {
        "db": "pmc", "id": numeric_id,
        "rettype": "full", "retmode": "xml",
    })

    # Check for error response
    if b"<ERROR>" in r.content or len(r.content) < 500:
        text = r.text[:300]
        return {"pmcid": pmcid, "error": f"Full text not available: {text}"}

    try:
        root = ET.fromstring(r.content)
    except ET.ParseError as e:
        return {"pmcid": pmcid, "error": f"XML parse error: {e}"}

    article = root.find(".//article")
    if article is None:
        return {"pmcid": pmcid, "error": "No article element in PMC XML"}

    # --- Title ---
    title = _all_text(article.find(".//article-title"))

    # --- Abstract ---
    abs_parts = []
    for abs_elem in article.findall(".//abstract"):
        for sec in abs_elem.findall("sec"):
            label = _all_text(sec.find("title"))
            body  = " ".join(_all_text(p) for p in sec.findall("p"))
            abs_parts.append(f"{label}: {body}" if label else body)
        for p in abs_elem.findall("p"):
            abs_parts.append(_all_text(p))
    abstract = "\n".join(abs_parts)

    # --- Body sections ---
    def extract_section(keywords: list[str]) -> str:
        """Find a body section by title keyword match."""
        body = article.find(".//body")
        if body is None:
            return ""
        for sec in body.findall(".//sec"):
            title_elem = sec.find("title")
            if title_elem is not None:
                t = (_all_text(title_elem)).lower()
                if any(kw in t for kw in keywords):
                    paras = [_all_text(p) for p in sec.findall(".//p")]
                    text  = " ".join(paras)
                    return textwrap.shorten(text, width=1200, placeholder="…")
        return ""

    methods = extract_section(["method", "material", "participant", "protocol", "design"])
    results = extract_section(["result", "finding", "outcome"])
    conclusion = extract_section(["conclusion", "discussion", "summary"])

    return {
        "pmcid":       pmcid,
        "pmc_url":     f"{PMC_BASE}/{pmcid}/",
        "title":       title,
        "abstract":    abstract,
        "methods":     methods,
        "results":     results,
        "conclusion":  conclusion,
        "error":       None,
    }


# ---------------------------------------------------------------------------
# .bib enrichment
# ---------------------------------------------------------------------------

def enrich_bib(bib_path: str) -> None:
    """
    Read .bib file and add pmcid + open_access flag to entries that have a
    pmid but are missing pmcid. Updates file in-place.
    Uses pubmed_fetch lookup (not zotero_sync) so it works standalone.
    """
    try:
        import bibtexparser
        from bibtexparser.bparser import BibTexParser
        from bibtexparser.bwriter import BibTexWriter
    except ImportError:
        sys.exit("bibtexparser not installed.  Run: pip install 'bibtexparser>=1.4.0,<2.0.0'")

    bib_file = Path(bib_path)
    if not bib_file.exists():
        sys.exit(f"File not found: {bib_file}")

    parser = BibTexParser(common_strings=True)
    with open(bib_file, encoding="utf-8") as f:
        db = bibtexparser.load(f, parser=parser)

    updated = 0
    for entry in db.entries:
        pmid = entry.get("pmid", "").strip()
        if not pmid:
            continue
        existing_pmcid = entry.get("pmcid", "").strip()
        if existing_pmcid:
            continue  # already has PMCID

        print(f"  Checking PMID {pmid} ({entry.get('ID', '?')})...", end=" ", flush=True)
        rec = fetch_pubmed_record(pmid)
        if rec.get("error"):
            print(f"error: {rec['error']}")
            continue

        if rec["pmcid"]:
            entry["pmcid"]       = rec["pmcid"]
            entry["open_access"] = "yes"
            updated += 1
            print(f"added PMCID {rec['pmcid']}")
        else:
            entry["open_access"] = "no"
            print("no PMC full text")

        # Also backfill abstract if missing
        if not entry.get("abstract") and rec.get("abstract"):
            entry["abstract"] = rec["abstract"]

    writer = BibTexWriter()
    writer.indent = "  "
    with open(bib_file, "w", encoding="utf-8") as f:
        f.write(bibtexparser.dumps(db, writer))

    print(f"\nDone. {updated} entries updated with PMCID.")


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def _wrap(text: str, width: int = 90, indent: str = "  ") -> str:
    return textwrap.fill(text, width=width, initial_indent=indent,
                         subsequent_indent=indent)


def _first_author_year(rec: dict) -> str:
    authors = rec.get("author_list", [])
    first   = authors[0].split()[0] if authors else "Unknown"
    year    = rec.get("year", "????")
    return f"{first} {year}"


def print_lookup(rec: dict) -> None:
    """Print a full, formatted lookup result."""
    SEP  = "─" * 72
    SEP2 = "· " * 36

    if rec.get("error"):
        print(f"\n[ERROR] PMID {rec['pmid']}: {rec['error']}")
        return

    oa_status = f"YES — {rec['pmc_url']}" if rec["open_access"] else "NO (subscription only)"
    n_authors = len(rec.get("author_list", []))
    all_authors = rec["authors"]
    short_authors = (", ".join(rec["author_list"][:4]) + f" … ({n_authors} total)"
                     if n_authors > 5 else all_authors)

    print(f"\n{SEP}")
    print(f"  PMID      {rec['pmid']}")
    print(f"  PMCID     {rec['pmcid'] or '—'}")
    print(f"  Open Access  {oa_status}")
    print(SEP)
    print(_wrap(rec["title"], indent="  Title     "))
    print(f"  Authors   {short_authors}")
    print(f"  Journal   {rec['journal']}  ({rec['year']})")
    if rec["doi"]:
        print(f"  DOI       https://doi.org/{rec['doi']}")
    print()

    # Abstract
    if rec["abstract_structured"]:
        print("  ABSTRACT")
        for label, text in rec["abstract_structured"].items():
            print(f"\n  [{label}]")
            print(_wrap(text, indent="    "))
    elif rec["abstract"]:
        print("  ABSTRACT")
        print(_wrap(rec["abstract"], indent="    "))
    else:
        print("  ABSTRACT  (not available)")

    # --- SOURCES.md block ---
    first_auth_year = _first_author_year(rec)
    journal_short   = rec["journal"].split(".")[0] if rec["journal"] else ""
    print(f"\n{SEP2}")
    print("  SOURCES.md entry (copy-paste):")
    print(f"  | {first_auth_year}, {journal_short} | **{rec['pmid']}** | [KEY POINT — fill in] | [section] |")
    if rec["pmcid"]:
        print(f"  PMC full text: {rec['pmc_url']}  → run: python tools/pubmed_fetch.py fulltext {rec['pmcid']}")

    # --- NOTEBOOK.md block ---
    first_sentence = (rec["abstract"].split(".")[0] + ".") if rec["abstract"] else ""
    print(f"\n{SEP2}")
    print("  NOTEBOOK.md entry (copy-paste):")
    print(f"  **PMID {rec['pmid']}** — {short_authors}, *{rec['journal']}* {rec['year']}.")
    if rec["pmcid"]:
        print(f"  Open Access: YES | PMCID: {rec['pmcid']} | {rec['pmc_url']}")
    else:
        print(f"  Open Access: NO (subscription only)")
    if first_sentence:
        print(_wrap(first_sentence, indent="  "))

    # --- BibTeX block ---
    key     = re.sub(r"[^A-Za-z0-9]", "", _first_author_year(rec).replace(" ", ""))
    # author_list stores "LastName Initials" — convert to BibTeX "Last, Initials"
    authors_bib = " and ".join(
        f"{a.split()[0]}, {' '.join(a.split()[1:])}" if len(a.split()) > 1 else a
        for a in rec.get("author_list", [])
    )
    print(f"\n{SEP2}")
    print("  BibTeX entry (copy-paste):")
    print(f"  @article{{{key},")
    print(f"    author  = {{{authors_bib}}},")
    print(f"    title   = {{{{{rec['title']}}}}},")
    print(f"    journal = {{{rec['journal']}}},")
    print(f"    year    = {{{rec['year']}}},")
    if rec["doi"]:
        print(f"    doi     = {{{rec['doi']}}},")
    print(f"    pmid    = {{{rec['pmid']}}},")
    if rec["pmcid"]:
        print(f"    pmcid   = {{{rec['pmcid']}}},")
    print( "  }")
    print(f"\n{SEP}")


def print_search_results(records: list[dict], query: str) -> None:
    """Print search results — one block per paper."""
    total = records[0].get("_total_results", len(records)) if records else 0
    print(f"\n{'═'*72}")
    print(f"  PubMed search: \"{query}\"")
    print(f"  Total hits: {total}  |  Showing: {len(records)}")
    print(f"{'═'*72}")

    for i, rec in enumerate(records, 1):
        if rec.get("error"):
            print(f"\n  [{i}] PMID {rec.get('pmid','?')} — ERROR: {rec['error']}")
            continue

        oa = f"OA: {rec['pmcid']}" if rec["open_access"] else "OA: no"
        print(f"\n  [{i}] PMID {rec['pmid']}  |  {oa}")
        print(_wrap(rec["title"], indent="      "))
        print(f"      {rec['authors'][:80]}{'…' if len(rec['authors'])>80 else ''}")
        print(f"      {rec['journal']} ({rec['year']})")

        # First 2 sentences of abstract
        abstract = rec.get("abstract", "")
        if abstract:
            sentences = re.split(r'(?<=[.!?])\s+', abstract.replace("\n", " "))
            snippet   = " ".join(sentences[:2])
            print(_wrap(snippet, indent="      "))

    print(f"\n{'═'*72}")
    print("  To look up any result in full: python tools/pubmed_fetch.py lookup <PMID>")
    print("  To get full text:              python tools/pubmed_fetch.py fulltext <PMCID>")


def print_fulltext(ft: dict) -> None:
    """Print structured PMC full text summary."""
    SEP = "─" * 72
    if ft.get("error"):
        print(f"\n[ERROR] {ft['pmcid']}: {ft['error']}")
        return

    print(f"\n{SEP}")
    print(f"  PMC Full Text — {ft['pmcid']}")
    print(f"  {ft['pmc_url']}")
    print(SEP)
    if ft["title"]:
        print(_wrap(ft["title"], indent="  "))
    print()

    for section, label in [
        ("abstract",   "ABSTRACT"),
        ("methods",    "METHODS (excerpt)"),
        ("results",    "RESULTS (excerpt)"),
        ("conclusion", "CONCLUSION (excerpt)"),
    ]:
        text = ft.get(section, "")
        if text:
            print(f"  [{label}]")
            print(_wrap(text, indent="    "))
            print()

    print(SEP)


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_lookup(args) -> None:
    """Look up a single PMID."""
    if not args.pmid:
        sys.exit("Usage: pubmed_fetch.py lookup <PMID>")
    if not API_KEY:
        print("[WARNING] NCBI_API_KEY not set — requests may be rate-limited")
    rec = fetch_pubmed_record(args.pmid)
    print_lookup(rec)


def cmd_search(args) -> None:
    """Batch search PubMed."""
    if not args.query:
        sys.exit('Usage: pubmed_fetch.py search "<query>" [--max N]')
    if not API_KEY:
        print("[WARNING] NCBI_API_KEY not set — requests may be rate-limited")
    print(f"Searching PubMed: {args.query!r}  (max {args.max} results)…")
    records = search_pubmed(args.query, max_results=args.max)
    if not records:
        print("No results found.")
        return
    print_search_results(records, args.query)


def cmd_fulltext(args) -> None:
    """Fetch PMC full text."""
    if not args.pmcid:
        sys.exit("Usage: pubmed_fetch.py fulltext <PMCID>  (e.g. PMC12345678)")
    if not API_KEY:
        print("[WARNING] NCBI_API_KEY not set — requests may be rate-limited")
    pmcid = args.pmcid if args.pmcid.startswith("PMC") else f"PMC{args.pmcid}"
    print(f"Fetching PMC full text for {pmcid}…")
    ft = fetch_pmc_fulltext(pmcid)
    print_fulltext(ft)


def cmd_enrich(args) -> None:
    """Enrich .bib file with PMCIDs."""
    bib_path = args.bib or str(ROOT / "proposal/05_bibliography/references.bib")
    if not API_KEY:
        print("[WARNING] NCBI_API_KEY not set — requests may be rate-limited")
    print(f"Enriching: {bib_path}")
    enrich_bib(bib_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="pubmed_fetch.py",
        description="PubMed/PMC lookup, search, full text, and .bib enrichment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              python tools/pubmed_fetch.py lookup 41758479
              python tools/pubmed_fetch.py search "POTS HRV wearable" --max 15
              python tools/pubmed_fetch.py fulltext PMC12150731
              python tools/pubmed_fetch.py enrich
              python tools/pubmed_fetch.py enrich --bib proposal/05_bibliography/references.bib

            IMPORTANT: Always run `lookup` before characterising a paper.
            Never describe a paper from its title alone.
        """),
    )
    sub = parser.add_subparsers(dest="command", metavar="command")
    sub.required = True

    # lookup
    p_lookup = sub.add_parser("lookup", help="Single PMID → abstract + PMC status + copy-paste blocks")
    p_lookup.add_argument("pmid", help="PubMed ID (e.g. 41758479)")
    p_lookup.set_defaults(func=cmd_lookup)

    # search
    p_search = sub.add_parser("search", help="Batch search → results with abstracts")
    p_search.add_argument("query", help="PubMed search query (quote multi-word terms)")
    p_search.add_argument("--max", type=int, default=20, metavar="N",
                           help="Maximum results to return (default: 20)")
    p_search.set_defaults(func=cmd_search)

    # fulltext
    p_ft = sub.add_parser("fulltext", help="Fetch + summarise PMC full text (open-access only)")
    p_ft.add_argument("pmcid", help="PMC ID (e.g. PMC12150731 or 12150731)")
    p_ft.set_defaults(func=cmd_fulltext)

    # enrich
    p_enrich = sub.add_parser("enrich", help="Add PMCIDs + open-access flags to .bib entries")
    p_enrich.add_argument("--bib", default=None, metavar="PATH",
                           help="Path to .bib file (default: proposal/05_bibliography/references.bib)")
    p_enrich.set_defaults(func=cmd_enrich)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
