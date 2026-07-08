# Independent replication report — NAB2 finding pressure-tested (2026-07-08)

A 5-member independent-lab team (**3 Opus agents + 2 Codex agents**), each re-deriving from the raw
CSVs (no trust in our numbers, adversarial mandate) against a shared claim set
(`.claude/scratch/lbd-debate/REPLICATION_TARGETS.md`). Two members did full **clean-room
re-implementations** importing none of our pipeline code.

## Verdict: the finding REPLICATES. Unanimous PASS across all 5 members.
Every headline number reproduced to the unit from independent raw-CSV computation. The confounder
and mechanism challenges could not be made to stick. All corrections below are documentation /
framing hygiene — **none changes the core result.**

| Member | Model | Scope | Verdict |
|---|---|---|---|
| Opus-Receipt | Opus | NAB2 receipt A1–A4 + 2 spot-checks | PASS (exact); caught cluster-ID bug |
| Opus-Funnel | Opus | funnel B1/B3/B4, from-scratch classifier | PASS (every count exact); 2 framing caveats |
| Opus-Confounder | Opus | STAT6 + EGR, adversarial | PASS — could not turn NAB2 into "just STAT6/EGR2" |
| Codex-1 | Codex | pipeline code correctness | PASS — exact funnel match; code sound |
| Codex-2 | Codex | clean-room re-implementation | PASS — A=3,935, NAB2 supported, proportions reproduce |

## What reproduced exactly (independent raw-CSV re-derivation)
- **NAB2 receipt:** 2/2 KD guides (best adj-p ≤1e-16, a numeric floor); effect −16.88, n_downstream
  301, no off-target; program Ota z +7.71 (adj-p 1.95e-13), Hollbacker n.s.; atopic-eczema clusters
  OR 3.90/FDR 0.0028 and OR 3.43/FDR 0.0224. Two spot-checks (BHLHE40, UFM1) also hold → not cherry-picked.
- **Funnel:** A=3,935 → 22,039 eligible → 43 disease-C-supported → **30 clean / 10 weak / 3 flagged /
  1 refuted-effect / 21,995 refuted-for-C**; pure-disjoint = 1 (NUDT1). Codex-1 and Opus-Funnel each
  reproduced these to the unit; Codex-2 reproduced A=3,935 and the clean/weak/flagged proportions.
- **Code correctness:** A universe genuinely **answer-free** (T3/disease never opened during A build);
  `answer=="supported"` correctly requires the full chain with n_downstream>0; FDR<0.05 applied
  per-specific-disease; effect=0 correctly demoted to `supported_weak`.

## Errors caught → fixed (this is why we replicate)
1. **Cluster-ID misalignment (found independently by Opus-Receipt AND Opus-Confounder).** Our
   confounder script printed sorted cluster IDs against row-order FDRs, mislabeling NAB2's significant
   atopic-eczema clusters as **74/90**; the true significant clusters are **90/100** (cluster 74 FDR
   0.52, non-significant). The locus test had run on cluster 74 (wrong) instead of 100. **Fixed:**
   script now derives significant clusters (no hardcode); re-run confirms clusters 90 & 100 are
   genome-wide functional immune modules (BACH2, BCL6, IRF4, CD28, CD200, CD226; only NAB2 on 12q13;
   STAT6 in neither) — locus-artifact **rejected on the correct clusters**.
2. **"~8× stronger" is the effect-size (log_fc) ratio, ~3× on z.** Corrected to "~8× on effect size /
   ~3× on z."
3. **Argument reframing (Opus-Confounder's key contribution).** We were defending with our weakest
   evidence:
   - Distinctness-from-STAT6 now rests on **cluster co-membership (STAT6 absent) + magnitude +
     guide-specificity (2/2 on-target, no off-target → molecularly NAB2)**, NOT on the identical
     {asthma, atopic eczema} disease profile (which actually *aids* the confounder).
   - Anti-EGR-mediation now rests on **D3 (paralog NAB1 shifts the program the opposite way,
     significant in BOTH contrasts)**, NOT on D2 (same-direction, a weak cross-cohort comparison —
     NAB2 sig in Ota, EGR2 sig only in Hollbacker at borderline p=0.049).

## Honest framing caveats the team surfaced (state these in any writeup)
- **Program hop is a tautology inside the funnel.** A is filtered on program-significance (T2<0.05)
  and HOP-2 tests the same, so `refuted_program`≡0 by construction — the program hop adds no
  independent discriminating power *to the funnel*. (NAB2's individual program receipt, z=7.71, is
  still real; the tautology is that all A genes pass, not that NAB2's is fake.)
- **"43 supported" is a joint gate×referee product, not referee-only.** The referee alone supports
  395/47,220 pairs; the literature/OpenTargets novelty gate culls 395→43. Read it as "referee-
  supported **among literature-eligible** pairs." The referee's confident-NO edge lives in its
  `refuted_effect` / `supported_weak` demotions, which are correctly computed.
- **T3 FDR provenance is inherited.** Every "supported" rests on T3's pre-computed FDR family; the
  referee faithfully inherits it (a substrate-provenance caveat, not a pipeline defect).
- **Direction wording:** NAB2's positive Th2_vs_Th1 log_fc is labeled "Th1-associated" because the
  receipt reports the KD-program direction — say "KD shifts the program toward Th1" to avoid confusion.

## Bottom line
NAB2 → Th1/Th2 → atopic eczema is a **genuine, reproducible, receipt-backed finding** that survived
a 5-member adversarial independent replication including two clean-room re-implementations. It is
**novel** (0 direct papers), **NAB2-specific** (guide on-target), **not a 12q13/STAT6 locus artifact**
(corrected clusters), and **not a simple EGR2 proxy** (paralog opposition). The honest residual is
that NAB2 and STAT6 share the same disease profile → present NAB2 as a strong, novel **co-regulator
of the type-2/atopic axis STAT6 governs**, defended by mechanism and guide-specificity, not by
disease-profile distinctness. Per-member reports: `.claude/scratch/lbd-debate/replication_*`.
