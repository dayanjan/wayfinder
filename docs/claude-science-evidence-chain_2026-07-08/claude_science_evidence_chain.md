# Evidence-Chain Adjudication — CD4⁺ T-cell Perturb-seq

**Role:** skeptical data-referee. **Condition:** `culture_condition == "Stim8hr"` throughout.
**Language is calibrated** (consistent with / supported / refuted / untested / flagged). No "discovered/proven".

**Claim under adjudication:** *NAB2 → Th1/Th2 polarization → atopic eczema* — does knocking down NAB2
shift the Th1/Th2 program in a way that ties, via disease-enriched gene modules, to atopic eczema?
Adjudicated as a 4-hop chain; each hop decided independently on a real table value.

---

## HOP 0 · GATE — did the NAB2 knockdown actually work? (T4)

**Reasoning.** Everything downstream is uninterpretable if the perturbation did not take. This gate is
the point of the exercise. I require NAB2's guides to show `signif_knockdown` at Stim8hr with guide
expression driven below NTC.

**Receipt (T4, Stim8hr):**

| guide | signif_knockdown | adj_p | guide_mean_expr | ntc_mean_expr | t |
|---|---|---|---|---|---|
| NAB2-2 | **True** | 1e-16 | 0.033 | 0.567 | -67.2 |
| NAB2-1 | **True** | 1e-16 | 0.079 | 0.567 | -26.6 |

2 of 2 guides pass. Expression falls from NTC 0.567 to 0.033/0.079 — a ~86–94% reduction, both at the
floor adj-p of 1e-16.

**HOP 0 verdict: PASSED.** The knockdown is real; downstream readouts are interpretable.

---

## HOP 1 · EFFECT — real on-target downstream transcriptional effect? (T1)

**Reasoning.** A working knockdown should produce a significant, on-target, reproducible downstream
signature — not an off-target smear.

**Receipt (T1, Stim8hr):** `ontarget_significant = True`; `ontarget_effect_size = -16.88`;
`n_downstream = 301`; `offtarget_flag = False`; `crossguide_correlation = 0.741`;
`crossdonor_correlation_mean = 0.736`.

301 downstream genes, large on-target effect, no off-target flag, and reproducibility across both
guides and donors.

**HOP 1 verdict: SUPPORTED.**

---

## HOP 2 · PROGRAM — does NAB2 shift the Th1/Th2 program? (T2)

**Reasoning.** T2 carries two independent polarization signatures (Ota 2021, Hollbacker 2021).
I report both. `log_fc > 0` = Th1-associated; significant iff `adj_p_value < 0.05`.

**Receipt (T2):**

| contrast | log_fc | zscore | adj_p_value | call |
|---|---|---|---|---|
| Th2_vs_Th1 (Ota 2021) | +0.633 | 7.71 | 1.95e-13 | **significant, Th1-associated** |
| Th2_vs_Th1 (Hollbacker 2021) | +0.609 | 2.39 | 0.205 | same direction, **not significant** |

Both contrasts point the **same way** (positive → Th1-associated) and the effect magnitudes are nearly
identical (+0.63 vs +0.61); significance clears in Ota but not in Hollbacker.

**HOP 2 verdict: SUPPORTED IN 1 OF 2 CONTRASTS (direction concordant).** Stated honestly: the program
shift is significant in the Ota signature and directionally consistent — but not independently
significant — in Hollbacker.

---

## HOP 3 · DISEASE — is NAB2 a member of an atopic-eczema-enriched cluster at FDR<0.05? (T3)

**Reasoning.** Explode `intersecting_genes`; filter `disease == "atopic eczema"` and
`gene_set == "downstream_Stim8hr"`; report NAB2's clusters' odds ratios and FDR.

**Receipt (T3, atopic eczema, downstream_Stim8hr):**

| cluster | odds_ratio | p_adj_fdr | significant |
|---|---|---|---|
| 100 | 3.90 | 0.0028 | **yes** |
| 90 | 3.43 | 0.022 | **yes** |
| 74 | 2.12 | 0.521 | no |
| 98 | 1.00 | 0.975 | no |

NAB2 is a member of **2 of 4** atopic-eczema clusters that are enriched at FDR<0.05.

**HOP 3 verdict: SUPPORTED.**

---

## Confounder stress-test — is the atopic signal just STAT6's cis shadow?

NAB2 sits ~1.9 kb from STAT6 (12q13), the master Th2/atopic-eczema TF. The worry: NAB2's atopic signal
is a genomic-locus / cis artifact of STAT6. Three in-data attacks:

**1. LOCUS test.** Member genes of NAB2's significant atopic-eczema clusters:
- **cluster 100** (OR 3.90): AGO2, NAB2, TBC1D10C, IL18RAP, REL, EGR2, CSF2, ETS1, ADO, **BACH2**
- **cluster 90** (OR 3.43): NSMCE1, **IL4**, IL22, TESPA1, NAB2, **IRF4**, IL26, AHI1, BCL2L11

**STAT6 is absent from both.** Members are canonical, genome-wide Th2/atopy regulators (BACH2, IRF4,
ETS1, REL, IL4) — not a 12q13 gene cluster. → **WEAKENS** the cis-artifact worry.

**2. PHENOCOPY / cis proxy.** If NAB2-KD phenocopied STAT6-KD, they would share perturbation-effect
clusters. NAB2 clusters (Stim8hr) = {74, 90, 98, 100}; STAT6 clusters = {30, 61, 85}. **Zero overlap.**
NAB2-KD does not phenocopy STAT6-KD. → **WEAKENS** the cis-artifact worry.

**3. REPRODUCIBILITY.** NAB2 crossguide_R = 0.741 (76th percentile of 1,102 populated perturbations) vs
STAT6 0.514 (53rd); crossdonor_R 0.736 vs 0.739 (comparable). NAB2 is at least as reproducible as STAT6.
→ **WEAKENS** the "noise near a real regulator" reading.

**All three checks WEAKEN the cis-artifact hypothesis.** This is consistent with the external
genome-wide DE result (run separately against the authors' 16.8 GB deposited matrix, not present here):
**STAT6 mRNA is UNMOVED under NAB2-KD (log2FC +0.09, adj-p 0.79, n.s.)** — NAB2 does not repress STAT6,
so the atopic signal cannot be STAT6's transcriptional shadow.

---

## Referee discriminates — two contrast cases, different verdicts

**SATB1 → Th1/Th2 → asthma @ Stim8hr — UNTESTED (the hero catch).**
GATE receipt (T4): SATB1-1 adj_p=0.70, SATB1-2 adj_p=0.75, **0/2 signif_knockdown**; guide_mean
2.386/2.404 vs NTC 2.349 (**no reduction**). T1: `ontarget_significant=False`, `n_downstream=0`.
T2 *does* show a Th2-associated hit (Ota log_fc=-0.186, z=-3.75, adj_p=9.1e-4) — **but the knockdown
never took, so this readout is uninterpretable.** Verdict = **UNTESTED**, explicitly *not* a negative.

**SLC1A5 → Th1/Th2 → asthma @ Stim8hr — REFUTED at the disease hop.**
GATE partial (SLC1A5-1 signif adj_p=0.0092; SLC1A5-2 n.s. adj_p=0.103). EFFECT weak:
`ontarget_significant=False`, `n_downstream=1`. DISEASE: SLC1A5 appears in **zero** asthma clusters
(downstream_Stim8hr) at any FDR — no disease-module membership. Verdict = **REFUTED** at HOP 3.

---

## Final calibrated verdict

The **NAB2 → Th1/Th2 → atopic eczema** chain is **SUPPORTED / CONSISTENT WITH the data** across all four
hops. The knockdown took (gate passed, 2/2 guides, ~90% reduction), produced a large reproducible
on-target downstream effect (301 genes, R≈0.74), shifted the Th1/Th2 program in a Th1-associated
direction (significant in Ota, direction-concordant in Hollbacker), and placed NAB2 in two
atopic-eczema-enriched clusters at FDR<0.05 (OR 3.90 and 3.43). The sharpest confounder — that this is
STAT6's cis shadow — is **weakened by every in-data check** (no locus artifact, no phenocopy,
reproducibility at/above STAT6), converging with the external finding that STAT6 mRNA is unmoved under
NAB2-KD. The referee is not a rubber stamp: SATB1 returns **UNTESTED** (failed gate) and SLC1A5 returns
**REFUTED** (no disease membership) on the same machinery.

## What we do NOT claim
- Not "discovered" or "proven" — this is receipt-backed consistency in observational Perturb-seq.
- **No causal disease mechanism and no in-vivo relevance** are established; T3 is cluster/odds-ratio
  co-membership, not a demonstrated pathway to eczema.
- The program shift (HOP 2) is significant in **one of two** polarization signatures; we do not claim
  cross-signature program-level proof, only direction-concordant support.
- The definitive cis-check (STAT6 mRNA under NAB2-KD) is **cited from an external genome-wide matrix
  not present in these four tables**; our independent work here bears only on the locus/phenocopy/
  reproducibility arguments.
