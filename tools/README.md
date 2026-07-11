# tools/ — citation resolution + verification stack

Ported 2026-07-11 from the `2026-03-05-LightsOut-R01` manuscript toolkit (the sibling project where the
citation machinery was battle-tested on a real preprint). These are standalone Python CLIs — runnable
headless, by Codex, or in CI — for building and auditing the manuscript bibliography.

## Tools
| Tool | Purpose |
|---|---|
| `crossref_lookup.py` | CrossRef REST: `doi <doi>`, `search <query>` (top 5), `cited-by <doi>`, `enrich` (fill missing DOIs in a `.bib` by title), `selftest`. |
| `pubmed_fetch.py` | PubMed/PMC: PMID lookup, batch search, PMC full-text, `.bib` PMCID enrichment. Reads `NCBI_API_KEY` from `.env` (optional; raises rate limit). |
| `citation_audit.py` | **Live** cross-check of `.bib` entries against OpenAlex + CrossRef + PubMed — flags wrong DOI, retractions, title/year drift. `resolve <key> --bib <path>` audits one entry; `audit --bib <path>` audits a set. |
| `claim_tracker.py` | Scans source for statistical claims + `\cite` keys vs `.bib` (LaTeX-oriented — see caveat). |
| `utils.py` | Shared helpers (`safe_print`, `find_project_root`, `.bib` load, summary formatting). Dependency of the above. |

## Usage for THIS repo (markdown manuscript)
The bibliography is `references/references.bib` (built via CrossRef, all entries live-audited `tier=OK`).

```bash
# validate every bib entry against the live literature (wrong-DOI / retraction / drift):
for k in swanson1986 henry2021 zhu2025 cheng2021; do
  python tools/citation_audit.py resolve $k --bib references/references.bib
done

# resolve a new DOI before adding it:
python tools/crossref_lookup.py doi <doi>
python tools/crossref_lookup.py search "<title words>"
```

## Caveat — LaTeX vs markdown
`citation_audit.py audit --tex <dir>` and `claim_tracker.py` scan LaTeX `\cite{}` keys, so the
"which refs are cited" cross-check is LaTeX-specific and reports `cited=0` on our markdown sections. The
**live-resolution engine is format-agnostic** — use `resolve <key> --bib` (above) to audit each entry.
When we assemble the submission (pandoc markdown → DOCX with a Frontiers CSL), citations become
`[@key]` and a markdown-aware cited-key check can be added then.

## Deps
`pip install -r tools/requirements.txt` (requests, python-dotenv, bibtexparser, pyyaml). Optional `.env`:
`NCBI_API_KEY` (PubMed rate limit), `ZOTERO_*` (only if using `zotero_sync`, not ported).
