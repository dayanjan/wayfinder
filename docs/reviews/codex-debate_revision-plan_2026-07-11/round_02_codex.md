CONV: still iterating | SANDING: None
DROPPED(5): F-003, F-005, F-006, F-007, F-008
NEW(6): F-009, F-010, F-011, F-012, F-013, F-014

POSITION: Claude has materially improved the plan: it no longer misrepresents internal diagnostics as validation, and C4 is honestly foregrounded as unresolved. However, the revision still does not move the paper to “machinery decides correctly”; more importantly, “calibrated” remains an unsupported performance claim, and the proposed C6 nulls, C3 positive controls, and C2 hard-negative design are not yet statistically well specified.

F-009 [P0] correctness - The top-line claim still overclaims calibration
  EVID: The revised roadmap declares “calibrated, receipt-backed prioritization” at docs/reviews/codex-debate_revision-plan_2026-07-11.md:8-11, while explicitly conceding that the analyses are behavioral diagnostics rather than validation. No repository artifact estimates predictive calibration, class-conditional error, precision, or probability 
  DO: Use “receipt-backed prioritization with explicit abstention and falsification diagnostics” as the defensible top line. Reserve “calibrated language” for vocabulary discipline, or define calibration narrowly and non-statistically. 

F-010 [P0] correctness - Two of the three proposed C6 permutations lack a valid null estimand
  EVID: FEASIBLE computationally, but statistically mis-specified as written at docs/reviews/codex-debate_revision-plan_2026-07-11.md:20 and :55. Eligibility is deterministically formed from AB, BC, and Open Targets at src/arbiter/lbd/propose.py:68-71, while clean survival is then determined by the exact-C referee at :75-109. Permuting already-el
  DO: Pre-specify one primary randomization test. For “is exact disease matching informative beyond cluster membership?”, permute disease labels among T3 disease-enrichment rows while preserving condition, cluster/gene-set structure, ro

F-011 [P1] correctness - The proposed canonical-regulator recovery panel is mismatched to a novelty-gated LBD funnel
  EVID: NEEDS-FRESH-CS-RUN/LIT for curation, and the proposed recovery metric is conceptually confounded. Canonical regulators such as STAT6, GATA3, TBX21, and IL4 are likely penalized or excluded by the novelty machinery: eligibility requires Open Targets known association <= tau at src/arbiter/lbd/propose.py:69-71, and ranking penalizes both li
  DO: Split the benchmark by pipeline component. Test canonical Th1/Th2 regulators only against the Perturb-seq referee substrate, blinded to literature/novelty gates, asking whether expected program/effect receipts are recovered. Separ

F-012 [P1] correctness - C2 hard negatives remain selected by the same rules being evaluated
  EVID: FEASIBLE offline but insufficiently specified. The proposed hard negatives are “literature-plausible / eligible pairs that fail exact-C or effect” at docs/reviews/codex-debate_revision-plan_2026-07-11.md:24. Exact-C failure is itself the outcome computed from T3 in src/arbiter/lbd/referee_triple.py:48-88, and effect failure is an outcome 
  DO: Define panels without using the evaluated verdict: sample from a frozen literature-only nomination rule, stratified by condition, AB strength, disease, and assay coverage. Then apply the referee and report the pre-specified decomp

F-013 [P1] correctness - Cross-condition robustness needs a common cohort and is not a held-out test
  EVID: FEASIBLE from existing artifacts: docs/cs-full-pipeline_2026-07-09/live-fullsweep-loose/sweep_Rest.json, sweep_Stim8hr.json, and sweep_Stim48hr.json exist. But each sweep rebuilds a condition-specific A universe via src/arbiter/lbd/propose.py:45-51 and condition-specific referee evidence at :81-86. Comparing each condition’s independently
  DO: Pre-register Stim8hr as the discovery cohort, freeze its eligible gene-disease pairs and scoring inputs, and evaluate only their QC/effect/program/exact-C receipts at Rest and Stim48hr. Report coverage first, then transition matri

F-014 [P2] correctness - The MVP ordering omits the most interpretable robustness check and over-prioritizes C6
  EVID: The roadmap’s MVP includes C6 and C2 hard negatives but excludes C3 temporal robustness and C10 threshold sensitivity at docs/reviews/codex-debate_revision-plan_2026-07-11.md:53-60. Yet threshold parameters are directly exposed by src/arbiter/lbd/propose.py:43-44 and existing sensitivity code already establishes the reporting framework at
  DO: Minimum viable scope: reframe/C1 architecture; C2 frozen literature-nomination decomposition; C10 small gate grid; frozen-cohort C3a; C4 foreground limitation; C9 enumeration if literature access works; four essential figures. Ide

NEXT: Replace “calibrated” with a strictly supportable claim, then specify the exact C6 exchangeability unit and a frozen, outcome-independent sampling frame for C2/C3; provide an MVP table distinguishing analyses that demonstrate rule behavior from those that can e
