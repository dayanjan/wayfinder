#!/usr/bin/env python3
"""
Citation Audit Tool - Verify every CITED reference against live scholarly sources.

Unlike claim_tracker.py (which checks that \\cite keys EXIST in references.bib),
this tool confirms each cited entry points to a REAL paper with CORRECT metadata,
is NOT retracted, and that its DOI/PMID actually resolve to the claimed work.

It cross-checks three authoritative sources:
  - OpenAlex  - existence, is_retracted flag, title/year, citation count
  - CrossRef  - DOI registrar record (authoritative DOI -> metadata)
  - PubMed    - PMID -> registered title + DOI (NCBI key from .env, polite pool)

The single highest-signal check is **DOI != PMID's registered DOI**: when an
entry's DOI and PMID point to different papers, one of them is wrong. In the
2026-05-31 audit this caught ~19 entries whose DOIs resolved to unrelated papers
(a fluorescent-probe paper, "MEWpy", a networking paper, etc.) that the
structural checks had passed for months. See LESSONS.md (2026-05-31).

Usage:
    python citation_audit.py audit                       Audit all grant-cited refs (proposal/**/*.tex, drafts excluded)
    python citation_audit.py audit --tex <dir> --bib <p> Audit an arbitrary doc (e.g. a manuscript folder)
    python citation_audit.py precheck                    Exit 1 if any HIGH-confidence problems found (CI gate)
    python citation_audit.py resolve <key> [--bib <p>]   Show authoritative resolution for one entry (debug)
    python citation_audit.py selftest                    Verify the tool runs against a known-good DOI

Flag tiers:
    HIGH   (real errors)        NOT_FOUND, RETRACTED, DOI!=PMID_DOI, PMID_NOT_FOUND
    REVIEW (confirm by hand)    DOI_TITLE_MISMATCH, YEAR_MISMATCH, PMID_TITLE_DIFF, NO_IDENTIFIER
                                These can be OpenAlex metadata artifacts (e.g. a wrong
                                indexing year on an arXiv DOI) - verify before editing.

Dependencies:  requests, bibtexparser, python-dotenv  (see requirements.txt)
"""

import os
import re
import sys
import time
import difflib
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests is required. Install with: pip install requests")
    sys.exit(1)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import (
    safe_print,
    find_project_root,
    load_config,
    scan_tex_files,
    read_tex_content,
    extract_citations,
    load_bib,
    normalize_doi,
)

OPENALEX = "https://api.openalex.org/works"
CROSSREF = "https://api.crossref.org/works"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

HIGH_FLAGS = {"NOT_FOUND", "RETRACTED", "DOI!=PMID_DOI", "PMID_NOT_FOUND"}


# --------------------------------------------------------------------------- #
# config / helpers
# --------------------------------------------------------------------------- #
def get_context():
    cfg = load_config()                         # loads .env into os.environ
    root = cfg.get("project_root") or find_project_root()
    ncbi = os.environ.get("NCBI_API_KEY", "")
    email = (os.environ.get("CONTACT_EMAIL")
             or os.environ.get("ACADEMIX_EMAIL")
             or os.environ.get("CROSSREF_EMAIL") or "")
    return root, ncbi, email


def _norm(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = re.sub(r"[{}\\$]", "", s.lower())
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _ratio(a, b):
    return difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _ua(email):
    return {"User-Agent": f"citation-audit/1.0 (mailto:{email})" if email else "citation-audit/1.0"}


def openalex_by_doi(doi, email):
    try:
        r = requests.get(f"{OPENALEX}/doi:{doi}", params={"mailto": email} if email else None,
                         headers=_ua(email), timeout=25)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def openalex_by_title(title, email):
    try:
        r = requests.get(OPENALEX, params={"filter": f"title.search:{_norm(title)}",
                         "per-page": 1, "mailto": email}, headers=_ua(email), timeout=25)
        res = r.json().get("results", []) if r.status_code == 200 else []
        return res[0] if res else None
    except Exception:
        return None


def crossref_by_doi(doi, email):
    try:
        r = requests.get(f"{CROSSREF}/{doi}", params={"mailto": email} if email else None,
                         headers=_ua(email), timeout=25)
        return r.json()["message"] if r.status_code == 200 else None
    except Exception:
        return None


def pubmed_summary(pmid, ncbi, email):
    try:
        p = {"db": "pubmed", "id": pmid, "retmode": "json"}
        if ncbi:
            p["api_key"] = ncbi
        r = requests.get(EUTILS, params=p, headers=_ua(email), timeout=25)
        d = r.json().get("result", {}).get(str(pmid))
        if not d or d.get("error"):
            return None
        doi = ""
        for a in d.get("articleids", []):
            if a.get("idtype") == "doi":
                doi = a.get("value", "")
        return {"title": d.get("title", ""), "doi": doi}
    except Exception:
        return None


# --------------------------------------------------------------------------- #
# core: verify one entry
# --------------------------------------------------------------------------- #
def verify_entry(entry, ncbi, email):
    etype = entry.get("ENTRYTYPE", "")
    doi = normalize_doi(entry.get("doi", "")) if entry.get("doi") else ""
    pmid = (entry.get("pmid") or "").strip()
    btitle = entry.get("title", "")
    byear = re.sub(r"[^0-9]", "", entry.get("year", ""))[:4]
    flags = []

    oa = openalex_by_doi(doi, email) if doi else None
    src = "openalex:doi" if oa else ""
    if not oa and btitle:
        oa = openalex_by_title(btitle, email)
        src = "openalex:title" if oa else ""
    cr = crossref_by_doi(doi, email) if doi else None
    pmrec = pubmed_summary(pmid, ncbi, email) if pmid else None

    found = bool(oa) or bool(cr) or bool(pmrec)
    otitle = (oa.get("display_name") if oa else None) or (cr.get("title", [""])[0] if cr else "")
    oyear = str(oa.get("publication_year")) if oa and oa.get("publication_year") else ""
    retracted = bool(oa.get("is_retracted")) if oa else False
    tr = _ratio(btitle, otitle) if (btitle and otitle) else 1.0

    # ---- identifier presence (software / self / grey-lit refs legitimately lack one)
    if not doi and not pmid:
        if etype in ("article", "inproceedings"):
            flags.append("NO_IDENTIFIER")
    # ---- existence: only an IDENTIFIER that fails to resolve is a real error.
    #      A title-only entry that doesn't resolve is usually software/a book/a
    #      self-citation, not a fabrication - NO_IDENTIFIER (REVIEW) already covers it.
    if (doi or pmid) and not found:
        flags.append("NOT_FOUND")
    # ---- retraction
    if retracted:
        flags.append("RETRACTED")
    # ---- PMID authoritative cross-check (highest signal)
    if pmid:
        if not pmrec:
            flags.append("PMID_NOT_FOUND")
        else:
            pdoi = normalize_doi(pmrec["doi"])
            if doi and pdoi and _norm(pdoi) != _norm(doi):
                flags.append("DOI!=PMID_DOI")
            if pmrec["title"] and btitle and _ratio(pmrec["title"], btitle) < 0.80:
                flags.append("PMID_TITLE_DIFF")
    # ---- DOI -> title sanity (only when we got the DOI's own record)
    if src == "openalex:doi" and btitle and otitle and tr < 0.78:
        flags.append("DOI_TITLE_MISMATCH")
    if src == "openalex:doi" and byear and oyear and abs(int(byear) - int(oyear)) > 1:
        flags.append("YEAR_MISMATCH")

    tier = "HIGH" if any(f in HIGH_FLAGS for f in flags) else ("REVIEW" if flags else "OK")
    return {
        "key": entry["ID"], "type": etype, "doi": doi, "pmid": pmid, "src": src,
        "found": found, "retracted": retracted,
        "cited_by": oa.get("cited_by_count") if oa else None,
        "bib_title": btitle, "src_title": otitle, "bib_year": byear, "src_year": oyear,
        "pmid_doi": normalize_doi(pmrec["doi"]) if pmrec and pmrec.get("doi") else "",
        "flags": flags, "tier": tier,
    }


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #
def collect_cited_keys(root, tex_dir=None):
    keys = set()
    if tex_dir:
        files = sorted(Path(tex_dir).rglob("*.tex"))
        files = [f for f in files if "drafts" not in str(f).replace("\\", "/").lower()
                 and not re.search(r"_\d{4}-\d{2}-\d{2}", f.name) and f.name != "standalone.tex"]
    else:
        files = scan_tex_files(root, include_drafts=False)
        files = [f for f in files if Path(f).name != "standalone.tex"]
    for f in files:
        for k in extract_citations(read_tex_content(f)):
            keys.add(k)
    return keys


def run_audit(root, ncbi, email, tex_dir=None, bib_path=None, report_scope="grant"):
    cited = collect_cited_keys(root, tex_dir)
    db = load_bib(bib_path)
    entries = {e["ID"]: e for e in db.entries}
    missing = sorted(k for k in cited if k not in entries)

    rows = []
    for key in sorted(cited):
        if key not in entries:
            continue
        rows.append(verify_entry(entries[key], ncbi, email))
        time.sleep(0.12)

    high = [r for r in rows if r["tier"] == "HIGH"]
    review = [r for r in rows if r["tier"] == "REVIEW"]
    clean = [r for r in rows if r["tier"] == "OK"]

    report = (Path(root) / "project-management" / "reviews" /
              f"citation_audit_{report_scope}_{date.today().isoformat()}.md")
    report.parent.mkdir(parents=True, exist_ok=True)
    L = [f"# Citation Audit ({report_scope}) - {date.today().isoformat()}\n",
         "Live verification via OpenAlex (existence/retraction), CrossRef (DOI registrar), "
         "PubMed (PMID->DOI cross-check).\n",
         f"- Cited keys: **{len(cited)}**",
         f"- Missing from .bib (LaTeX would error): **{len(missing)}** {missing or ''}",
         f"- HIGH (real errors): **{len(high)}**",
         f"- REVIEW (confirm by hand - may be source artifacts): **{len(review)}**",
         f"- Clean: **{len(clean)}**\n"]
    for label, group in (("HIGH - real errors", high), ("REVIEW - confirm by hand", review)):
        if group:
            L.append(f"## {label}\n")
            for r in group:
                L.append(f"- **{r['key']}** ({r['type']}) - {', '.join(r['flags'])}")
                L.append(f"  - bib: \"{r['bib_title'][:80]}\" ({r['bib_year']}) doi:{r['doi'] or '-'} pmid:{r['pmid'] or '-'}")
                L.append(f"  - resolved ({r['src'] or 'crossref/pubmed'}): \"{r['src_title'][:80]}\" "
                         f"({r['src_year']}) retracted={r['retracted']} pmid_doi:{r['pmid_doi'] or '-'}")
            L.append("")
    L.append("## Clean\n")
    L.extend(f"- {r['key']} - doi:{r['doi'] or '-'} cited_by={r['cited_by']}" for r in clean)
    report.write_text("\n".join(L), encoding="utf-8")

    safe_print(f"\n=== CITATION AUDIT ({report_scope}) ===")
    safe_print(f"cited={len(cited)} missing={len(missing)} HIGH={len(high)} REVIEW={len(review)} clean={len(clean)}")
    if missing:
        safe_print(f"MISSING FROM BIB: {missing}")
    for r in high:
        safe_print(f"  HIGH   {r['key']}: {', '.join(r['flags'])}")
    for r in review:
        safe_print(f"  REVIEW {r['key']}: {', '.join(r['flags'])}")
    safe_print(f"Report: {report}")
    return len(missing) + len(high)


def run_resolve(root, ncbi, email, key, bib_path=None):
    db = load_bib(bib_path)
    entries = {e["ID"]: e for e in db.entries}
    if key not in entries:
        safe_print(f"{key} not in bib"); return 1
    r = verify_entry(entries[key], ncbi, email)
    for k, v in r.items():
        safe_print(f"  {k}: {v}")
    return 0


def selftest(root, ncbi, email):
    oa = openalex_by_doi("10.1038/s41467-022-34537-6", email)
    ok = bool(oa) and "display_name" in oa
    safe_print(f"OpenAlex reachable: {ok} -> {oa.get('display_name','')[:60] if oa else 'FAIL'}")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "audit"
    root, ncbi, email = get_context()

    def opt(name):
        return args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else None

    if cmd in ("audit", "live", "precheck", "live-precheck"):
        gating = cmd in ("precheck", "live-precheck")
        scope = "manuscript" if opt("--tex") else "grant"
        rc = run_audit(root, ncbi, email, tex_dir=opt("--tex"), bib_path=opt("--bib"), report_scope=scope)
        sys.exit(1 if (gating and rc > 0) else 0)
    elif cmd == "resolve":
        sys.exit(run_resolve(root, ncbi, email, args[1], bib_path=opt("--bib")))
    elif cmd == "selftest":
        sys.exit(selftest(root, ncbi, email))
    else:
        safe_print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
