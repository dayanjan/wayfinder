#!/usr/bin/env python3
"""
CrossRef Lookup Tool - Query the CrossRef REST API for DOI metadata, citation counts, and DOI enrichment.

Usage:
    python crossref_lookup.py doi <doi>           Look up a single DOI
    python crossref_lookup.py search <query>      Search CrossRef by title/query (top 5)
    python crossref_lookup.py cited-by <doi>      Show works that cite a given DOI (top 10)
    python crossref_lookup.py enrich              Find missing DOIs in references.bib via title search
    python crossref_lookup.py selftest            Verify tool works with a known DOI

Dependencies:
    pip install requests bibtexparser
"""

import re
import sys
import time

try:
    import requests
except ImportError:
    print("Error: requests is required. Install with: pip install requests")
    sys.exit(1)

from utils import (
    safe_print,
    find_project_root,
    load_bib,
    save_bib,
    normalize_doi,
    jaccard_similarity,
    format_summary_header,
)


# =============================================================================
# Configuration
# =============================================================================

CROSSREF_API = "https://api.crossref.org"
MAILTO = "grant-tools@example.com"
MAX_RETRIES = 3
JACCARD_THRESHOLD = 0.75


# =============================================================================
# CrossRefClient - Core API client
# =============================================================================

class CrossRefClient:
    """REST client for the CrossRef API (polite pool)."""

    def __init__(self, mailto=MAILTO):
        self.mailto = mailto
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"GrantTools/1.0 (mailto:{mailto})",
        })

    def _get(self, endpoint, params=None):
        """GET request with retry on 429 and rate limit respect.

        Args:
            endpoint: API endpoint path (e.g., "/works/10.1234/test").
            params: Optional query parameters dict.

        Returns:
            Parsed JSON response dict.
        """
        url = f"{CROSSREF_API}{endpoint}"
        if params is None:
            params = {}
        params["mailto"] = self.mailto

        for attempt in range(MAX_RETRIES):
            resp = self.session.get(url, params=params, timeout=30)
            if resp.status_code == 429:
                wait = 2 ** attempt
                safe_print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            return resp.json()

        resp.raise_for_status()
        return resp.json()

    def lookup_doi(self, doi):
        """Look up a single DOI and return structured metadata.

        Args:
            doi: DOI string (with or without URL prefix).

        Returns:
            Dict with title, authors, journal, year, type, is_referenced_by_count, DOI.
            None if not found.
        """
        doi = normalize_doi(doi)
        data = self._get(f"/works/{doi}")
        if not data:
            return None

        item = data.get("message", {})
        return self._parse_work(item)

    def search(self, query, rows=5):
        """Search CrossRef by title/query.

        Args:
            query: Search query string.
            rows: Number of results to return (default 5).

        Returns:
            List of result dicts with title, authors, journal, year, DOI, type, cited_by.
        """
        data = self._get("/works", params={
            "query": query,
            "rows": rows,
            "sort": "relevance",
        })
        if not data:
            return []

        results = []
        for item in data.get("message", {}).get("items", []):
            parsed = self._parse_work(item)
            if parsed:
                results.append(parsed)
        return results

    def cited_by(self, doi, rows=10):
        """Find works that cite a given DOI.

        Uses CrossRef's reverse lookup via the filter parameter.

        Args:
            doi: DOI to find citations for.
            rows: Number of citing works to return (default 10).

        Returns:
            List of result dicts for citing works.
        """
        doi = normalize_doi(doi)
        data = self._get("/works", params={
            "filter": f"references:{doi}",
            "rows": rows,
            "sort": "published",
            "order": "desc",
        })
        if not data:
            return []

        results = []
        for item in data.get("message", {}).get("items", []):
            parsed = self._parse_work(item)
            if parsed:
                results.append(parsed)
        return results

    def find_doi_for_title(self, title, year=None):
        """Search CrossRef for a DOI matching a given title.

        Args:
            title: Title string to search for.
            year: Optional publication year to filter results.

        Returns:
            Tuple of (doi_string, similarity_score) or (None, 0.0).
        """
        # Clean LaTeX from title
        clean = re.sub(r"(?<![\\])[{}]", "", title)
        clean = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", clean)
        clean = re.sub(r"[{}]", "", clean)

        params = {
            "query.title": clean,
            "rows": 5,
            "sort": "relevance",
        }
        if year:
            params["filter"] = f"from-pub-date:{year},until-pub-date:{year}"

        data = self._get("/works", params=params)
        if not data:
            return None, 0.0

        items = data.get("message", {}).get("items", [])
        best_doi = None
        best_score = 0.0

        for item in items:
            item_title = ""
            titles = item.get("title", [])
            if titles:
                item_title = titles[0]

            sim = jaccard_similarity(title, item_title)
            if sim > best_score:
                best_score = sim
                best_doi = item.get("DOI", "")

        if best_score >= JACCARD_THRESHOLD and best_doi:
            return best_doi, best_score
        return None, best_score

    @staticmethod
    def _parse_work(item):
        """Parse a CrossRef work item into a standardized dict.

        Args:
            item: Raw CrossRef work item dict.

        Returns:
            Dict with title, authors, journal, year, DOI, type, cited_by.
        """
        if not item:
            return None

        # Title
        titles = item.get("title", [])
        title = titles[0] if titles else ""

        # Authors
        authors = []
        for author in item.get("author", []):
            given = author.get("given", "")
            family = author.get("family", "")
            if family:
                authors.append(f"{family} {given}".strip())
            elif author.get("name"):
                authors.append(author["name"])

        # Journal
        containers = item.get("container-title", [])
        journal = containers[0] if containers else ""

        # Year
        date_parts = item.get("published-print", {}).get("date-parts", [[]])
        if not date_parts or not date_parts[0]:
            date_parts = item.get("published-online", {}).get("date-parts", [[]])
        if not date_parts or not date_parts[0]:
            date_parts = item.get("issued", {}).get("date-parts", [[]])
        year = str(date_parts[0][0]) if date_parts and date_parts[0] else ""

        return {
            "DOI": item.get("DOI", ""),
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "type": item.get("type", ""),
            "cited_by": item.get("is-referenced-by-count", 0),
        }


# =============================================================================
# Commands
# =============================================================================

def cmd_doi(args):
    """Look up a single DOI and print metadata."""
    if not args:
        safe_print("Usage: crossref_lookup.py doi <doi>")
        return 1

    doi = args[0]
    client = CrossRefClient()

    safe_print(format_summary_header("CROSSREF DOI LOOKUP"))

    result = client.lookup_doi(doi)
    if not result:
        safe_print(f"\n  DOI not found: {doi}")
        return 1

    authors_str = ", ".join(result["authors"][:5])
    if len(result["authors"]) > 5:
        authors_str += ", ..."

    safe_print(f"  DOI:      {result['DOI']}")
    safe_print(f"  Title:    {result['title']}")
    safe_print(f"  Authors:  {authors_str}")
    safe_print(f"  Journal:  {result['journal']}")
    safe_print(f"  Year:     {result['year']}")
    safe_print(f"  Type:     {result['type']}")
    safe_print(f"  Cited by: {result['cited_by']}")

    return 0


def cmd_search(args):
    """Search CrossRef and print top results."""
    if not args:
        safe_print("Usage: crossref_lookup.py search <query>")
        return 1

    query = " ".join(args)
    client = CrossRefClient()

    safe_print(format_summary_header("CROSSREF SEARCH"))
    safe_print(f"  Query: {query}\n")

    results = client.search(query, rows=5)
    if not results:
        safe_print("  No results found.")
        return 0

    for i, r in enumerate(results, 1):
        authors_str = ", ".join(r["authors"][:3])
        if len(r["authors"]) > 3:
            authors_str += ", ..."
        safe_print(f"  [{i}] {r['title']}")
        safe_print(f"      DOI:     {r['DOI']}")
        safe_print(f"      Authors: {authors_str}")
        safe_print(f"      Journal: {r['journal']}  Year: {r['year']}")
        safe_print(f"      Cited by: {r['cited_by']}")
        safe_print("")

    return 0


def cmd_cited_by(args):
    """Show works that cite a given DOI."""
    if not args:
        safe_print("Usage: crossref_lookup.py cited-by <doi>")
        return 1

    doi = args[0]
    client = CrossRefClient()

    safe_print(format_summary_header("CROSSREF CITED-BY"))
    safe_print(f"  DOI: {doi}\n")

    results = client.cited_by(doi, rows=10)
    if not results:
        safe_print("  No citing works found (or not available from CrossRef).")
        return 0

    safe_print(f"  Found {len(results)} citing works:\n")
    for i, r in enumerate(results, 1):
        authors_str = ", ".join(r["authors"][:3])
        if len(r["authors"]) > 3:
            authors_str += ", ..."
        safe_print(f"  [{i}] {r['title']}")
        safe_print(f"      DOI:     {r['DOI']}")
        safe_print(f"      Authors: {authors_str}")
        safe_print(f"      Journal: {r['journal']}  Year: {r['year']}")
        safe_print("")

    return 0


def cmd_enrich(args):
    """Scan references.bib for entries missing DOI. Try to find DOIs via CrossRef title search."""
    client = CrossRefClient()
    project_root = find_project_root()

    safe_print(format_summary_header("CROSSREF DOI ENRICH"))

    bib_db = load_bib()
    entries = bib_db.entries
    safe_print(f"\n  Loaded {len(entries)} BibTeX entries")

    missing_doi = [e for e in entries if not e.get("doi", "").strip()]
    safe_print(f"  Entries missing DOI: {len(missing_doi)}")

    if not missing_doi:
        safe_print("\n  All entries already have DOIs. Nothing to enrich.")
        return 0

    found = 0
    not_found = 0
    errors = 0

    safe_print("")
    for i, entry in enumerate(missing_doi):
        citekey = entry.get("ID", "?")
        title = entry.get("title", "")
        year = entry.get("year", "")

        if not title:
            safe_print(f"  [{i+1:>3}/{len(missing_doi)}] {citekey}: skip (no title)")
            not_found += 1
            continue

        try:
            doi, score = client.find_doi_for_title(title, year)
            if doi:
                entry["doi"] = doi
                found += 1
                safe_print(f"  [{i+1:>3}/{len(missing_doi)}] {citekey}: found DOI {doi} (score={score:.2f})")
            else:
                not_found += 1
                safe_print(f"  [{i+1:>3}/{len(missing_doi)}] {citekey}: no match (best={score:.2f})")
        except Exception as e:
            errors += 1
            safe_print(f"  [{i+1:>3}/{len(missing_doi)}] {citekey}: error - {e}")

        # Polite rate limiting
        time.sleep(0.1)

    # Save if we found any
    if found > 0:
        save_bib(bib_db)

    safe_print(f"\n{'=' * 50}")
    safe_print(f"Enrichment Summary:")
    safe_print(f"  DOIs found:     {found}")
    safe_print(f"  Not found:      {not_found}")
    safe_print(f"  Errors:         {errors}")
    if found > 0:
        safe_print(f"  Saved to:       references.bib")

    return 0


def cmd_selftest(args):
    """Self-test: look up a known disease-related DOI and verify the response."""
    safe_print(format_summary_header("CROSSREF SELF-TEST"))

    client = CrossRefClient()
    test_doi = "10.1016/j.autneu.2018.06.004"
    errors = []

    # Test 1: DOI lookup
    safe_print(f"\n  Test 1: Looking up DOI {test_doi}")
    try:
        result = client.lookup_doi(test_doi)
        if not result:
            errors.append("DOI lookup returned None")
        else:
            if not result.get("title"):
                errors.append("DOI lookup returned empty title")
            else:
                safe_print(f"    Title: {result['title'][:80]}")
                safe_print(f"    Year:  {result['year']}")
                safe_print(f"    Cited: {result['cited_by']}")
                safe_print("    OK")
    except Exception as e:
        errors.append(f"DOI lookup failed: {e}")

    # Test 2: Search
    safe_print(f"\n  Test 2: Searching for 'randomized controlled trial'")
    try:
        results = client.search("randomized controlled trial", rows=3)
        if not results:
            errors.append("Search returned no results")
        else:
            safe_print(f"    Found {len(results)} results")
            safe_print(f"    Top: {results[0]['title'][:70]}")
            safe_print("    OK")
    except Exception as e:
        errors.append(f"Search failed: {e}")

    # Test 3: find_doi_for_title
    safe_print(f"\n  Test 3: Finding DOI by title match")
    try:
        test_title = "randomized controlled trial"
        doi, score = client.find_doi_for_title(test_title)
        if doi:
            safe_print(f"    Found: {doi} (score={score:.2f})")
            safe_print("    OK")
        else:
            safe_print(f"    No match found (best score={score:.2f})")
            safe_print("    OK (search worked, match threshold not met)")
    except Exception as e:
        errors.append(f"find_doi_for_title failed: {e}")

    # Summary
    safe_print("")
    if errors:
        safe_print(f"FAILED: {len(errors)} errors:")
        for e in errors:
            safe_print(f"  - {e}")
        return 1
    else:
        safe_print("All tests passed.")
        return 0


# =============================================================================
# Main CLI
# =============================================================================

def main():
    if len(sys.argv) < 2:
        safe_print(__doc__)
        return 1

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "doi": cmd_doi,
        "search": cmd_search,
        "cited-by": cmd_cited_by,
        "enrich": cmd_enrich,
        "selftest": cmd_selftest,
    }

    if command not in commands:
        safe_print(f"Unknown command: {command}")
        safe_print(f"Available: {', '.join(commands)}")
        return 1

    try:
        return commands[command](args)
    except requests.RequestException as e:
        safe_print(f"\nAPI Error: {e}")
        return 1
    except Exception as e:
        safe_print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
