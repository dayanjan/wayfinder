#!/usr/bin/env python3
"""
Shared utilities for NIH R01 grant tools.

Provides common functions used across consistency_check.py, parameter_registry.py,
crossref_lookup.py, claim_tracker.py, clinicaltrials_monitor.py, and nih_reporter.py.

Usage:
    from utils import safe_print, find_project_root, scan_tex_files, ...
"""

import os
import re
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


# =============================================================================
# Output helpers
# =============================================================================

def safe_print(text):
    """Print text with fallback for Unicode encoding errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))


def format_summary_header(title):
    """Format a consistent summary header."""
    return f"{'=' * 70}\n{title}\n{'=' * 70}"


def format_summary_footer(stats_dict):
    """Format a stats dictionary as aligned summary lines."""
    if not stats_dict:
        return ""
    max_key = max(len(k) for k in stats_dict)
    lines = []
    for key, value in stats_dict.items():
        lines.append(f"  {key:<{max_key + 1}} {value}")
    return "\n".join(lines)


# =============================================================================
# Project navigation
# =============================================================================

def find_project_root(start=None):
    """Find the project root directory (where .env or CLAUDE.md lives).

    Searches upward from start (or the tools/ directory) for a directory
    containing .env, CLAUDE.md, or a proposal/ folder.

    Returns:
        Path object for the project root.
    """
    if start:
        current = Path(start).resolve()
    else:
        current = Path(__file__).resolve().parent.parent

    # If we started from tools/, go up one level
    if current.name == "tools":
        current = current.parent

    # Search upward for project markers
    for _ in range(10):
        if (current / "CLAUDE.md").exists() or (current / "proposal").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent

    # Fallback: assume we're in the right place
    return Path(__file__).resolve().parent.parent


def load_config(require_keys=None):
    """Load environment variables from .env file.

    Args:
        require_keys: List of required environment variable names, or None.

    Returns:
        Dict with project_root (Path) and all env vars.
    """
    project_root = find_project_root()
    env_path = project_root / ".env"

    if env_path.exists() and load_dotenv is not None:
        load_dotenv(env_path)

    config = {
        "project_root": project_root,
    }

    if require_keys:
        for key in require_keys:
            val = os.environ.get(key, "")
            if not val:
                safe_print(f"Error: {key} not set in .env or environment")
                sys.exit(1)
            config[key] = val

    return config


# =============================================================================
# TeX file operations
# =============================================================================

def scan_tex_files(project_root=None, include_drafts=False):
    """Find all .tex files under proposal/.

    Args:
        project_root: Project root path. Auto-detected if None.
        include_drafts: If False (default), skip files in drafts/ subdirectories.

    Returns:
        List of Path objects sorted by name.
    """
    if project_root is None:
        project_root = find_project_root()
    project_root = Path(project_root)

    proposal_dir = project_root / "proposal"
    if not proposal_dir.is_dir():
        return []

    tex_files = sorted(proposal_dir.rglob("*.tex"))

    if not include_drafts:
        tex_files = [f for f in tex_files if "drafts" not in f.parts]

    # Also skip standalone.tex files (compilation wrappers, no content)
    tex_files = [f for f in tex_files if f.name != "standalone.tex"]

    return tex_files


def read_tex_content(tex_path):
    """Read a .tex file and return its content.

    Args:
        tex_path: Path to the .tex file.

    Returns:
        String content of the file, or empty string on error.
    """
    try:
        with open(tex_path, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError) as e:
        safe_print(f"  Warning: Could not read {tex_path}: {e}")
        return ""


def extract_citations(tex_content):
    r"""Extract all citation keys from \cite{}, \citep{}, \citet{} commands.

    Args:
        tex_content: String content of a .tex file.

    Returns:
        Set of citation key strings.
    """
    keys = set()
    # Match \cite{key1,key2}, \citep{key}, \citet{key}, \citeauthor{key}, etc.
    pattern = r"\\cite[tp]?\*?\{([^}]+)\}"
    for match in re.finditer(pattern, tex_content):
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


# =============================================================================
# BibTeX operations
# =============================================================================

def load_bib(bib_path=None):
    """Load and parse a .bib file using bibtexparser.

    Args:
        bib_path: Path to .bib file. Defaults to proposal/05_bibliography/references.bib.

    Returns:
        bibtexparser BibDatabase object.
    """
    try:
        import bibtexparser
        from bibtexparser.bparser import BibTexParser
    except ImportError:
        safe_print("Error: bibtexparser is required. Install with: pip install 'bibtexparser>=1.4.0,<2.0.0'")
        sys.exit(1)

    if bib_path is None:
        bib_path = find_project_root() / "proposal" / "05_bibliography" / "references.bib"

    bib_path = Path(bib_path)
    if not bib_path.exists():
        safe_print(f"Error: BibTeX file not found: {bib_path}")
        sys.exit(1)

    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    with open(bib_path, "r", encoding="utf-8") as f:
        return bibtexparser.load(f, parser=parser)


def save_bib(bib_db, bib_path=None):
    """Write a BibDatabase back to disk.

    Args:
        bib_db: bibtexparser BibDatabase object.
        bib_path: Output path. Defaults to proposal/05_bibliography/references.bib.
    """
    try:
        import bibtexparser
        from bibtexparser.bwriter import BibTexWriter
    except ImportError:
        safe_print("Error: bibtexparser is required.")
        sys.exit(1)

    if bib_path is None:
        bib_path = find_project_root() / "proposal" / "05_bibliography" / "references.bib"

    writer = BibTexWriter()
    writer.indent = "  "
    writer.order_entries_by = None
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write(bibtexparser.dumps(bib_db, writer=writer))


# =============================================================================
# Text similarity
# =============================================================================

def jaccard_similarity(text1, text2):
    """Compute Jaccard similarity on word tokens.

    Args:
        text1, text2: Strings to compare.

    Returns:
        Float between 0.0 and 1.0.
    """
    if not text1 or not text2:
        return 0.0
    t1 = set(re.findall(r"\w+", text1.lower()))
    t2 = set(re.findall(r"\w+", text2.lower()))
    if not t1 or not t2:
        return 0.0
    return len(t1 & t2) / len(t1 | t2)


def normalize_doi(doi):
    """Normalize a DOI for comparison.

    Strips URL prefix and lowercases.

    Args:
        doi: DOI string (may include https://doi.org/ prefix).

    Returns:
        Normalized lowercase DOI string.
    """
    if not doi:
        return ""
    doi = re.sub(r"^https?://doi\.org/", "", doi.strip())
    return doi.lower()


# =============================================================================
# Self-test
# =============================================================================

def selftest():
    """Run self-test to verify utils functions work correctly."""
    safe_print(format_summary_header("UTILS SELF-TEST"))

    errors = []

    # Test find_project_root
    root = find_project_root()
    if not (root / "proposal").is_dir():
        errors.append(f"find_project_root: proposal/ not found at {root}")
    else:
        safe_print(f"  find_project_root: {root} OK")

    # Test scan_tex_files
    tex_files = scan_tex_files(root)
    if len(tex_files) < 10:
        errors.append(f"scan_tex_files: expected 10+ files, got {len(tex_files)}")
    else:
        safe_print(f"  scan_tex_files: found {len(tex_files)} .tex files OK")

    # Test extract_citations
    sample = r"\cite{Smith2024} and \citep{Jones2023,Lee2022} and \citet{Brown2021}"
    cites = extract_citations(sample)
    expected = {"Smith2024", "Jones2023", "Lee2022", "Brown2021"}
    if cites != expected:
        errors.append(f"extract_citations: expected {expected}, got {cites}")
    else:
        safe_print(f"  extract_citations: {len(cites)} keys extracted OK")

    # Test jaccard_similarity
    sim = jaccard_similarity("the quick brown fox", "the quick brown dog")
    if not (0.5 < sim < 0.9):
        errors.append(f"jaccard_similarity: unexpected value {sim}")
    else:
        safe_print(f"  jaccard_similarity: {sim:.3f} OK")

    # Test normalize_doi
    doi = normalize_doi("https://doi.org/10.1234/TEST")
    if doi != "10.1234/test":
        errors.append(f"normalize_doi: expected '10.1234/test', got '{doi}'")
    else:
        safe_print(f"  normalize_doi: '{doi}' OK")

    # Test format helpers
    header = format_summary_header("TEST")
    if "TEST" not in header:
        errors.append("format_summary_header: missing title")
    else:
        safe_print("  format_summary_header: OK")

    footer = format_summary_footer({"Files": 10, "Errors": 0})
    if "Files" not in footer:
        errors.append("format_summary_footer: missing key")
    else:
        safe_print("  format_summary_footer: OK")

    # Summary
    if errors:
        safe_print(f"\nFAILED: {len(errors)} errors:")
        for e in errors:
            safe_print(f"  - {e}")
        return 1
    else:
        safe_print(f"\nAll tests passed.")
        return 0


if __name__ == "__main__":
    sys.exit(selftest())
