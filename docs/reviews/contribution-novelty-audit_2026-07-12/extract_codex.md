# Codex extractor register (captured from stdout log)

### C-CODEX-01

- **ID**: C-CODEX-01
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: Wayfinder fills a missing LBD triage step by testing machine-generated hypotheses against independent experimental data, rather than ranking them only by literature-derived plausibility or rarity.
- **Location**: Abstract; §1; §2.1; §2.4; §5.1; §5.4
- **The paper's own hedge**: It claims to close the *triage* loop—deciding what merits follow-up—not the experimental-follow-up loop, and does not claim predictive correctness.
- **What would need to be true in the literature for this to be genuinely novel**: No earlier LBD system should already combine candidate generation with hypothesis-by-hypothesis adjudication against held experimental datasets. A search should specifically inspect Arrowsmith, SemMedDB/SemRep-based LBD, PubMed-scale predication systems, modern graph/link-prediction LBD, time-sliced LBD evaluation, and biomedical systems that rerank literature-derived candidates using omics, CRISPR-screen, functional-genomics, or assay evidence.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — evidence-grounded reranking is a natural extension of LBD and likely has precedents, but the precise held-data adjudication framing may be distinctive.

### C-CODEX-02

- **ID**: C-CODEX-02
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: Wayfinder provides a deterministic, non-LLM referee that evaluates every proposed gene → T-cell program → disease chain and returns a per-hop quantitative receipt—such as knockdown significance, effect size, program score, odds ratio, and FDR.
- **Location**: Abstract; §1; §2.2; §2.4; §3.3; §5.4
- **The paper's own hedge**: The disease receipt is a genetic-association nomination, not experimental evidence of disease causality; “supported” means only that the chain passed the defined receipt tests.
- **What would need to be true in the literature for this to be genuinely novel**: No prior LBD, evidence-graph, causal-chain validation, claim-verification, or AI-scientist system should already issue structured hop-level verdicts grounded in deterministic experimental lookups. Candidate systems include PaperQA/PaperQA2, FutureHouse Robin, SciAgents, Google’s AI co-scientist, CRISPR-grounded hypothesis benchmarks, scientific claim-verification systems, and provenance-bearing biomedical knowledge graphs.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — provenance and evidence chains are well-established ideas, but combining them with deterministic perturbation receipts at every hop is more specific.

### C-CODEX-03

- **ID**: C-CODEX-03
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The referee makes falsification a first-class outcome by returning a confident, receipt-backed *refuted* verdict rather than functioning as a confirmation-only filter.
- **Location**: Abstract; §1; §2.4; §3.3; §4.2; §5.1; §5.4
- **The paper's own hedge**: Within the main funnel, most rejection occurs at the substrate-inherited disease hop; the referee’s own strongest negative discrimination is concentrated in knockdown QC and, less often, effect/program failures.
- **What would need to be true in the literature for this to be genuinely novel**: Earlier LBD or AI-hypothesis systems must not already produce explicit negative/refuted decisions from independent experiments. Searches should cover falsification-oriented LBD, negative-evidence knowledge graphs, biomedical hypothesis rejection, contradiction detection, experimental claim verification, and perturbation-based hypothesis triage.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — explicit rejection is common in validation pipelines, but may be uncommon as the central deliverable of an LBD system.

### C-CODEX-04

- **ID**: C-CODEX-04
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: Wayfinder distinguishes *untested* from *refuted*: a perturbation that fails knockdown quality control triggers abstention rather than being interpreted as biological absence of effect.
- **Location**: Abstract; §1; §2.4; §3.3; §4.1b; §4.2; §5.1; §5.4
- **The paper's own hedge**: Abstention is bounded to what the selected Perturb-seq substrate can test; it is a data-quality decision, not a biological conclusion.
- **What would need to be true in the literature for this to be genuinely novel**: No previous perturbation-screen interpretation system, selective-prediction framework, evidence-aware LBD tool, or AI-scientist system should already use QC-gated abstention and explicitly separate failed measurement from negative biology. Relevant prior art includes CRISPR-screen QC pipelines, Perturb-seq analysis frameworks, “reject option” or selective classification, assay-aware decision systems, and three-valued scientific claim verification.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — treating failed perturbations as uninterpretable is standard experimental logic, although elevating it into an explicit LBD verdict contract may still be a useful implementation contribution.

### C-CODEX-05

- **ID**: C-CODEX-05
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The specific combination of an LBD front end, deterministic experimental back end, per-hop receipts, QC-gated abstention, and first-class falsification has not previously been provided by AI-scientist or LBD systems.
- **Location**: §2.4
- **The paper's own hedge**: The asserted gap is described as “narrow and specific,” and the authors say only that they are “not aware” of a system with this combination.
- **What would need to be true in the literature for this to be genuinely novel**: No single prior system may contain substantially all these elements, even if each exists separately. The audit must directly compare the full feature set against Google AI co-scientist, PaperQA2, Robin, SciAgents, autonomous chemistry/ML scientists, PerturbQA-like systems, and experimental-data-grounded biomedical agents.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — combination claims are often defensible when narrowly drafted, but can amount to integration novelty rather than a new scientific principle.

### C-CODEX-06

- **ID**: C-CODEX-06
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: Wayfinder enforces a division of labour in which deterministic tools compute every biological receipt while language models are limited to interpretation, judgment, and provenance assembly.
- **Location**: §2.3; §2.4; §3.1; §3.4; §5.3
- **The paper's own hedge**: Model interpretation remains judgment; objective weights are human-designed; the critic enforces language and receipt consistency rather than independently validating biology.
- **What would need to be true in the literature for this to be genuinely novel**: Prior tool-using scientific agents must not already separate deterministic computation from LLM interpretation in essentially this fashion. Candidate prior art includes PaperQA2, Robin, ReAct/tool-use agents, code-executing scientific copilots, provenance-aware agents, and neuro-symbolic biomedical reasoning systems.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — this is established tool-use architecture and good scientific hygiene, though its rigorous application here may be contributory.

### C-CODEX-07

- **ID**: C-CODEX-07
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The candidate universe is constructed without consulting disease evidence, making it “disease-answer-free” and preventing disease-label leakage during candidate-gene selection.
- **Location**: §3.2; §4.1; §4.6
- **The paper's own hedge**: The universe is not evidence-free: it is preselected using the same knockdown, effect, and program evidence later reread by the referee, making the program hop tautological within the funnel.
- **What would need to be true in the literature for this to be genuinely novel**: No prior LBD evaluation or omics-prioritization pipeline should already use outcome-blind candidate construction or leakage-resistant held-evidence design in an equivalent way. Search time-sliced LBD, nested feature selection, target-prioritization benchmarks, and answer-free biomedical evaluation protocols.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — avoiding target leakage is standard methodology; the particular construction is useful but unlikely to be conceptually new.

### C-CODEX-08

- **ID**: C-CODEX-08
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The ranking objective balances both literature bridge arms, rewards strong perturbational effects, penalizes direct gene–disease literature and curated association, and thereby prioritizes candidates that are both data-loud and near-novel without rewarding pure obscurity.
- **Location**: §3.2; §4.1; §4.1b–c
- **The paper's own hedge**: The weights are human choices, fixed before the sweep; ranking affects which survivor is foregrounded but not its referee verdict. NAB2 is sensitive to an aggressive literature-floor threshold.
- **What would need to be true in the literature for this to be genuinely novel**: No earlier LBD scoring method should already combine balanced ABC evidence, novelty penalties, known-association penalties, and experimental-effect strength in a comparable objective. Candidate prior art includes rarity-adjusted LBD, balanced-path scoring, graph novelty metrics, target-prioritization scores, and multi-objective evidence ranking.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — weighted composite ranking functions of this kind are common; novelty would likely lie in the exact application rather than the mathematical form.

### C-CODEX-09

- **ID**: C-CODEX-09
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The full generation, evidence-integration, provenance, and language-audit loop was operated within an agentic scientific workbench using an author model and a distinct reviewer model at separate checkpoints.
- **Location**: Abstract; §1; §2.3; §3.4; §4.5; §5.1
- **The paper's own hedge**: Reviewer independence is role-, model-, and checkpoint-level within one vendor/model family, not cross-vendor epistemic independence; the audit checks receipt consistency and calibrated wording, not biological truth.
- **What would need to be true in the literature for this to be genuinely novel**: No previous actor–critic AI-scientist workflow should already generate an analysis, check its numeric claims against artifacts, and revise its own scientific language. Candidate systems include AI Scientist, Google AI co-scientist, SciAgents, Robin, multi-agent peer-review systems, Reflexion-style agents, and automated manuscript fact-checking.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — author–critic agent architectures and automated verification are already widespread; the artifact-level scientific audit may be the more distinctive detail.

### C-CODEX-10

- **ID**: C-CODEX-10
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: A headless browser driver converted an API-less, manually operated scientific workbench into a re-runnable, audited, “replicable-in-principle” agentic pipeline with logged approvals and retrieved provenance.
- **Location**: Abstract; §3.4; §4.5; §5.1; §5.3
- **The paper's own hedge**: It is UI-dependent browser automation over an unstable interface, not a durable API; the full-scale reproduction used cached external responses and was not a live crawl.
- **What would need to be true in the literature for this to be genuinely novel**: No previous work should already use browser automation or robotic process automation to make API-less scientific-agent environments reproducible and provenance-bearing. Search browser-use agents, UI automation for scientific workflows, RPA-based reproducible research, headless operation of computational notebooks, and audit-trail capture for agentic systems.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — browser automation is old, but presenting it as a reproducibility bridge for an agentic scientific workbench may be a novel operational contribution.

### C-CODEX-11

- **ID**: C-CODEX-11
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The workbench reproduced the complete funnel and ranking digit-for-digit and the sensitivity panel byte-for-byte, demonstrating that an otherwise one-off agentic analysis can be rerun and inspected.
- **Location**: Abstract; §4.5; §5.1
- **The paper's own hedge**: The full-scale reproduction used cached literature/association responses with live network access prohibited; reproducibility remains dependent on the workbench UI.
- **What would need to be true in the literature for this to be genuinely novel**: Prior agentic-science studies must not already report exact artifact-level reproduction of full workflows inside an interactive workbench. Search reproducible autonomous-scientist pipelines, deterministic agent replay, notebook provenance, workflow replay, and audit-store-based agent reconstruction.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — exact replay is valuable empirical evidence, though probably an engineering demonstration rather than a fundamentally new method.

### C-CODEX-12

- **ID**: C-CODEX-12
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The referee demonstrably spans support, refutation, and abstention with receipts, including perfect abstention on all 2,430 failed-knockdown controls.
- **Location**: Abstract; §4.1; §4.1b; §4.2
- **The paper's own hedge**: This is explicitly a behavioral diagnostic, not external validation, precision/recall measurement, or evidence that the verdicts are correct at scale.
- **What would need to be true in the literature for this to be genuinely novel**: No prior experimental-hypothesis referee should already demonstrate three-way receipt-backed decisions and zero-leakage QC abstention on perturbation data. Relevant comparisons include CRISPR-screen QC systems, selective prediction, assay validity gates, and biomedical claim-verification benchmarks.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — perfect conformance to a deterministic rule mainly establishes implementation correctness, not a new scientific capability.

### C-CODEX-13

- **ID**: C-CODEX-13
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: The negative-control analysis localizes the referee’s genuine discrimination: disease-hop stringency is inherited from the enrichment substrate, whereas the referee’s own edge is primarily the knockdown-QC gate, which rejects or abstains on roughly one in six arbitrary or association-prioritized genes.
- **Location**: Abstract; §4.1b; §4.2; §4.2b; §5.3
- **The paper's own hedge**: The label-shuffle result does not show better-than-chance selectivity; the observed support count is below the shuffled mean, and the mechanism is not interpreted. Own-hop culls are not claimed to establish overall decision accuracy.
- **What would need to be true in the literature for this to be genuinely novel**: No earlier LBD or AI-referee study should already decompose apparent discrimination into model/referee-added versus substrate-inherited components using label permutations and out-of-funnel controls. Search negative-control methodology in target prioritization, permutation-tested knowledge graphs, enrichment-label shuffling, assay-aware LBD, and evaluation of AI-scientist filters.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — permutation controls are standard, but using them to audit where an agentic hypothesis referee’s discrimination actually originates is a meaningful methodological result.

### C-CODEX-14

- **ID**: C-CODEX-14
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: Wayfinder reduced 22,039 literature-eligible gene–program–disease hypotheses to 43 supported pairs and 30 clean receipt-complete nominations.
- **Location**: Abstract; §1; §3.2; §4.1; §5.1; §5.4
- **The paper's own hedge**: The 43 are jointly produced by the literature gate and referee; the referee alone supports 395 of 47,220 pairs. The program hop is pre-gated and cannot fail within the funnel, and the counts do not establish precision or recall.
- **What would need to be true in the literature for this to be genuinely novel**: This is novel only as an application/result of the proposed pipeline, not if prior systems already performed equivalent Perturb-seq-backed culling on the same Zhu/Dann CD4 T-cell resource or reported the same candidate set.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **LOW** — the exact funnel is likely specific to this implementation and threshold set, although its scientific importance is separate from novelty.

### C-CODEX-15

- **ID**: C-CODEX-15
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: The deposited Perturb-seq data are consistent with NAB2 being a regulator of the Th1/Th2 polarization program: successful NAB2 knockdown produces a large transcriptional effect and a significant Th2-associated shift in one marker contrast.
- **Location**: Abstract; §1; §4.3; §4.4b; §5.4
- **The paper's own hedge**: The role is “consistent with” and “re-derived,” not proven; only the Ota contrast is significant, while the Höllbacher contrast is not. The data do not settle the direction of NAB2’s biological action.
- **What would need to be true in the literature for this to be genuinely novel**: No earlier paper should directly connect NAB2 perturbation, expression, or function to Th1/Th2 polarization or a Th2 transcriptional program. Search NAB2 with Th1, Th2, T-helper differentiation, GATA3, IL-4, IFN-γ, TBX21/T-bet, EGR1/EGR2, and T-cell activation; Collins et al. 2008 and other EGR–NAB T-cell studies are especially important.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — NAB2’s EGR-coregulator role in T cells is already known, so a polarization-specific connection may be new but biologically adjacent to established work.

### C-CODEX-16

- **ID**: C-CODEX-16
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: NAB2 → Th1/Th2 polarization → atopic eczema is a literature-novel or near-novel regulatory nomination that the surfaced literature had not previously made.
- **Location**: Abstract; §1; §4.3; §5.4
- **The paper's own hedge**: “Near-novel” is operationally defined by six direct co-mentions and a low Open Targets association score, not strict A–C absence. The literature audit was targeted rather than systematic, and novelty is claimed only in the surfaced literature. The eczema hop is a GWAS-based nomination without LD control or colocalization.
- **What would need to be true in the literature for this to be genuinely novel**: There must be no prior direct NAB2–atopic dermatitis/eczema association, no 12q13 GWAS paper nominating NAB2, no eQTL/TWAS/colocalization study implicating NAB2, and no paper joining NAB2-mediated T-helper polarization to eczema. Searches should include NAB2 with atopic dermatitis, atopic eczema, atopy, 12q13, STAT6, TWAS, eQTL, GWAS fine-mapping, and colocalization.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — NAB2 resides in a well-studied atopy locus next to STAT6, making prior genetic nomination or locus-level mention quite plausible even if the full mechanistic chain is new.

### C-CODEX-17

- **ID**: C-CODEX-17
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: There is no detectable expression-level CRISPRi cis-effect on neighboring STAT6 under NAB2 knockdown at Stim8hr, strengthening the interpretation that the observed perturbation signal is NAB2-specific rather than STAT6 bleed-through.
- **Location**: Abstract; §1; §4.3 figure; §4.4; §4.4b; §5.4
- **The paper's own hedge**: One aggregate expression null excludes only a detectable expression-level effect at that condition; it does not exclude transient, subset-specific, chromatin-level, or other cis mechanisms, and it does not prove the eczema link.
- **What would need to be true in the literature for this to be genuinely novel**: No prior analysis of the Zhu/Dann Perturb-seq dataset, NAB2 CRISPRi experiments, or 12q13 regulatory architecture should already report that STAT6 expression remains unchanged after NAB2 targeting. Search NAB2/STAT6 cis-regulation, CRISPRi collateral repression, convergent overlapping genes, 12q13 chromatin contacts, and the source dataset’s supplementary analyses.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **LOW** — this exact perturbation-by-neighbor null result is likely newly extracted from the deposited matrix, even though the inference from a null is necessarily narrow.

### C-CODEX-18

- **ID**: C-CODEX-18
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: NAB2’s significant eczema-associated modules are genome-wide functional immune modules rather than a locally colocated 12q13 gene-set artifact; STAT6 is absent from the corrected significant modules 90 and 100.
- **Location**: §4.3; §4.4b; §4.6
- **The paper's own hedge**: This rejects only the cluster-membership artifact; it does not resolve whether the eczema disease label is inherited through LD at 12q13.
- **What would need to be true in the literature for this to be genuinely novel**: No previous analysis of the source perturbation/enrichment tables should already characterize NAB2’s modules, their corrected cluster identities, their immune composition, or STAT6’s absence. The source Zhu/Dann manuscript, supplementary module definitions, later reanalyses, and 12q13 network studies are the key prior art.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **LOW** — the corrected module-level observation appears highly dataset-specific, though interpreting module composition as excluding a locus artifact may be less novel than the underlying calculation.

### C-CODEX-19

- **ID**: C-CODEX-19
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: The Perturb-seq and module evidence support a NAB2 regulatory nomination, but the NAB2-specific provenance of the atopic-eczema association remains unresolved because the disease label may be inherited through LD from the 12q13/STAT6 atopy locus.
- **Location**: Abstract; §4.3; §4.4b; §5.3
- **The paper's own hedge**: This is explicitly presented as an open question, not a settled NAB2 → eczema link; resolving it requires variant-level colocalization and may require a detectable NAB2 cis-eQTL in CD4 T cells.
- **What would need to be true in the literature for this to be genuinely novel**: The exact decomposition of the NAB2 claim into perturbation specificity, module membership, and unresolved LD-label provenance must not have been made previously. Search fine-mapping and colocalization of the 12q13 atopic-dermatitis locus, especially work distinguishing NAB2 from STAT6.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — locus ambiguity around adjacent genes is standard genetics, but applying the decomposition to this specific nomination may be new.

### C-CODEX-20

- **ID**: C-CODEX-20
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: Public lesional atopic-dermatitis expression data show reduced NAB2 in lesions, including per-cell reductions in keratinocyte and T/NK compartments rather than merely altered cell composition.
- **Location**: §5.2
- **The paper's own hedge**: The analysis is exploratory, outside the referee substrate, and the evidence across voting arms is mixed; expression association cannot distinguish effector from brake.
- **What would need to be true in the literature for this to be genuinely novel**: No original dataset publication or later reanalysis should already report lower NAB2 in atopic-dermatitis lesions, keratinocytes, T cells, or NK cells. Search each cited/accessioned bulk and single-cell dataset, NAB2 differential expression in atopic dermatitis, and lesion/non-lesion transcriptional signatures.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **HIGH** — differential-expression results from public disease datasets are often already present in source papers, supplements, portals, or subsequent reanalyses.

### C-CODEX-21

- **ID**: C-CODEX-21
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: The combined evidence is more consistent with NAB2 acting as a Th2 brake that is lost or suppressed in chronic atopic-dermatitis lesions than as a Th2 driver.
- **Location**: §5.2
- **The paper's own hedge**: This is advanced as a directional question, not an established mechanism; the Perturb-seq directional metrics do not settle the sign, and expression cannot distinguish an effector from a compensatory brake.
- **What would need to be true in the literature for this to be genuinely novel**: No prior mechanistic or expression study should already propose NAB2 as a negative regulator of Th2 activity, type-2 inflammation, or atopic dermatitis. Search NAB2/EGR corepression, Th2 brakes, IL-4/STAT6 feedback, chronic-lesion suppressors, and NAB-family functions in allergic inflammation.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — the specific brake model may be new, but negative-feedback roles for EGR/NAB coregulators could provide close precedent.

### C-CODEX-22

- **ID**: C-CODEX-22
- **Type**: BIOLOGY
- **Claim (verbatim or tight paraphrase)**: If the NAB2-as-brake interpretation holds, therapeutic NAB2 knockdown would likely be directionally wrong; restoration or up-modulation of NAB2 is the falsifiable intervention to test next.
- **Location**: §5.2; §5.3b
- **The paper's own hedge**: This is explicitly a nominated experiment, not a therapeutic claim; only a restoration perturbation showing dampened Th2 activity could support it.
- **What would need to be true in the literature for this to be genuinely novel**: No prior study or patent should already propose NAB2 activation, restoration, or stabilization for atopic dermatitis or Th2 disease, and no prior perturbation should show that increasing NAB2 suppresses Th2 markers.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — the intervention direction is a new extrapolation from the proposed brake model, but it currently rests on incomplete directional evidence.

### C-CODEX-23

- **ID**: C-CODEX-23
- **Type**: METHOD
- **Claim (verbatim or tight paraphrase)**: Independent cross-family, adversarial reimplementation reproduced every headline numerical result and exposed correctable errors, supporting that the reported quantities are properties of the deposited data rather than artifacts of the authors’ code.
- **Location**: Abstract; §1; §4.6
- **The paper's own hedge**: Not every replicator checked every quantity, although every headline quantity was checked by at least one clean-room member; this supports computational robustness, not biological validity.
- **What would need to be true in the literature for this to be genuinely novel**: No prior publication should already use a multi-model adversarial “replication lab,” including clean-room reimplementations by different model families, as a validation method for an agentic scientific analysis. Compare multi-agent code review, computational reproducibility audits, adversarial collaboration, ensemble scientific agents, and cross-model replication studies.
- **Novelty-risk prior (pre-search, your cross-model gut)**: **MEDIUM** — independent reimplementation is traditional, but packaging cross-vendor agents as an adversarial replication lab may be genuinely recent.

## Codex extractor's honest first read

Pre-search, this looks like a real integration and research-workflow contribution, but not obviously a new scientific paradigm. Its strongest methodological distinction is the tightly scoped combination of LBD generation, deterministic held-data adjudication, per-hop receipts, explicit abstention, and negative verdicts; most individual ingredients are familiar. The NAB2 perturbation and STAT6-neighbor checks look like genuine dataset-derived findings, while the eczema connection is much more vulnerable because NAB2 sits inside a known atopy locus and the disease label lacks colocalization. The manuscript is unusually candid about leakage, tautological funnel stages, substrate-inherited stringency, and the difference between computational robustness and biological validity. Bluntly, the work is more convincing as a carefully engineered, auditable triage demonstration with one intriguing nomination than as proof that the method advances biological discovery at scale.
