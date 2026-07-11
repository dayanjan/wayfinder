# Sensitivity panel — Claude Science reproduction vs. local ground truth (2026-07-10)

The manuscript's §4.1b sensitivity panel (`../sensitivity_panel.py`) was run two ways and compared,
as the dogfood gate the paper claims (native reproduction + independent self-audit, §4.5):

1. **Local ground truth** — `../sensitivity_results.json` (Windows, `PYTHONPATH=src python …`).
2. **Claude Science reproduction** — `sensitivity_results.cs.json`. The same script was staged
   unchanged into the CS tree (`/home/dayanjan/pyzobot-cs-stage1`) and run **inside the CS kernel**
   (OPERON = Opus 4.8), driven headlessly via the `drive-claude-science` skill (1 auto-approved card).

## Result: byte-identical (delta 0), Reviewer-verified

`json.load` equality **True**; identical `sha256` of the canonicalized JSON. Because the label-shuffle
null is seeded (`SEED = 20260710`), even the 2,000-permutation null distribution reproduces to the digit
(`null_mean 467.727 ± 10.935`), not merely in expectation. Verified on two script versions: the initial
panel (`sha cb9cfe70…`) and the codex-debate-hardened panel that adds `signed_z = −5.645`,
`empirical_p_lower = 0.0005`, `empirical_p_two_sided = 0.001`, and the per-gene disease-cardinality
decomposition (`sha 49797eae…`). Both reproduced delta-0 in CS.

The CS **Reviewer (Sonnet 5)** independently cross-checked the reported numbers against the
tool-produced JSON and the saved artifact at three points and returned **pass**:
> "All reported control numbers (Control 1/2/3) verbatim match the tool-produced JSON and the saved
> artifact … n_failed_kd_genes=2430, n_untested=2430, fraction_untested=1.0; pair_space_AxC=47220,
> observed=406, null_mean=467.727, null_sd=10.935, empirical_p=1.0, fold_over_null=0.87;
> default_rank_check=4, nab2_rank_min=1, nab2_rank_max=8, nab2_rank_median=4, top5=0.889."

## Honesty note (sandbox)

The CS workspace filesystem is **read-only for the staged tree**, so the script's `write_text` to
`docs/manuscript/analysis/sensitivity_results.json` raised an `OSError`; the CS agent redirected the
write to its own workspace root and **diffed the captured JSON against an earlier saved artifact
(byte-identical)** before proceeding — a reasoned, evidence-backed workaround, logged by the Reviewer
as a justified `wontfix` rather than an unaddressed deviation. The reproduction itself is unaffected.

## Provenance
- org `741d6512-1f39-4a9e-b5bb-9663fd77e1a5` · project `proj_e79dc78fbb2f` ·
  workspace `6d3ed8e1-6559-4572-a847-c15cee1586c1` · saved artifact `de8bb2bc-…`
- OPERON = Claude Opus 4.8 · REVIEWER = Claude Sonnet 5 · audit store `operon-cli.db`
