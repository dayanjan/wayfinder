# PyzoBot hypothesis-referee — data QC & join map

Source: `~/pyzobot-data/` (Marson/Pritchard genome-scale CD4+ Perturb-seq supplementary tables). Read-only.

## 1. Per-table QC

### T1 — DE_stats.suppl_table.csv  (gene -> EFFECT)
- **33,983 rows x 20 cols**; grain = perturbation x culture_condition (no duplicate [target_contrast, culture_condition]).
- **11,526** unique perturbations (ENSG == gene symbol, 1:1). Conditions balanced: Rest 11,287 / Stim8hr 11,415 / Stim48hr 11,281.
- `index` = `target_contrast` + "_" + `culture_condition` (100% reconstructable — decomposable composite key).
- Effect categories: on-target KD 21,216 / no on-target KD 12,383 / putative off-target 384. `offtarget_flag` True in 2,837 rows.
- **Quality issues:** reproducibility columns are mostly empty — `crossdonor_correlation_*` 85.9% NaN, `crossguide_correlation` 91.2% NaN (populated only where multi-donor/guide data exist); `target_baseMean` 17.2% NaN. `Unnamed: 0` is a redundant row index.

### T2 — Th2_Th1_polarization...suppl_table.csv  (gene -> PROGRAM shift)
- **37,288 rows x 9 cols**; grain = gene(SYMBOL) x contrast.
- **25,672** unique symbols; **11,616 duplicate symbols** — expected: two reference contrasts (Ota 2021 n=24,821; Hollbacker 2021 n=12,467). Choose one or facet by `contrast` when joining.
- log_fc in [-10.56, 8.64]; 8,437 genes at adj_p<0.05. `adj_p_value` 1.3% NaN.

### T3 — cluster_autoimmune_enrichment_results.suppl_table.csv  (program -> DISEASE)
- **5,236 rows x 15 cols**; grain = cluster x disease x gene_set (unique). **77 clusters x 17 diseases x 4 gene_sets** (downstream_Rest/Stim8hr/Stim48hr + regulators).
- 185 enrichments at p_adj_fdr<0.05. **924 negative-control rows** (`negative_control_disease=True`) — exclude from real hypotheses.
- **Quality issue:** `intersecting_genes` is a **stringified Python list** — must `ast.literal_eval` before use. 1,814 unique member genes total.

### T4 — guide_kd_efficiency.suppl_table.csv  (guide -> KD-QC gate)
- **73,765 rows x 15 cols**; grain = guide x culture_condition (no dups).
- **24,972** guides -> **12,604** genes (multiple guides/gene). `signif_knockdown` True in 54,094 rows; `high_confidence_no_effect_guides` in 7,002.
- **Quality issue:** ~1.3% of rows lack `perturbed_gene_id`/`rank`/p-values — drop before gating. `Unnamed: 0` holds the guide id.

## 2. Join keys (verified by overlap)

| link | from -> to | key | shared |
|---|---|---|---|
| **gate** | T4 -> T1 | `perturbed_gene_id`+`culture_condition` <-> `target_contrast`+`culture_condition` (ENSG) | 11,422 ENSG |
| **effect -> program** | T1 -> T2 | `target_contrast_gene_name` <-> `variable` (SYMBOL) | 10,422 symbols |
| **program -> disease** | T2 -> T3 | `variable` <-> `intersecting_genes` (exploded SYMBOL) | 1,748 / 1,814 |
| **gene -> disease (direct)** | T1 -> T3 | `target_contrast_gene_name` <-> `intersecting_genes` | 1,692 |

Condition vocabulary is **identical** across T1, T4, and T3's `gene_set` suffix: `Rest`, `Stim8hr`, `Stim48hr` — so joins can (and should) be condition-matched.

## 3. Referee chain for one gene G

1. **QC gate (T4):** keep G only if it has >=1 guide with `signif_knockdown=True` in the condition of interest (aggregate guides -> gene).
2. **Effect (T1):** look up G's `ontarget_effect_size` / `ontarget_significant` / `n_downstream` at that condition.
3. **Program (T2):** map G symbol to `log_fc`/`zscore` in the Th1<->Th2 contrast (pick Ota or Hollbacker).
4. **Disease (T3):** find clusters whose `intersecting_genes` contain G (condition-matched `gene_set`) and read `odds_ratio`/`p_adj_fdr` per autoimmune disease; drop `negative_control_disease` rows.

Join on **ENSG** for T1<->T4 and on **gene SYMBOL** for T1<->T2<->T3.
