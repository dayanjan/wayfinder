# Referee receipt chain

Deterministic 4-hop data referee over the CD4+ T-cell CRISPRi Perturb-seq supplementary tables. Status vocabulary is exactly **supported / refuted / untested / flagged**; nothing is called *proven* or *discovered*. Significance threshold **alpha = 0.05** throughout. Every number below is copied from the tables by `referee.py` — none is hardcoded.

**Chain:** HOP 0 knockdown-QC gate (T4) → HOP 1 on-target effect (T1) → HOP 2 Th1/Th2 program shift (T2) → HOP 3 disease enrichment (T3).

**Why HOP 0 is load-bearing:** a guide is informative only if it actually silenced the gene. An empty downstream result could mean *no biology* or *never silenced* — indistinguishable — so a failed knockdown is **untested**, never *no effect*. Only downstream of a passed gate can a null become **refuted**.

---

## NAB2 @ Stim8hr

**Overall verdict:** consistent with a validated gene -> Th1/Th2 program -> disease chain re-derived from the tables

**Gate passed:** True

### HOP 0 — knockdown-QC gate (T4) → `supported`

Knockdown QC passed: 2 of 2 guide(s) reached signif_knockdown (best adj_p = 1e-16); guide mean expr 0.05603 vs NTC 0.5672.

| n_guides | n_signif | best_adj_p | mean_guide_expr | mean_ntc_expr |
|---|---|---|---|---|
| 2 | 2 | 1e-16 | 0.05603 | 0.5672 |

### HOP 1 — on-target effect (T1) → `supported`

On-target knockdown is significant with 301 downstream DE gene(s) (effect size -16.88, category 'on-target KD').

| ontarget_significant | ontarget_effect_size | ontarget_effect_category | n_downstream | offtarget_flag |
|---|---|---|---|---|
| True | -16.88 | on-target KD | 301 | False |

### HOP 2 — Th1/Th2 program shift (T2) → `supported`

Th1/Th2 program shift is significant in at least one reference contrast — Th2_vs_Th1 (Ota 2021): log_fc=0.6332, z=7.708, adj_p=1.95e-13, significant (Th1-associated); Th2_vs_Th1 (Hollbacker 2021): log_fc=0.6085, z=2.391, adj_p=0.205, not significant.

| contrast | log_fc | zscore | adj_p_value | significant | direction |
|---|---|---|---|---|---|
| Th2_vs_Th1 (Ota 2021) | 0.6332 | 7.708 | 1.955e-13 | True | Th1-associated |
| Th2_vs_Th1 (Hollbacker 2021) | 0.6085 | 2.391 | 0.2046 | False | — |

### HOP 3 — disease enrichment (T3) → `supported`

NAB2 is a member of 4 disease-enriched cluster(s) at FDR<0.05 in gene_set 'downstream_Stim8hr', spanning disease(s): asthma, atopic eczema.

gene_set = `downstream_Stim8hr`; 4 significant cluster(s) at FDR<0.05; diseases: asthma, atopic eczema.

Every significant (disease, cluster, odds_ratio, p_adj_fdr):

| disease | cluster | odds_ratio | p_adj_fdr |
|---|---|---|---|
| atopic eczema | 100 | 3.899 | 0.002832 |
| asthma | 100 | 2.189 | 0.02003 |
| atopic eczema | 90 | 3.43 | 0.02238 |
| asthma | 90 | 2.613 | 0.02238 |

---

## IL2 @ Rest

**Overall verdict:** untested — knockdown failed the QC gate; any null downstream result cannot be read as a negative

**Gate passed:** False

### HOP 0 — knockdown-QC gate (T4) → `untested`

Knockdown QC failed: 0 of 2 guide(s) reached signif_knockdown (best adj_p = 0.32); guide mean expr 0.03072 vs NTC 0.03559. A guide is informative only if it actually silenced the gene, so any null downstream result here is UNTESTED, never 'no effect'.

| n_guides | n_signif | best_adj_p | mean_guide_expr | mean_ntc_expr |
|---|---|---|---|---|
| 2 | 0 | 0.32 | 0.03072 | 0.03559 |

**Caveats:** target barely expressed — nothing to knock down

---

## SLC1A5 @ Stim8hr

**Overall verdict:** chain breaks at HOP 1 (on-target effect (T1)): On-target knockdown is not significant in T1 (effect size -3.456, category 'no on-target KD', n_downstream=1).

**Gate passed:** True

### HOP 0 — knockdown-QC gate (T4) → `supported`

Knockdown QC passed: 1 of 2 guide(s) reached signif_knockdown (best adj_p = 0.00919); guide mean expr 1.423 vs NTC 1.487.

| n_guides | n_signif | best_adj_p | mean_guide_expr | mean_ntc_expr |
|---|---|---|---|---|
| 2 | 1 | 0.009188 | 1.423 | 1.487 |

### HOP 1 — on-target effect (T1) → `refuted`

On-target knockdown is not significant in T1 (effect size -3.456, category 'no on-target KD', n_downstream=1).

| ontarget_significant | ontarget_effect_size | ontarget_effect_category | n_downstream | offtarget_flag |
|---|---|---|---|---|
| False | -3.456 | no on-target KD | 1 | False |

### HOP 2 — Th1/Th2 program shift (T2) → `supported`

Th1/Th2 program shift is significant in at least one reference contrast — Th2_vs_Th1 (Ota 2021): log_fc=0.1941, z=3.699, adj_p=0.00109, significant (Th1-associated); Th2_vs_Th1 (Hollbacker 2021): log_fc=0.4763, z=1.681, adj_p=0.535, not significant.

| contrast | log_fc | zscore | adj_p_value | significant | direction |
|---|---|---|---|---|---|
| Th2_vs_Th1 (Ota 2021) | 0.1941 | 3.699 | 0.001089 | True | Th1-associated |
| Th2_vs_Th1 (Hollbacker 2021) | 0.4763 | 1.681 | 0.5347 | False | — |

### HOP 3 — disease enrichment (T3) → `refuted`

SLC1A5 appears in 9 cluster(s) of gene_set 'downstream_Stim8hr' but none reach FDR<0.05 (best p_adj_fdr=0.0538, disease 'type 1 diabetes mellitus', odds_ratio=2.732).

gene_set = `downstream_Stim8hr`; appears in 9 cluster(s), none at FDR<0.05.

| best_disease | best_odds_ratio | best_p_adj_fdr |
|---|---|---|
| type 1 diabetes mellitus | 2.732 | 0.05383 |

---

## Reviewer audit

Two independent audits were run on this writeup.

**Numeric audit — PASS.** Every number in this document was re-derived from the raw
CSVs by a second, independent code path (different pandas idioms) and diffed against
`verdicts.json`: HOP 0 gate aggregates (`n_guides`, `n_signif`, `best_adj_p`,
`mean_guide_expr`, `mean_ntc_expr`), HOP 1 T1 effect fields, HOP 2 both-contrast
`log_fc`/`zscore`/`adj_p_value` and significance flags, and HOP 3 `odds_ratio`/`p_adj_fdr`
for every significant cluster (NAB2) and the best-hit refuted case (SLC1A5). All values
reproduced to numerical tolerance; no mismatches.

**Language audit — one flag, retained by design (noted, not fixed).** The calibration
reviewer flagged the word **"validated"** in NAB2's overall verdict, arguing it is stronger
than the per-hop `supported` statuses warrant. That exact phrase is prescribed *verbatim*
by the referee specification's OVERALL rule for a fully-supported chain
("consistent with a **validated** gene -> Th1/Th2 program -> disease chain re-derived from
the tables"). Per the task instruction not to change flagged items without noting them, the
wording is **retained** to stay faithful to the spec; this note records the disagreement.
The reviewer confirmed no other violations: status vocabulary is exactly
supported/refuted/untested/flagged throughout, the IL2 gate failure is correctly termed
**untested** (never "no effect"), and "proven"/"discovered" appear nowhere.

---
