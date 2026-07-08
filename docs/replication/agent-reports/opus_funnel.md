# Independent replication — CLAIM SET B (the funnel)

**Reviewer posture:** independent lab, re-derived the *referee side* from the raw CSVs with a
from-scratch classifier that imports **no repo referee code** (`indep_funnel.py` = pure raw-CSV
re-implementation; `indep_eligible.py` = same classifier over the eligible set, using the repo's
`sources.py` **only** for the cached Europe PMC / OpenTargets gate values, which B2 permits as given).
Condition of record: **Stim8hr**, significance **FDR/adj-p < 0.05** throughout.

## Verdict: **PASS — the funnel replicates exactly.** Every B1/B3/B4 count reproduced to the unit.

| Claim | Claimed | My independent count | Result |
|---|---|---|---|
| B1 A universe (KD-gate ∩ effect ∩ program-sig T2<0.05), Stim8hr | ~3,935 | **3,935** (unique genes; 11,740 gene×condition rows all-conditions) | **PASS** (exact) |
| B2 eligible (gene×disease) pairs after ab/bc/OT gate | 22,039 | **22,039** (ab_gate 50th-pct = **26**, exact) | PASS (cached, but gate re-applied and reproduced) |
| B3 disease-C-supported survivors | 43 | **43** | **PASS** |
| — CLEAN full-chain (gate+effect+program+disease-C, n_down>0) | 30 | **30** | **PASS** |
| — supported_weak (n_downstream = 0) | 10 | **10** | **PASS** |
| — supported_flagged (off-target) | 3 | **3** | **PASS** |
| — refuted_effect | 1 | **1** | **PASS** |
| — refuted_for_c | 21,995 | **21,995** | **PASS** |
| B4 pure-disjoint (ac_lit=0) among clean | 1 (NUDT1×T1D, eff=4) | **1 — NUDT1 × type 1 diabetes, effect n_down=4** | **PASS** |

The 30 clean-supported pairs I reproduce include **NAB2 × asthma** and **NAB2 × atopic eczema**
(the headline), internally consistent with CLAIM SETS A/C.

## Adversarial statistics/logic checks

**(a) Is the A universe truly answer-free? — YES.** A is built from T4 (KD gate), T1 (effect),
and T2 (program-significance, adj-p<0.05) **only**; the T3 disease table is never opened during the
A build. The program-significance filter is a gene→**program** signal (Th1/Th2), not gene→disease —
no disease/T3 information leaks in. Structurally clean.
- **Caveat worth flagging (redundancy, not a leak):** the A-universe program filter and the
  referee's HOP-2 PROGRAM test are the *same* T2 adj-p<0.05 condition. So every A gene passes HOP-2
  by construction → `refuted_program` is **0** by design (confirmed: it never appears in the class
  counts). The PROGRAM hop is therefore *pre-satisfied* by A membership and cannot independently
  refute any funnel pair. Honest, but the "4-hop chain" is effectively a 3-constraint chain
  (gate + effect + disease-C) once inside the A universe; the program hop is a membership tautology.

**(b) Is FDR<0.05 applied correctly and per-specific-disease? — YES.** HOP-3 filters the exploded
T3 to `gene == sym AND gene_set == downstream_Stim8hr AND disease == C`, then keeps rows with
`p_adj_fdr < 0.05`. My re-implementation builds `gene → {diseases with ≥1 FDR<0.05 cluster row}`
per specific disease and reproduces the counts exactly. The referee reads T3's **pre-computed**
`p_adj_fdr` column (the enrichment analysis's own FDR); it does not re-invent FDR.

**(c) Is "clean full-chain" defined honestly (effect=0 excluded)? — YES.** `n_downstream == 0`
routes to `supported_weak`, never to clean `supported`. Confirmed: all 10 supported_weak have
n_down=0; all 30 clean supported have n_down>0. The effect-size floor is real.

**(d) Multiple-testing across the 22,039 tests? — NO NEW INFLATION, one inherited caveat.**
The 22,039 referee evaluations are **table lookups**, not fresh hypothesis tests — each pair's
disease support is a membership check against T3's already-FDR-corrected column. So running 22,039
of them introduces **no new multiplicity burden**. The only residual concern is inherited from T3:
the soundness of every "supported" rests entirely on how T3's FDR family was defined
(per disease×gene_set vs. globally). The referee cannot fix that; it faithfully inherits it. Not a
funnel defect — a substrate-provenance caveat.
- **Bigger honest point on "43":** the referee is *permissive*. Over the full A×12 = 47,220 pairs
  (cache-independent, `indep_funnel.py`) the referee alone supports **395** disease-C pairs
  (298 clean / 85 weak / 12 flagged) with 11 refuted_effect. The ab/bc/OpenTargets **gate** is what
  culls 395→43 (and 47,220→22,039). So the "43 confident survivors" is a **joint gate×referee**
  product, not a referee-only result; the novelty/co-mention gate does most of the narrowing. This
  is the correct design for a novelty generator, but the headline number should be read as
  "referee-supported **among literature-eligible** pairs," not "referee-supported, full stop."

**(e) Does pure-disjoint = 1 (NUDT1) hold? — YES.** NUDT1 × type 1 diabetes is the **sole**
clean-supported pair with zero Europe PMC A–C co-mentions (ac_lit=0), effect n_down=4 — reproduced
exactly. (The ac_lit=0 rests on the cached Europe PMC count, taken as given per B2; the referee/effect
side — NUDT1 clean-supported, n_down=4 — I derived independently from raw T1/T3/T4.)

## Bottom line
The funnel **replicates cleanly and honestly**: 3,935 → 22,039 → 43 (30 clean / 10 weak / 3 flagged)
→ 1 pure-disjoint, every number exact against a from-scratch raw-CSV re-derivation. The classifier
logic is sound — effect=0 is correctly demoted, FDR is per-specific-disease, and the A universe is
genuinely answer-free. Two fair-but-not-fatal caveats to state in any writeup: (1) the PROGRAM hop is
a tautology inside the A universe (refuted_program≡0 by construction), so it adds no independent
discriminating power to the funnel; (2) the "43 supported" is dominated by the literature/OpenTargets
gate, not the referee (which supports 395/47,220 on its own) — the confident-NO edge lives in the
`refuted_effect` / `supported_weak` demotions, and those are correctly and honestly computed.
