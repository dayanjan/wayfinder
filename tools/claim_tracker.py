#!/usr/bin/env python3
"""
Claim Tracker Tool - Scan .tex files for statistical claims and citations, audit against .bib.

Usage:
    python claim_tracker.py scan       Find all claims in .tex files
    python claim_tracker.py audit      Audit claims: check citations, flag uncited stats, find orphans
    python claim_tracker.py report     Formatted report organized by file and verification status
    python claim_tracker.py precheck   Pre-compilation check (exit 0=clean, 1=issues)
    python claim_tracker.py selftest   Verify tool finds claims in actual .tex files

Dependencies:
    pip install bibtexparser
"""

import re
import sys
from pathlib import Path

from utils import (
    safe_print,
    find_project_root,
    scan_tex_files,
    read_tex_content,
    extract_citations,
    load_bib,
    format_summary_header,
    format_summary_footer,
)


# =============================================================================
# Claim detection patterns
# =============================================================================

STATISTICAL_PATTERNS = [
    r"\d+(?:\.\d+)?%",                         # percentages: 42%, 3.5%
    r"[Pp]\s*[<>=]\s*0?\.\d+",                 # p-values: p < 0.05, P = .001
    r"OR\s*=?\s*\d+",                           # odds ratio: OR = 2.5, OR 3
    r"HR\s*=?\s*\d+",                           # hazard ratio: HR = 1.8
    r"RR\s*=?\s*\d+",                           # risk ratio: RR = 2
    r"\d+(?:\.\d+)?-fold",                      # fold change: 2.5-fold
    r"[Nn]\s*=\s*\d+",                          # sample size: N = 150, n=42
]

COMPARATIVE_PATTERNS = [
    r"higher than",
    r"lower than",
    r"compared to",
    r"associated with",
    r"significantly",
    r"increased",
    r"decreased",
    r"reduced",
]

CITATION_PATTERN = r"\\cite[tp]?\*?\{[^}]+\}"


# =============================================================================
# ClaimTracker - Core analysis engine
# =============================================================================

class ClaimTracker:
    """Scans .tex files for claims containing statistics, citations, or comparative language."""

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self._stat_re = re.compile("|".join(STATISTICAL_PATTERNS))
        self._comp_re = re.compile("|".join(COMPARATIVE_PATTERNS), re.IGNORECASE)
        self._cite_re = re.compile(CITATION_PATTERN)
        self._cite_keys_re = re.compile(r"\\cite[tp]?\*?\{([^}]+)\}")

    def extract_claims(self, tex_path):
        """Parse a .tex file and extract claims.

        A claim is any sentence that contains a statistical pattern, a citation,
        or comparative language.

        Args:
            tex_path: Path to the .tex file.

        Returns:
            List of claim dicts with keys: text, file, line_num, citation_keys,
            has_statistic, claim_type.
        """
        content = read_tex_content(tex_path)
        if not content:
            return []

        claims = []
        lines = content.split("\n")
        rel_path = str(Path(tex_path).relative_to(self.project_root))

        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip LaTeX commands, comments, empty lines, and markup-only lines
            if not stripped or stripped.startswith("%"):
                continue
            if stripped.startswith("\\") and not any(c.isalpha() and c.islower() for c in stripped[1:5]):
                continue
            # Skip LaTeX environment/formatting lines (enumerate, itemize, labels)
            if re.search(r"\\(?:begin|end)\{(?:enumerate|itemize|description|figure|table|tabular)", stripped):
                continue
            if re.match(r"^\s*\\(?:item|label|ref|caption)\b", stripped):
                continue

            # Split line into sentences (period-delimited segments)
            sentences = self._split_sentences(stripped)

            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) < 10:
                    continue

                has_stat = bool(self._stat_re.search(sentence))
                has_cite = bool(self._cite_re.search(sentence))
                has_comp = bool(self._comp_re.search(sentence))

                if not (has_stat or has_cite or has_comp):
                    continue

                # Extract citation keys
                cite_keys = []
                for match in self._cite_keys_re.finditer(sentence):
                    for key in match.group(1).split(","):
                        key = key.strip()
                        if key:
                            cite_keys.append(key)

                # Filter out methodological descriptions that aren't empirical claims
                # e.g., "5-fold cross-validation", "N-fold", "2-fold symmetric"
                if has_stat and not has_cite:
                    # Check if the only statistical match is an X-fold methodological term
                    stat_matches = self._stat_re.findall(sentence)
                    method_terms = re.findall(
                        r"\d+(?:\.\d+)?-fold\s+(?:cross|inner|outer|symmetric|validation|CV)",
                        sentence, re.IGNORECASE
                    )
                    if stat_matches and len(stat_matches) == len(method_terms):
                        continue  # All stat matches are methodological, skip

                # Determine claim type
                if has_stat:
                    claim_type = "statistical"
                elif has_cite and has_comp:
                    claim_type = "comparative-cited"
                elif has_cite:
                    claim_type = "cited"
                else:
                    claim_type = "comparative"

                claims.append({
                    "text": sentence,
                    "file": rel_path,
                    "line_num": line_num,
                    "citation_keys": cite_keys,
                    "has_statistic": has_stat,
                    "claim_type": claim_type,
                })

        return claims

    def extract_all_claims(self):
        """Scan all .tex files and extract all claims.

        Returns:
            List of claim dicts from all files.
        """
        tex_files = scan_tex_files(self.project_root)
        all_claims = []
        for tex_path in tex_files:
            claims = self.extract_claims(tex_path)
            all_claims.extend(claims)
        return all_claims

    def audit_claims(self, claims, bib_db):
        """Audit claims against the .bib database.

        Args:
            claims: List of claim dicts from extract_all_claims.
            bib_db: bibtexparser BibDatabase object.

        Returns:
            Dict with keys:
                uncited_stats: claims with statistics but no citation
                missing_keys: list of (key, file, line_num) for keys not in .bib
                orphaned_entries: .bib keys never cited in any .tex file
                verified: claims with valid citations
        """
        bib_keys = {entry["ID"] for entry in bib_db.entries}

        # Gather all citation keys used across all .tex files (not just claims)
        all_cited_keys = set()
        tex_files = scan_tex_files(self.project_root)
        for tex_path in tex_files:
            content = read_tex_content(tex_path)
            all_cited_keys.update(extract_citations(content))

        uncited_stats = []
        missing_keys = []
        verified = []
        seen_missing = set()

        for claim in claims:
            keys = claim["citation_keys"]

            # Check for missing .bib keys
            for key in keys:
                if key not in bib_keys and key not in seen_missing:
                    missing_keys.append({
                        "key": key,
                        "file": claim["file"],
                        "line_num": claim["line_num"],
                    })
                    seen_missing.add(key)

            # Flag statistical claims with no citation
            if claim["has_statistic"] and not keys:
                uncited_stats.append(claim)
            elif keys:
                # Check that at least one key exists in .bib
                valid = any(k in bib_keys for k in keys)
                if valid:
                    verified.append(claim)

        # Find orphaned .bib entries
        orphaned = []
        for entry in bib_db.entries:
            if entry["ID"] not in all_cited_keys:
                orphaned.append(entry["ID"])

        return {
            "uncited_stats": uncited_stats,
            "missing_keys": missing_keys,
            "orphaned_entries": orphaned,
            "verified": verified,
        }

    @staticmethod
    def _split_sentences(text):
        """Split text into sentence-like segments.

        Handles period-delimited sentences while respecting abbreviations
        and decimal numbers.

        Args:
            text: Input text string.

        Returns:
            List of sentence strings.
        """
        # Split on period followed by space and uppercase, or end of string
        # But keep the whole thing if no good split point
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\\])", text)
        if not parts:
            return [text]
        return parts


# =============================================================================
# Commands
# =============================================================================

def cmd_scan(args):
    """Find all claims in .tex files."""
    project_root = find_project_root()
    tracker = ClaimTracker(project_root)

    safe_print(format_summary_header("CLAIM SCAN"))

    claims = tracker.extract_all_claims()

    if not claims:
        safe_print("\n  No claims found.")
        return 0

    # Group by file
    by_file = {}
    for claim in claims:
        by_file.setdefault(claim["file"], []).append(claim)

    for filepath, file_claims in sorted(by_file.items()):
        safe_print(f"\n--- {filepath} ---")
        for claim in file_claims:
            cite_str = ", ".join(claim["citation_keys"]) if claim["citation_keys"] else "[no citation]"
            tag = "STAT" if claim["has_statistic"] else "CITE" if claim["citation_keys"] else "COMP"
            text_preview = claim["text"][:100]
            if len(claim["text"]) > 100:
                text_preview += "..."
            safe_print(f"  :{claim['line_num']:<4} [{tag}] {text_preview}")
            if claim["citation_keys"]:
                safe_print(f"         keys: {cite_str}")

    safe_print(f"\n  Total claims found: {len(claims)}")
    stats = {}
    for claim in claims:
        stats[claim["claim_type"]] = stats.get(claim["claim_type"], 0) + 1
    for ctype, count in sorted(stats.items()):
        safe_print(f"    {ctype}: {count}")

    return 0


def cmd_audit(args):
    """Audit claims against .bib file."""
    project_root = find_project_root()
    tracker = ClaimTracker(project_root)

    safe_print(format_summary_header("CLAIM AUDIT"))

    claims = tracker.extract_all_claims()
    bib_db = load_bib()
    audit = tracker.audit_claims(claims, bib_db)

    # Uncited statistical claims
    safe_print(f"\n--- Uncited Statistical Claims ---")
    if audit["uncited_stats"]:
        for claim in audit["uncited_stats"]:
            text_preview = claim["text"][:70]
            if len(claim["text"]) > 70:
                text_preview += "..."
            safe_print(f'  {claim["file"]}:{claim["line_num"]}  "{text_preview}"  [NO CITATION]')
    else:
        safe_print("  None found.")

    # Missing citation keys
    safe_print(f"\n--- Missing Citation Keys ---")
    if audit["missing_keys"]:
        for mk in audit["missing_keys"]:
            safe_print(f'  \\cite{{{mk["key"]}}}  in {mk["file"]}:{mk["line_num"]}  [NOT IN .bib]')
    else:
        safe_print("  None found.")

    # Orphaned .bib entries
    safe_print(f"\n--- Orphaned .bib Entries ---")
    if audit["orphaned_entries"]:
        for key in audit["orphaned_entries"]:
            safe_print(f"  {key}  [in .bib but never cited in any .tex file]")
    else:
        safe_print("  None found.")

    # Summary
    safe_print(f"\nSummary:")
    summary = {
        "Total claims found:": len(claims),
        "Claims with citations:": len(audit["verified"]),
        "Uncited statistical claims:": len(audit["uncited_stats"]),
        "Missing .bib keys:": len(audit["missing_keys"]),
        "Orphaned .bib entries:": len(audit["orphaned_entries"]),
    }
    safe_print(format_summary_footer(summary))

    return 0


def cmd_report(args):
    """Generate a formatted report of all claims organized by file and verification status."""
    project_root = find_project_root()
    tracker = ClaimTracker(project_root)

    safe_print(format_summary_header("CLAIM VERIFICATION REPORT"))

    claims = tracker.extract_all_claims()
    bib_db = load_bib()
    bib_keys = {entry["ID"] for entry in bib_db.entries}

    if not claims:
        safe_print("\n  No claims found.")
        return 0

    # Categorize each claim
    by_file = {}
    for claim in claims:
        keys = claim["citation_keys"]
        if claim["has_statistic"] and not keys:
            status = "UNCITED-STAT"
        elif keys and all(k in bib_keys for k in keys):
            status = "VERIFIED"
        elif keys and any(k not in bib_keys for k in keys):
            status = "MISSING-KEY"
        elif keys:
            status = "CITED"
        else:
            status = "UNCITED"

        claim["status"] = status
        by_file.setdefault(claim["file"], []).append(claim)

    for filepath, file_claims in sorted(by_file.items()):
        safe_print(f"\n{'=' * 60}")
        safe_print(f"  {filepath}")
        safe_print(f"{'=' * 60}")

        # Group by status within file
        for status in ["VERIFIED", "CITED", "UNCITED-STAT", "MISSING-KEY", "UNCITED"]:
            status_claims = [c for c in file_claims if c["status"] == status]
            if not status_claims:
                continue
            safe_print(f"\n  [{status}] ({len(status_claims)})")
            for claim in status_claims:
                text_preview = claim["text"][:80]
                if len(claim["text"]) > 80:
                    text_preview += "..."
                cite_str = ", ".join(claim["citation_keys"]) if claim["citation_keys"] else ""
                safe_print(f"    :{claim['line_num']:<4} {text_preview}")
                if cite_str:
                    safe_print(f"           keys: {cite_str}")

    # Overall summary
    total = len(claims)
    verified = sum(1 for c in claims if c.get("status") == "VERIFIED")
    uncited_stat = sum(1 for c in claims if c.get("status") == "UNCITED-STAT")
    missing = sum(1 for c in claims if c.get("status") == "MISSING-KEY")

    safe_print(f"\n{'=' * 60}")
    safe_print(f"OVERALL SUMMARY")
    safe_print(f"{'=' * 60}")
    summary = {
        "Total claims:": total,
        "Verified:": verified,
        "Uncited statistics:": uncited_stat,
        "Missing .bib keys:": missing,
    }
    safe_print(format_summary_footer(summary))

    return 0


def cmd_precheck(args):
    """Pre-compilation check. Exit 0 if clean, exit 1 if issues found."""
    project_root = find_project_root()
    tracker = ClaimTracker(project_root)

    safe_print(format_summary_header("CLAIM PRE-CHECK"))

    claims = tracker.extract_all_claims()
    bib_db = load_bib()
    audit = tracker.audit_claims(claims, bib_db)

    issues = []

    # Statistical claims without citations
    for claim in audit["uncited_stats"]:
        text_preview = claim["text"][:60]
        if len(claim["text"]) > 60:
            text_preview += "..."
        issues.append(f'  UNCITED STAT  {claim["file"]}:{claim["line_num"]}  "{text_preview}"')

    # Missing .bib keys
    for mk in audit["missing_keys"]:
        issues.append(f'  MISSING KEY   \\cite{{{mk["key"]}}} in {mk["file"]}:{mk["line_num"]}')

    if issues:
        safe_print(f"\n  FAIL: {len(issues)} issues found:\n")
        for issue in issues:
            safe_print(issue)
        safe_print(f"\n  Fix these before compiling.")
        return 1
    else:
        safe_print(f"\n  PASS: No uncited statistics or missing citation keys.")
        safe_print(f"  Total claims checked: {len(claims)}")
        safe_print(f"  Verified citations:   {len(audit['verified'])}")
        return 0


def cmd_selftest(args):
    """Self-test: scan actual .tex files and verify claim detection works."""
    safe_print(format_summary_header("CLAIM TRACKER SELF-TEST"))

    project_root = find_project_root()
    tracker = ClaimTracker(project_root)
    errors = []

    # Test 1: scan_tex_files finds files
    tex_files = scan_tex_files(project_root)
    safe_print(f"\n  Test 1: Found {len(tex_files)} .tex files")
    if len(tex_files) < 5:
        errors.append(f"Expected at least 5 .tex files, found {len(tex_files)}")
    else:
        safe_print("    OK")

    # Test 2: Extract claims
    claims = tracker.extract_all_claims()
    safe_print(f"\n  Test 2: Found {len(claims)} total claims")
    if len(claims) < 5:
        errors.append(f"Expected at least 5 claims, found {len(claims)}")
    else:
        safe_print("    OK")

    # Test 3: Statistical claims exist
    stat_claims = [c for c in claims if c["has_statistic"]]
    safe_print(f"\n  Test 3: Found {len(stat_claims)} statistical claims")
    if len(stat_claims) < 1:
        errors.append("Expected at least 1 statistical claim")
    else:
        safe_print(f"    Example: {stat_claims[0]['text'][:80]}...")
        safe_print("    OK")

    # Test 4: Claims with citations exist
    cited_claims = [c for c in claims if c["citation_keys"]]
    safe_print(f"\n  Test 4: Found {len(cited_claims)} claims with citations")
    if len(cited_claims) < 1:
        errors.append("Expected at least 1 claim with citations")
    else:
        safe_print("    OK")

    # Test 5: Claim type distribution
    type_counts = {}
    for c in claims:
        type_counts[c["claim_type"]] = type_counts.get(c["claim_type"], 0) + 1
    safe_print(f"\n  Test 5: Claim type distribution:")
    for ctype, count in sorted(type_counts.items()):
        safe_print(f"    {ctype}: {count}")
    safe_print("    OK")

    # Test 6: Audit against .bib
    safe_print(f"\n  Test 6: Audit against .bib")
    try:
        bib_db = load_bib()
        audit = tracker.audit_claims(claims, bib_db)
        safe_print(f"    Verified claims:      {len(audit['verified'])}")
        safe_print(f"    Uncited statistics:    {len(audit['uncited_stats'])}")
        safe_print(f"    Missing .bib keys:     {len(audit['missing_keys'])}")
        safe_print(f"    Orphaned .bib entries: {len(audit['orphaned_entries'])}")
        safe_print("    OK")
    except Exception as e:
        errors.append(f"Audit failed: {e}")

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
        "scan": cmd_scan,
        "audit": cmd_audit,
        "report": cmd_report,
        "precheck": cmd_precheck,
        "selftest": cmd_selftest,
    }

    if command not in commands:
        safe_print(f"Unknown command: {command}")
        safe_print(f"Available: {', '.join(commands)}")
        return 1

    try:
        return commands[command](args)
    except Exception as e:
        safe_print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
