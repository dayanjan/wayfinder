# NAB2 — cumulative knowledge synthesis + novelty audit of our finding

Independent 4-agent literature audit (2026-07-08), grounded in a 155-paper NAB2 corpus
(Europe PMC + OpenAlex + Semantic Scholar via `src/arbiter/lit/`) plus targeted follow-up
searches, then cross-checked against our own Perturb-seq data. Purpose: honestly calibrate
the "near-novel" claim for **NAB2 → Th1/Th2 → atopic eczema**.

## Bottom line
Our finding is **more genuinely novel than the ac_lit=6 count suggested — literally zero papers
directly link NAB2 to Th1/Th2 polarization OR to atopic eczema** — and the audit *strengthens*
the project by surfacing exactly the two skeptical caveats a good referee must flag:

1. **STAT6-adjacency confounder (disease hop).** NAB2 sits **~1.9 kb from STAT6** on 12q13.3 —
   STAT6 being *the* master Th2 / atopic-dermatitis / IgE transcription factor. Every 12q13 atopy
   GWAS signal in the literature resolves to STAT6, never NAB2. So NAB2's atopic-eczema link could
   be STAT6's shadow via shared regulation / LD.
   *Our-data check (partial defense):* NAB2 and STAT6 land in **different** atopic-eczema-enriched
   clusters (NAB2: clusters 74/90, FDR 0.0028/0.0224; STAT6: cluster 30, FDR 0.0005) — NAB2's
   signal is not literally "in STAT6's module." And the perturbation **knocked down NAB2
   specifically** (on-target, adj-p 1e-16, no off-target), so the *functional* Th1/Th2 effect is a
   real NAB2 loss-of-function phenotype, not STAT6 bleed. The residual concern is whether the
   disease-cluster enrichment itself maps to the shared 12q13 locus.
2. **EGR-mediation caveat (mechanism).** NAB2's entire documented T-cell role is as an **EGR
   corepressor**; every published Th-relevant effect in this axis runs through EGR1/EGR2/EGR3, not
   NAB2 as an independent driver. The observed program shift could be EGR-target-mediated.

**This is the project's thesis in action:** the tool proposed a genuinely unexplored hypothesis;
an independent audit confirmed the novelty *and* caught a confounder a naive pipeline would ship
silently. Present NAB2 as **novel, receipt-backed, NAB2-specific in function — but flagged for
STAT6 adjacency and EGR mediation**, not as a clean discovery.

## 1. What NAB2 is (molecular)
- Transcriptional **corepressor of the EGR family** (EGR1/NGFI-A/Zif268, EGR2/Krox20, EGR3) — binds
  the EGR R1 domain and represses transactivation (Svaren 1996, mapped it to 12q13.3, doi:10.1128/mcb.16.7.3545).
- Represses by recruiting the **CHD4 subunit of the NuRD** remodeling/deacetylase complex (2006,
  doi:10.1074/jbc.m600775200); paralog **NAB1**; conserved NCD1 (EGR-interaction) + NCD2 (repression) domains.
- **EGR-inducible negative-feedback loop** (EGR1/2/3 induce NAB2). **Context-dependent** — can also
  *coactivate* (notably TCR-induced NAB2 coactivates IL-2 in T cells, 2006, doi:10.4049/jimmunol.177.12.8301).

## 2. NAB2 in immunology & T cells — activation, not polarization
- The **EGR–NAB axis is a T-cell activation-vs-tolerance rheostat.** EGR2/EGR3 are negative
  regulators enforcing anergy (2005, ~464 cites); their conditional KO causes lupus-like autoimmunity (2012).
- NAB2 sits on the **opposite (pro-activation) arm**: *Egr-1/NAB2 enhance* T-cell function while
  *Egr-2/Egr-3 inhibit* it (2008, doi:10.1002/eji.200737157) — the NAB2-in-T-cell anchor paper,
  with an autoimmune-pneumonitis readout. NAB2 co-activates IL-2 (2006). It regulates secondary
  **CD8** responses via TRAIL (2011) — not CD4 lineage.
- **Th1/Th2 verdict: 0 direct papers.** Nothing in the corpus or live search links NAB2 to
  Th1/Th2/Th17/Treg, GATA3, IL-4, or IL-13. NAB2's only CD4 footprint is general activation
  (IL-2), not lineage choice. The Th-relevant signal in this axis is EGR2/EGR3 (anergy), not NAB2.

## 3. NAB2 in disease & genetics — defined by the STAT6 fusion
- **The dominant clinical fact: the NAB2–STAT6 fusion is the pathognomonic driver of solitary
  fibrous tumor (SFT).** A somatic 12q13 inversion fuses NAB2's repression N-terminus to STAT6's
  transactivation domain, flipping NAB2 from an EGR1 *repressor* into a constitutive EGR1-target
  *activator* (discovered 2013: Chmielecki doi:10.1038/ng.2509 ~820 cites; Robinson doi:10.1038/ng.2522
  ~596). Nuclear STAT6 IHC is the diagnostic standard (2014).
- **Genetics:** NAB2 is **not** a headline GWAS-disease gene and carries **no established germline
  disease association**. Its salient genomic fact is the **12q13.3 adjacency to STAT6** (a Th2/allergy
  locus). No causal NAB1/NAB2 mutations in peripheral neuropathies despite the EGR2/myelination role.
- Other roles are mechanistic, not disease-causal: Schwann-cell myelination (Egr2·NAB complex, 2008).

## 4. The novelty audit of our finding (the crux)
| Claim | Literature evidence | Verdict |
|---|---|---|
| NAB2 → Th1/Th2 polarization (functional) | 0 direct papers | **Novel**; NAB2-specific (direct KD); caveat: could be EGR-mediated |
| NAB2 → atopic eczema (disease) | 0 direct papers; 12q13 atopy signals all → STAT6 | **Novel**; caveat: STAT6-adjacency confounder |
| NAB2 → any autoimmune/allergic disease (direct) | 0 direct (only indirect via EGR corepressor role) | Novel |
| Positive control: STAT6 → atopic eczema/asthma in our data | referee-supported (as expected) | pipeline finds known biology too |

## 5. What this means for the demo / framing
- **Lead with the honesty.** "The tool proposed NAB2→Th1/Th2→atopic eczema; an independent
  literature audit found ZERO prior papers on either link (genuinely novel); the same audit caught
  that NAB2 is 1.9 kb from STAT6, the master atopic gene — so we flag the disease link as
  STAT6-confounded rather than claim a clean discovery." That caveat-awareness *is* the moat.
- **The defensible core:** the NAB2-specific knockdown producing 301 downstream DEs + a strong Th1/Th2
  shift is a real, novel functional phenotype. The disease attribution is the part to hedge.
- **Do NOT** say NAB2 is "known/established" (it isn't) or imply the EGR2 corepressor mechanism is
  referee evidence.

## 6. Recommended next checks (optional, strengthen the story)
- Check how the T3 disease clusters map to genomic loci — is NAB2's atopic-eczema enrichment driven
  by the shared 12q13 locus, or by independent co-expression? (If independent, the finding is stronger.)
- Compare NAB2 vs STAT6 downstream DE-gene overlap — distinct programs argue against pure STAT6 shadow.
- If time permits, an EGR-target-overlap check to address the mechanism caveat.

## Method & sources
4 independent Claude agents (molecular / immunology / disease / genetics), each over the 155-paper
corpus + targeted Europe PMC / OpenAlex / Semantic Scholar queries, synthesized here and cross-checked
against `referee_triple` on our Perturb-seq tables. Corpus + per-agent syntheses:
`.claude/scratch/lbd-debate/nab2_*`. Tool: `src/arbiter/lit/search.py`.
