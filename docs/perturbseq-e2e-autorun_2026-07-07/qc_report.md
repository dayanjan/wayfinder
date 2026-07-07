# QC Report — Marson/Pritchard CD4+ T-cell Perturb-seq supplementary tables

Source: `~/pyzobot-data/` (four CSVs). All tables load without parse errors.
Condition vocabulary is **consistent** across DE and KD: `{Rest, Stim8hr, Stim48hr}`.

---

## 1. `guide_kd_efficiency.suppl_table.csv` — HOP 0: knockdown-QC gate (per guide)
- **Rows:** 73,765  |  **Unique guides:** 24,972  |  **Unique target genes (ENSG):** 12,604
- **Grain:** one row per guide × culture_condition. 1–3 guides per gene×condition (median 2).
- **Key identifier cols:** `Unnamed: 0` (guide id, e.g. `AAAS-1`), `perturbed_gene_id` (ENSG), `culture_condition`.
- **Gate column:** `signif_knockdown` (bool) → True=54,094 / False=19,671. Also `high_confidence_no_effect_guides` (True=7,002).
- **Receipts:** `guide_mean_expr`, `ntc_mean_expr`, `t_statistic`, `p_value`, `adj_p_value`, `rank`.
- **Quality issues:**
  - **933 guides have null `perturbed_gene_id`** (no ENSG mapping) → cannot be gated to a gene; excluded from the HOP0 aggregate.
  - **1,041 rows have null `p_value`/`adj_p_value`** (degenerate test).

## 2. `DE_stats.suppl_table.csv` — HOP 1: on-target effect (per gene × condition)
- **Rows:** 33,983  |  **Unique genes:** 11,526 (ENSG) = 11,526 (symbol).
- **Grain:** exactly one row per gene×condition (**0 duplicate keys**).
- **Key identifier cols:** `target_contrast` (ENSG), `target_contrast_gene_name` (symbol), `culture_condition`, `index`=`{ENSG}_{condition}`.
- **ROSETTA STONE:** ENSG↔symbol is strictly **1:1** here — this table bridges KD's ENSG world to POL/ENR's symbol world.
- **Effect cols:** `ontarget_significant` (True=21,216), `ontarget_effect_size`, `ontarget_effect_category` ({'on-target KD': 21216, 'no on-target KD': 12383, 'putative off-target': 384}), `offtarget_flag` (True=2,837), `n_downstream`, `n_total_de_genes`.
- **Reproducibility cols (sparse by design — only populated for hits):** `crossdonor_correlation_mean` 85.9% null, `crossdonor_correlation_min` 85.9% null, `crossguide_correlation` 91.2% null. Absence ≠ failure; treated as "not reported".

## 3. `Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv` — HOP 2: Th1/Th2 program (per gene × contrast)
- **Rows:** 37,288  |  **Unique genes (symbol):** 25,672.
- **Grain:** one row per gene × contrast (**0 duplicate keys**). NO condition dimension.
- **Key identifier col:** `variable` (gene symbol). Join to DE via symbol.
- **TWO contrasts** (facet HOP2 by both): `Th2_vs_Th1 (Ota 2021)` = 24,821 rows, `Th2_vs_Th1 (Hollbacker 2021)` = 12,467 rows. Coverage differs → a gene may be present in one contrast only.
- **Receipts:** `log_fc`, `lfcSE`, `stat`, `zscore`, `p_value`, `adj_p_value`.
- **Quality issues:** 482 null `adj_p_value`.

## 4. `cluster_autoimmune_enrichment_results.suppl_table.csv` — HOP 3: disease enrichment (per cluster × disease × gene_set)
- **Rows:** 5,236  |  **Clusters:** 77  |  **Diseases:** 17.
- **Grain:** one row per cluster × disease × gene_set.
- **`gene_set` encodes condition** (1,309 rows each): `downstream_Rest`→Rest, `downstream_Stim8hr`→Stim8hr, `downstream_Stim48hr`→Stim48hr, `regulators`→condition-independent.
- **Gene linkage:** genes live in **`intersecting_genes`** as a **stringified Python list** → parse with `ast.literal_eval`, then explode. A gene links to a disease if it is a member.
- **Receipts:** `odds_ratio`, `ci_low`, `ci_high`, `p_value`, `p_adj_fdr`, `cluster_size`, 2×2 counts.
- **Quality issues / handling rules:**
  - **924 negative-control rows** (`negative_control_disease=True`) → **EXCLUDE** from HOP3 verdicts.
  - **995 null-OR rows** = **empty intersection** (`intersecting_genes == '[]'`, Fisher not computable) — distinct from negative controls (733 are real diseases with 0 overlap). Contribute no gene memberships.

---

## Cross-table join topology (verified overlaps)
| Edge | Left key | Right key | Overlap |
|---|---|---|---|
| KD → DE | `perturbed_gene_id` (ENSG) + `culture_condition` | `target_contrast` (ENSG) + `culture_condition` | 11,422 / 11,526 genes |
| DE → POL | `target_contrast_gene_name` (symbol) | `variable` (symbol) | 10,422 genes |
| DE/POL → ENR | gene symbol | ∈ `ast.literal_eval(intersecting_genes)` | 1,692 of 1,814 ENR genes are DE targets |

**Design consequence:** the KD gate is queried FIRST. A gene with no `signif_knockdown=True` guide in a condition is **UNTESTED** in that condition — a downstream "no effect" in DE cannot be interpreted as biology because the perturbation itself was not established.
