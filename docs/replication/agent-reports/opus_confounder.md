# Independent replication — CLAIM SET C (STAT6 confounder) + D (EGR mechanism)

**Reviewer:** independent lab, adversarial skeptic. **Method:** my own pandas over the four raw
CSVs. I re-implemented each referee hop myself from reading `pyzobot_referee.py`; I did **not**
call the project's referee. Condition of record = Stim8hr, gene_set `downstream_Stim8hr`, FDR/adj-p
< 0.05. Scripts: `.claude/scratch/lbd-debate/opus_indep_CD.py`, `opus_cytoband.py` (MyGene REST for
cytobands). Disease profile restricted to the 12 **eligible** diseases (matches `load_c()`), which is
what the claims mean by "supported."

---

## Verdict table (my numbers)

| Claim | Status | My result vs claim |
|---|---|---|
| C1 clusters = 74 & 90 | **FAIL (IDs) / PASS (conclusion)** | Significant atopic-eczema clusters are **90 & 100**, not 74 & 90. Cluster 74 FDR=**0.52** (not significant). STAT6 absent from the real clusters; locus-artifact still refuted. |
| C1 only NAB2+TESPA1 on 12q13 | **PASS (with nuance)** | On the corrected clusters: cl90 12q13={NAB2, TESPA1}; cl100 12q13={NAB2}. Genome-wide spread (16–20 chromosome arms). |
| C2 z 7.71 vs 2.66 | **PASS** | NAB2 z=+7.71 (Ota), STAT6 z=+2.66 (Ota). Exact match. Both Th1-assoc, Ota-only. |
| C2 "NAB2 ~8× stronger" | **PARTIAL** | 8× is the **log_fc** ratio (0.633/0.080=7.9×). The **z** ratio is only **2.9×** (7.71/2.66). The claim pairs the z-values with a magnitude that comes from log_fc. |
| C3 identical {asthma, atopic eczema} | **PASS** | Both profiles = {asthma, atopic eczema}. Jaccard = 1.00. Reproduced exactly. |
| D1 EGR2 11/12; NAB2 2; NAB1/EGR1/EGR3 0 | **PASS** | EGR2 = 11/12 (missing Hashimoto's); NAB2 = 2; NAB1/EGR1/EGR3 = 0. All exact. |
| D2 NAB2 dir = EGR2 dir (Th1) | **PARTIAL** | Same **sign** in all 4 measurements — but significance lands in **mutually exclusive** contrasts and EGR2's only significant contrast is **borderline (adj-p=0.049)**. |
| D3 NAB1 opposite (Th2), 0 diseases | **PASS** | NAB1 z=−3.52 (Ota), −3.34 (Holl), significant in **both**; 0 diseases. Strongest anti-confounder signal in the set. |

---

## What I reproduced (numbers)

**C1 — NAB2 atopic-eczema clusters (T3, downstream_Stim8hr):**
```
cluster  odds_ratio  p_adj_fdr   -> significant?
   100      3.899      0.00283    YES  (the OR≈3.90 headline)
    90      3.430      0.02239    YES  (borderline)
    74      2.117      0.52079    NO
    98      1.004      0.97538    NO
```
The two FDR<0.05 clusters are **90 and 100**. The claim's "74 and 90" is wrong: cluster 74 is not
significant (FDR 0.52), and cluster **100** (the actual OR≈3.90/FDR≈0.0028 receipt cited in A4) is
missing from C1's list. **The project's own confounder script hardcodes `for cl in [74, 90]`
(`docs/nab2_stat6_confounder_check.py:34`) — so its published locus test ran on cluster 74, a
non-significant cluster, and never tested cluster 100.**

Locus test on the corrected clusters (MyGene cytobands; STAT6 and NAB2 both = 12q13.3, TESPA1 = 12q13.2):
```
cluster 90 : 37 members, STAT6 absent, on-12q13 = {NAB2, TESPA1}, spread over 16 chrom. arms
cluster 100: 38 members, STAT6 absent, on-12q13 = {NAB2},          spread over 20 chrom. arms
(cluster 74: 30 members, STAT6 absent, on-12q13 = {NAB2, TESPA1} — same conclusion, wrong cluster)
```
So the *conclusion* survives on the right clusters: STAT6 is not a co-member, only NAB2 (± TESPA1)
sits on 12q13, and the modules are genuinely genome-wide. Not a physical-linkage artifact.

**C2 — program shift (T2):**
```
NAB2  Ota z=+7.71 adjp=1.95e-13 (sig, Th1)   Holl z=+2.39 adjp=0.205 (ns)
STAT6 Ota z=+2.66 adjp=2.68e-02 (sig, Th1)   Holl z=+0.82 adjp=0.881 (ns)
```

**C3 — supported disease profile (full clean chain, eligible-12):** NAB2 = {asthma, atopic eczema};
STAT6 = {asthma, atopic eczema}. Identical. (STAT6 also passes gate 2/2, effect −18.7, n_down=232 —
a fully valid, comparably-strong perturbation.)

**D — module (Stim8hr):**
```
gene  gate  effect(size, n_down, offt)      program (log_fc; z; sig)
NAB2  2/2   sup (-16.9, 301, F)   Ota +0.63/z7.71 SIG(Th1)   Holl +0.61/z2.39 ns
NAB1  2/2   sup (-15.1,   0, F)   Ota -0.24/z-3.52 SIG(Th2)  Holl -0.69/z-3.34 SIG(Th2)
EGR1  2/2   sup ( -4.7,   6, F)   Ota -0.47 ns               Holl -0.21 ns          -> program refuted
EGR2  2/2   sup (-11.1, 854, F)   Ota +0.33/z0.86 ns         Holl +2.44/z3.06 SIG(Th1, adjp=0.049)
EGR3  2/2   sup ( -3.8, 101, F)   Ota +1.08 ns               Holl +0.11 ns          -> program refuted
```
D1 supported-disease breadth (eligible-12): EGR2=11, NAB2=2, NAB1=0, EGR1=0, EGR3=0. NAB1's 0 is
because n_downstream=0 (empty effect → chain can't complete), not disproven cluster membership.

---

## Adversarial case #1 — "NAB2's eczema signal IS just STAT6" (steelman)

The surface facts look like textbook confounding: NAB2 sits ~1.9 kb from STAT6, the atopic/Th2
master gene (E3); NAB2 and STAT6 have **identical** referee disease profiles (C3, Jaccard 1.0);
both push the program the **same** direction. If the "NAB2 signal" were STAT6 bleeding through, this
is exactly what you'd see.

**Where I can make the confounder bite (real weaknesses the authors under-state):**

1. **C3 gives the confounder zero discriminating evidence to overcome.** The referee's disease layer
   cannot tell NAB2 from STAT6 — same two diseases, same direction. Every argument for "distinct
   biology" rests on *magnitude* (C2) and *cluster co-membership* (C1); the disease profile itself
   actively looks confounded. A reviewer who only reads the verdict profiles would conclude NAB2 ≈
   STAT6.
2. **The magnitude separation is smaller than advertised.** On the proper statistic (z), NAB2 is
   2.9× STAT6, not 8×. 8× is a log_fc ratio and log_fc is not the reliability of the shift. So "NAB2
   is a much stronger, distinct effect" is a ~3× argument dressed as an ~8× argument.
3. **The eczema enrichment is thinner than the headline.** NAB2 appears in 4 atopic-eczema clusters;
   only 2 pass FDR, and one of those (cluster 90) is borderline at FDR=0.022. And **the published
   locus check tested the wrong cluster (74, FDR=0.52).** A QC that mislabels its own supporting
   clusters is exactly the kind of thing a confounder hides behind.

**Why the confounder still fails (the data that breaks it):**

- **The perturbation is molecularly NAB2, not STAT6.** 2/2 on-target guides, `offtarget_flag=False`,
  n_downstream=301. If the guides silently hit STAT6, the off-target QC would flag it; it doesn't.
- **STAT6 is independently knocked down and is weaker.** STAT6-KD gives z=+2.66 vs NAB2's +7.71.
  NAB2-KD does *more* to the program than STAT6-KD does — inconsistent with NAB2 being a STAT6 proxy.
- **STAT6 is not in NAB2's clusters and the modules are genome-wide** (16–20 arms; only NAB2±TESPA1
  on 12q13). The enrichment is functional co-expression, not 12q13 linkage.

**Net on C:** the confounder is *credible at the disease-profile layer* and the authors should not
lean on C3 as evidence of distinctness — it is the opposite. But the guide-level KD specificity plus
STAT6's own weaker, separately-measured perturbation plus non-linked cluster membership refute the
"it's just STAT6" story. Confounder **rejected**, but by C1+C2 mechanics, not by C3.

## Adversarial case #2 — "NAB2 is just EGR2's de-repressor / EGR-mediated" (steelman)

The de-repression prediction: NAB2/NAB1 are EGR corepressors; NAB2-KD removes the brake → EGR
activity ↑ → phenotype OPPOSITE to EGR2-KD. The authors argue same-direction (D2) refutes this.

**Where D2 is genuinely weak (adversarial item 4 is correct):** NAB2 and EGR2 are **never
co-significant in the same reference cohort.** NAB2's significant contrast is Ota (z=7.71); EGR2's is
Hollbacker (z=3.06, **adj-p=0.049 — barely under threshold**); each is NS in the other's contrast.
"Same direction" is therefore a comparison of a rock-solid Ota signal against a borderline Hollbacker
signal — different datasets, one of them fragile. D2 as literally stated ("same direction in the
significant contrast") is a cross-cohort comparison and should be labeled PARTIAL, not a clean refutation.

**And D1's breadth contrast does NOT refute EGR-mediation** — it's compatible with it. NAB2's
{asthma, atopic eczema} is a strict **subset** of EGR2's 11 diseases. A narrow modulator acting
through/parallel to EGR2 would look exactly like this. So the "EGR2 broad, NAB2 narrow" contrast
cannot distinguish "independent regulator" from "narrow EGR2-downstream effector."

**Why EGR-mediation still fails (the strongest single fact in the whole assignment — D3):** NAB1,
NAB2's **paralog in the same corepressor family**, goes the **opposite** direction (Th2; z=−3.52/−3.34,
significant in **both** contrasts). If NAB1 and NAB2 were both generic EGR corepressors, their KDs
should look alike; instead they are cleanly opposite. That non-redundancy is real, robust (both
contrasts significant, unlike the NAB2-vs-EGR2 comparison), and is the best evidence that NAB2 is a
distinct regulator rather than a swappable EGR brake. On the sign level, NAB2 is also positive (Th1)
in *both* contrasts, so it never behaves like an EGR-de-repressor in either dataset.

**Net on D:** the EGR-de-repression model is disfavored, but the authors are leaning on the weakest
leg (D2, cross-cohort, EGR2 borderline). They should reframe the argument around **D3 (paralog
opposition, both-contrast-significant)**, which is the actually-robust refutation.

---

## Overall calibrated verdict

**The "genuine novel regulator" conclusion replicates, but two of its supporting claims are
mis-stated and one QC was run on the wrong object.**

- **Robust:** C2 z-scores, C3 identical profile, D1 breadth, D3 paralog opposition all reproduce
  exactly. NAB2 is a validated, on-target, genome-wide-module perturbation whose effect is not a
  12q13 linkage artifact and not a STAT6 proxy at the guide level.
- **Fragile / needs correction:**
  1. **C1 cluster IDs are wrong (74/90 → should be 90/100); the confounder script tested
     non-significant cluster 74 and never tested cluster 100.** Fix the hardcoded `[74, 90]`.
     Conclusion survives, but the receipt is currently pointing at the wrong cluster — a real
     credibility hole for a project whose whole thesis is "a receipt for every hop."
  2. **C2's "~8×" conflates log_fc with z.** State it as "~8× on effect size / ~3× on z" or drop the
     multiplier.
  3. **C3 is the confounder's best evidence, not the finding's** — presenting identical profiles as
     support for distinctness is backwards. Distinctness comes from C1 (co-membership) + C2 (magnitude)
     + guide specificity, and those should carry the argument.
  4. **D2 is a cross-cohort comparison with a borderline EGR2 contrast (p=0.049).** Downgrade it and
     promote **D3** as the load-bearing anti-EGR-mediation evidence.

**Bottom line:** I could not turn NAB2 into "just STAT6" or "just EGR2" — the guide-level KD
specificity, STAT6's weaker independent perturbation, and especially the NAB1 paralog opposition hold
up. But the finding is currently **over-claimed in its statistics (C2 8×), mis-referenced in its
clusters (C1 74 vs 100), and defended with its weakest evidence (C3 for distinctness, D2 for
mechanism).** Corrected and re-argued around C1(90/100)+C2(z)+D3, the novel-regulator conclusion is
**consistent with the data and survives an adversarial confounder + mechanism attack** — a
calibrated *PASS with mandatory corrections*, not a clean sweep.
