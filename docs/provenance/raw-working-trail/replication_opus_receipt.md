# Independent replication — CLAIM SET A (NAB2 × atopic eczema @ Stim8hr)

**Replicator:** independent lab (Opus). **Method:** every number below re-derived by me directly
from the raw supplementary CSVs with pandas. I read `src/arbiter/lbd/referee_triple.py` and
`docs/perturbseq-qc_2026-07-07/pyzobot_referee.py` ONLY to understand their claimed method; no
number here is taken from their code or their claims. NAB2 = `ENSG00000166886` (confirmed from T1).

## Verdict (one line)
**The NAB2 receipt REPLICATES.** All four gates A1–A4 reproduce to the stated precision from raw
data, and two independent spot-check receipts (BHLHE40, UFM1) also hold. The finding is robust.
Three caveats are worth recording — none refute the receipt — the most important being a **cluster-ID
error in Claim Set C1** (the atopic-eczema clusters are **100 & 90, not 74 & 90**).

---

## A1 — KNOCKDOWN GATE  → **PASS**
NAB2 guides @ Stim8hr (`guide_kd_efficiency`, filtered `perturbed_gene_id==ENSG00000166886`):

| metric | claim | my value | match |
|---|---|---|---|
| guides signif_knockdown | 2/2 | **2 / 2 True** | ✓ |
| best guide adj_p | ≈ 1e-16 | **1e-16** (both guides) | ✓ (see caveat 1) |
| mean guide expr | ≈ 0.056 | **0.05603** (0.0332 & 0.0789) | ✓ |
| NTC mean expr | ≈ 0.567 | **0.56719** | ✓ |

## A2 — EFFECT  → **PASS**
NAB2 @ Stim8hr (`DE_stats`):

| metric | claim | my value | match |
|---|---|---|---|
| ontarget_significant | True | **True** | ✓ |
| ontarget_effect_size | ≈ −16.9 | **−16.8816** | ✓ (sign negative = KD lowers target ✓) |
| n_downstream | 301 | **301** | ✓ |
| offtarget_flag | False | **False** | ✓ |

(Cross-condition sanity: Rest eff −3.54 / n_down 1 / non-sig; Stim48hr eff −8.68 / n_down 6 / sig.
Stim8hr is genuinely the strongest condition — the "condition of record" choice is justified.)

## A3 — PROGRAM (T2)  → **PASS**
NAB2 in `Th2_Th1_polarization_signature`:

| contrast | claim | my value | match |
|---|---|---|---|
| Ota 2021 log_fc | ≈ +0.63 | **+0.63319** | ✓ |
| Ota 2021 zscore | ≈ +7.71 | **+7.7077** | ✓ |
| Ota 2021 adj_p | ≈ 1.96e-13 | **1.9548e-13** (significant) | ✓ |
| Hollbacker 2021 adj_p | ≈ 0.20 (NOT sig) | **0.20462** (z=+2.39, NOT sig) | ✓ |

Significant in 1/2 reference contrasts → program gate passes under their "≥1 contrast" rule.

## A4 — DISEASE (T3, atopic eczema specifically)  → **PASS**
Clusters in `downstream_Stim8hr`, `disease=='atopic eczema'`, whose `intersecting_genes`
(ast.literal_eval) contain NAB2:

| cluster | OR | FDR (p_adj_fdr) | claim match |
|---|---|---|---|
| **100** | **3.8985** | **0.002832** | ✓ (claim OR≈3.90 / FDR≈0.0028) |
| **90** | **3.4304** | **0.022385** | ✓ (claim OR≈3.43 / FDR≈0.0224) |
| 74 | 2.1172 | 0.520791 | not significant |
| 98 | 1.0037 | 0.975382 | not significant |

Two clusters clear **FDR<0.05 for atopic eczema specifically** (not "any disease"); I filtered on
`disease=='atopic eczema'` before testing, and `negative_control_disease==False` (a real disease,
not a control). The disease call is correctly specific. **A4 holds.**

**Full-chain classification:** gate ✓ + effect sig (n_downstream=301>0) + program sig + disease-C ✓,
offtarget_flag False → this is a **clean full-chain "supported"** triple (the money-shot class), which
matches the referee's own `answer=="supported"` branch.

---

## Independent spot-checks (2 other clean-supported genes) — both **HOLD**
- **BHLHE40 × ankylosing spondylitis:** KD 2/2, effect −17.86 sig / n_down 1996 / offtarget False,
  program Ota log_fc −0.769 z −8.04 adj_p 1.5e-14 sig, disease cluster **77 OR 3.63 FDR 0.0066**. ✓
- **UFM1 × multiple sclerosis:** KD 2/2, effect −32.61 sig / n_down 2278 / offtarget False,
  program Ota log_fc +0.208 z +6.73 adj_p 2e-10 sig, disease cluster **100 OR 2.89 FDR 0.0137**. ✓

Both are genuine clean full-chain receipts. The pipeline is not cherry-picking NAB2.

---

## Caveats / method flags (none refute A1–A4)

1. **adj_p = 1e-16 is a numerical FLOOR, not a measured value.** 37,377 of 73,765 guide rows share
   exactly 1e-16. So A1's "best adj_p ≈ 1e-16" should read "adj_p ≤ 1e-16 (clamped)". Harmless — the
   gate is `signif_knockdown==True` (both guides), which does not depend on the exact floored p.

2. **DISCREPANCY with Claim C1 — wrong cluster IDs.** C1 states "NAB2's atopic-eczema clusters are
   **74 and 90**." That is incorrect: NAB2's *significant* atopic-eczema clusters are **100 and 90**
   (cluster 74 has FDR=0.52 — NOT significant; NAB2 is merely a member). The A4 numbers themselves
   are right (they describe clusters 100 & 90); only the C1 *label* "74" is the error, and it should
   be "100". This propagates into C1's downstream 12q13 argument (it should check clusters 100 & 90's
   members, not 74 & 90). **STAT6 is in neither 100 nor 90** (STAT6's atopic-eczema clusters are
   30/61/85), so C1's core claim "STAT6 is in neither of NAB2's clusters" still holds after the fix —
   but the cluster IDs in C1 must be corrected 74→100.

3. **A3 sign convention is deliberate but counter-intuitive.** Referee (`pyzobot_referee.py:236`) sets
   `direction = "Th2-associated" if log_fc<0 else "Th1-associated"`. NAB2's Th2_vs_Th1 log_fc is
   **positive (+0.63)** — by the raw contrast name that means NAB2 is *expressed higher in Th2*. The
   referee labels this "Th1-associated" because it reports the *knockdown-program* direction (KD of a
   Th2-biased gene pushes toward Th1). This is internally consistent with D2/D3's KD framing, but a
   reader who takes "Th1-associated" as the gene's own polarization would be misled — the gene itself
   is Th2-biased. Recommend the receipt state "KD shifts program toward Th1" explicitly. The direction
   does not affect A4 (cluster enrichment is direction-agnostic).

4. **Minor, Claim C2:** "NAB2 ~8× stronger than STAT6" is a *log_fc* ratio (0.633/0.080 = 7.9×), not
   the z ratio the sentence implies (z 7.71/2.66 = 2.9×). Both z values reproduce (NAB2 +7.71,
   STAT6 +2.66); just label the "8×" as coming from log_fc.

**Bottom line:** A1 PASS, A2 PASS, A3 PASS, A4 PASS. The NAB2 × atopic-eczema @ Stim8hr receipt is
fully reproducible from raw data and is a clean full-chain supported triple. Fix the C1 cluster IDs
(74→100) and clarify the A3 KD-direction wording; neither weakens the headline receipt.
