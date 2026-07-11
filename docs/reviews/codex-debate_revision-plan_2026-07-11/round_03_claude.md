# Round 3 — Claude's final revision-plan (accepts all 6 round-2 findings)

All six round-2 findings accepted and folded into the roadmap
(`docs/reviews/codex-debate_revision-plan_2026-07-11.md`, "Round-2 refinements"). The plan is now specified
to be outcome-independent and pre-registered. No pushbacks.

**F-009 top-line ACCEPTED.** Top line = **"receipt-backed prioritization with explicit *abstention* (untested)
and *falsification* (refuted) diagnostics."** "Calibrated" is used ONLY for vocabulary discipline, never as a
predictive-performance claim. Title unchanged from R2 (prioritization, not adjudication/closing-the-loop).

**F-010 C6 null ACCEPTED — single pre-specified estimand.** Exchangeability unit = **T3 disease-enrichment
rows**. The one primary randomization test: permute the `disease` label across T3 rows *within the fixed
condition gene-set (`downstream_Stim8hr`), preserving cluster/gene-set membership and each row's FDR/OR
marginals*, then recompute how many of the fixed eligible pairs pass the exact-disease hop. Null question:
"is exact gene→disease matching informative beyond a gene's generic cluster membership?" Report observed vs
null distribution of exact-disease passes (this is the disease hop's *own* selectivity, isolated from the
deterministic AB/BC/Open-Targets eligibility, which is NOT permuted). Drop the gene-label and eligible-pair
permutations (circular per F-010).

**F-011 positive control ACCEPTED — referee-only, gate-blinded.** Take canonical Th1/Th2 regulators
(GATA3, TBX21, STAT6, IL4, IL12A, IL4R, …) and run the **referee substrate hops (QC/effect/program) directly,
bypassing the novelty gate entirely** (they are excluded by `ac_known ≤ τ` by design). Metric: fraction whose
expected program/effect receipts recover. This tests the *referee*, kept explicitly separate from the
novelty-gated *funnel*.

**F-012 C2 hard-negatives ACCEPTED — frozen, outcome-independent frame.** Sampling frame = a **frozen
literature-only nomination rule** (e.g. top-K by AB co-mention), stratified by condition / AB strength /
disease / assay coverage — defined WITHOUT the referee verdict. Then apply the referee and report the
pre-specified untested/refuted/supported decomposition vs the naive literature-only baseline.

**F-013 C3a ACCEPTED — frozen discovery cohort.** Pre-register **Stim8hr as the discovery cohort**; freeze its
eligible (gene,disease) pairs + scoring inputs; evaluate ONLY those pairs' QC/effect/program/exact-C receipts
at Rest and Stim48hr. Report coverage first, then a transition matrix (supported→{supported,weak,refuted,
untested}). Not independent per-condition funnels.

**F-014 MVP ACCEPTED — re-ordered.** MVP = (1) reframe + C1 construction-vs-referee architecture; (2) C2
frozen-literature-nomination decomposition; (3) C10 small gate grid (ab_gate_pct × min_bc × τ, Stim8hr);
(4) frozen-cohort C3a; (5) C4 foreground limitation + 12q13 lit subsection; (6) C9 enumeration if literature
access works; (7) the four essential figures. C6 stays as the single well-specified null (not headline).

**For round 3 convergence, please confirm:** (a) the C6 exchangeability unit (T3 rows, disease-label-only
permutation preserving cluster/marginals) is the correct principled null and nothing else needs permuting;
(b) the referee-only positive control (F-011) and frozen-nomination C2 (F-012) are now genuinely
outcome-independent; (c) any residual place where the plan still lets a diagnostic read as validation; (d)
whether this MVP is sufficient for a credible Major-Revision resubmission, or one more analysis is essential.
