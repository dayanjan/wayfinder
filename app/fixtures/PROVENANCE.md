# app/fixtures — curated LBD sweep data for the Hypothesis Engine screen

Checked-in copies of the cached LBD full-sweep outputs so the app never depends on the gitignored
`data/lbd_out/` scratch (debate F-006). These are **regenerable** — the source of truth is the
pipeline, not these files.

| file | what | source |
|---|---|---|
| `sweep_Stim8hr.json` | the full audited funnel + `ranked_clean_supported` (30 rows) + params | `data/lbd_out/sweep_Stim8hr.json` |
| `lbd_questions_Stim8hr.json` | the 30-item clean question set | `data/lbd_out/lbd_questions_Stim8hr.json` |

- **Condition:** Stim8hr. **Generated:** 2026-07-07 (the autonomous LBD-proposer session).
- **Regenerate:** `PYTHONPATH=src python -m arbiter.lbd.propose --condition Stim8hr`
  (writes to `data/lbd_out/`; copy the two files here to refresh).
- **Funnel of record:** a_genes 3,935 → eligible 22,039 → disease-C-supported 43 → **30 clean
  full-chain supported** (10 weak · 3 flagged · 1 refuted-effect · 21,995 refuted-for-C).
