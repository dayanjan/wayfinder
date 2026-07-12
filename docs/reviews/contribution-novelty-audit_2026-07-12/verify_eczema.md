# V-ECZEMA — literature-novelty audit of B2–B5 (NAB2 ↔ atopic eczema / 12q13 / STAT6 cis)

**Verifier:** V-ECZEMA (highest-risk biology family). **Date:** 2026-07-12.
**Method:** live `search_all` over Europe PMC / OpenAlex-class index; 18 queries, abstracts pulled
for the decisive papers. Read-only. Cannot prove a negative — reports queries + findings.

**Decisive question (operator):** *Is NAB2 already a named 12q13 AD candidate gene?*
**Answer: No.** Across every dedicated AD candidate-causal-gene prioritization paper surfaced
(Sobczyk/Paternoster JID 2021; Multi-Tissue TWAS JID 2022; Budu-Aggrey Nat Commun 2023; the 2025
multi-ancestry keratinocyte-integration GWAS), the **named/prioritized 12q13 gene is STAT6** — NAB2
is **never** surfaced as a prioritized or named AD/asthma/allergy candidate. NAB2's *physical
residence* inside the 12q13 atopy locus is fully known (it is a "known locus passenger"); its
*nomination as an AD gene* is not in the literature. Caveat: abstracts, not full supplementary
locus tables, were read — I cannot exclude NAB2 appearing as a "gene-in-region" row in some
supplement; but it is not a *named candidate* in any prioritization result.

---

## B2 — "NAB2 → atopic eczema" as a literature-novel disease nomination
### VERDICT: PARTIALLY-ANTICIPATED (appropriately scoped; NOT overstated *as written*)

**Why not NOT-NOVEL:** No paper nominates NAB2 as an AD candidate gene. The three canonical AD
gene-prioritization efforts name other genes at their single-candidate loci
(IL6R, ADO, PRR5L, IL7R, ETS1, INPP5D, MDM1, TRAF3; novel alternates SLC22A5, IL2RA, DEXI, STMN3 —
**no NAB2**; Sobczyk JID 2021). The Multi-Tissue TWAS (JID 2022) causal set is FLG, AQP3, PDCD1,
ADCY3, DOLPP1 — **no NAB2**. So a *gene-level* NAB2 nomination is genuinely absent from the
surfaced literature.

**Why not fully NOVEL (the threat is real):** NAB2 sits *inside* the well-known **12q13 atopy
locus**, immediately adjacent to STAT6 — a famous, repeatedly-replicated AD/atopy GWAS locus
(Paternoster 2015 ng.3424; Budu-Aggrey 2023 s41467-023-41180-2; 1999 12q13 linkage 10.1016/s0091-6749(99)70398-2).
The manuscript's disease hop is an **Open Targets GWAS-based label with no colocalization**, so the
NAB2→eczema *disease* signal is LD-plausibly the neighboring STAT6 signal re-labeled onto its
passenger neighbor. The **disease-label novelty is therefore thin**; the durable novelty is the
*Th2 regulatory receipt* for NAB2 (that is B1's territory), not a new eczema locus.

**Not overstated — because the manuscript foregrounds exactly this.** §4.3/§4.4b explicitly call
the eczema link "a genetic-association nomination (an Open Targets GWAS-based disease label, without
colocalization or LD control), not an expression claim or a proof of disease causality," state NAB2
"lies within the 12q13 atopic-dermatitis susceptibility locus, immediately adjacent to STAT6," and
label the verdict "a receipt-backed regulatory nomination with an unresolved disease-label
provenance." That scoping is accurate. **The §4.4b caveat is load-bearing:** if the abstract phrases
B2 as a bare "novel NAB2–eczema link" *without* the 12q13/LD caveat, it WOULD be OVERSTATED — a
cross-checker should confirm the abstract carries the hedge (I audited §4.3/§4.4/§4.4b only).

**Moves science forward?** Weakly as a *disease* discovery (it re-labels a known atopy locus); the
value is the honest confounder framing + the gene-level Th2 nomination, not a novel eczema gene.

## B3 — STAT6 cis-effect "ruled out at the expression level" + "~43 kb makes cis-spread unlikely"
### VERDICT: NOVEL (re-analysis) · geometric "43 kb is safe" argument PARTIALLY-SUPPORTED by lit

**(a) No prior NAB2-KD→STAT6 report.** The entire NAB2↔STAT6 literature is the **Solitary Fibrous
Tumor NAB2-STAT6 fusion oncogene** (dozens of hits: modpathol 2013 10.1038/modpathol.2013.164;
gcc 2013 10.1002/gcc.22083; etc.) — a genomic fusion, unrelated to a CRISPRi cis-repression readout
in CD4⁺ T cells. No paper reports NAB2 knockdown moving/not-moving STAT6. The re-analysis result is
novel and uncontradicted.

**(b) Does the CRISPRi-spread literature support "43 kb is safe"? Partially — and honestly hedged.**
- CRISPRi direct repression is sharply **TSS-proximal** and chromatin-accessibility-dependent
  (Gao/Radhakrishnan NAR 2016 gkw583: efficiency "relies heavily on precise recruitment to the TSS";
  proximity to CAGE-TSS predicts function) — supports that on-target repression is focused at the
  guide's own TSS.
- **Lensch et al. 2022 (eLife 75115)** — the manuscript's cited spreading reference — is a
  **double-edged** support: KRAB silencing DOES spread to a neighboring gene "within hours, with a
  time delay that increases with distance," and this spreading is **NOT blocked by classical cHS4
  insulators.** So (i) spread is distance-dependent (supports the *direction* of the "43 kb → less
  likely" argument), but (ii) their tested geometries are **short-range synthetic dual-gene
  reporters (kb-scale)** — the paper does **not** establish 43 kb as a proven-safe threshold, and it
  shows KRAB spread can cross insulators to reach neighbors. "43 kb → strong promoter-directed spread
  unlikely" is a reasonable *extrapolation*, not a literature-proven safe distance.
- The manuscript does not over-rely on geometry: it calls the confounder "*a priori* weak," says
  "geometry alone is not decisive," settles it **empirically** (STAT6 log₂FC +0.087, adj-p 0.788,
  ranked 5,444/10,282; a cis-artifact would push STAT6 *down*), and scopes the claim to "one
  aggregate Stim8hr expression null … not every conceivable cis channel." That structure is sound
  and **not overstated.**

**Moves science forward?** Yes, methodologically — a clean, deposited-data cis-artifact
falsification is a reusable template for CRISPRi/Perturb-seq neighbor-confounders.

## B4 — clusters 90/100 are genome-wide functional immune modules (STAT6 absent), not a 12q13 artifact
### VERDICT: UNVERIFIABLE-BY-LIT (dataset-specific; not contradicted)

This is a property of the internal Perturb-seq enrichment substrate (module membership of
BACH2/BCL6/IRF4/CD28/IL4/IL10, STAT6 absent). No external paper confirms or contradicts it — it is
not a literature claim. Reassurance is internal: the adversarial replication lab (§4.6) caught the
74/90→90/100 cluster-ID mislabel and re-ran the locus test, which strengthens confidence in
correctness. No lit contradiction found. Verify computationally, not by literature.

## B5 — the 12q13 LD-inheritance confounder is foregrounded, not discharged
### VERDICT: ADEQUATE / well-calibrated (literature makes the confounder MORE serious, as claimed)

The hedge is not just adequate — the literature actively *validates* keeping it open:
- **Neighboring-gene co-regulation defeats eQTL/coloc gene-assignment** (Mostafavi/… xhgg 2024
  10.1016/j.xhgg.2024.100348): even best colocalization methods have low precision; "assigning
  fine-mapped pQTLs to their closest protein-coding gene outperformed all colocalization methods,"
  and "prioritizing novel targets requires triangulation from multiple sources." NAB2/STAT6 are
  exactly the adjacent-gene case this warns about.
- Every AD prioritization paper names **STAT6** (not NAB2) as the 12q13 gene — so the manuscript's
  "lead signal … plausibly STAT6's" is well-grounded.

The manuscript correctly (i) separates the three locus artifacts (cis-effect / cluster-membership /
LD-label), (ii) rules out the two its data can address, and (iii) explicitly leaves the
LD-inherited-label one open, noting even variant-level coloc "presupposes a detectable NAB2 cis-eQTL
in CD4⁺ T cells." This is honest, appropriately un-triumphant, and consistent with the calibrated-
language discipline the paper argues for. **Moves science forward?** Yes — as a model of a nomination
stated with its provenance boundary intact.

---

## Retrieved evidence appendix (load-bearing papers for a Phase-D cross-checker)

### NAB2 is NOT a named AD candidate — the prioritization literature (decisive for B2)
- **Sobczyk, …, Paternoster. "Triangulating Molecular Evidence to Prioritize Candidate Causal Genes
  at Established Atopic Dermatitis Loci."** JID 2021, DOI 10.1016/j.jid.2021.03.027 (preprint
  10.1101/2020.11.30.20240838). *25 reproducible AD loci; ADGAPP pipeline over 103 QTL/functional
  resources. Single-candidate loci: IL6R, ADO, PRR5L, IL7R, ETS1, INPP5D, MDM1, TRAF3; two-candidate:
  IL18R1/IL18RAP, LRRC32/EMSY; novel alternates: SLC22A5, IL2RA, MDM1, DEXI, ADO, STMN3.* **NAB2
  absent; STAT6 not among single candidates.**
- **"Multi-Tissue Integrative Analysis Identifies Susceptibility Genes for Atopic Dermatitis."** JID
  2022, DOI 10.1016/j.jid.2022.09.006. *TWAS (JTI) + MR, ~840k Europeans; 51 assoc / 19 causal genes
  incl. FLG, AQP3, PDCD1, ADCY3, DOLPP1.* **NAB2 absent.**
- **Budu-Aggrey, … "European and multi-ancestry GWAS meta-analysis of atopic dermatitis…"** Nat
  Commun 2023, DOI 10.1038/s41467-023-41180-2. *Largest AD GWAS; 81 European + 15 multi-ancestry
  loci; per-locus candidate-gene prioritization by multi-omic integration.* Abstract names no NAB2.
- **"Integration of GWAS, QTLs and keratinocyte functional assays reveals molecular mechanisms of
  atopic dermatitis."** Nat Commun 2025, DOI 10.1038/s41467-025-58310-7. *Multi-ancestry, 101 loci,
  fine-mapping + QTL coloc + keratinocyte assays.* Abstract names no NAB2.

### The 12q13 atopy locus = a STAT6 locus (known; frames B2's LD threat and B5)
- **Paternoster, … "Multi-ethnic GWAS … identifies new risk loci for atopic dermatitis."** Nat Genet
  2015, DOI 10.1038/ng.3424. *31 AD loci; 12q13/STAT6 is an established atopy locus.*
- **1999, "Dense mapping of chromosome 12q13.12-q23.3 and linkage to asthma and atopy,"**
  DOI 10.1016/s0091-6749(99)70398-2 (and 2000 10.1046/j.1365-2222.2000.00954.x, "linkage and
  association of atopy with 12q13–24"). *12q13 is a long-standing atopy linkage/association region.*
- STAT6 IgE/atopy variant literature (jmg 2004 10.1136/jmg.2004.020263; jaci 2005
  10.1016/j.jaci.2004.10.006) — STAT6 is the atopy-driver at this locus.

### NAB2↔STAT6 literature is the SFT fusion oncogene, NOT a T-cell cis relationship (B3a)
- STAT6 nuclear-expression / NAB2-STAT6 fusion in Solitary Fibrous Tumor: modpathol 2013
  10.1038/modpathol.2013.164; gcc 2013 10.1002/gcc.22083; ajpath 2014 10.1016/j.ajpath.2013.12.016.
  *Fusion oncology; no NAB2-KD→STAT6 cis-repression report exists.*

### CRISPRi cis-spread literature (B3b — "is 43 kb safe?")
- **Lensch, …, Bintu. "Dynamic spreading of chromatin-mediated gene silencing and reactivation
  between neighboring genes in single cells."** eLife 2022, DOI 10.7554/elife.75115 (preprint
  10.1101/2021.11.04.467237). *KRAB silencing spreads between neighboring genes within hours; time
  delay increases with distance; NOT blocked by classical cHS4 insulators. Synthetic dual-gene
  reporters (kb-scale) — does not test 43 kb.* **Supports promoter-proximal/distance-decaying spread
  but does NOT establish 43 kb as safe; shows spread crosses insulators.**
- **Gao et al. "Optimizing sgRNA position markedly improves … dCas9-mediated transcriptional
  repression."** NAR 2016, DOI 10.1093/nar/gkw583. *CRISPRi efficacy is TSS-proximal, CAGE-TSS-
  and open-chromatin-dependent.* Supports that on-target repression is focused at the guide's TSS.
- **"Bidirectional promoter activity … off-target repression of neighboring gene."** eLife 2022,
  DOI 10.7554/elife.81086. *Neighboring-gene-effect mechanism (cassette/promoter divergent
  transcript); relevant to residual 3′ read-through channel the manuscript names.*
- **"Seed sequences mediate off-target activity in the CRISPR-interference system,"** Cell Genomics
  2024, DOI 10.1016/j.xgen.2024.100693; **"Systematic identification of seed-driven off-target
  effects in Perturb-seq,"** 2026. *CRISPRi off-target is largely sequence/seed-driven (trans), a
  distinct channel from distance-based cis-spread — orthogonal caveat, not addressed by B3.*

### Neighboring-gene assignment is hard (B5 adequacy)
- **"Extensive co-regulation of neighboring genes complicates the use of eQTLs in target gene
  prioritization."** HGG Advances 2024, DOI 10.1016/j.xhgg.2024.100348. *Colocalization methods have
  poor precision; nearest-gene beats coloc; novel-target prioritization needs multi-source
  triangulation.* **Directly validates the manuscript's decision to leave the NAB2-vs-STAT6 LD-label
  question open.**

---

## Query log (18)
NAB2 atopic dermatitis · NAB2 eczema · NAB2 atopy · NAB2 12q13 · Paternoster AD GWAS 12q13 ·
12q13 AD GWAS candidate genes STAT6 · AD susceptibility locus 12q13 genes · Triangulating candidate
causal genes AD loci · Multi-Tissue TWAS AD · Paternoster 2015 multi-ethnic AD GWAS · European
multi-ancestry AD GWAS · co-regulation neighboring genes eQTL · NAB2 STAT6 AD locus candidate ·
AD eQTL 12q13 STAT6 NAB2 CD4 · STAT6 AD GWAS neighboring genes fine-mapping · CRISPRi dCas9 KRAB
spreading distance · CRISPRi off-target adjacent gene · dCas9 KRAB heterochromatin spreading range ·
Dynamic spreading neighboring genes (Lensch) · Optimizing sgRNA position CRISPRi · Bidirectional
promoter off-target · NAB2 asthma allergic 12q13 · NAB2 Th2 regulator · GWAS QTL keratinocyte AD.
(Result: NAB2 never surfaced as a named AD/asthma/allergy candidate gene in any query.)
