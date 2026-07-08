# Independent replication targets — pressure-test these exact claims

You are an independent lab. Treat every number below as a CLAIM to be reproduced or refuted from
the **raw data**, not trusted. Re-derive independently. Report matches AND mismatches. No cutting
corners: if you can't reproduce a number, say so and show what you got instead.

## Raw data (the ground truth — compute from THESE, not from our claims)
- `data/guide_kd_efficiency.suppl_table.csv` (T4) — guide × condition; `signif_knockdown`, `perturbed_gene_id` (ENSG), `culture_condition`, `guide_mean_expr`, `ntc_mean_expr`, `adj_p_value`.
- `data/DE_stats.suppl_table.csv` (T1) — perturbation × condition; `target_contrast_gene_name` (SYMBOL), `target_contrast` (ENSG), `culture_condition`, `ontarget_significant`, `ontarget_effect_size`, `n_downstream`, `offtarget_flag`.
- `data/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv` (T2) — gene(`variable`) × `contrast`; `log_fc`, `zscore`, `adj_p_value`. Contrasts: "Th2_vs_Th1 (Ota 2021)", "Th2_vs_Th1 (Hollbacker 2021)".
- `data/cluster_autoimmune_enrichment_results.suppl_table.csv` (T3) — `cluster` × `disease` × `gene_set`; `odds_ratio`, `p_adj_fdr`, `intersecting_genes` (stringified python list — ast.literal_eval), `negative_control_disease`.
- Condition of record: **Stim8hr**. Disease gene_set suffix: `downstream_<condition>`. Significance: FDR/adj-p < 0.05.

## CLAIM SET A — the NAB2 headline receipt (NAB2 × atopic eczema @ Stim8hr)
- A1 GATE: NAB2 has **2/2 guides** with signif_knockdown=True, best guide adj_p ≈ **1e-16**; mean guide expr ≈ **0.056** vs NTC ≈ **0.567**.
- A2 EFFECT: NAB2 `ontarget_significant`=True, `ontarget_effect_size` ≈ **−16.9**, `n_downstream` = **301**, `offtarget_flag`=False.
- A3 PROGRAM: NAB2 in T2 — Ota 2021 `log_fc` ≈ +0.63, `zscore` ≈ **+7.71**, adj_p ≈ **1.96e-13** (significant, Th1-associated); Hollbacker 2021 NOT significant (adj_p ≈ 0.20).
- A4 DISEASE: NAB2 in atopic-eczema-enriched clusters with **OR ≈ 3.90, FDR ≈ 0.0028** AND **OR ≈ 3.43, FDR ≈ 0.0224** (≥1 cluster FDR<0.05 → disease supported for atopic eczema specifically).

## CLAIM SET B — the funnel (Stim8hr)
- B1 A universe (KD-gate ∩ effect ∩ program-significant T2 adj_p<0.05) ≈ **3,935 genes**.
- B2 candidate (gene×disease) pairs after gate [ab≥ab_gate(50th pct) AND bc≥3 AND OpenTargets-known≤0.1] ≈ **22,039**. (ab/bc are Europe PMC co-mention counts; you may take our cached values as given for B2, but re-derive the referee side below independently.)
- B3 referee **disease-C-supported** survivors = **43**; of which **CLEAN full-chain supported (gate+effect+program+disease-C all hold, n_downstream>0) = 30**; supported_weak(n_downstream=0)=**10**; supported_flagged(offtarget)=**3**; refuted_effect=**1**; refuted_for_c=**21,995**.
- B4 pure-disjoint (ac_lit=0) among clean supported = **1** (NUDT1 × type 1 diabetes, effect=4).

## CLAIM SET C — STAT6 confounder checks
- C1 NAB2's atopic-eczema clusters are **74 and 90**; STAT6 is in **neither**; of ~67 member genes only NAB2+TESPA1 are on 12q13 → genome-wide functional modules, NOT a 12q13 locus artifact.
- C2 NAB2 program shift z ≈ **+7.71** (Ota) vs STAT6 z ≈ **+2.66** (Ota) → NAB2 ~8× stronger; both Th1-associated.
- C3 NAB2 referee-supported disease profile = **{asthma, atopic eczema}**; STAT6 = **{asthma, atopic eczema}** (identical).

## CLAIM SET D — EGR mechanism check
- D1 EGR2 referee-supported for **11/12** diseases (broad); NAB2 for **2** (narrow atopic); NAB1 and EGR1 and EGR3 for **0**.
- D2 NAB2-KD program direction (Th1) is the **same** as EGR2-KD (not opposite) → inconsistent with NAB2 acting purely as EGR2's de-repressor.
- D3 NAB1 (paralog corepressor) program direction is **Th2** (opposite NAB2), 0 diseases.

## CLAIM SET E — novelty (literature)
- E1 **Zero** papers directly link NAB2 to Th1/Th2 polarization.
- E2 **Zero** papers directly link NAB2 to atopic dermatitis/eczema.
- E3 NAB2 sits **~1.9 kb from STAT6** on chr12q13.3 (the atopic/Th2 master gene).

## Rules of engagement (no corner-cutting)
1. Re-derive from the RAW CSVs. You MAY read our code (`src/arbiter/lbd/`) to understand the claimed method, but the numbers you report must be YOUR independent computation.
2. Adversarial: actively try to break each claim. A refuted claim with evidence is the most valuable output.
3. Report EXACT numbers you obtained next to the claim, and PASS / FAIL / PARTIAL per item.
4. Flag any statistical or logical error in the method (multiple-testing, FDR application, answer-leakage into the A universe, the ab-gate, the full-chain definition).
5. State your overall verdict: does the finding replicate, and where is it fragile?
