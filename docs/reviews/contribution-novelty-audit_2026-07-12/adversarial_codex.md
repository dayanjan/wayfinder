# Codex adversarial review (captured from stdout log)

Th1/Th2 markers with an orthogonal method to control for CRISPRi \emph{cis}-artifacts. None of these is gating
for the present contribution --- a prioritization method with explicit abstention and falsification
diagnostics --- but each is a rung on the ladder from association to cause, and naming them precisely is part
of the calibrated-language discipline the paper argues for.

\subsection*{5.4 Conclusion}\label{conclusion}

Literature-based discovery has never lacked for hypotheses; it has lacked a disciplined way to decide which
ones to pursue, and the candor to say \emph{no}. Wayfinder pairs a machine hypothesis-generator with a
deterministic referee that evaluates each proposal against a held experimental substrate and returns a
prioritization verdict with a receipt at every hop --- supporting, refuting, or declining to test --- and runs the whole loop,
including an audit of its own language, inside an agentic workbench whose work we can reproduce and inspect.
Applied to a genome-scale CD4\textsuperscript{+} T-cell resource, it culled tens of thousands of machine-generated hypotheses
to a small set of receipt-backed survivors, of which NAB2 $\rightarrow$ Th1/Th2 $\rightarrow$ atopic eczema is the worked example: a
literature-novel regulatory nomination whose sharpest artifactual confounder we ruled out at the expression level against the study
authors' own data, and which points to a concrete, falsifiable next experiment. The contribution is the
method and what it found --- receipt-backed prioritization of machine-generated hypotheses, with explicit
abstention and falsification diagnostics --- and the confident, receipt-backed \emph{no} that a triage step
must be willing to give.

[31;1mMicrosoft.PowerShell_profile.ps1: [31;1mCannot dot-source this command because it was defined in a different language mode. To invoke this command without importing its contents, omit the '.' operator.[0m

codex
1. **Target:** Overall contribution; M1–M3, M8, M10  
   **The attack:** The manuscript presents a prioritization method without evaluating prioritization quality. It reports no precision, recall, enrichment over baselines, calibration, false-refutation rate, prospective success, or time-sliced recovery. The funnel merely proves that thresholds remove candidates. Rank stability proves that similar hand-chosen weights produce a similar ranking, not that the ranking is scientifically useful. A method whose central output is “which hypothesis deserves bench time?” must show that its ordering is better than simpler alternatives—effect size alone, perturbation FDR alone, disease enrichment alone, random ranking, or standard LBD scores. The manuscript explicitly admits that it has measured behavior, not correctness. That is not merely a limitation; it leaves the principal methods claim unevaluated.  
   **Severity:** **FATAL**  
   **What would rebut me:** A credible external or time-sliced benchmark showing that Wayfinder materially outperforms simple component-score and established LBD baselines, including performance on supported, refuted, and abstained cases.  
   **Search to confirm:**  
   - `"literature based discovery" experimental data hypothesis prioritization benchmark precision recall`  
   - `"literature based discovery" time slicing evaluation ranked hypotheses precision@k`  
   - `"biomedical hypothesis generation" held-out experimental validation ranking baseline`  
   - `"Perturb-seq" hypothesis prioritization literature discovery`

2. **Target:** B2, B5, B7; the claimed NAB2–atopic-eczema finding  
   **The attack:** The disease nomination may be nothing more than a locus passenger. NAB2 sits beside STAT6 in the established 12q13 atopy locus. The disease receipt assigns GWAS-derived labels without fine-mapping, LD control, colocalization, or gene-specific variant-to-function evidence. Thus, “NAB2 → eczema” may arise because an aggregated enrichment table transfers a regional STAT6 signal onto NAB2-related modules. Showing that NAB2 CRISPRi does not reduce STAT6 expression addresses guide spillover; it does absolutely nothing to establish that the eczema association belongs to NAB2 rather than STAT6. The manuscript knows this, yet still promotes the unresolved chain as its flagship “finding.” Until the locus attribution is resolved, the disease edge is not a biological result.  
   **Severity:** **FATAL** for the biological headline; **MAJOR** for the methods paper  
   **What would rebut me:** Fine-mapping or colocalization demonstrating that the atopic-dermatitis signal shares a causal variant with NAB2 expression or regulation in a relevant immune cell, with materially weaker evidence for STAT6; alternatively, functional variant evidence directly implicating NAB2.  
   **Search to confirm:**  
   - `"NAB2" "atopic dermatitis"`  
   - `"NAB2" eczema GWAS`  
   - `"NAB2" atopy 12q13 STAT6`  
   - `"12q13" atopic dermatitis fine mapping STAT6 NAB2`  
   - `"atopic dermatitis" GWAS colocalization NAB2 STAT6`  
   - `"NAB2" eQTL CD4 T cells STAT6`  
   - `"rs324011" NAB2 STAT6 atopy`

3. **Target:** M1, M2, M3, M4  
   **The attack:** M1 looks like novelty by conjunction: assemble enough qualifiers—LBD front end, deterministic non-LLM referee, held pre-existing substrate, per-hop receipts, QC abstention, first-class falsification—and almost any implementation becomes unprecedented. Each substantive primitive is familiar: evidence-grounded ranking, tool-mediated deterministic computation, provenance, QC-based missingness, selective prediction/abstention, negative findings, and held-out experimental evaluation. “No prior system has this exact bundle” is not a scientific gap unless the bundle produces a demonstrated capability unavailable from simpler combinations. Here it has not. The paper risks patent-claim novelty rather than conceptual novelty.  
   **Severity:** **FATAL** if M1 remains the load-bearing novelty claim  
   **What would rebut me:** A systematic review showing that neighboring systems genuinely cannot adjudicate generated hypotheses against existing experimental measurements with provenance and abstention—and evidence that this exact integration yields better scientific decisions than those neighbors.  
   **Search to confirm:**  
   - `"literature based discovery" "experimental evidence" ranking hypotheses`  
   - `"literature based discovery" data-driven validation candidate hypotheses`  
   - `"hypothesis generation" deterministic tools experimental data abstention`  
   - `"biomedical hypothesis" evidence graph provenance per claim`  
   - `"selective prediction" biomedical decision support abstention quality control`  
   - `"negative evidence" literature based discovery hypothesis rejection`

4. **Target:** M1 relative to AI co-scientist, Robin/PaperQA2, and PerturbQA  
   **The attack:** The neighbor exclusions appear definitional rather than functional. Robin analyzes real assay data in an iterative research loop; AI co-scientist ranks and critiques hypotheses and reportedly sends selected candidates to experimental validation; PerturbQA connects biological questions to perturbational readouts. Calling new experiments categorically different from a “held substrate,” or prediction scoring categorically different from a “referee,” may preserve wording novelty while evading the real comparison: do these systems already integrate hypotheses with empirical measurements, reject weak candidates, and expose evidence? The manuscript compares prose descriptions, not tasks, inputs, outputs, failure modes, or benchmark performance.  
   **Severity:** **MAJOR**  
   **What would rebut me:** Primary documentation demonstrating that none of these systems can ingest existing assay results, issue evidence-grounded negative or abstaining judgments, and return inspectable claim-level evidence—and a task-matched comparison showing Wayfinder adds a nontrivial capability.  
   **Search to confirm:**  
   - `"Robin" FutureHouse assay data hypothesis experimental results agent`  
   - `"Robin: A multi-agent system for automating scientific discovery" assay data`  
   - `"AI co-scientist" hypothesis ranking experimental validation negative results`  
   - `"PerturbQA" perturbation data question answering CRISPR`  
   - `"PaperQA2" scientific agents evidence citations claims`  
   - `"AI co-scientist" falsification critique tournament hypotheses`  
   - `"Robin" hypothesis rejection evidence provenance`

5. **Target:** B1, B7  
   **The attack:** “NAB2 is a literature-novel Th1/Th2 regulator” may simply rename known EGR–NAB biology. NAB proteins are established feedback coregulators of EGR transcription factors, and EGR2/EGR3 are deeply implicated in T-cell activation, tolerance, differentiation, and cytokine programs. If prior work already places NAB2 in activated T cells or EGR-controlled helper-T-cell regulation, then observing a Th1/Th2 signature after NAB2 knockdown is an incremental dataset annotation, not a new mechanism. Moreover, the manuscript does not establish direction: its own data cannot tell whether NAB2 is a Th2 brake or driver. “Regulator” is therefore broad enough to be true but too weak to constitute a mechanistic advance.  
   **Severity:** **MAJOR**  
   **What would rebut me:** Absence of prior evidence connecting NAB2—not merely EGR2/3—to helper-T-cell polarization, coupled with independent perturbational evidence showing a reproducible, directional effect on Th1/Th2 fate or canonical effector outputs.  
   **Search to confirm:**  
   - `"NAB2" T cell differentiation`  
   - `"NAB2" Th2 OR "T helper 2"`  
   - `"NAB2" Th1 polarization`  
   - `"NAB2" T cell activation cytokine`  
   - `"EGR2 NAB2" T cells`  
   - `"EGR1 NAB2" IL-4 IFNG T cell`  
   - `"NAB proteins" helper T cell differentiation`

6. **Target:** M3, M10; the “confident, receipt-backed no” headline  
   **The attack:** The paper’s own negative control largely dissolves its supposed moat. The dramatic disease-hop rejection rate survives label shuffling, showing that it comes from sparse/FDR-filtered substrate labels, not intelligent discrimination by Wayfinder. The program hop is tautological inside the selected universe because candidates were preselected for program significance. What remains as the referee’s distinctive negative logic is mostly ordinary experimental QC: failed knockdown means uninterpretable, not negative. That is correct practice, but calling it a new falsification method inflates laboratory hygiene into a scientific contribution. Worse, `refuted-for-C` can mean only “this sparse table lacks a significant label,” not positive evidence against the biological hypothesis. “Refuted” is consequently too strong unless power and false-negative behavior are known.  
   **Severity:** **MAJOR**  
   **What would rebut me:** Evidence that the negative verdicts predict genuinely false hypotheses with controlled error, outperform absence-of-significance and simple QC rules, and remain discriminative on an external dataset with known negatives.  
   **Search to confirm:**  
   - `"failed perturbation" untested not negative CRISPR screen quality control`  
   - `"CRISPR screen" knockdown efficiency false negative quality control`  
   - `"Perturb-seq" quality control failed knockdown interpretation`  
   - `"selective classification" abstention biomedical experiments`  
   - `"absence of significance" evidence against hypothesis gene set enrichment`

7. **Target:** Overall contribution; M1, M6, M7, M10  
   **The attack:** This reads as an engineered demo dressed as a methods paper. It has one substrate, one cell type, one program, one flagship, no prospective experiment, no external biological replication, no method benchmark, and no decision-quality evaluation. Considerable space is spent on browser automation, model roles, costs, cache behavior, byte identity, and an adversarial agent “lab.” Those establish software execution and arithmetic reproducibility, not scientific validity. The five-agent replication is especially easy to overread: multiple models reprocessing the same tables cannot create independent biological evidence. A Frontiers/bioinformatics referee could reasonably say the manuscript demonstrates a workflow but does not validate a general method or establish a biological finding.  
   **Severity:** **FATAL** for a full research article; potentially salvageable as a resource, workflow, or proof-of-concept article  
   **What would rebut me:** Application to multiple independent substrates/programs, baseline comparisons, external validation, and at least one prospective or genuinely independent retrospective success.  
   **Search to confirm:**  
   - `site:frontiersin.org bioinformatics methods paper validation external dataset benchmark requirements`  
   - `site:frontiersin.org "Frontiers in Research Metrics and Analytics" article types methods validation`  
   - `site:frontiersin.org "Research Metrics and Analytics" literature based discovery`  
   - `"bioinformatics methods" reviewers benchmark external validation novel method`

8. **Target:** M6, M7  
   **The attack:** The reproducibility claims are weaker than their prominence suggests. Full-scale “native reproduction” reused cached external responses, so it tested deterministic replay, not reproducibility of the original data-acquisition process. The live run was a different 12-gene exercise and did not recover NAB2. The headless driver targets an undocumented interface and is admitted to be unstable. Byte-for-byte equality of deterministic outputs from identical inputs is expected, not an empirical contribution. Cross-model clean-room recalculation is useful error checking, but it validates arithmetic—not novelty, prioritization performance, or biology.  
   **Severity:** **MAJOR**  
   **What would rebut me:** A fresh third-party rerun from public source acquisition through final ranking, using frozen query dates/versions and no private cache or unstable UI, that recovers the reported results under a documented executable protocol.  
   **Search to confirm:**  
   - `"agentic science" reproducibility provenance workflow`  
   - `"LLM agent" reproducible scientific workflow cached API responses`  
   - `"AI scientist" reproducibility independent replication`  
   - `"browser automation" scientific workflow reproducibility`

9. **Target:** M8, M9; the 22,039 → 30 funnel  
   **The attack:** The funnel is partly circular. The universe is selected using knockdown, effect, and Th1/Th2 evidence, after which the referee rereads those same signals. Consequently, two or three “receipts” are eligibility conditions masquerading as independent corroborating hops. The program hop cannot refute anyone inside the funnel. The ultimate 30 survivors reflect a literature gate conjoined with a sparse disease-enrichment table; they are not 30 independently validated chains. “Disease-answer-free” avoids direct label leakage but does not remove selection bias or double use of evidence.  
   **Severity:** **MAJOR**  
   **What would rebut me:** A genuinely held-out adjudication design in which candidate generation does not use the perturbational features later counted as receipts, plus a comparison showing performance beyond selection-induced enrichment.  
   **Search to confirm:**  
   - `"double dipping" feature selection validation same data biomarker discovery`  
   - `"selection bias" hypothesis generation validation same dataset`  
   - `"circular analysis" genomics candidate selection evaluation`  
   - `"data leakage" biological discovery pipeline feature selection held out validation`

10. **Target:** B3, B4  
    **The attack:** The STAT6 analysis rules out only one narrow artifact: a detectable steady-state expression decrease in STAT6 under NAB2 CRISPRi at the measured condition. It does not rule out altered STAT6 isoforms, chromatin regulation, transcriptional interference not visible at gene-level abundance, guide-specific enhancer effects, downstream STAT6 activity, or shared cis-regulatory architecture. “The signal is NAB2-specific” therefore exceeds the test. Likewise, STAT6 being absent from two genome-wide modules does not demonstrate that their disease labels are locus-independent; module enrichment and locus attribution are different inferential layers.  
    **Severity:** **MAJOR** for the claim of NAB2 specificity; **MINOR** if rewritten as a narrowly negative expression result  
    **What would rebut me:** Orthogonal NAB2 perturbations, rescue, guide-level concordance away from shared regulatory elements, direct STAT6 activity measurements, and locus-resolved chromatin/variant evidence.  
    **Search to confirm:**  
    - `"CRISPRi" cis spreading neighboring gene 43 kb promoter`  
    - `"CRISPR interference" bidirectional promoter neighboring gene off-target cis effects`  
    - `"NAB2 STAT6" overlapping 3' ends regulatory`  
    - `"NAB2 STAT6" chromatin interaction enhancer`  
    - `"CRISPRi" transcriptional interference gene-level RNA unchanged`

11. **Target:** B6, B7  
    **The attack:** Lower NAB2 expression in lesional skin does not rescue the disease mechanism. Lesional-versus-nonlesional expression is vulnerable to treatment, inflammation severity, activation state, sampling site, pseudoreplication, and cell-state composition within broad “T/NK” or keratinocyte bins. Even a genuine decrease cannot distinguish cause, compensation, or consequence. The paper explicitly lacks the sign of the Th2 change after NAB2 knockdown, yet advances a “Th2 brake” and restoration experiment. That direction is underdetermined by its own evidence and risks turning an association into a therapeutic narrative.  
    **Severity:** **MAJOR** for B7; **MINOR** for the descriptive B6 result  
    **What would rebut me:** Replication across independent cohorts with donor-level statistics, a clear perturbational direction on canonical Th2 outputs, and NAB2 restoration reducing those outputs in primary CD4 T cells.  
    **Search to confirm:**  
    - `"NAB2" lesional atopic dermatitis transcriptome`  
    - `"NAB2" atopic dermatitis single cell RNA-seq`  
    - `"NAB2" eczema skin expression`  
    - `"NAB2" keratinocyte inflammation`  
    - `"NAB2" Th2 brake`  
    - `"NAB2 overexpression" IL4 GATA3 T cells`

12. **Target:** M5; overall framing  
    **The attack:** The actor–critic language audit is good editorial practice, not a scientific result. Catching “validated” and “definitive” demonstrates that the first model overstated the evidence and a second model corrected two words. It does not establish the reliability of model judgment, especially within one model family and without blinded human adjudication or measured error rates. Giving this episode manuscript-level prominence makes the work look optimized for a hackathon narrative rather than a durable scientific contribution.  
    **Severity:** **MINOR** alone; **MAJOR** as a claimed contribution  
    **What would rebut me:** A systematic evaluation showing that the critic materially improves factual calibration across many cases relative to single-model and human-review baselines.  
    **Search to confirm:**  
    - `"LLM as judge" scientific writing calibration factuality critic`  
    - `"actor critic" biomedical scientific hypothesis verification language model`  
    - `"self critique" language model scientific claims calibration`  
    - `"multi-agent" biomedical claim verification factual accuracy`

**BOTTOM LINE:** **Do not publish in its present form.** The paper contains a competent, unusually candid proof of concept, and one thing survives the attack: deterministic per-hop receipts plus explicit handling of failed perturbations is a sensible workflow design worth releasing. But sensible design is not yet a validated method, and NAB2–eczema is not yet a defensible biological contribution. For a Frontiers-family research article, the combination of no decision-quality benchmark, n=1 deep analysis, same-substrate circularity, and unresolved 12q13 attribution falls below the bar. The single most important live-literature task is to determine whether variant-level studies, eQTL/TWAS work, or earlier functional literature already assign the 12q13 atopy signal to NAB2 versus STAT6. If NAB2 is already implicated, novelty collapses; if STAT6 owns the signal, the flagship collapses; only credible NAB2-specific locus evidence would preserve the biological headline.
