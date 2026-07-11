# Wayfinder manuscript — consolidated review dossier + revision plan (2026-07-11)

Combines: (0) Claude's visual PDF inspection; (A) independent Review A (journal-referee, scored); (B)
independent Review B (referee-report style); into a deduplicated **concern register** and a resource-tagged
**revision plan**. This is the artifact for a 3-round repo-read codex-debate on *how best to address each
concern with what we have* — the Claude Science (CS) instrument, the four literature APIs
(CrossRef/PubMed/OpenAlex/Semantic Scholar), the existing analyses/data, and any new CS analysis worth running.

---

## 0. Visual inspection (Claude, from the compiled PDF)
- **Colored headings** (maroon title, navy subsections) — atypical for a scientific manuscript; **FIXED** → black.
- **§3.2 ranking equation bled into the right margin and showed literal `$\beta$$\cdot$`** (pandoc verbatim, no math, no wrap) — **FIXED** → amsmath display equation, within margins.
- **No figures anywhere.** Fig 1 (the loop schematic), Fig 4 (NAB2 4-hop chain + STAT6 callout), Fig 5 (self-audit) are referenced in the outline/prose but **absent from the PDF**. **OPEN — highest-visibility gap.**
- **Abstract is a single dense ~350-word block** — should be split.
- Overall the PDF "does not yet read like a proper manuscript" — driven by the above + structural issues below.

## A. Review A — key points (scored: Novelty 9.5, Importance 8.5, Rigor 6.5, Clarity 8.5, Evidence 6; Major Revision)
- A1. **Referee not truly independent / circular** — the A-universe is pre-filtered on the same KD/effect/program evidence the referee re-reads. Partially answered; answer not strong enough.
- A2. **Hop 2 (program) is a guaranteed tautology** (`refuted_program≡0`) — contributes zero discrimination; separate construction-filters from referee-decisions; consider removing from the figure.
- A3. **Disease hop is secondary association, not biological validation** — "adjudication" implies ground truth; prefer "receipt-backed evidence integration" / "evidence-backed prioritization".
- A4. **Negative control unconvincing** — observed 406 is *below* the null 468±11; demonstrates label-dependence, not better-than-random discrimination; move to supplementary.
- A5. **NAB2 over-weighted (~4 pp)** — the paper is about Wayfinder; restructure to general-evaluation → several examples → NAB2 as one case study.
- A6. **Trying to prove too many things** (LBD × agentic × browser-automation × CS × reproducibility × critic × cross-vendor × NAB2 × STAT6 × expression-meta × DepMap) — dilutes the central message.
- A7. **CS/browser-automation ~20–25% of text** — implementation detail; method should survive if CS disappears; move to Methods.
- A8. **Weights β/w/w₂ hand-chosen; no external benchmark** — compared to what? (random / Open Targets / gene-prioritization / other LBD). Why min() not geometric mean / Pareto? Could weights be learned?
- A9. **Title overclaims** ("Closing the loop" = solved LBD) — more precise title.
- A10. **Missed opportunity** — elevate the general vision (AI that generates → adjudicates → provenance → calibrates → rejects) earlier; it generalizes beyond LBD.

## B. Review B — key points (Major Revision; "honest demonstration the machinery behaves as designed", not yet "decides correctly")
- B1. **The "confident no" is thinner than framed (load-bearing).** Disease-hop refutation is substrate-inherited (shuffle 0.99% vs true 0.86%, indistinguishable); the referee's *own* no reduces to QC-untested + **one** refuted-effect pair. QC-gate control (2,430→100% untested) is near-tautological (those genes were defined by failing that QC). Title claim outruns evidence for *how often* the no is right. Honest version: shown the *machinery* for a calibrated no, not that it discriminates at scale.
- B2. **No external validation of any "supported" call; no performance metric.** Need a held-out / cross-substrate / external ground-truth check, even crude — else contribution ≈ "honestly-documented re-application of existing FDRs".
- B3. **12q13/LD confounder for NAB2 (the central threat to the flagship).** NAB2 ~1.9 kb from STAT6 in the 12q13 atopy locus; cis-*expression* falsified, but the eczema *label* is GWAS with no colocalization/LD control → the "novel" link could be the 12q13 signal on a neighbor. Gets one sentence vs STAT6's full subsection. Address LD/coloc or foreground the unresolved provenance.
- B4. **ac_lit=6 vs "zero papers" tension** — reconcile: what are the 6 co-mentions, why don't they count?
- B5. **Multiple testing across the joint procedure unaddressed** — no global-null expectation for the whole pipeline; is 30/22,039 surprising?
- B6. **Agentic-workbench material overreaches** — "self-audit" is *language hygiene*, not epistemic verification; "reproducible" sits awkwardly with "no stable public contract" (replicable-in-principle); trim/appendix so biology stays foreground; reads like a product demo.
- B7. **One caught bug (cluster-ID 74/90→90/100) raises prior on uncaught ones** — what verification did the *corrected* confounder script receive?
- B-minor: determinism claim undersells human choices (12-disease set, vocabularies, gate thresholds — only ranking weights swept); reconcile −16.9 vs −16.88; note substrate is a **preprint**; split abstract; confirm Figs 4/5 present + captioned.

---

## Consolidated concern register (deduplicated, prioritized)
| # | Concern | Raised by | Class |
|---|---|---|---|
| C1 | Referee independence / circularity (same evidence builds universe + adjudicates) | A1, B1 | evidentiary |
| C2 | "Confident no" mostly substrate-inherited; referee's own no = QC-untested + 1 refuted-effect | B1, A4 | evidentiary |
| C3 | No external validation / no baseline / no performance metric | A8, B2 | evidentiary |
| C4 | NAB2 12q13/LD provenance unresolved (the flagship's central threat) | B3 | evidentiary |
| C5 | Negative control (label-shuffle) demonstrates label-dependence, not discrimination | A4, B1 | evidentiary |
| C6 | Multiple-testing / joint global-null for the whole procedure | B5 | evidentiary |
| C7 | Hop-2 tautology — separate construction filters from referee decisions | A2 | framing/rigor |
| C8 | "Adjudication" overclaims; disease hop = integration/prioritization | A3, A9 | framing |
| C9 | ac_lit=6 vs "zero papers" reconciliation | B4 | rigor |
| C10 | Weights/thresholds justification (β/w/w₂; gate thresholds; min vs alternatives; learnable?) | A8, B-minor | rigor |
| C11 | Corrected-confounder-script verification (bug raises prior) | B7 | rigor |
| C12 | NAB2 over-weighted → Wayfinder-first, NAB2 as one case study | A5 | structure |
| C13 | CS/browser-automation overweight (~20-25%) → Methods/appendix | A7, B6 | structure |
| C14 | Scope sprawl (proving too many things) | A6 | structure |
| C15 | Elevate the general vision (evidence-grounded adjudication beyond LBD) | A10 | framing |
| C16 | Self-audit = language hygiene, not epistemic verification (keep separate) | B6 | framing |
| C17 | "Reproducible" overclaim vs API-less UI dependence | B6 | framing |
| C18 | FIGURES MISSING (Fig 1 loop, Fig 4 NAB2 chain, Fig 5 self-audit) | visual, B-minor | presentation |
| C19 | Title overclaim ("Closing the loop") | A9, B | framing |
| C20 | Abstract single dense block → split | visual, B | presentation |
| C21 | Numeric −16.9 vs −16.88; preprint status of substrate | B-minor | rigor |
| C22 | Colored headings; equation margin bleed | visual | presentation — **FIXED** |

---

## Claude's proposed revision plan (resource-tagged; the debate should harden this)
**Legend:** [CS] = new Claude Science analysis · [LIT] = literature/APIs · [REFRAME] = prose/structure · [FIG] = figure · [DEFER] = out of scope for this paper.

- **C1 circularity** — [REFRAME] Restructure §3 to *visually and textually separate* "construction filters" (KD/effect/program pre-gate) from "referee decisions" (disease-specificity + demotions). State plainly the referee's independent contribution is (a) the disease-C specificity test and (b) the QC/effect demotions on *arbitrary* genes, and lean on the out-of-funnel ledger as the independence evidence. Possibly rename the in-funnel hops "construction" vs the out-of-funnel application "adjudication".
- **C2 + C5 confident-no / control** — [CS] Strengthen the referee's *own* discrimination where it genuinely owns it: run the referee on a **large random/out-of-funnel gene panel** and measure QC-untested and effect-refuted rates vs a matched null (this is the referee's real edge, not the disease hop). [REFRAME] Demote the disease-hop label-shuffle to supplementary; retitle the claim to "machinery for a calibrated no" + the out-of-funnel discrimination rate. Consider dropping/softening the title's "worth trusting".
- **C3 baseline/external validation** — [CS]+[LIT] Add at least one baseline comparison: rank the same eligible pairs by (i) literature-rarity alone, (ii) Open Targets association, (iii) random, and show the referee's supported set differs/concentrates on independently-supported biology. [CS] A **cross-condition held-out** check (train/define on Stim8hr, test survivors' behavior at Rest/Stim48hr) is feasible with existing data. External ground-truth for "supported" calls via [LIT] (known Th1/Th2 regulators from OpenAlex/S2) — a crude precision proxy.
- **C4 12q13/LD** — [CS]+[LIT] The highest-value new analysis: address LD/colocalization for NAB2→eczema directly. Options with our data: (a) check whether *other* 12q13 neighbors show the same eczema-cluster membership (locus-wide vs NAB2-specific); (b) [LIT] pull the atopic-dermatitis GWAS/coloc literature for the 12q13 locus; (c) if we cannot resolve it, **foreground** it as the flagship's key open question (promote from one sentence to a subsection), balancing the STAT6 subsection.
- **C6 joint FDR** — [CS] Compute a global-null expectation for the *whole* pipeline (permute the substrate end-to-end, count "supported" survivors) → report expected survivors under null vs observed 30. Bounded CS-kernel analysis.
- **C7 hop-2 tautology** — [REFRAME]+[FIG] In Fig 1/3 and §3.3, mark hop-2 as a construction-inherited check, not an independent funnel filter.
- **C8 + C19 adjudication/title** — [REFRAME] Soften "adjudication" where the disease hop is involved → "evidence integration / prioritization"; retitle (candidate: "Receipt-backed prioritization for literature-based discovery using Perturb-seq evidence"). Keep "adjudication" only for the hops the referee owns.
- **C9 ac_lit vs zero-papers** — [CS]/[LIT] Reconcile: ac_lit=6 is raw Europe PMC co-mention (any context); the 4-agent audit found 0 papers making the *specific mechanistic* claim. State both numbers + what each measures.
- **C10 weights/thresholds** — [CS] Extend the sensitivity sweep to the **gate thresholds** (ab_gate percentile, bc, ac_known τ) and report survivor/rank stability; [REFRAME] justify min() (balanced-bridge rationale) + acknowledge learnable weights as future work.
- **C11 corrected-script verification** — [REFRAME] State what verification the corrected confounder script received (the 5-agent replication re-derived the corrected clusters); cite it.
- **C12 + C14 NAB2/scope** — [REFRAME] Restructure Results: lead with the ledger + discrimination evidence across several examples; NAB2 becomes one (deep) case study; move the NAB2 direction/DepMap thread fully to Discussion/supplementary.
- **C13 + C16 + C17 CS de-weight** — [REFRAME] Compress §3.4/§4.5 to a Methods subsection + appendix; separate *language-hygiene self-audit* from *epistemic verification* explicitly; downgrade "reproducible" → "replicable-in-principle (UI-dependent)".
- **C15 vision** — [REFRAME] Add a short framing paragraph (Intro + Discussion) positioning Wayfinder as a general architecture for evidence-grounded hypothesis adjudication.
- **C18 figures** — [FIG][CS] Build Fig 4 (NAB2 4-hop chain, CS kernel) + the §4.1b sensitivity panel; Figs 1/3/5 schematics (HTML/SVG asset pipeline). Non-negotiable.
- **C20 abstract** — [REFRAME] Split into 2–3 shorter paragraphs (or a lightly-structured abstract).
- **C21 numerics/preprint** — [REFRAME] Reconcile −16.9/−16.88 (use −16.9 throughout, note −16.88 exact); state the substrate is a 2025 preprint.
- **Wet-lab external validation of a supported call** — [DEFER] explicitly future work.

**Open strategic questions for the debate:**
1. Is the honest reframe (referee owns QC/effect + disease-specificity; disease-hop stringency is substrate-inherited) *enough*, or do we need the C3 baseline + C6 joint-null to make the discrimination claim stand?
2. Can C4 (12q13/LD) be resolved with data we have (locus-wide neighbor check) or does it become a foregrounded limitation?
3. How far to de-weight CS — Methods-only, or keep the "reproducible agentic science over an API-less platform" as a *secondary* contribution?
4. Minimum figure set for credibility (which of Fig 1/3/4/5 + the 4.1b panel are essential vs nice-to-have)?
5. Which CS analyses are highest-value-per-effort (baseline ranking, cross-condition held-out, joint-null, threshold sensitivity, 12q13 locus-wide) — and which are feasible with existing cached data vs need fresh live runs?
