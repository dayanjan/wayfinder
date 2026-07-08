# Independent source-paper read — NAB2 → Th1/Th2 → atopic-eczema hypothesis

**Reader role:** independent scientist reading the *original* Zhu et al. 2025 CD4+ Perturb-seq preprint, assessing the team's downstream NAB2→eczema hypothesis against what the paper itself says and did.
**Paper read:** full text (63 pages) extracted from the PDF; every claim below is cited to a page and, where possible, quoted verbatim.

---

## BOTTOM LINE

**The paper's methods and findings WEAKEN — or at minimum fail to support — the *causal* NAB2→atopic-eczema reading, and they leave the STAT6 confounder wide open and unaddressed.** Three facts drive this: (1) the paper's disease-enrichment attributes a gene to "atopic eczema" using **Open Targets genetic-association evidence (GWAS + gene-burden + ClinVar), not co-expression** — a locus/position-based label that is exactly the kind of signal a 12q13 LD block (STAT6's neighborhood) can manufacture (p50); (2) **the paper never mentions NAB2 at all** — zero occurrences — so the NAB2→eczema link is entirely the team's own supplementary-table mining, not a paper claim; and (3) the paper itself frames all module-disease enrichment as **hypothesis-generating / candidate-nomination**, never causal, and its Limitations section contains **no colocalization, fine-mapping, or LD/neighboring-gene control** (p25–26, p30).

Two nuances keep this from being fatal, and the team should hold both: (a) the *module→eczema* enrichment can still be genuine biology if the Th2 module aggregates multiple **independent** atopic loci (STAT6 on 12q, IL13/IL4 on 5q31, IL4R on 16p, GATA3 on 10p) rather than being carried by 12q13 alone — the paper's Fisher-on-clusters method is sound at that level; (b) the specific threat of the STAT6 shadow lands hardest on the **NAB2→module direction** (is NAB2 a real trans-regulator, or is a CRISPRi guide 1.9 kb from STAT6 reading out a *cis* effect on STAT6?), which is precisely a knockdown-QC / cis-artifact question — the project's hero feature. Calibrated verdict the team should carry forward: **"untested / flagged — STAT6 genomic shadow not excluded,"** not "consistent with a novel NAB2→eczema link."

---

## Q1 — How was the disease-cluster enrichment computed? (the load-bearing question)

**Answer: a hybrid — functionally-defined co-regulation clusters tested against GWAS/genetic-evidence-defined disease-gene sets. The disease *membership* of any gene is genomic/GWAS-based, NOT co-expression-based.** This does not resolve the STAT6 confounder; it inherits it.

Verbatim method (p50, "Analysis of effects of autoimmunity GWAS genes"):

> "We queried the OpenTargets Platform API (v4) to retrieve genes with genetic association with autoimmune diseases (rheumatoid arthritis, systemic lupus erythematosus, inflammatory bowel disease, multiple sclerosis, type 1 diabetes, psoriasis, ankylosing spondylitis, **asthma**, Hashimoto's thyroiditis, celiac disease, and **atopic eczema**) and non-autoimmune control diseases (coronary artery disease, macular degeneration, and chronic kidney disease). We included genes with a minimum genetic evidence score of 0.1 … **derived from GWAS associations, gene burden studies, and somatic mutation data, which includes evidence from ClinVar**."

> "We then performed **Fisher's exact tests** to assess enrichment of disease-associated genes in two gene sets for each condition: (a) cluster regulators and (b) condition-specific downstream target genes… we excluded clusters containing fewer than five unique regulators."

Figure 7's legend confirms the label: *"Enrichment of **GWAS-evidence genes** (Open Targets) for autoimmune and control diseases…"* and *"-log10(FDR) of the **fisher exact test** for enrichment in GWAS-evidence genes"* (p26).

**What this means for the STAT6 confounder.** The two ingredients have different provenance:
- **The clusters** = functional co-regulation: genes grouped by correlated *perturbation effects* (HDBSCAN on perturbation-effect correlations; Suppl. Table 9). This part is genuine co-regulation, not position.
- **The disease label on each gene** = Open Targets **genetic evidence ≥ 0.1**, which is GWAS locus-to-gene (plus burden/ClinVar). Whether a gene "is an atopic-eczema gene" is therefore a **genomic-position/association** call. Open Targets distributes genetic-association credit across genes near a GWAS locus; a gene ~1.9 kb from the true causal gene at a shared/LD locus (NAB2 next to STAT6 at 12q13.3) can pick up an atopic-eczema evidence score that is really the STAT6-locus signal. The paper does **no** colocalization or fine-mapping to break this (confirmed: "colocali", "coloc", "fine-map", "linkage disequilibrium", "nearby gene" all appear **0 times** in the full text).

So the honest reading of Q1: the enrichment machinery is real and the clusters are functional, **but the atopic-eczema attribution is exactly a GWAS-locus label**, and the paper provides no mechanism that would distinguish a genuine NAB2/Th2→eczema co-regulation signal from the 12q13/STAT6 genomic shadow. **This weakens the causal claim.**

(For completeness, note a *separate, non-disease* enrichment the paper also runs — cluster *function* annotation via CORUM/STRING/KEGG/Reactome hypergeometric tests, p43. That is functional, but it is not how disease is attributed. Disease attribution is the Open Targets/GWAS route above.)

---

## Q2 — Does the paper mention NAB2?

**No. NAB2 appears zero times in the entire 63-page text** (title, abstract, results, methods, figures, references). The paper's own top Th2 regulators are **IL4R, STAT6, GATA3, RARA**, plus the novel hit **FBXO32** (p16) — NAB2 is not among them, not in any figure, not in any vignette. The NAB2→Th1/Th2→eczema link is **entirely the team's own finding** from the deposited supplementary tables; it is not a claim, hit, or even a footnote in the source paper.

---

## Q3 — Does the paper discuss atopic dermatitis / eczema / STAT6 / Th2, and does it name gene hits?

- **"eczema" / "atopic":** each appears **exactly once**, both on **p50**, only inside the Open Targets disease-query list ("…asthma, Hashimoto's thyroiditis, celiac disease, and atopic eczema"). **"dermatitis" appears 0 times.** The paper **never names a specific gene hit for atopic eczema/dermatitis** — eczema is one of 11 disease sets fed to the enrichment, never discussed on its own, never tied to a named gene.
- **STAT6:** discussed only as a **canonical/master Th2 regulator** — *"Top Th2 regulators included: IL4R; STAT6 (a transcription factor activated by IL4R signaling) and GATA3 (a master transcription factor induced by STAT6)"* (p16); also as a SUMOylation substrate (p20) and in a reference (p54). **STAT6 is never discussed in a disease/eczema context** in this paper.
- **Th2:** heavily discussed (Figure 4, p14–18). Named Th2 regulators/hits: **IL4R, STAT6, GATA3, RARA** (known) and **FBXO32** (novel), with markers **GATA3, CCR4, IL13** up in Th2 vs **IFNG, EOMES, TBX21** up in Th1 (p15).
- The paper explicitly notes some Th2-model regulators are tied to allergy-adjacent genetics only loosely: *"CDKAL1 … and PAN2, have been implicated in autoimmune disease pathogenesis … or associated with eosinophil counts, a Th2-dependent phenotype"* (p16) — i.e., the closest the paper comes to an allergy phenotype is eosinophil counts, not eczema, and not via NAB2.

---

## Q4 — How was the Th1/Th2 signature derived (the T2 table)? Any caveat on the two reference contrasts?

The Th2/Th1 signature is derived from **published bulk RNA-seq of FACS-sorted human Th1 and Th2 cells**, from two references, then reconstructed from perturbation effects (p15):

> "We derived a Th2/Th1 signature from published bulk RNA-seq data of Th1 and Th2 cells FACS-sorted from human donors (Figure 4B) [39,40], and verified the signature's robustness across independent cohorts (Suppl. Figure 16A)."

The two reference contrasts, verbatim from the reference list:
- **[39] = Ota M, Nagafuchi Y, Hatano H, … *Cell*. 2021;184:3006–3021** ("Dynamic landscape of immune cell-specific gene regulation in immune-mediated diseases") — the **"Ota 2021"** contrast (discovery cohort).
- **[40] = Höllbacher B, Duhen T, Motley S, … *ImmunoHorizons*. 2020;4:585–596** ("Transcriptomic profiling of human effector and regulatory T cell subsets…") — the replication cohort.

**Citation-hygiene flag for the team:** your label "Hollbacker 2021" is slightly wrong on both axes — the author is **Höllbacher** (with the umlaut/second "h"), and the year is **2020**, not 2021 (*ImmunoHorizons* 2020). Worth fixing wherever it appears in receipts/UI.

**Caveats the paper itself raises around this signature:**
- **Modest reconstruction accuracy:** mean cross-validation R = **0.39** (discovery) and **0.27** (independent validation cohort) (p15). Real signal (beats K562 and scrambled controls), but not high.
- **Two regulators came out backwards:** *"We found only 2 regulators whose inferred direction was opposite expectations: TRAF3 … and IL4"* (p16) — attributed to context-specificity and paracrine dampening of cytokine knockdowns.
- **Subtle single-cell effects:** *"The subtle magnitude of these shifts likely reflects that full polarization requires the coordinated action of multiple regulators, in concert with external signal input"* (p18).
- **Not measured in polarizing conditions:** the cells were **not cultured in Th1/Th2-polarizing conditions** — *"The population of perturbed CD4+ T cells was not cultured in polarizing conditions"* (p18); the Limitations reiterate *"the regulatory rewiring driven by polarizing cytokines … remains unmapped"* (p30). So the Th2 signature is *inferred/reconstructed*, not observed under polarization.

---

## Q5 — Does the paper support, contradict, or contextualize NAB2→eczema? Is module-disease enrichment framed as causal, correlational, or hypothesis-generating?

**The paper is silent on NAB2 specifically (Q2), so it neither supports nor contradicts the NAB2 link directly — but it contextualizes it, and the context leans skeptical.**

- **Framing is explicitly hypothesis-generating / nomination, never causal.** The gene-trait section uses nomination language throughout: clusters "**nominate** putative immunological functions," genes are "**putative** core genes," and the summary is *"**guilt-by-perturbational association can nominate** immunological roles for disease-implicated genes with previously unknown function in T cells"* (p26). The Discussion calls the whole framework a *"**proof-of-concept**"* (p28). Even the authors treat module-disease enrichment as candidate-prioritization, not proof — so a causal NAB2→eczema claim built on the same machinery is, at best, hypothesis-level.
- **STAT6 as the obvious competing causal gene.** The paper repeatedly casts STAT6 as **the** master Th2 regulator that induces GATA3 and sits directly downstream of IL4R (p16). That a well-established Th2/atopic master gene sits 1.9 kb from NAB2 raises the prior that a 12q13 atopic-eczema genetic signal belongs to STAT6, not NAB2 — the paper gives you no reason to prefer NAB2.
- **The paper's own analogous vignettes hedge causality with orthogonal evidence.** For its highlighted novel disease-gene nominations (LRRC25, FAM20B), the authors bring **cross-guide and cross-donor reproducibility** as support (FAM20B: between-guide R=0.81, cross-donor mean R=0.50; p25–26). The team's NAB2 finding should be held to the same bar — and additionally to a *cis*-artifact check that those vignettes didn't need (because they weren't 1.9 kb from a master TF).

**Net:** the paper contextualizes NAB2→eczema as, at most, a hypothesis worth testing, and actively supplies the competing explanation (STAT6) without any tool to rule it out.

---

## Q6 — Author caveats bearing on our finding (LD, neighboring genes, module interpretation)

- **No LD / neighboring-gene / colocalization control anywhere.** The Limitations section (p30) lists: off-target guide effects (only 2 gRNAs/target), pseudobulk masking single-cell heterogeneity, non-polarized culture (Th2 rewiring unmapped), and the general need to link transcriptional effects to immune functions. It says **nothing** about GWAS locus-to-gene ambiguity, LD, or *cis*-neighbor confounding — and no such language exists in the whole paper (Q1). **The STAT6-shadow confounder is neither raised nor controlled by the authors.** That makes the team's caveat legitimate and *unaddressed by the source* — you are not overriding a control the paper ran; you are flagging a gap the paper left open.
- **Knockdown-efficiency heterogeneity is explicitly acknowledged** — *"potential heterogeneity of knock-down efficiencies (Suppl. Figure 17B)"* (p18). This is directly relevant to the project's knockdown-QC hero feature: the paper concedes KD efficiency varies, which is the failed-knockdown→*untested*-not-*negative* axis.
- **Module interpretation is deliberately loose.** Cluster function annotation leans on *"a combination of Gene Ontology analysis, **LLM lookup**, and manual literature search"* for clusters without strong database enrichment (p43) — i.e., some module annotations are themselves soft/AI-assisted, reinforcing that module-level disease claims are interpretive, not definitive.
- **The disease enrichment is at cluster granularity, and small clusters are the risk.** The method drops clusters with <5 regulators (p50), but a cluster whose eczema overlap is carried by a single 12q13 gene would still pass if the cluster is otherwise large — the Fisher test does not know that two overlapping genes (e.g. STAT6 + NAB2) are the *same locus*. This is the concrete mechanism by which the STAT6 shadow could inflate a module's atopic-eczema enrichment.

---

## How the team should calibrate (actionable)

1. **Separate the two claims.** *Module→atopic-eczema* enrichment may be genuine **if** you can show it aggregates independent loci (list the eczema-associated genes driving the overlap and their chromosomal locations; if STAT6/NAB2 at 12q13 is one of several — 5q31 IL13/IL4, 16p IL4R, 10p GATA3 — the module link survives). *NAB2→module* (NAB2 as a bona fide Th2 trans-regulator) is the fragile leg.
2. **The STAT6 shadow is specifically a *cis*-artifact question for NAB2.** A CRISPRi guide targeting NAB2's TSS 1.9 kb from STAT6 can plausibly repress STAT6 in *cis*; the paper's model masks a gene's effect on *itself* but not on its genomic neighbor. Check whether NAB2 knockdown moves STAT6 expression in the deposited DE tables — if it does, the Th2 effect is likely STAT6's, and the verdict is **flagged / untested**, not a novel link.
3. **Fix the citation:** Höllbacher **2020** (*ImmunoHorizons*), not "Hollbacker 2021."
4. **Match the paper's own bar:** it supported its novel nominations (LRRC25, FAM20B) with cross-guide + cross-donor reproducibility. Report those same statistics for NAB2 before any "consistent with" language.

---

## Formal citation (as printed on the PDF)

Zhu R, Dann E, Yan J, Reyes Retana J, Goto R, Guitche RC, Petersen LK, Ota M, Pritchard JK, Marson A. **"Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits."** *bioRxiv* 2025.12.23.696273; posted December 24, 2025. doi:10.64898/2025.12.23.696273. Preprint, not peer-reviewed; CC-BY 4.0. (Corresponding authors: R. Zhu, E. Dann, J.K. Pritchard, A. Marson.)
