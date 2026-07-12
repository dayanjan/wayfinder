# Contribution / Novelty Claim Register — Extractor 2 (uncontaminated read)

Manuscript: "Receipt-backed prioritization for literature-based discovery using Perturb-seq evidence" (Wayfinder).
Scope: every claim presented as NOVEL or as a CONTRIBUTION — method and biology, explicit and implicit.
Extraction/characterization only; no literature search run, no final verdict rendered.

---

### C2-01
- **Type**: METHOD
- **Claim**: The central contribution — "receipt-backed prioritization of machine-generated hypotheses, with explicit abstention and falsification diagnostics." Pairing LBD generation with a deterministic referee that adjudicates each hypothesis against a held experimental substrate and returns a prioritization verdict with a receipt at every hop.
- **Location**: abstract; §1 (¶3–4); §5.4
- **Paper's own hedge**: "the contribution is the method and what it found — not a demonstration of predictive correctness"; explicitly narrower than "closing the LBD loop" (only triage, not experimental follow-up); "not a software product."
- **Novelty test**: Look for any prior LBD or hypothesis-triage system that scores candidate links against an independent experimental dataset (not literature statistics) and emits per-link verdicts. Searches: "literature-based discovery experimental validation triage", "hypothesis prioritization held-out experimental data LBD", "ABC discovery grounding perturbation data", "evidence-grounded ranking LBD candidates". Also check Swanson-lineage reviews (Henry & McInnes 2017; Sebastian 2017) for any "data-grounded" extension.
- **Novelty-risk prior**: MEDIUM — the specific combination (LBD front-end + deterministic held-substrate back-end + abstain/refute verdicts) is plausibly unclaimed, but "ground hypotheses in real data" is a widely-pursued instinct; risk is that a niche system already did a version of this.

### C2-02
- **Type**: METHOD
- **Claim**: The explicit "gap" claim in §2.4 — the authors are "not aware of a system that does the specific combination Wayfinder targets: a **deterministic, non-LLM referee** that scores each hypothesis against a **held, pre-existing** experimental substrate and returns a per-hop **experimental** receipt (OR, p-value, effect size) for every causal edge, with a QC-gated **abstention** and a **falsification** as first-class verdicts."
- **Location**: §2.4 (novelty crux)
- **Paper's own hedge**: "We are not aware, however, of a system..." (knowledge-scoped, not proven absence); careful not to strawman named neighbors; distinguishes Robin/chemistry-ML systems as generating NEW experiments vs adjudicating a HELD one.
- **Novelty test**: This is the load-bearing differentiator. Interrogate each named neighbor to check the distinction holds: Google AI co-scientist (Gottweis 2025), FutureHouse Robin/PaperQA2 (robin2025, paperqa2024), SciAgents (2025), PerturbQA (perturbqa2025), Coscientist/Boiko 2023, AI-Scientist 2024. Also search beyond the cited set: "agent adjudicates hypothesis against existing screen dataset", "non-LLM referee CRISPR screen hypothesis", "held-out Perturb-seq hypothesis scoring agent", "deterministic verdict gene-disease against perturbation atlas". Key falsifier: any system that queries a *pre-existing* dataset per-hypothesis and can *abstain on data quality*.
- **Novelty-risk prior**: MEDIUM — the conjunction is narrow and the "held pre-existing substrate + non-LLM + abstain" trio is a genuine wedge; but PerturbQA and perturbation-benchmarking work sits close, and a reviewer may argue the wedge is a re-description of "retrieval-grounded eval," not a new system class.

### C2-03
- **Type**: METHOD
- **Claim**: The abstention diagnostic — distinguishing a **refuted** hypothesis from an **untested** one; a failed knockdown is reported as *untested* (an artifact caught), never as a false negative. QC-gated abstention as a first-class verdict.
- **Location**: abstract; §1 (¶4); §3.3 (Hop 0); §4.2; §5.1
- **Paper's own hedge**: framed as one of two defining diagnostics; scoped to knockdown-QC (T4) mechanism.
- **Novelty test**: Search for prior hypothesis-evaluation or perturbation-analysis systems that separate "no measurable effect" from "perturbation failed QC / gene not knocked down." Searches: "distinguish untested from negative CRISPR knockdown QC", "abstention hypothesis evaluation LLM biomedical", "failed knockdown false negative guardrail Perturb-seq", "selective prediction abstain gene screen". Note: knockdown-QC gating itself is standard in Perturb-seq analysis; the novel claim is elevating it to a *verdict class* in a triage referee — check whether that framing is genuinely new vs a repackaging of routine QC.
- **Novelty-risk prior**: MEDIUM — the underlying QC step is standard practice; novelty rests entirely on the framing as a first-class abstention verdict in an LBD referee. Overstatement risk if a searcher reads it as "new QC method."

### C2-04
- **Type**: METHOD
- **Claim**: The falsification diagnostic / "confident, receipt-backed **no**" — the referee is willing to refute a plausible claim with a real experimental receipt; falsification (not confirmation) is the moat/point.
- **Location**: abstract; §1; §4.2 (SLC1A5); §5.1; §5.4
- **Paper's own hedge**: heavily hedged internally — §4.1b concedes the disease-hop's near-total refutation is *substrate-inherited* (from the enrichment study's FDR family), not the referee's own discrimination; the referee's *own* confident-no is relocated to the knockdown-QC gate (§4.2b, ~1-in-6 untested).
- **Novelty test**: Search for LLM/agent hypothesis systems framed around *rejecting* plausible claims rather than generating plausible ones. Searches: "LLM hypothesis refutation confident no biomedical", "falsification agent scientific claim rejection", "negative result hypothesis generator LBD". Contrast against AI co-scientist / generators optimizing for plausibility (the paper's own framing). The novelty here is a stance/design goal more than an algorithm — a searcher should check whether "systems that say no" is already a recognized design pattern.
- **Novelty-risk prior**: MEDIUM — "willingness to say no" is rhetorically strong but the paper itself shows the disease-hop no is inherited, not earned; overstatement risk is real, though the QC-gate no is defensible.

### C2-05
- **Type**: METHOD
- **Claim**: Two distinct receipt classes kept explicit throughout — experimental receipts (knockdown/effect/program hops) vs an association/genetic-nomination receipt (disease hop, GWAS-based, no coloc/LD control). A calibration discipline that keeps claims within what receipts support.
- **Location**: abstract; §2.2; §3.3; §4.3
- **Paper's own hedge**: this IS the hedge — explicitly downgrades the disease hop to "nomination, not experimental causality."
- **Novelty test**: Low-priority as an independent novelty (it's an epistemic-hygiene convention). Search "evidence-type stratification hypothesis receipt experimental vs association" only to confirm it isn't a named prior framework. Mostly a contribution-by-discipline claim, not a system novelty.
- **Novelty-risk prior**: LOW — presented as careful practice, not as a novel invention; unlikely to be "defeated," more a matter of whether it counts as a contribution at all.

### C2-06 (IMPLICIT)
- **Type**: METHOD
- **Claim**: The agentic self-audit mechanism — the whole loop ran inside an agentic workbench where an *independent critic model* (distinct model, distinct checkpoints, same family) enforced **calibrated language** on the platform's own output, flagging and removing overstated words ("validated," "definitive") from the machine's own text. "The paper's own thesis was applied to the machine that generated it."
- **Location**: abstract; §1; §2.3; §3.4; §4.5; §5.1
- **Paper's own hedge**: scoped precisely — "language hygiene plus receipt-consistency," NOT independent epistemic verification of the biology; "role/model/checkpoint independence within a single family," NOT cross-vendor; applies to manuscript-facing output only (a legacy "validated" string persists in a raw log).
- **Novelty test**: Search for prior actor–critic / self-review LLM systems that enforce *calibrated/hedged language* on scientific output. Searches: "LLM critic calibrated language scientific claims", "actor critic model overstatement removal manuscript", "self-audit language hygiene agent science", "reviewer model flags overclaiming hypothesis". Related: constitutional-AI / self-critique literature, PaperQA2's citation grounding. Check whether "critic enforces calibrated language" is distinct from generic actor-critic verification.
- **Novelty-risk prior**: MEDIUM–HIGH — actor-critic and self-critique LLM setups are well-established; the specific twist (critic polices *calibrated scientific language*, not correctness) is narrower but may be viewed as an application of known self-review patterns rather than a novel mechanism.

### C2-07 (IMPLICIT)
- **Type**: METHOD
- **Claim**: Reproducibility of an API-less agentic workbench via headless browser automation — driving Claude Science's web UI headlessly (auto-approving in-loop sandbox cards for zero-click operation), turning a one-off hand-paced web session into a "re-runnable, audited pipeline"; "an under-appreciated route to replicable-in-principle (UI-dependent) agentic science." Analyses reproduced byte-for-byte (sensitivity panel) / digit-for-digit (funnel) when driven programmatically.
- **Location**: abstract; §3.4; §4.5; §5.1
- **Paper's own hedge**: "replicable in principle, subject to the platform's user interface"; candidly "browser automation against a UI with no stable public contract" (§5.3); "a small step, but a real one."
- **Novelty test**: Search for prior work on headless/programmatic driving of agentic scientific workbenches or on reproducibility of LLM-agent analyses. Searches: "headless automation agentic scientific workbench reproducibility", "browser automation LLM agent pipeline reproducible", "Claude Science automation", "reproducible agentic science UI driver Playwright". This is likely genuinely under-explored in the literature (very recent tooling); risk is the *contribution* being seen as engineering plumbing rather than a research contribution.
- **Novelty-risk prior**: LOW–MEDIUM — as a literature-novel claim, low risk (few will have published on driving Claude Science headlessly); but its weight as a *scientific* contribution is contestable, and "byte-for-byte reproduction against a local cache under a no-live-call guard" is a recomputation, not an independent replication (the paper admits this).

### C2-08 (IMPLICIT)
- **Type**: METHOD
- **Claim**: Independent cross-model / cross-vendor replication as a validity check — a five-member "replication lab" (3 Opus-class + 2 Codex/different-vendor agents), two doing clean-room re-implementations importing none of the pipeline code, under an adversarial mandate; unanimous pass; caught and corrected real errors (cluster-ID misalignment 74/90 → 90/100; effect-size overstatement 8× → 3×).
- **Location**: abstract; §3.4(iii); §4.6
- **Paper's own hedge**: "evidence of computational robustness, not of biological validity"; "not every member re-checked every number."
- **Novelty test**: Search for prior use of multi-agent adversarial cross-vendor replication as a verification protocol for computational findings. Searches: "cross-model replication LLM agents adversarial verification", "clean-room reimplementation agent scientific result", "multi-vendor agent replication lab findings". Likely under-published as a named method; the claim is more "we did a rigorous check" than "we invented a method," so novelty-audit weight is modest.
- **Novelty-risk prior**: LOW — few competing publications on this exact protocol; the risk is it reads as good practice rather than a novel contribution.

### C2-09 (IMPLICIT)
- **Type**: METHOD
- **Claim**: Disease-answer-free universe construction — the candidate gene set A is built from perturbation data alone (knockdown-QC + effect + program), never reading the disease table T3, so the gene list cannot be contaminated by the disease answer it is later tested against. Plus the novelty gate designed to *not* reward obscurity (gates on ab ≥ percentile, not on zero co-mention).
- **Location**: §3.2; §4.1
- **Paper's own hedge**: "disease-answer-free, not evidence-free" — explicitly notes hops 0–2 are pre-gated within the funnel (program hop is a tautology), so within-funnel discrimination is limited; this candor is repeated in §4.1/§5.
- **Novelty test**: Search for "answer-leakage prevention" / data-hygiene analogues in LBD or ML-for-biology. Searches: "disease-answer-free candidate construction LBD", "avoid rewarding obscurity literature novelty gate", "leakage-free gene universe hypothesis test". This is a methodological-hygiene claim; check the Stoeger 2018 understudied-genes framing for prior "obscurity ≠ importance" arguments (the paper cites it).
- **Novelty-risk prior**: LOW–MEDIUM — sound design but plausibly a re-expression of standard leakage-avoidance; the "don't reward obscurity" idea is already in the cited Stoeger literature.

### C2-10 (IMPLICIT)
- **Type**: METHOD
- **Claim**: The balanced ranking objective — score = min(z(log1p ab), z(log1p bc)) + β·z(log1p effect) − w·log1p(ac_lit) − w2·ac_known — with the min() term forcing a *balanced* bridge (one strong axis cannot rescue a weak other) and effect as a "loud in the data" reward. Explicitly "the only human judgment in an otherwise mechanical pipeline."
- **Location**: §3.2; robustness in §4.1b (weight grid), §4.1c (threshold grid)
- **Paper's own hedge**: weights set *priority* not *verdict* (verdict is weight-independent); robustness shown (NAB2 rank 1–8, median 4, top-5 in 89%); "objective's structure/weights fixed before the sweep, not tuned to any survivor."
- **Novelty test**: Low novelty priority — a hand-designed scoring function. Search only to confirm the min()-balanced-bridge formulation isn't lifted from a named LBD ranking scheme. "balanced ABC score min z LBD ranking", "conjunctive bridge score literature discovery."
- **Novelty-risk prior**: LOW — presented as engineering, not claimed as novel; the paper explicitly calls it a human design choice, so little to defeat.

### C2-11 (IMPLICIT)
- **Type**: METHOD
- **Claim**: Out-of-funnel / hard-negative discrimination test — applying the referee to a *frozen* naive curated-association nominator's top 600 guesses (top-50 Open Targets-scored genes per disease, chosen without reference to the referee), showing the referee's own hops cull 15.7% including strongly-associated flagship pairs (IL36RN×psoriasis 0.82, TREX1×lupus 0.78, PADI4×RA 0.68), each *untested* for failed knockdown. A test that does not choose genes by the outcome being evaluated.
- **Location**: §4.2b
- **Paper's own hedge**: reported "separately from, and not conflated with, the disease hop's substrate-inherited stringency"; framed as the referee's *own* edge.
- **Novelty test**: This is a diagnostic design more than a standalone novel claim; audit mainly for whether the biology hard-negatives (IL36RN/TREX1/PADI4 failing QC in *this* screen) are correctly characterized. Search: "IL36RN psoriasis Perturb-seq knockdown", "PADI4 rheumatoid arthritis CRISPRi CD4 knockdown efficiency". Low as a *novelty* claim.
- **Novelty-risk prior**: LOW — a verification design, not a claimed invention.

### C2-12
- **Type**: BIOLOGY
- **Claim**: NAB2 is a Th1/Th2 (specifically Th2) regulator — a **literature-novel regulatory nomination**. Perturbation data support it hop-by-hop: 2/2 guides significant, on-target effect −16.9, 301 downstream DE genes, Th2-associated in the Ota contrast (z = 7.71). An independent four-agent literature audit surfaced no papers connecting NAB2 to Th1/Th2 polarization; NAB2's only described T-cell role is as an EGR-family coregulator (Egr-1/NAB2 tuning T-cell activation, Collins 2008), distinct from polarization.
- **Location**: abstract; §1; §4.3; §5.4
- **Paper's own hedge**: "consistent with a re-derived NAB2→Th1/Th2 chain the literature has not made"; "targeted agent search, not an exhaustive systematic review, so we claim novelty in the surfaced literature rather than proven absence"; not significant in the Höllbacher contrast (one of two, reported).
- **Novelty test**: The core biology-novelty claim. Search PubMed/Europe PMC: "NAB2 Th2", "NAB2 Th1 Th2 polarization", "NAB2 T helper differentiation", "NAB2 GATA3 / IL-4 CD4 T cell", "NGFI-A binding protein 2 T cell polarization". Check EGR2/NAB2 immunology literature (EGR2 is a known T-cell tolerance/Th regulator — is NAB2's role implied via EGR2?). Also Open Targets / GWAS catalog for NAB2–immune associations. A single prior paper linking NAB2 to Th2/GATA3 would defeat "literature-novel."
- **Novelty-risk prior**: MEDIUM — NAB2 is an EGR co-regulator and EGR2 is a well-studied T-cell factor, so a NAB2→Th differentiation link may already exist implicitly in the EGR2/Egr axis literature; the "surfaced literature" hedge is doing a lot of protective work.

### C2-13
- **Type**: BIOLOGY
- **Claim**: NAB2 → atopic eczema nomination — NAB2's downstream signature enriches in two atopic-eczema modules (OR 3.90/FDR 0.0028; OR 3.43/FDR 0.0224), a literature-novel gene→disease connection.
- **Location**: abstract; §4.3; §5.4
- **Paper's own hedge**: strongly hedged — a "genetic-association nomination" (GWAS-based label, no coloc/LD control), "not an expression claim or a proof of disease causality"; the LD-inheritance-within-12q13 confounder is foregrounded as unresolved (§4.4b, §5.3).
- **Novelty test**: Search "NAB2 atopic dermatitis", "NAB2 eczema", "NAB2 12q13 atopy GWAS", "NAB2 STAT6 locus atopic dermatitis". Critical adjacency risk: NAB2 sits in the 12q13 atopy locus next to STAT6 (a master atopy gene) — check whether NAB2 has already been implicated (even as a locus passenger) in AD GWAS/eQTL papers (Paternoster 2015 and follow-ups). If NAB2 appears in any 12q13 AD fine-mapping/eQTL paper, the "novel" framing weakens.
- **Novelty-risk prior**: MEDIUM–HIGH — the 12q13/STAT6 co-location means NAB2 may already appear in atopic-dermatitis locus literature as a candidate; the paper itself concedes it cannot rule out LD inheritance, so the disease link is the most vulnerable biology claim.

### C2-14
- **Type**: BIOLOGY
- **Claim**: The STAT6 cis-effect confounder is ruled out at the expression level — under NAB2 knockdown, STAT6 is unmoved (log2FC +0.087, adj p 0.788; ranks 5,444/10,282), so the observed Th2/eczema signal is NAB2-specific, not CRISPRi bleed onto the adjacent STAT6. Corroborated by shared-cluster (zero), reproducibility (R 0.74), and the authors' own off-target flag (False for NAB2).
- **Location**: abstract; §4.3; §4.4; §5.3
- **Paper's own hedge**: tightly scoped — "one aggregate Stim8hr expression null excludes a detectable expression-level cis-effect, not every conceivable cis channel (transient, subset-specific, chromatin-level)"; leaned on together with the geometric argument; "does not prove the disease link."
- **Novelty test**: Not a literature-novelty claim per se (it's an analysis result on the authors' data); audit for *correctness*: does the deposited GWCD4i.DE_stats.h5ad actually show STAT6 unmoved under NAB2-KD? Check CRISPRi cis-effect spreading literature (Lensch 2022, cited) for the ~43kb promoter-distance argument's validity. Search "CRISPRi cis-effect neighboring gene distance dCas9-KRAB spread kb".
- **Novelty-risk prior**: LOW (as a novelty claim) — it's a data-analysis result, well-hedged; the risk is analytical (is 43 kb really outside the spread window?), not prior-art.

### C2-15
- **Type**: BIOLOGY
- **Claim**: NAB2 acts as a "Th2 brake" lost/suppressed in chronic atopic-dermatitis lesions — exploratory mining shows NAB2 reads *down* in lesional AD skin (bulk log2FC −0.32, FDR 0.002; anti-correlated with Th2 activity ρ −0.34; single-cell per-cell reduction in keratinocyte −0.51, T/NK −0.57), suggesting the therapeutic direction is restoration/up-modulation, not knockdown.
- **Location**: §5.2
- **Paper's own hedge**: heavily hedged — "exploratory," "a nomination for the next experiment, not a finding"; "we advance the brake model as the directional *question* to test rather than an established concordance"; concordance turns on the sign of the Th2-program change, which the substrate does not settle; only a perturbation (restoring NAB2) can confirm.
- **Novelty test**: Search "NAB2 lesional atopic dermatitis expression", "NAB2 downregulated eczema skin", "NAB2 Th2 brake / suppressor". Check the public AD expression datasets used (accessions in the direction-analysis record) for whether NAB2 direction is already noted. Also whether any prior work casts an EGR/NAB2 module as a Th2 negative regulator.
- **Novelty-risk prior**: LOW–MEDIUM — presented explicitly as a hypothesis-to-test, not a finding; low overstatement risk given the hedging, though the underlying direction data could already be reported in an AD transcriptomics paper.

### C2-16 (IMPLICIT)
- **Type**: METHOD
- **Claim**: The negative-control / self-honesty result that the disease hop's stringency is *substrate-inherited*, not the referee's own — established by a 2,000-permutation label shuffle (null passes 467.7±10.9 ≈ observed 406; observed sits 5.6 SD below null; upper-tail p = 1.0). Presented as "the most important honesty check in the paper," and the finding that "the disease hop's stringency is inherited from the substrate rather than supplied by the referee" is called a *result* the negative controls locate precisely.
- **Location**: abstract; §4.1b (Control 2); §4.2b; §5.3; Fig 3A
- **Paper's own hedge**: this is itself a de-escalation / honesty claim — explicitly *reduces* the referee's credit; "we explicitly do not claim a rarer-than-chance selectivity."
- **Novelty test**: Not a prior-art-defeatable novelty claim; it is a self-limiting diagnostic. Audit only for internal consistency (does the label-shuffle logic support "inherited"?). No literature search needed to defeat it; its role in the audit is that it *weakens* C2-04's referee-discrimination claim.
- **Novelty-risk prior**: LOW — it is a candor claim, not a novelty claim; noted here because it materially bounds the "confident no" contribution.

---

## Extractor 2 — honest first read

Pre-search impression, clearly labeled. This reads as a **genuine, narrowly-scoped methodological contribution wrapped in unusually disciplined hedging** — not obvious repackaging. The real wedge (C2-01/C2-02) is the *conjunction*: an LBD generator feeding a deterministic, non-LLM referee that adjudicates each hypothesis against a *held, pre-existing* perturbation dataset and can *abstain* on QC grounds. Each ingredient exists elsewhere (LBD ranking, actor-critic LLMs, perturbation benchmarks like PerturbQA, AI-scientist agents), so the novelty stands or falls on whether that exact combination — and specifically the QC-gated *untested* verdict and the *held-substrate* framing — is truly unclaimed; that is the highest-value search target. The most vulnerable claims are the biology: NAB2→Th2 regulator (C2-12) and especially NAB2→atopic-eczema (C2-13), because NAB2 sits beside STAT6 in the 12q13 atopy locus and may already surface in AD GWAS/eQTL literature as a locus passenger — the paper itself cannot discharge the LD-inheritance confounder and admits it. Notably, the manuscript pre-emptively demotes several of its own strongest-sounding claims (the "confident no" is largely substrate-inherited, C2-16; reproduction is a cache recomputation, not a live crawl), which lowers overstatement risk but also shrinks what is left to credit. The implicit contributions (self-audit language-critic C2-06, headless-workbench reproducibility C2-07) are literature-novel but contestable as *scientific* rather than *engineering* contributions.

---

## Executive summary (for the caller)

Extracted **16 contribution/novelty claims** — 10 METHOD (incl. 6 flagged as implicit) and 4 BIOLOGY, plus one self-limiting honesty diagnostic. The novelty crux is the §2.4 conjunction (C2-01/C2-02): an LBD front-end + deterministic non-LLM referee scoring each hypothesis against a *held, pre-existing* Perturb-seq substrate, with QC-gated **abstention** and **falsification** as first-class verdicts — each ingredient has neighbors (PerturbQA, AI co-scientist, Robin, actor-critic LLMs), so novelty rests on the exact combination being unclaimed. Highest-risk claims to search: **C2-13** (NAB2→atopic eczema — NAB2 may already appear in 12q13/STAT6 atopy-locus GWAS/eQTL literature; paper cannot rule out LD inheritance) and **C2-12** (NAB2→Th2 regulator — possible implicit prior art via the EGR2/NAB2 axis). Implicit method claims (C2-06 self-audit language critic; C2-07 headless-workbench reproducibility) are literature-novel but may read as engineering, not science. The manuscript hedges aggressively and even demotes its own "confident no" (C2-16), lowering overstatement risk.
