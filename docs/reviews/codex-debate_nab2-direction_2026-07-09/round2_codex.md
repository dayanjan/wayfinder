# Round 2 Codex Review — NAB2 Direction GEO Mining Plan v2

Live checks used NCBI E-utilities + GEO FTP on 2026-07-09; evidence snapshots:
`.claude/scratch/round2_geo/adopted_dataset_checks.json`,
`tcell_focus_checks.json`, `tcell_nab2_probe_checks.json`,
`final_tcell_matrix_probe_hits.json`. v2 correctly incorporated my Round-1 P0/P1s:
ARM B is privileged, ARM C is now skin-first, GSE183953 is context only, NAB2 row/probe resolution is deterministic,
bulk attribution is guarded, and the "tracks != effector" ceiling is explicit.

## A. New Dataset Verification + T-cell Arm

| Dataset | Status | Evidence | Use |
|---|---:|---|---|
| GSE130588 | PASS | GEO summary: 208 samples, GPL570. Series says skin biopsies from 52 AD patients randomized dupilumab/placebo for 16 weeks; sample metadata include `skin biopsy`, Week0/4/16, `tissue: LS/NL`, `treatment: Dupilumab/Placebo`, subject id. Series matrix exists; RAW tar exists. Exact matrix rows found for NAB2 probes `212803_at` and `216017_s_at`. | ARM C primary. Model lesion status + week + treatment + subject; do not pool LS/NL. |
| GSE59294 | PARTIAL | GEO summary: 40 samples, GPL570. Series says pre/post skin biopsies from AD patients treated with dupilumab/placebo; metadata include `human skin biopsy`, `LS/NL skin`, `time: Pre/Post`, treatment arms B/C/D/placebo, patient id. Matrix + RAW tar exist. Exact matrix row found for `212803_at`; `216017_s_at` not found in the series matrix although present on GPL570. | ARM C backup is usable via `212803_at`, but v2 §2 should not say both NAB2 probes are present in this matrix. |
| GSE204762 | PASS | GEO summary: human/mouse scRNA; human GPL18573 matrix exists. Series summary: 310,691 cells from whole skin, 19 adults, non-lesional/lesional skin from 11 AD patients plus healthy and scleroderma. Metadata include `skin`, `disease: Atopic dermatitis/Healthy`, sample titles with AD non-lesional and lesional; FTP RAW tar lists per-sample `.h5ad.gz` matrices. | ARM D primary. Use human GPL18573/h5ad files only. |
| GSE204765 | PASS-as-superseries | Superseries with GPL18573 matrix and RAW tar; overall design says "Refer to individual Series"; same human sample titles/metadata and `.h5ad.gz` members as GSE204762, plus related modalities. | Cite as superseries context, but execute from GSE204762 to avoid double-counting. |

Verified T-cell candidates that close v2 §2:

| Dataset | Status | Evidence | Use |
|---|---:|---|---|
| GSE32959 | PASS | Human cord-blood CD4+ Th cells, GPL570, n=37. Design: activated CD4+ cells polarized Th1 with IL-12 or Th2 with IL-4 + anti-IL-12 at 12/24/48/72h, 3 biological reps. Series matrix exists. Exact NAB2 rows `212803_at` and `216017_s_at` found. Note: 26 samples are a reanalysis of GSE17974 CEL files. | Best T-cell polarization arm: Th2 vs activated and Th1 vs activated by timepoint; report probe concordance. |
| GSE60678 | PASS | Naive CD4+ T cells from 4 healthy buffy-coat donors, Agilent GPL14550, n=48. Design: Th1 conditions (IL-12 + IL-2 + anti-IL-4) and Th2 conditions (IL-4 + IL-2 + anti-IL-12 + anti-IFNg), 6h/24h/3d/6d/8d. GPL14550 annotates `A_33_P3248794` as NAB2/Entrez 4665; exact matrix row found. | Independent adult-donor Th1/Th2 polarization validation; prefer donor-paired mixed model. |
| GSE17851 | PASS backup | Human cord-blood CD4+ cells, GPL6102, n=54. Control vs STAT6 siRNA; activated +/- IL-4 at 12/24/48/72h, 3 reps. GPL6102 annotates `ILMN_1663554` as NAB2/Entrez 4665; exact matrix row found. | IL-4/STAT6-specific backup; primary contrast should be control-siRNA Act+IL-4 vs Act. |

## B. Findings on v2

P0 — §2/§3 should add an explicit **ARM T** or T-cell appendix now that suitable datasets exist.
Without this, the final can still over-transfer skin/epithelial ARM B to the T-cell mechanistic claim. Fix:
add GSE32959 primary + GSE60678 backup as a non-voting or privileged context arm, and require the final wording
to state whether T-cell NAB2 direction agrees with skin/epithelial direction.

P1 — §1 decision rule is mostly sound, but still lacks conflict handling inside an arm. ARM A has two endpoints
(lesional FC and NAB2/type-2 rho), ARM C has two NAB2 probes in primary but one probe in backup, and backups may
be non-equivalent. Fix: predefine endpoint hierarchy: for each arm, call direction only if the primary NAB2
contrast and score correlation are concordant or one is explicitly secondary; probe discordance => AMBIGUOUS;
backup absence is not a failure if the primary passes and backup is declared sensitivity-only.

P1 — §3.4 type-2 score list is acceptable as a pre-specification but too cytokine-heavy for skin RNA-seq/scRNA.
IL4/IL5 will often fail detection, and CCL17/CCL22 can track immune-cell abundance rather than per-cell Th2 tone.
Fix: define numeric detection gates now: bulk RNA-seq CPM/normalized count threshold in >=20% samples; arrays
above background or expressed above lower-quartile intensity; scRNA pseudobulk gene detected in >=10% of donors
or >=20 cells per condition. Always report: full score, detection-filtered score, and chemokine/receptor-only
sensitivity (`CCL17/CCL22/CCL26/TSLP/IL4R/IL31`) with dropped genes listed.

P1 — §3.5 cell-composition guard is feasible, but "deconvolve OR ARM-D pseudobulk" should become "deconvolve AND
ARM-D pseudobulk when possible." Deconvolution/marker covariates are feasible for GSE330551 and arrays but are
model-dependent and weak for skin compartments. ARM-D pseudobulk from GSE204762 h5ad matrices is more reliable
for attribution if cell annotations are present; if annotations are absent, first verify/rebuild coarse labels
(keratinocyte, fibroblast, endothelial, myeloid, T/NK). Use deconvolution to adjust ARM A; use ARM D to interpret
which compartment carries NAB2.

P1 — §3.6 STAT6/12q13.3 adjustment is not concrete enough. Fix: define it as a sensitivity model, not the primary
contrast: `NAB2_expr ~ condition_or_score + STAT6_expr + cell_composition_covariates + batch/donor`, with donor
random/fixed effects where paired. For ARM C also test `delta_NAB2 ~ treatment + delta_STAT6` by subject/time.
Report whether the condition coefficient changes sign or shrinks >50%. Do not overinterpret STAT6 adjustment:
STAT6 may be a mediator of IL-4/IL-13 response, so adjustment can be a collider/over-control, not just cis cleanup.

P2 — §4 pre-flight should include "NAB2 measurable after platform annotation" not only exact symbol/probe rows;
GSE60678/GSE17851 show why. Store the platform mapping evidence beside results.

P2 — §2 table should correct GSE59294 NAB2 row wording: matrix has `212803_at` verified; `216017_s_at` was not
found live in the downloadable series matrix.

## C. Convergence Verdict

NEEDS-ROUND-3-ON: add/decide ARM T, codify intra-arm conflict rules, make STAT6 adjustment executable; otherwise v2 is directionally sound and the remaining issues are polish.
