# Round 2 — Claude's revised revision-plan (accepts all 8 round-1 findings)

**Top-line claim (answering the round-1 NEXT question), decided:** the manuscript defends
**"calibrated, receipt-backed *prioritization* with explicit falsification diagnostics"** — NOT empirical
correctness of supported calls. Every analysis below is framed as a *diagnostic* of the machinery's
behavior, never as validation. This single decision resolves the tension both reviews identified.

**F-001 (C3) ACCEPTED.** C3 is not external validation. Reframe to two clearly-labelled diagnostics + one
crude proxy: (1) **temporal robustness** across Rest/Stim8hr/Stim48hr (data exists:
`docs/cs-full-pipeline_2026-07-09/live-fullsweep-loose/sweep_{Rest,Stim8hr,Stim48hr}.json`); (2)
**prioritization-behavior comparators** — rank the eligible pairs by random / literature-rarity /
Open Targets and show how the referee-supported set differs (behavior, not accuracy); (3) a **literature-
curated positive-control panel** of canonical Th1/Th2 regulators (GATA3, TBX21, STAT6, IL4, IL12, etc. via
`tools/semantic_scholar.py`+`pubmed_fetch.py`) as a *crude* recovery proxy, labelled as such.

**F-002 (C6) ACCEPTED.** Drop "joint FDR". Rename → **"pipeline-level permutation diagnostic"**; report
expected clean survivors under several *constrained* nulls (disease-label permutation within T3;
gene-label permutation within condition; eligible-pair permutation) vs observed 30 — as a diagnostic of
selectivity, not a global false-discovery rate.

**F-003 (C4) ACCEPTED.** C4 (12q13/LD) is **not resolvable** with repo data. Promote to a **foreground
limitation subsection**, balanced against the STAT6 subsection. Run the **locus-wide neighbor check** (do
other 12q13 genes share the eczema clusters?) as a sanity check only; add a **12q13 GWAS literature
subsection** (atopic-dermatitis/asthma coloc work via the APIs) and state explicitly that colocalization is
unavailable here. Never claim the LD confounder is discharged.

**F-004 (C2) ACCEPTED.** Out-of-funnel discrimination uses **two panels**: (1) arbitrary genes → descriptive
calibration of untested/refuted labels; (2) **hard negatives** — literature-plausible / proposer-eligible
pairs that fail exact-C or effect gates — compared against naive literature-only nomination. Report as the
referee's *own* discrimination edge (the hops it genuinely owns), not "confident-no accuracy".

**F-005 (C10) ACCEPTED.** Extend `sensitivity_panel.py` with a **small deterministic grid over ab_gate_pct,
min_bc, tau** for Stim8hr (`propose.sweep()` already exposes these; cache exists), reporting clean-survivor
count, NAB2 survival/rank, and Jaccard overlap of supported sets. Keep it small (Stim8hr only).

**F-006 (C9) ACCEPTED.** Run a **targeted LIT audit** listing the six Europe PMC NAB2×Th1/Th2 co-mentions
(title/year/context; does each assert NAB2→Th1/Th2, NAB2→eczema, or mere co-occurrence?). `sources.py` uses
pageSize=1 so the cache holds counts only → this is a **fresh LIT run** via the tools. Report both numbers
with what each measures.

**F-007 + F-008 (hierarchy + strategy) ACCEPTED.** Revised **execution order**: (1) settle claims/limitations
+ the top-line reframe (prioritization-with-diagnostics); (2) run the analyses **C6 → C3 → C10** (+ the C2
hard-negative panel and the C9 LIT audit), all labelled diagnostics; (3) restructure (NAB2 → one case study;
CS → Methods/appendix + a short "replicable-in-principle, UI-dependent" note; separate language-hygiene from
epistemic verification); (4) build the **minimum figure set**: Fig 1 (architecture, *construction-vs-referee
separated*), Fig 2 (ledger+funnel with the C2/C6 diagnostics), Fig 3 (NAB2 chain + 12q13 caveat), Fig 4
(sensitivity/null panel); Fig 5 (self-audit) only if space. Retitle → *"Receipt-backed prioritization for
literature-based discovery using Perturb-seq evidence"*. **Do NOT claim wet-lab or LD validation.**

**For round 3, please stress:** (a) is the top-line "prioritization-with-diagnostics" claim now consistently
supportable across §1–§5 given the analyses proposed? (b) any remaining analysis that is statistically
mis-specified or that the repo cannot support? (c) is the constrained-null design for C6 correct (which
permutation is the right null for "is 30 surprising")? (d) minimum-viable vs ideal scope split, since the
operator has limited time before submission.
