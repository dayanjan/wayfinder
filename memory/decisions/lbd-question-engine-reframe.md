---
name: lbd-question-engine-reframe
description: The core reframe — LBD as a question-GENERATION engine that fills the Researcher-track cold-start gap ("rich dataset, no question")
metadata:
  type: project
---

**The reframe (operator, 2026-07-07) — the strategic heart of the project.**
The Researcher track asks each participant to *bring a question* and use Claude Science + their own/provided
data to answer it. The unfilled gap: **what if you have a rich dataset but do not know what question to ask?**
Claude Science is a superb data-grounded ANSWERING engine and — by design (anti-confabulation, reviewer-gated,
"compute don't confabulate") — it will NOT invent speculative questions. So "what should I ask this dataset?"
is a real, unaddressed cold-start problem, made worse by the flood of atlas/screen datasets that outpace anyone's
ability to interrogate them.

**Our answer:** use **literature-based discovery (LBD, Swanson ABC)** as a QUESTION-GENERATION engine — mine the
literature for the highest-value *untested* hypotheses the dataset is uniquely positioned to resolve, then hand
those questions to **Claude Science + the datasets** to answer via the referee/Validator [[hardware-and-claude-science-placement]].

**Why it's strong:** (1) turns the apparent weakness ("I have no question of my own") into the thesis; (2) fills a
gap Claude Science structurally cannot fill itself; (3) answers the dead R01 critique one level up — LBD generates
*the right questions*, not unvalidated noise; the data-referee culls. See the killer-critique thesis in `docs/plan.md`.

**Winning guardrail:** the FINDING must stay the star for Researcher judges — "LBD found question Q -> Claude Science
+ data answered Q -> here is the reproducible, receipt-backed result," with the LBD engine as the *method that got
you there* (which is exactly what the track asks: "how Claude Science got you there"). Do not let the tool eclipse
the finding.

**Compute/compliance:** LBD proposer = API queries (PubTator3 / SemMedDB / Open Targets / PubMed / OpenAlex /
GWAS Catalog) + set logic; laptop CPU, no GPU/Colab. Referee = CPU pandas. Both fresh code (NEW WORK ONLY). Full
build spec: `docs/lbd-proposer-spec.md`. Dataset = Zhu/Dann/Pritchard/Marson genome-scale CD4+ T-cell Perturb-seq
(bioRxiv 2025.12.23.696273); A=regulators, B=programs (Th1/Th2, aging, cytokine × 3 conditions), C=~17 autoimmune diseases.
