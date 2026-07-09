# Plan — resolve the DIRECTION of NAB2 modulation in atopic-dermatitis skin, via orthogonal GEO mining (v3)

**2026-07-09.** Hardened by Rounds 1–2 of a repo-read codex-debate (Codex verified every dataset live against
GEO; `docs/reviews/codex-debate_nab2-direction_2026-07-09/round{1,2}_codex.md` — all findings accepted). Goal:
determine, from independent human transcriptomics, the DIRECTION OF ASSOCIATION between NAB2 and the pathogenic
Th2 program — in **CD4 T cells** (on-point) and in **AD skin** (target tissue) — to INFORM (not prove) whether a
topical NAB2 therapeutic should down- or up-modulate. Orthogonal validation of NAB2 → Th1/Th2 → atopic eczema.
New work; calibrated language.

## 0. The ceiling (state up front)
Expression mining establishes **direction of association**, not therapeutic direction: a gene that *tracks* Th2
may be a pathogenic effector OR an induced negative-feedback brake. Strongest honest output = a **DOWN- or
UP-modulation HYPOTHESIS, association-backed**, upgraded to "perturbation-consistent" only if the cytokine-
perturbation arm (B) agrees. Verdicts: **DOWN-hyp / UP-hyp / AMBIGUOUS / NO-CALL**.

## 1. Arms + decision rule
Voting arms A, T, B, C (B privileged = only perturbation-of-Th2 arm); D = cell context (non-voting).
- **ARM A — Skin association.** NAB2 **lesional vs non-lesional/healthy** log2FC+FDR AND Spearman ρ(NAB2, type-2
  score); cell-composition-guarded (§3.5).
- **ARM T — CD4 T-cell association (on-point).** In isolated CD4 T cells, is NAB2 **up in Th2- vs Th1-polarized
  (or vs activated)**? This most directly tests the Perturb-seq finding's own direction. (Marker-validated
  polarity: our T2 signature has +log_fc = Th2 — cross-check ARM T against that.)
- **ARM B — Skin/epithelial cytokine causation.** Does **IL-4/IL-13 induce** NAB2 in skin cells? Labeled
  EPITHELIAL (not T-cell). Closest to causal but in vitro.
- **ARM C — Skin treatment reversal.** Does NAB2 **fall after dupilumab** in *skin*? (blood = context, no vote.)
- **ARM D — Cell resolution.** scRNA: which compartment (T cell vs keratinocyte) carries the NAB2 signal, AD vs
  healthy — interprets ARM A and tells us what a topical would hit.
- **DECISION RULE:**
  1. Per-arm gate: |log2FC| ≥ 0.3 (or |ρ| ≥ 0.3) AND FDR < 0.05.
  2. **Intra-arm conflict (P1):** each arm has a PRIMARY endpoint (ARM A: lesional FC; ARM T/B/C: the primary
     contrast's NAB2 change) and a SECONDARY (ARM A: type-2 ρ; multi-probe/backup). Call an arm's direction only
     if primary passes; if primary vs secondary (or the two array probes) **disagree in sign → that arm =
     AMBIGUOUS**. Backup-dataset absence is NOT failure if the primary passes (declare backup sensitivity-only).
  3. **Overall:** ≥2 voting arms concordant (post-gate, post-conflict) → DOWN-hyp or UP-hyp. **If A/T/C agree but
     B is null/opposite → "association-backed, not perturbation-backed."** <2 usable voting arms → NO-CALL.
  4. **Final wording MUST state whether the T-cell direction (ARM T) agrees with the skin direction (ARM A/B/C).**

## 2. Datasets (Rounds 1–2 live-verified)
| GSE | arm | status | platform | groups | NAB2 row |
|---|---|---|---|---|---|
| GSE330551 | A | PASS | RNA-seq | 174 skin: Lesion/Non-Lesion/Control (the n=174 set, not a 30-study meta-set) | `NAB2` in counts.txt.gz (raw→normalize) |
| **GSE32959** | **T (primary)** | PASS | array GPL570 | cord-blood CD4+ Th, **Th1(IL-12) / Th2(IL-4)** polarization, 12–72h ×3 | probes `212803_at`,`216017_s_at` |
| GSE60678 | T (backup) | PASS | array GPL14550 | naive CD4+ adult donors, Th1/Th2 conditions, 6h–8d | `A_33_P3248794`=NAB2 (donor-paired) |
| GSE17851 | T (STAT6 test) | PASS | array GPL6102 | cord-blood CD4+, **ctrl vs STAT6-siRNA**, Act±IL-4, 12–72h | `ILMN_1663554`=NAB2 |
| GSE292848 | B (primary) | PASS | RNA-seq | NativeSkin ctrl + **IL-4/IL-13/IL-4+13/IL-22** 24h ×5 (separable) | `ENSG00000166886` |
| GSE282371 | B (backup) | PASS | RNA-seq | keratinocyte equivalents + IL-4+IL-13 (combined) | `NAB2` in count TSVs |
| GSE130588 | C (primary) | PASS | array GPL570 | **skin**, 52 AD, dupilumab/placebo, wk0/4/16, LS/NL | probes `212803_at`,`216017_s_at` |
| GSE59294 | C (backup) | PARTIAL | array GPL570 | **skin** pre/post dupilumab | ONLY `212803_at` verified in matrix (not `216017_s_at`) |
| GSE183953 | C context | DEMOTED | scRNA PBMC | 4 AD pre/post — blood proxy, no vote | raw H5 |
| GSE204762 | D (primary) | PASS | scRNA | 310,691 cells whole skin: AD lesional/non-lesional + healthy (h5ad) | scRNA features |
| GSE288946/GSE328048 | D backup | PARTIAL | scRNA | AD vs healthy / keratinocyte subclusters | MTX (needs annotation) |
(GSE204765 = superseries of GSE204762; execute from GSE204762 to avoid double-counting.)

## 3. Method (deterministic)
1. **NAB2 resolver:** Ensembl `ENSG00000166886` / symbol `NAB2` / Entrez `4665`; collapse dup rows (sum counts
   RNA-seq; max-mean-intensity probe array) AND report every probe — sign-discordant probes ⇒ arm AMBIGUOUS,
   never cherry-pick. Pre-flight = "NAB2 measurable after platform annotation," store the mapping evidence.
2. **Normalize** raw counts (DESeq2/limma-voom) before contrasts; model donor/batch/study covariates (GSE330551).
3. **Contrasts:** paired/mixed model by patient/donor where metadata support it; NAB2 log2FC, direction, FDR.
4. **Type-2 score (pre-specified + detection gates, P1):** genes {IL13,IL4,IL5,IL31,CCL17,CCL22,CCL26,TSLP,IL4R};
   detection gate: bulk = normalized CPM above threshold in ≥20% samples; array = above background/lower-quartile;
   scRNA pseudobulk = detected in ≥10% donors or ≥20 cells/condition. Report THREE scores: full, detection-
   filtered, and chemokine/receptor-only sensitivity {CCL17,CCL22,CCL26,TSLP,IL4R,IL31}; list dropped genes.
5. **Cell-composition (P0/P1):** for ARM A bulk, **deconvolve (marker covariates) AND corroborate with ARM-D
   pseudobulk-by-cell-type** when possible — deconvolution ADJUSTS ARM A; ARM D INTERPRETS which compartment
   moves. If GSE204762 lacks cell labels, rebuild coarse labels (keratinocyte/fibroblast/endothelial/myeloid/T-NK).
6. **STAT6 / 12q13.3 (P1, concrete):** (a) DIRECT test — in GSE17851, is NAB2's IL-4 induction STAT6-siRNA-
   dependent? (better than statistical adjustment). (b) SENSITIVITY model (not primary):
   `NAB2 ~ condition_or_score + STAT6 + cell_comp + batch/donor` (donor random/fixed where paired); ARM C:
   `ΔNAB2 ~ treatment + ΔSTAT6` by subject. Report if the condition coefficient flips sign or shrinks >50%.
   **CAVEAT:** STAT6 is a mediator of IL-4/IL-13 signaling, so adjusting for it can be collider/over-control, not
   just cis-cleanup — present as sensitivity context, do not let it override the primary contrast.

## 4. Acceptance + pre-flight gates
Per-dataset pre-flight (all pass or arm = NO-CALL): processed matrix present; NAB2 resolved via platform
annotation; ≥3 biological units/contrast; metadata sufficient for the contrast. Deliverable
`docs/nab2-direction-geo_<date>/`: per-arm table (dataset, contrast, NAB2 log2FC/ρ, direction, FDR, type-2
correlation, STAT6), the triangulated **DOWN-hyp / UP-hyp / association-backed / AMBIGUOUS / NO-CALL** call with
the explicit **ARM-T-vs-skin agreement statement**, and calibrated caveats. Every number traces to a downloaded
matrix; explicit no-call path.

## 5. Honesty guardrails
- **Tracks ≠ effector** (brake vs driver — only perturbation separates them; language stays "consistent with a
  DOWN/UP hypothesis" unless B agrees). **Association ≠ causation. Bulk ≠ per-cell. Blood ≠ skin.
  Skin-epithelial ≠ CD4-T-cell** (say which tissue each arm speaks for; ARM T is the T-cell voice).
- Effect sizes + direction always, never bare "significant"; weak/inconsistent → AMBIGUOUS/NO-CALL, plainly.
- Extract covariates (lesion chronicity, washout, age/sex, site, severity, S. aureus, meds); report robustness.

## 6. Out of scope
Wet-lab validation; modality/delivery design; any claim a GEO association proves therapeutic direction.
