# 2. Background

> **DRAFT v1 — for CS actor–critic review.** Dual-teach Background (LBD/informatics readers + bench
> scientists). Honors the outline v1.2 framing: approach-not-product; two receipt classes; self-audit =
> role/model/checkpoint independence; calibrated language. ~1,050 words. Citations are placeholders in
> [author year] form pending the citation resolver.

---

## 2.1 The follow-up problem in literature-based discovery

Literature-based discovery formalizes a simple observation: two facts can each be established in the
literature while the conclusion that joins them has never been written down. Swanson's original
formulation connects an entity **A** to an intermediate concept **B**, and **B** to an outcome **C**,
where the **A–C** link is absent [Swanson 1986]. In *open* discovery one fixes **A** and searches for
reachable **C**; in *closed* discovery one fixes both **A** and **C** and asks whether a plausible **B**
bridges them. Four decades of work have refined how the intermediate terms are linked, filtered, and
ranked, and have applied the paradigm across biomedicine — including our own use of an ABC pipeline to
connect a plasma-metabolite signal to a druggable target in cardiac arrest [Henry et al. 2021].

The paradigm's persistent weakness is not generation but *triage*. An ABC search over a large corpus
returns thousands of candidate links, and the ranking signals available to classical LBD are properties
of the literature — how rare a co-mention is, how strong an intermediate association looks. Rarity in the
literature, however, tracks *obscurity* at least as strongly as it tracks *importance*: a gene can look
novel simply because no one has studied it. The result is a long ranked list that no laboratory can work
through, and the field has said so of itself. Reviewing a proposal to extend this line of work, three
reviewers named the problem directly — LBD *"generates an enormous number of hypotheses, almost none of
which ever get followed up"* (NIH 1R01LM015392-01). Standard evaluations of LBD (time-slicing, link
prediction) measure whether the generator would have *rediscovered* known links, not whether a specific
proposed hypothesis is *true in fresh experimental data* [cf. Henry et al. 2021, who forwent statistical
evaluation on these grounds]. What has been missing is an adjudication step: a way to put each
machine-generated hypothesis to a data test and record a verdict — including a *no*.

## 2.2 A held experimental substrate, and what counts as a receipt at each hop

The adjudication step needs data that exists independently of the hypotheses being posed. We use a
genome-scale CRISPRi Perturb-seq resource in primary human CD4+ T cells [Zhu, Dann, Yan, … Marson 2025],
in which thousands of genes are individually knocked down and single-cell RNA sequencing reads out the
transcriptional consequence of each perturbation across stimulation conditions. Because the measurements
were made before — and without reference to — any triple we test, they function as a *held substrate*: the
referee queries them retrospectively rather than commissioning new experiments. The analysis is
CPU-feasible because it runs over the study's aggregated supplementary tables — per-guide knockdown
efficiency, differential-expression statistics, a Th1/Th2 polarization signature, and a
cluster-to-autoimmune-disease enrichment — rather than the raw multi-million-cell matrices.

Crucially, the four tables do not all supply the same *kind* of evidence, and we keep the distinction
explicit throughout. The first three hops — did the knockdown work, did the perturbation produce a real
transcriptional effect, did that effect shift the T-cell program — are backed by **experimental
receipts**: direct measurements from the perturbation data. The fourth hop — does the perturbed gene's
downstream signature enrich for a disease — is an **association receipt**: the disease labels derive from
genetic evidence (GWAS and related association data, without colocalization or linkage-disequilibrium
control), so a positive verdict at this hop is a *nomination*, not a claim of experimental disease
causality. Reading the substrate as an experimental oracle for the first three hops but an association
signal for the fourth is what keeps the eventual claims calibrated.

## 2.3 Agentic language models as a scientific instrument

The generation, adjudication, and provenance in this work were carried out inside an *agentic* language-
model environment, and because that setting is newer to the discovery-informatics reader than the biology
or the LBD, we describe what it does and — more importantly — what discipline makes it trustworthy for
science. Contemporary language models can be given *tools*: they can call code, query a web API, or read a
file, and act on the returned values rather than on their own recollection. They can also be composed into
an *actor–critic* configuration, in which one model performs an analysis and a second, independent model
reviews it.

Two design commitments make this usable as an instrument rather than a source of confident narration.
First, we separate deterministic *lookups* from *judgment*. Every data receipt in Wayfinder — a knockdown
efficiency, an effect size, an enrichment odds ratio — is produced by deterministic code, reproducible and
free of model discretion; the language model *interprets* receipts and assembles the verdict, but it never
asserts a biological fact that a table value does not support. Visible agency is reserved for judgment, not
for data retrieval. Second, the work runs on a scientific workbench — Claude Science, a persistent-kernel
environment — in which an author model and an independent reviewer model operate at separate checkpoints:
the reviewer verifies each reported number against the underlying artifacts and enforces calibrated
language on the output, and in this work it flagged and removed overstated words (for example "validated"
and "definitive") from the platform's own text. We are precise about what this independence is and is not:
it is *role, model, and checkpoint* independence — a distinct reviewer model at distinct verification
points — within a single model family, not cross-vendor independence. Independence across model families
is provided separately and externally (Section 4.6), by replicating the finding with a different vendor's
models. With that boundary stated, the agentic workbench lets a single researcher run generation,
data-grounded adjudication, and a self-audit of the result's language on one bench — the capability the
rest of this paper puts to work.
