#!/usr/bin/env python3
"""
Zotero Sync Tool - Two-way sync between local references.bib and Zotero group library.

Usage:
    python zotero_sync.py push    [--bib <path>]   Parse .bib -> create items in Zotero (skip duplicates)
    python zotero_sync.py pull    [--bib <path>]   Fetch Zotero items -> append new to .bib (never overwrites)
    python zotero_sync.py status  [--bib <path>]   Compare local vs Zotero: in-sync / local-only / zotero-only
    python zotero_sync.py verify  [--bib <path>]   Cross-check matched pairs for field discrepancies
    python zotero_sync.py enrich  [--bib <path>]   Enrich .bib with abstracts, PMIDs, DOIs from PubMed

Environment:
    ZOTERO_API_KEY              Zotero API key (required for push/pull/status/verify)
    ZOTERO_GROUP_ID   Zotero group library ID (required for push/pull/status/verify)
    NCBI_API_KEY                PubMed API key (required for enrich)

Dependencies:
    pip install requests python-dotenv bibtexparser
"""

import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests is required. Install with: pip install requests")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is required. Install with: pip install python-dotenv")
    sys.exit(1)

try:
    import bibtexparser
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter
    from bibtexparser.bibdatabase import BibDatabase
except ImportError:
    print("Error: bibtexparser is required. Install with: pip install 'bibtexparser>=1.4.0,<2.0.0'")
    sys.exit(1)


def safe_print(text):
    """Print text with fallback for Unicode encoding errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))


# =============================================================================
# Configuration
# =============================================================================

DEFAULT_BIB_PATH = "proposal/05_bibliography/references.bib"
ZOTERO_API_BASE = "https://api.zotero.org"
PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
BATCH_SIZE = 50  # Zotero POST limit
MAX_RETRIES = 3
JACCARD_THRESHOLD = 0.85
PUBMED_RATE_DELAY = 0.11  # ~10 requests/sec with API key

# BibTeX entry type -> Zotero item type
ENTRY_TYPE_MAP = {
    "article": "journalArticle",
    "inproceedings": "conferencePaper",
    "book": "book",
    "incollection": "bookSection",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "techreport": "report",
}

# Zotero item type -> BibTeX entry type
ZOTERO_TYPE_MAP = {v: k for k, v in ENTRY_TYPE_MAP.items()}
ZOTERO_TYPE_MAP["conferencePaper"] = "inproceedings"
ZOTERO_TYPE_MAP["thesis"] = "phdthesis"
ZOTERO_TYPE_MAP["webpage"] = "misc"
ZOTERO_TYPE_MAP["document"] = "misc"
ZOTERO_TYPE_MAP["report"] = "techreport"


def load_config(bib_override=None, require_zotero=True):
    """Load environment variables and resolve bib path."""
    # Find project root (where .env lives)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    env_path = project_root / ".env"

    if env_path.exists():
        load_dotenv(env_path)

    api_key = os.environ.get("ZOTERO_API_KEY", "")
    group_id = os.environ.get("ZOTERO_GROUP_ID", "")

    if require_zotero:
        if not api_key:
            safe_print("Error: ZOTERO_API_KEY not set in .env or environment")
            sys.exit(1)
        if not group_id:
            safe_print("Error: ZOTERO_GROUP_ID not set in .env or environment")
            sys.exit(1)

    ncbi_api_key = os.environ.get("NCBI_API_KEY", "")
    bib_path = bib_override or str(project_root / DEFAULT_BIB_PATH)

    return {
        "api_key": api_key,
        "group_id": group_id,
        "ncbi_api_key": ncbi_api_key,
        "bib_path": bib_path,
        "project_root": str(project_root),
    }


# =============================================================================
# ZoteroSync - Core sync engine
# =============================================================================

class ZoteroSync:
    """Two-way sync between local .bib and Zotero group library."""

    def __init__(self, api_key, group_id, bib_path):
        self.api_key = api_key
        self.group_id = group_id
        self.bib_path = bib_path
        self.base_url = f"{ZOTERO_API_BASE}/groups/{group_id}"
        self.headers = {
            "Zotero-API-Key": api_key,
            "Content-Type": "application/json",
        }

    # -----------------------------------------------------------------
    # API helpers
    # -----------------------------------------------------------------

    def _api_get(self, endpoint, params=None):
        """GET request with retry on 429."""
        url = f"{self.base_url}{endpoint}"
        for attempt in range(MAX_RETRIES):
            resp = requests.get(url, headers=self.headers, params=params)
            if resp.status_code == 429:
                wait = 2 ** attempt
                safe_print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        resp.raise_for_status()
        return resp

    def _api_post(self, endpoint, json_data):
        """POST request with retry on 429."""
        url = f"{self.base_url}{endpoint}"
        for attempt in range(MAX_RETRIES):
            resp = requests.post(url, headers=self.headers, json=json_data)
            if resp.status_code == 429:
                wait = 2 ** attempt
                safe_print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        resp.raise_for_status()
        return resp

    def _get_item_template(self, item_type):
        """Fetch a blank Zotero item template for the given type."""
        url = f"{ZOTERO_API_BASE}/items/new"
        resp = requests.get(url, params={"itemType": item_type})
        resp.raise_for_status()
        return resp.json()

    def fetch_all_items(self):
        """Fetch all items from the Zotero group library (paginated)."""
        items = []
        start = 0
        limit = 100
        while True:
            resp = self._api_get("/items", params={
                "start": start,
                "limit": limit,
                "itemType": "-attachment || note",
            })
            batch = resp.json()
            if not batch:
                break
            items.extend(batch)
            total = int(resp.headers.get("Total-Results", 0))
            start += limit
            if start >= total:
                break
        return items

    def create_items(self, zotero_items):
        """Create items in Zotero in batches of 50. Returns (created, errors)."""
        created = 0
        errors = []
        for i in range(0, len(zotero_items), BATCH_SIZE):
            batch = zotero_items[i:i + BATCH_SIZE]
            try:
                resp = self._api_post("/items", batch)
                result = resp.json()
                if "successful" in result:
                    created += len(result["successful"])
                if "failed" in result:
                    for key, err in result["failed"].items():
                        errors.append(f"Item {int(key) + i}: {err.get('message', str(err))}")
            except requests.RequestException as e:
                errors.append(f"Batch {i//BATCH_SIZE + 1}: {e}")
        return created, errors

    # -----------------------------------------------------------------
    # BibTeX I/O
    # -----------------------------------------------------------------

    def load_bib(self):
        """Load and parse the .bib file. Returns bibtexparser BibDatabase."""
        if not os.path.exists(self.bib_path):
            safe_print(f"Error: BibTeX file not found: {self.bib_path}")
            sys.exit(1)
        parser = BibTexParser(common_strings=True)
        parser.ignore_nonstandard_types = False
        with open(self.bib_path, "r", encoding="utf-8") as f:
            bib_db = bibtexparser.load(f, parser=parser)
        return bib_db

    def save_bib(self, bib_db):
        """Write the BibDatabase back to disk."""
        writer = BibTexWriter()
        writer.indent = "  "
        writer.order_entries_by = None  # preserve order
        with open(self.bib_path, "w", encoding="utf-8") as f:
            f.write(bibtexparser.dumps(bib_db, writer=writer))

    # -----------------------------------------------------------------
    # Field mapping: BibTeX -> Zotero
    # -----------------------------------------------------------------

    def _parse_bib_authors(self, author_str):
        """Parse BibTeX author string into Zotero creators list.

        Handles:
          - "Last, First and Last, First"
          - "{Organization Name}"
          - "Last, First and others"
        """
        creators = []
        if not author_str:
            return creators

        parts = re.split(r"\s+and\s+", author_str)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if part.lower() == "others":
                continue
            # Institutional author: wrapped in braces
            if part.startswith("{") and part.endswith("}"):
                creators.append({
                    "creatorType": "author",
                    "name": part[1:-1],
                })
                continue
            # "Last, First" format
            if "," in part:
                last, first = part.split(",", 1)
                creators.append({
                    "creatorType": "author",
                    "lastName": last.strip(),
                    "firstName": first.strip(),
                })
            else:
                # "First Last" or single name
                tokens = part.rsplit(" ", 1)
                if len(tokens) == 2:
                    creators.append({
                        "creatorType": "author",
                        "firstName": tokens[0].strip(),
                        "lastName": tokens[1].strip(),
                    })
                else:
                    creators.append({
                        "creatorType": "author",
                        "name": part,
                    })
        return creators

    def _classify_misc(self, entry):
        """Determine Zotero type for @misc entries."""
        if entry.get("url"):
            return "webpage"
        return "document"

    def bib_to_zotero(self, entry):
        """Convert a single BibTeX entry dict to a Zotero item dict."""
        entry_type = entry.get("ENTRYTYPE", "misc").lower()

        if entry_type == "misc":
            zotero_type = self._classify_misc(entry)
        else:
            zotero_type = ENTRY_TYPE_MAP.get(entry_type, "document")

        template = self._get_item_template(zotero_type)

        # Creators
        template["creators"] = self._parse_bib_authors(entry.get("author", ""))

        # Title
        title = entry.get("title", "")
        # Remove LaTeX braces from title
        title = re.sub(r"(?<![\\])[{}]", "", title)
        template["title"] = title

        # Date / year
        template["date"] = entry.get("year", "")

        # DOI - strip URL prefix if present
        doi = entry.get("doi", "")
        doi = re.sub(r"^https?://doi\.org/", "", doi)
        if "DOI" in template:
            template["DOI"] = doi

        # URL
        if "url" in template:
            template["url"] = entry.get("url", "")

        # Journal / publication
        if "publicationTitle" in template:
            template["publicationTitle"] = entry.get("journal", "") or entry.get("booktitle", "")

        # Volume, issue, pages
        if "volume" in template:
            template["volume"] = entry.get("volume", "")
        if "issue" in template:
            template["issue"] = entry.get("number", "")
        if "pages" in template:
            template["pages"] = entry.get("pages", "")

        # Publisher
        if "publisher" in template:
            template["publisher"] = entry.get("publisher", "")

        # Extra: PMID + note
        extra_parts = []
        pmid = entry.get("pmid", "")
        if pmid:
            extra_parts.append(f"PMID: {pmid}")
        note = entry.get("note", "")
        if note:
            extra_parts.append(note)
        # Store the BibTeX citation key for round-tripping
        extra_parts.append(f"Citation Key: {entry.get('ID', '')}")
        if "extra" in template:
            template["extra"] = "\n".join(extra_parts)

        # Conference-specific
        if "proceedingsTitle" in template:
            template["proceedingsTitle"] = entry.get("booktitle", "")

        return template

    # -----------------------------------------------------------------
    # Field mapping: Zotero -> BibTeX
    # -----------------------------------------------------------------

    def _format_bib_authors(self, creators):
        """Convert Zotero creators list to BibTeX author string."""
        parts = []
        for c in creators:
            if c.get("creatorType") not in ("author", "editor"):
                continue
            if "name" in c:
                # Institutional
                parts.append("{" + c["name"] + "}")
            else:
                last = c.get("lastName", "")
                first = c.get("firstName", "")
                parts.append(f"{last}, {first}" if first else last)
        return " and ".join(parts)

    def _make_citation_key(self, zotero_item):
        """Generate a citation key from a Zotero item."""
        data = zotero_item.get("data", zotero_item)

        # Check if there's a citation key stored in extra
        extra = data.get("extra", "")
        for line in extra.split("\n"):
            if line.startswith("Citation Key:"):
                return line.split(":", 1)[1].strip()

        # Generate from first author + year
        creators = data.get("creators", [])
        year = data.get("date", "")[:4]
        if creators:
            c = creators[0]
            name = c.get("lastName", c.get("name", "Unknown"))
            name = re.sub(r"[^a-zA-Z]", "", name)
        else:
            name = "Unknown"
        return f"{name}{year}"

    def zotero_to_bib(self, zotero_item):
        """Convert a Zotero item to a BibTeX entry dict."""
        data = zotero_item.get("data", zotero_item)
        zotero_type = data.get("itemType", "document")

        entry_type = ZOTERO_TYPE_MAP.get(zotero_type, "misc")

        entry = {
            "ENTRYTYPE": entry_type,
            "ID": self._make_citation_key(zotero_item),
        }

        # Title
        title = data.get("title", "")
        if title:
            entry["title"] = title

        # Authors
        authors = self._format_bib_authors(data.get("creators", []))
        if authors:
            entry["author"] = authors

        # Year
        date = data.get("date", "")
        if date:
            entry["year"] = date[:4]

        # Journal / booktitle
        pub = data.get("publicationTitle", "") or data.get("proceedingsTitle", "")
        if pub:
            if entry_type == "inproceedings":
                entry["booktitle"] = pub
            else:
                entry["journal"] = pub

        # Volume, number, pages
        if data.get("volume"):
            entry["volume"] = data["volume"]
        if data.get("issue"):
            entry["number"] = data["issue"]
        if data.get("pages"):
            entry["pages"] = data["pages"]

        # DOI
        if data.get("DOI"):
            entry["doi"] = data["DOI"]

        # URL
        if data.get("url"):
            entry["url"] = data["url"]

        # Publisher
        if data.get("publisher"):
            entry["publisher"] = data["publisher"]

        # Parse extra for PMID and note
        extra = data.get("extra", "")
        note_parts = []
        for line in extra.split("\n"):
            line = line.strip()
            if line.startswith("PMID:"):
                entry["pmid"] = line.split(":", 1)[1].strip()
            elif line.startswith("Citation Key:"):
                continue  # already used
            elif line:
                note_parts.append(line)
        if note_parts:
            entry["note"] = "\n".join(note_parts)

        return entry

    # -----------------------------------------------------------------
    # Duplicate detection
    # -----------------------------------------------------------------

    @staticmethod
    def _normalize_doi(doi):
        """Normalize DOI for comparison."""
        if not doi:
            return ""
        doi = re.sub(r"^https?://doi\.org/", "", doi.strip())
        return doi.lower()

    @staticmethod
    def _jaccard_tokens(text1, text2):
        """Compute Jaccard similarity on word tokens."""
        if not text1 or not text2:
            return 0.0
        t1 = set(re.findall(r"\w+", text1.lower()))
        t2 = set(re.findall(r"\w+", text2.lower()))
        if not t1 or not t2:
            return 0.0
        return len(t1 & t2) / len(t1 | t2)

    def find_match(self, bib_entry, zotero_items):
        """Find matching Zotero item for a BibTeX entry.

        Match priority:
        1. DOI exact match
        2. PMID exact match (in Zotero extra field)
        3. Title Jaccard > 0.85 + year match

        Returns matching Zotero item or None.
        """
        bib_doi = self._normalize_doi(bib_entry.get("doi", ""))
        bib_pmid = bib_entry.get("pmid", "").strip()
        bib_title = bib_entry.get("title", "")
        bib_year = bib_entry.get("year", "")

        for item in zotero_items:
            data = item.get("data", item)

            # 1. DOI match
            if bib_doi:
                z_doi = self._normalize_doi(data.get("DOI", ""))
                if z_doi and z_doi == bib_doi:
                    return item

            # 2. PMID match
            if bib_pmid:
                extra = data.get("extra", "")
                for line in extra.split("\n"):
                    if line.strip().startswith("PMID:"):
                        z_pmid = line.split(":", 1)[1].strip()
                        if z_pmid == bib_pmid:
                            return item

            # 3. Title similarity + year match
            z_title = data.get("title", "")
            z_year = (data.get("date", "") or "")[:4]
            if bib_year and z_year and bib_year == z_year:
                sim = self._jaccard_tokens(bib_title, z_title)
                if sim >= JACCARD_THRESHOLD:
                    return item

        return None

    def find_match_bib(self, zotero_item, bib_entries):
        """Find matching BibTeX entry for a Zotero item.

        Same logic as find_match but reversed direction.
        """
        data = zotero_item.get("data", zotero_item)
        z_doi = self._normalize_doi(data.get("DOI", ""))
        z_title = data.get("title", "")
        z_year = (data.get("date", "") or "")[:4]

        # Extract PMID from extra
        z_pmid = ""
        extra = data.get("extra", "")
        for line in extra.split("\n"):
            if line.strip().startswith("PMID:"):
                z_pmid = line.split(":", 1)[1].strip()
                break

        for entry in bib_entries:
            # 1. DOI match
            if z_doi:
                bib_doi = self._normalize_doi(entry.get("doi", ""))
                if bib_doi and bib_doi == z_doi:
                    return entry

            # 2. PMID match
            if z_pmid:
                bib_pmid = entry.get("pmid", "").strip()
                if bib_pmid and bib_pmid == z_pmid:
                    return entry

            # 3. Title similarity + year
            bib_title = entry.get("title", "")
            bib_year = entry.get("year", "")
            if z_year and bib_year and z_year == bib_year:
                sim = self._jaccard_tokens(z_title, bib_title)
                if sim >= JACCARD_THRESHOLD:
                    return entry

        return None


# =============================================================================
# PubMedEnricher - Fetch abstracts, PMIDs, DOIs from NCBI E-utilities
# =============================================================================

class PubMedEnricher:
    """Enrich BibTeX entries with data from PubMed."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_params = {"api_key": api_key} if api_key else {}

    def _get(self, endpoint, params):
        """GET request to NCBI E-utilities with rate limiting and retry."""
        url = f"{PUBMED_BASE}/{endpoint}"
        all_params = {**self.base_params, **params}
        for attempt in range(MAX_RETRIES):
            time.sleep(PUBMED_RATE_DELAY)
            resp = requests.get(url, params=all_params)
            if resp.status_code == 429:
                wait = 2 ** attempt
                safe_print(f"  PubMed rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp
        resp.raise_for_status()
        return resp

    def search_by_pmid(self, pmid):
        """Fetch full record by PMID. Returns parsed dict or None."""
        resp = self._get("efetch.fcgi", {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml",
        })
        return self._parse_efetch_xml(resp.text)

    def search_by_doi(self, doi):
        """Search PubMed by DOI, return PMID if found."""
        doi = re.sub(r"^https?://doi\.org/", "", doi.strip())
        resp = self._get("esearch.fcgi", {
            "db": "pubmed",
            "term": f"{doi}[DOI]",
            "retmode": "json",
        })
        data = resp.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])
        if id_list:
            return id_list[0]
        return None

    def search_by_title(self, title, year=""):
        """Search PubMed by title (+ year). Returns (PMID, confidence) or (None, 0)."""
        # Clean LaTeX from title
        clean = re.sub(r"(?<![\\])[{}]", "", title)
        clean = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", clean)  # \textbf{x} -> x
        clean = re.sub(r"[{}]", "", clean)

        query = f"{clean}[Title]"
        if year:
            query += f" AND {year}[PDAT]"

        resp = self._get("esearch.fcgi", {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 5,
        })
        data = resp.json()
        id_list = data.get("esearchresult", {}).get("idlist", [])

        if len(id_list) == 1:
            return id_list[0], 1.0  # Unique match = high confidence
        elif len(id_list) > 1:
            # Multiple results — fetch titles and Jaccard-match
            for pmid in id_list:
                record = self.search_by_pmid(pmid)
                if record:
                    sim = ZoteroSync._jaccard_tokens(title, record.get("title", ""))
                    if sim >= JACCARD_THRESHOLD:
                        return pmid, sim
            return None, 0.0
        return None, 0.0

    def _parse_efetch_xml(self, xml_text):
        """Parse PubMed efetch XML into a dict with abstract, doi, title, authors."""
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return None

        article = root.find(".//PubmedArticle")
        if article is None:
            return None

        result = {}

        # PMID
        pmid_el = article.find(".//PMID")
        if pmid_el is not None:
            result["pmid"] = pmid_el.text

        # Title
        title_el = article.find(".//ArticleTitle")
        if title_el is not None:
            result["title"] = "".join(title_el.itertext())

        # Abstract
        abstract_parts = []
        for abs_text in article.findall(".//AbstractText"):
            label = abs_text.get("Label", "")
            text = "".join(abs_text.itertext())
            if label:
                abstract_parts.append(f"{label}: {text}")
            else:
                abstract_parts.append(text)
        if abstract_parts:
            result["abstract"] = " ".join(abstract_parts)

        # DOI
        for id_el in article.findall(".//ArticleId"):
            if id_el.get("IdType") == "doi":
                result["doi"] = id_el.text
                break

        # Authors
        authors = []
        for author_el in article.findall(".//Author"):
            last = author_el.findtext("LastName", "")
            fore = author_el.findtext("ForeName", "")
            if last:
                authors.append(f"{last}, {fore}" if fore else last)
            else:
                collective = author_el.findtext("CollectiveName", "")
                if collective:
                    authors.append("{" + collective + "}")
        if authors:
            result["authors"] = " and ".join(authors)

        # Journal
        journal_el = article.find(".//Journal/Title")
        if journal_el is not None:
            result["journal"] = journal_el.text

        # Year
        year_el = article.find(".//PubDate/Year")
        if year_el is not None:
            result["year"] = year_el.text
        else:
            # Try MedlineDate
            medline_el = article.find(".//PubDate/MedlineDate")
            if medline_el is not None and medline_el.text:
                m = re.match(r"(\d{4})", medline_el.text)
                if m:
                    result["year"] = m.group(1)

        return result


# =============================================================================
# Commands
# =============================================================================

def cmd_enrich(sync, ncbi_api_key):
    """Enrich .bib entries with abstracts, missing PMIDs, and DOIs from PubMed."""
    safe_print("=" * 70)
    safe_print("PUBMED ENRICH")
    safe_print("=" * 70)

    if not ncbi_api_key:
        safe_print("\nError: NCBI_API_KEY not set in .env or environment")
        safe_print("Get one at: https://www.ncbi.nlm.nih.gov/account/settings/")
        return 1

    pubmed = PubMedEnricher(ncbi_api_key)

    safe_print(f"\nLoading: {sync.bib_path}")
    bib_db = sync.load_bib()
    entries = bib_db.entries
    safe_print(f"  Found {len(entries)} BibTeX entries")

    # Categorize entries
    non_pubmed_types = {"misc"}
    stats = {
        "already_complete": 0,
        "enriched_by_pmid": 0,
        "enriched_by_doi": 0,
        "enriched_by_title": 0,
        "skipped_not_pubmed": 0,
        "not_found": 0,
        "errors": 0,
        "fields_added": {"abstract": 0, "pmid": 0, "doi": 0},
    }

    for i, entry in enumerate(entries):
        entry_type = entry.get("ENTRYTYPE", "").lower()
        citekey = entry.get("ID", "?")
        has_abstract = bool(entry.get("abstract", "").strip())
        has_pmid = bool(entry.get("pmid", "").strip())
        has_doi = bool(entry.get("doi", "").strip())

        # Skip entries that are already complete
        if has_abstract and has_pmid and has_doi:
            stats["already_complete"] += 1
            continue

        # Skip non-PubMed types (misc without DOI/PMID = FDA notices, ClinicalTrials, etc.)
        if entry_type in non_pubmed_types and not has_pmid and not has_doi:
            stats["skipped_not_pubmed"] += 1
            safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: skip (non-PubMed @{entry_type})")
            continue

        # Strategy 1: Have PMID — fetch directly
        if has_pmid:
            try:
                record = pubmed.search_by_pmid(entry["pmid"].strip())
                if record:
                    updated = _apply_enrichment(entry, record)
                    if updated:
                        stats["enriched_by_pmid"] += 1
                        for field in updated:
                            stats["fields_added"][field] += 1
                        safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: +{', '.join(updated)} (via PMID)")
                    else:
                        stats["already_complete"] += 1
                    continue
            except Exception as e:
                safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: error fetching PMID {entry['pmid']} - {e}")
                stats["errors"] += 1
                continue

        # Strategy 2: Have DOI but no PMID — search DOI to find PMID, then fetch
        if has_doi and not has_pmid:
            try:
                pmid = pubmed.search_by_doi(entry["doi"])
                if pmid:
                    record = pubmed.search_by_pmid(pmid)
                    if record:
                        updated = _apply_enrichment(entry, record)
                        if "pmid" not in updated:
                            # Always add the PMID we discovered
                            entry["pmid"] = pmid
                            updated.append("pmid")
                        stats["enriched_by_doi"] += 1
                        for field in updated:
                            stats["fields_added"][field] += 1
                        safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: +{', '.join(updated)} (via DOI)")
                        continue
                # DOI not in PubMed — not everything is indexed
                if not has_abstract:
                    stats["not_found"] += 1
                    safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: not in PubMed (DOI search)")
                    continue
            except Exception as e:
                safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: error searching DOI - {e}")
                stats["errors"] += 1
                continue

        # Strategy 3: No PMID, no DOI (or DOI failed) — search by title
        title = entry.get("title", "")
        year = entry.get("year", "")
        if title:
            try:
                pmid, confidence = pubmed.search_by_title(title, year)
                if pmid and confidence >= JACCARD_THRESHOLD:
                    record = pubmed.search_by_pmid(pmid)
                    if record:
                        updated = _apply_enrichment(entry, record)
                        if "pmid" not in updated and not has_pmid:
                            entry["pmid"] = pmid
                            updated.append("pmid")
                        if record.get("doi") and not has_doi:
                            entry["doi"] = record["doi"]
                            if "doi" not in updated:
                                updated.append("doi")
                        stats["enriched_by_title"] += 1
                        for field in updated:
                            stats["fields_added"][field] += 1
                        safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: +{', '.join(updated)} (via title, conf={confidence:.2f})")
                        continue
                stats["not_found"] += 1
                safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: not found in PubMed")
            except Exception as e:
                safe_print(f"  [{i+1:>2}/{len(entries)}] {citekey}: error searching title - {e}")
                stats["errors"] += 1
        else:
            stats["not_found"] += 1

    # Save
    sync.save_bib(bib_db)

    # Report
    total_enriched = stats["enriched_by_pmid"] + stats["enriched_by_doi"] + stats["enriched_by_title"]
    safe_print(f"\n{'=' * 50}")
    safe_print(f"Enrichment Summary:")
    safe_print(f"  Already complete:  {stats['already_complete']}")
    safe_print(f"  Enriched (PMID):   {stats['enriched_by_pmid']}")
    safe_print(f"  Enriched (DOI):    {stats['enriched_by_doi']}")
    safe_print(f"  Enriched (title):  {stats['enriched_by_title']}")
    safe_print(f"  Skipped (non-PM):  {stats['skipped_not_pubmed']}")
    safe_print(f"  Not found:         {stats['not_found']}")
    safe_print(f"  Errors:            {stats['errors']}")
    safe_print(f"\n  Fields added:")
    safe_print(f"    abstracts: +{stats['fields_added']['abstract']}")
    safe_print(f"    PMIDs:     +{stats['fields_added']['pmid']}")
    safe_print(f"    DOIs:      +{stats['fields_added']['doi']}")
    safe_print(f"\n  Total entries enriched: {total_enriched}")
    safe_print(f"  Saved to: {sync.bib_path}")

    return 0


def _apply_enrichment(entry, pubmed_record):
    """Apply PubMed data to a BibTeX entry. Only fills missing fields.

    Returns list of field names that were added.
    """
    updated = []

    # Abstract
    if not entry.get("abstract", "").strip() and pubmed_record.get("abstract"):
        entry["abstract"] = pubmed_record["abstract"]
        updated.append("abstract")

    # PMID
    if not entry.get("pmid", "").strip() and pubmed_record.get("pmid"):
        entry["pmid"] = pubmed_record["pmid"]
        updated.append("pmid")

    # DOI
    if not entry.get("doi", "").strip() and pubmed_record.get("doi"):
        entry["doi"] = pubmed_record["doi"]
        updated.append("doi")

    return updated


def cmd_push(sync):
    """Push local .bib entries to Zotero group library (skip duplicates)."""
    safe_print("=" * 70)
    safe_print("ZOTERO PUSH")
    safe_print("=" * 70)

    safe_print(f"\nLoading: {sync.bib_path}")
    bib_db = sync.load_bib()
    entries = bib_db.entries
    safe_print(f"  Found {len(entries)} BibTeX entries")

    safe_print("\nFetching existing Zotero items...")
    zotero_items = sync.fetch_all_items()
    safe_print(f"  Found {len(zotero_items)} items in Zotero")

    # Find entries that need to be created
    to_create = []
    skipped = 0
    for entry in entries:
        match = sync.find_match(entry, zotero_items)
        if match:
            skipped += 1
        else:
            to_create.append(entry)

    safe_print(f"\n  Skipping {skipped} (already in Zotero)")
    safe_print(f"  Creating {len(to_create)} new items")

    if not to_create:
        safe_print("\nNothing to push. All entries are in sync.")
        return 0

    # Convert to Zotero format
    safe_print("\nConverting to Zotero format...")
    zotero_payloads = []
    conversion_errors = []
    for entry in to_create:
        try:
            payload = sync.bib_to_zotero(entry)
            zotero_payloads.append(payload)
        except Exception as e:
            conversion_errors.append(f"  {entry.get('ID', '?')}: {e}")

    if conversion_errors:
        safe_print(f"\n  Conversion errors ({len(conversion_errors)}):")
        for err in conversion_errors:
            safe_print(err)

    # Upload
    safe_print(f"\nUploading {len(zotero_payloads)} items to Zotero...")
    created, errors = sync.create_items(zotero_payloads)
    safe_print(f"  Created: {created}")

    if errors:
        safe_print(f"  Errors ({len(errors)}):")
        for err in errors:
            safe_print(f"    {err}")

    safe_print(f"\nSummary: {created} created, {skipped} skipped, {len(errors)} errors")
    return 0 if not errors else 1


def cmd_pull(sync):
    """Pull Zotero items and append new entries to .bib (never overwrites)."""
    safe_print("=" * 70)
    safe_print("ZOTERO PULL")
    safe_print("=" * 70)

    safe_print(f"\nLoading: {sync.bib_path}")
    bib_db = sync.load_bib()
    entries = bib_db.entries
    safe_print(f"  Found {len(entries)} local BibTeX entries")

    safe_print("\nFetching Zotero items...")
    zotero_items = sync.fetch_all_items()
    safe_print(f"  Found {len(zotero_items)} items in Zotero")

    # Find Zotero items not in local .bib
    new_items = []
    matched = 0
    for item in zotero_items:
        match = sync.find_match_bib(item, entries)
        if match:
            matched += 1
        else:
            new_items.append(item)

    safe_print(f"\n  Matched: {matched}")
    safe_print(f"  New from Zotero: {len(new_items)}")

    if not new_items:
        safe_print("\nNothing to pull. All Zotero items are in local .bib.")
        return 0

    # Convert and append
    safe_print("\nConverting and appending...")
    existing_ids = {e["ID"] for e in entries}
    added = 0
    for item in new_items:
        try:
            bib_entry = sync.zotero_to_bib(item)
            # Ensure unique citation key
            base_key = bib_entry["ID"]
            key = base_key
            suffix = 2
            while key in existing_ids:
                key = f"{base_key}_{suffix}"
                suffix += 1
            bib_entry["ID"] = key
            existing_ids.add(key)
            bib_db.entries.append(bib_entry)
            safe_print(f"  + {key}: {bib_entry.get('title', '?')[:60]}")
            added += 1
        except Exception as e:
            data = item.get("data", item)
            safe_print(f"  Error converting: {data.get('title', '?')[:50]} - {e}")

    if added > 0:
        sync.save_bib(bib_db)
        safe_print(f"\nSaved {added} new entries to {sync.bib_path}")
    else:
        safe_print("\nNo entries added.")

    return 0


def cmd_status(sync):
    """Compare local .bib vs Zotero: show sync status."""
    safe_print("=" * 70)
    safe_print("ZOTERO STATUS")
    safe_print("=" * 70)

    safe_print(f"\nLoading: {sync.bib_path}")
    bib_db = sync.load_bib()
    entries = bib_db.entries
    safe_print(f"  Local entries: {len(entries)}")

    safe_print("\nFetching Zotero items...")
    zotero_items = sync.fetch_all_items()
    safe_print(f"  Zotero items: {len(zotero_items)}")

    in_sync = []
    local_only = []
    zotero_only = []

    # Check each local entry against Zotero
    matched_zotero_keys = set()
    for entry in entries:
        match = sync.find_match(entry, zotero_items)
        if match:
            in_sync.append((entry, match))
            matched_zotero_keys.add(match.get("key", ""))
        else:
            local_only.append(entry)

    # Check Zotero items not matched
    for item in zotero_items:
        if item.get("key", "") not in matched_zotero_keys:
            zotero_only.append(item)

    # Report
    safe_print(f"\n  In Sync:      {len(in_sync)}")
    safe_print(f"  Local Only:   {len(local_only)}")
    safe_print(f"  Zotero Only:  {len(zotero_only)}")

    if local_only:
        safe_print(f"\n--- Local Only (not in Zotero) ---")
        for entry in local_only:
            title = entry.get("title", "?")[:60]
            safe_print(f"  {entry['ID']}: {title}")

    if zotero_only:
        safe_print(f"\n--- Zotero Only (not in local .bib) ---")
        for item in zotero_only:
            data = item.get("data", item)
            title = data.get("title", "?")[:60]
            safe_print(f"  [{item.get('key', '?')}] {title}")

    if not local_only and not zotero_only:
        safe_print("\nAll entries are in sync!")

    return 0


def cmd_verify(sync):
    """Cross-check matched pairs for field discrepancies."""
    safe_print("=" * 70)
    safe_print("ZOTERO VERIFY")
    safe_print("=" * 70)

    safe_print(f"\nLoading: {sync.bib_path}")
    bib_db = sync.load_bib()
    entries = bib_db.entries

    safe_print("Fetching Zotero items...")
    zotero_items = sync.fetch_all_items()

    # Find matched pairs
    pairs = []
    for entry in entries:
        match = sync.find_match(entry, zotero_items)
        if match:
            pairs.append((entry, match))

    safe_print(f"\n  Matched pairs to verify: {len(pairs)}")

    if not pairs:
        safe_print("  No matched pairs found.")
        return 0

    # Check fields
    fields_to_check = [
        ("title", "title"),
        ("year", "date"),
        ("doi", "DOI"),
        ("journal", "publicationTitle"),
    ]

    total_discrepancies = 0
    clean_count = 0

    for entry, zotero_item in pairs:
        data = zotero_item.get("data", zotero_item)
        discrepancies = []

        for bib_field, z_field in fields_to_check:
            bib_val = entry.get(bib_field, "").strip()
            z_val = (data.get(z_field, "") or "").strip()

            # Normalize for comparison
            if bib_field == "doi":
                bib_val = sync._normalize_doi(bib_val)
                z_val = sync._normalize_doi(z_val)
            elif bib_field == "year":
                z_val = z_val[:4]
            elif bib_field == "title":
                # Remove LaTeX braces for comparison
                bib_val_clean = re.sub(r"(?<![\\])[{}]", "", bib_val)
                if bib_val_clean.lower() != z_val.lower() and bib_val_clean and z_val:
                    discrepancies.append(
                        f"    {bib_field}: bib='{bib_val_clean[:50]}' vs zotero='{z_val[:50]}'"
                    )
                continue

            if bib_val and z_val and bib_val.lower() != z_val.lower():
                discrepancies.append(
                    f"    {bib_field}: bib='{bib_val}' vs zotero='{z_val}'"
                )
            elif bib_val and not z_val:
                discrepancies.append(f"    {bib_field}: missing in Zotero")
            elif z_val and not bib_val:
                discrepancies.append(f"    {bib_field}: missing in BibTeX")

        # Check authors
        bib_authors = entry.get("author", "")
        z_creators = data.get("creators", [])
        bib_author_count = len(re.split(r"\s+and\s+", bib_authors)) if bib_authors else 0
        # Exclude "others" from count
        if bib_authors and "others" in bib_authors.lower():
            bib_author_count -= 1
        z_author_count = len([c for c in z_creators if c.get("creatorType") == "author"])
        if bib_author_count > 0 and z_author_count > 0 and abs(bib_author_count - z_author_count) > 1:
            discrepancies.append(
                f"    authors: bib has {bib_author_count}, zotero has {z_author_count}"
            )

        if discrepancies:
            total_discrepancies += len(discrepancies)
            safe_print(f"\n  {entry['ID']}:")
            for d in discrepancies:
                safe_print(d)
        else:
            clean_count += 1

    safe_print(f"\n{'=' * 50}")
    safe_print(f"Summary: {clean_count} clean, {total_discrepancies} discrepancies in {len(pairs) - clean_count} entries")

    return 0 if total_discrepancies == 0 else 1


# =============================================================================
# Main CLI
# =============================================================================

def main():
    if len(sys.argv) < 2:
        safe_print(__doc__)
        return 1

    command = sys.argv[1]

    # Parse --bib option
    bib_override = None
    args = sys.argv[2:]
    if "--bib" in args:
        idx = args.index("--bib")
        if idx + 1 < len(args):
            bib_override = args[idx + 1]

    all_commands = ["push", "pull", "status", "verify", "enrich"]

    if command not in all_commands:
        safe_print(f"Unknown command: {command}")
        safe_print(f"Available: {', '.join(all_commands)}")
        return 1

    # enrich only needs NCBI key, not Zotero
    require_zotero = command != "enrich"
    config = load_config(bib_override, require_zotero=require_zotero)

    try:
        if command == "enrich":
            # enrich uses BibTeX I/O from ZoteroSync but doesn't need Zotero API
            sync = ZoteroSync(config["api_key"], config["group_id"], config["bib_path"])
            return cmd_enrich(sync, config["ncbi_api_key"])
        else:
            sync = ZoteroSync(config["api_key"], config["group_id"], config["bib_path"])
            zotero_commands = {
                "push": cmd_push,
                "pull": cmd_pull,
                "status": cmd_status,
                "verify": cmd_verify,
            }
            return zotero_commands[command](sync)
    except requests.RequestException as e:
        safe_print(f"\nAPI Error: {e}")
        return 1
    except Exception as e:
        safe_print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
