# 1. Introduction

> **DRAFT v1 — for CS actor–critic review.** Honors the debate-hardened outline (`docs/manuscript/OUTLINE.md`
> v1.2): two receipt classes, ledger *demonstrates* (not proves), triage-not-replacement framing,
> role/model/checkpoint self-audit, calibrated language throughout (never "proven/definitive/validated/genuine").
> **Open voice decision:** drafted in editorial first-person plural ("we") per FRMA convention; solo author —
> switch to "I" if preferred. ~700 words. R01 quote is verbatim from the funded critique.

---

A researcher today works between two floods. On one side is the literature: more than a million new
articles appear each year, and any single mechanistic question is now spread across more papers than one
person can read. On the other side is the data: a single genome-scale screen returns effect estimates for
thousands of genes across thousands of genetic perturbations, and a lab that runs one is often left
holding a matrix of measurements with no obvious question to ask of it. The two floods share a shape —
far more has been *measured* and *written down* than has been *connected* — and the gap between them is
where discoveries wait.

Literature-based discovery (LBD) was designed to bridge exactly that gap. Since Swanson's demonstration
that fish oil and Raynaud's disease were linked by facts already in print but never joined [Swanson 1986],
LBD has framed a hypothesis as a triangle: an entity **A** relates to an intermediate program **B**, **B**
relates to an outcome **C**, yet **A** and **C** have never been connected directly. If both legs are
supported and the closing edge is missing from the literature, that missing edge is a candidate discovery.
The paradigm is now four decades old and has been applied across biomedicine, our own prior work included:
we used an ABC co-occurrence pipeline to connect a plasma-metabolite signal to a druggable target in
cardiac arrest, a link we then confirmed in vivo [Henry et al. 2021].

But LBD has a chronic, well-documented weakness, and it is worth stating in the words that named it. In
the review of a funded proposal to extend this line of work (NIH 1R01LM015392-01), three reviewers
converged on a single objection:

> *"This application has the same major problem that has plagued all LBD work: it generates an enormous
> number of hypotheses, almost none of which ever get followed up."*

They were right. LBD is a generator, and a generator with no discriminating filter overproduces: it turns
one flood into another. Classic LBD ranks candidates by properties of the *literature* — how rare a
co-mention is, how strong an intermediate link looks — but rarity in the literature tracks *obscurity* as
readily as it tracks *importance*, and a ranked list, however long, is not an answer. What has been
missing is not more generation but adjudication: a way to ask, of each machine-generated hypothesis,
*is this actually supported by data?* — and to be willing to answer **no**.

Here we describe **Wayfinder**, an approach to closing that loop. The approach pairs LBD generation with
a deterministic referee that adjudicates each proposed *gene → T-cell program → disease* triple against a
held experimental substrate — a genome-scale CRISPRi Perturb-seq resource in primary human CD4+ T cells
[Zhu, Dann, Yan, … Marson 2025] — and returns a verdict with a receipt at every hop. We instantiate the
approach in a concrete, reproducible implementation, but the contribution is the *method* — receipt-backed
adjudication of machine-generated hypotheses — and what it found, not a software product.
The receipts are of two kinds, and we keep them distinct: the knockdown, effect, and program hops are
backed by *experimental* measurements from the perturbation data; the disease hop is an *association*
receipt (genetic enrichment), a nomination rather than a claim of experimental causality.

Two features define the approach. First, the referee is willing to say a confident, receipt-backed **no**,
and it distinguishes a *refuted* hypothesis from an *untested* one: when a gene's knockdown fails quality
control, the result is reported as *untested*, never as a negative — an artifact caught rather than a false
negative recorded. Falsification, not confirmation, is the point. Second, the entire loop — generation,
adjudication, and the assembly of its own provenance — was run inside an agentic scientific workbench
(Claude Science), in which one model authored the analysis and an independent reviewer model, at separate
checkpoints, verified every number and enforced calibrated language on the output, flagging and removing
overstated words from the platform's own text. The platform checked its own work.

We demonstrate Wayfinder on the CD4+ T-cell resource, where it posed 22,039 gene→program→disease
hypotheses and a deterministic referee culled them to a small set of receipt-backed survivors. We use a
ledger of adjudicated verdicts to *demonstrate* that the referee discriminates — supporting, refuting, and
declining to test — and a negative-control panel to show the discrimination is not an artifact of the
setup. The highest-ranked near-novel survivor, a nomination that **NAB2** regulates Th1/Th2 polarization
with a genetic link to atopic eczema, serves as the worked example, including a falsification of its
sharpest confounder against the study authors' own genome-wide data. Wayfinder does not replace
experimental follow-up; it makes the prior question — *which of these thousands is worth a bench's time?*
— answerable, with a receipt.

The remainder of this paper is organized as follows. Section 2 provides background on the LBD follow-up
problem, the Perturb-seq substrate, and agentic language models for scientific work. Section 3 details the
generator, the referee, and the workbench. Section 4 reports the verdict ledger, the confident-no and
quality-control behavior, the NAB2 worked example and its confounder falsification, the native
reproduction and self-audit, and an independent cross-model replication. Section 5 discusses what the
agentic loop changes, the next experiment it nominates, and the study's limitations.
