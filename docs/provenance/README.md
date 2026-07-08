# Provenance — raw working trail (full audit)

The complete, unedited working artifacts behind the NAB2 finding and its validation, preserved so the
provenance of the work can be verified without doubt. The polished/distilled versions live in
`docs/` (finding, synthesis, replication report, source-paper read) and `docs/replication/`
(methodology + agent prompts/reports); **this directory is the raw evidence they were derived from.**

`raw-working-trail/` — 52 files, verbatim from the working scratch directory. Two handling notes:
- **Codex run-logs** (`*_codex.log`, `codex_consult.log`, `codex_moneyshot.log`,
  `codex_replicate_*.log`, sweep/preflight logs) are the raw terminal traces (they contain ANSI
  escape codes and long reasoning narration) — kept unedited on purpose: the raw trace is the proof
  the agents actually ran and what they did. The actionable content is at the tail of each.
- **Literature corpora** (`nab2_corpus.json`, `nab2_relevant.json`) have **abstract text stripped**
  (third-party copyrighted text not redistributed); bibliographic metadata (title, DOI, year,
  citations, source, url) is kept so the retrieval record is fully auditable. Abstracts regenerate
  via `src/arbiter/lit/search.py`.

## What's here, by phase
| Phase | Key raw files |
|---|---|
| Spec-hardening codex-debate (3 rounds) | `round{1,2,3}_prompt.md`, `round{1,2,3}_preamble.md`, `round{1,2,3}_codex.log`, `round_0{1,2,3}_codex.json` |
| Codex code consult + money-shot consult | `codex_consult_prompt.md` + `.log` + `_verdict.txt`; `codex_moneyshot_prompt.md` + `.log` + `_verdict.txt` |
| LBD build working scripts + outputs | `resolve_efo.py`, `build_nab2_corpus.py`, `run_ranked_pilot.py`, `stat6_confounder_checks.py`, `egr_mechanism_check.py`; `efo_resolution.json`, `preflight_sample.json`, `ranked_pilot.json`, `sweep_Stim8hr*.log`, `mygene_cache.json` |
| 5-agent independent replication | `REPLICATION_TARGETS.md` (frozen protocol); `codex_replicate_{1,2}_*.md` (prompts) + `.log` (raw runs); `replication_opus_{receipt,funnel,confounder}.md` (Opus reports); **`opus_indep_CD.py`, `indep_eligible.py`, `opus_cytoband.py`** (the replication agents' own from-scratch scripts — direct evidence of the clean-room re-implementations) |
| Literature corpora (metadata) | `nab2_corpus.json`, `nab2_relevant.json` (abstracts stripped) |

## Integrity notes
- Secret-scanned before commit: no `.env` values and no key patterns appear in any preserved file.
- The API response cache (`data/lbd_cache/`) and the source-paper PDF (`references/*.pdf`) remain
  gitignored (regenerable / not-redistributed) — every result that depends on them is reproducible
  via the committed scripts.
- Cross-reference: distilled outputs at `../lbd_finding_nab2_2026-07-08.md`,
  `../replication_report_2026-07-08.md`, `../replication/`, `../source_paper_read_eczema_2026-07-08.md`.
