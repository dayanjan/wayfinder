# PyzoBot Hypothesis-Referee — BATCH ranking

`pyzobot_referee_batch.py` runs `referee(gene, condition)` over every candidate and ranks by a
transparent **chain_score**. Reproducible: `python pyzobot_referee_batch.py` regenerates the CSVs.

## Candidate set (condition-matched)
Genes that **pass the HOP-0 knockdown-QC gate** AND appear in a T3 autoimmune-disease-enriched
cluster at **FDR<0.05** for the *same* condition (negative-control rows excluded).
**602 (gene, condition) pairs** — Stim8hr 324, Stim48hr 208, Rest 70.

## chain_score
`chain_score = kd_ok * (effect_term + program_term + disease_term) * (1 + novelty_bonus)`
- **effect_term** = log1p(|HOP-1 effect size|), capped
- **program_term** = best HOP-2 -log10(adj_p) across BOTH contrasts (Ota 2021 & Hollbacker 2021)
- **disease_term** = log2(odds_ratio) + 0.5*-log10(FDR), best HOP-3 hit
- **novelty_bonus** (<=0.30) rewards *less obvious* chains: fewer disease clusters + program significant in only one contrast, so blockbuster hubs don't crowd out subtle-but-solid candidates.
Every term traces to a printed receipt; weights are module constants.

## Status distribution within the candidate set
- HOP-1 EFFECT: {'supported': 482, 'refuted': 93, 'flagged': 22, 'untested': 5}
- HOP-2 PROGRAM: {'supported': 439, 'refuted': 147, 'untested': 16}
- HOP-3 DISEASE: all supported (candidate definition).

## Top 5 chains
| rank | gene | condition | top disease | effect_size | program adj-p | disease OR | disease FDR | chain_score |
|--|--|--|--|--|--|--|--|--|
| 1 | ITK | Stim8hr | asthma | -2.7816 | 2.13e-81 | 20.424 | 4.97e-05 | 36.1844 |
| 2 | ZBTB25 | Stim8hr | asthma | -10.4949 | 2.70e-36 | 20.424 | 4.97e-05 | 36.1823 |
| 3 | CHD7 | Stim8hr | asthma | -15.6679 | 3.10e-49 | 20.424 | 4.97e-05 | 34.8827 |
| 4 | TRAT1 | Stim8hr | autoimmune disease | -13.9348 | 2.27e-61 | 3.0405 | 5.05e-06 | 34.8629 |
| 5 | CRIM1 | Stim8hr | autoimmune disease | -12.2948 | 3.17e-21 | 3.0405 | 5.05e-06 | 34.8629 |

1. **ITK @ Stim8hr -> asthma** — the strongest chain. Validated KD, program shift significant
   in both contrasts (best adj-p 2e-81), asthma cluster OR 20.4 (FDR 5e-5). ITK is a T-cell
   receptor-proximal kinase; the chain is *consistent with* an established asthma axis re-derived here.
2. **ZBTB25 @ Stim8hr -> asthma** — near-identical score but **flagged**: large effect
   (-10.5) with an off-target flag in DE_stats, so the effect hop carries a caveat. A less obvious
   transcription-factor candidate worth follow-up *because* the referee surfaced the flag rather than hiding it.
3. **CHD7 @ Stim8hr -> asthma** — chromatin remodeler, 2,277 downstream DE genes, OR 20.4.
4-5. **TRAT1 / CRIM1 @ Stim8hr -> autoimmune disease** — both strong, condition-matched full chains.

## Notable non-YES cases (the value of calibration)
- **Disease link WITHOUT a program shift (147 cases).**
  Gate + disease both supported, but HOP-2 Th1/Th2 shift **refuted** in both contrasts — e.g.
  **CDK6 @ Stim8hr** (autoimmune OR 3.04, FDR 5e-6; program adj-p 0.073) and **GPR183 @ Stim8hr**.
  These genes sit in disease-enriched clusters but do not themselves move the polarization program:
  a disease association that is *not* mediated by Th1/Th2 skewing on this evidence. High-value
  leads precisely because they are less obvious, but the chain is partial — not a clean YES.
- **Off-target flags (22 cases).** e.g. ZBTB25, APOBR —
  effect present but `offtarget_flag` set; the referee downgrades EFFECT to *flagged*.
- **Effect refuted despite gate pass (93 cases).** Pooled
  `ontarget_significant=False` even though >=1 guide passed the gate (e.g. GLUL, CSF2RB) — a
  single-guide vs pooled disagreement the referee reports rather than smooths over.
- **UNTESTED artifacts** are excluded from this table by construction (they never pass HOP-0), which
  is the point: the ranking cannot be polluted by genes whose knockdown failed.

## Files
- `pyzobot_referee_ranked.csv` — requested schema (gene, condition, top_disease, overall_status,
  kd_ok, effect_size, program_adj_p, disease_OR, disease_FDR, chain_score).
- `pyzobot_referee_ranked_full.csv` — all term/status columns for auditing.
