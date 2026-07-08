# NAB2 — cumulative knowledge synthesis + novelty audit of our finding

Independent 4-agent literature audit (2026-07-08), grounded in a 155-paper NAB2 corpus
(Europe PMC + OpenAlex + Semantic Scholar via `src/arbiter/lit/`) plus targeted follow-up
searches, then cross-checked against our own Perturb-seq data. Purpose: honestly calibrate
the "near-novel" claim for **NAB2 → Th1/Th2 → atopic eczema**.

## Bottom line
Our finding is **more genuinely novel than the ac_lit=6 count suggested — literally zero papers
directly link NAB2 to Th1/Th2 polarization OR to atopic eczema** — and the audit *strengthens*
the project by surfacing exactly the two skeptical caveats a good referee must flag:

1. **STAT6-adjacency confounder (disease hop) — checked, substantially reduced.** NAB2 sits
   **~1.9 kb from STAT6** on 12q13.3 — STAT6 being *the* master Th2 / atopic-dermatitis / IgE
   transcription factor. Every 12q13 atopy GWAS signal in the literature resolves to STAT6, never
   NAB2. So NAB2's atopic-eczema link could a priori be STAT6's shadow via shared regulation / LD.
   Two follow-up checks (2026-07-08, `.claude/scratch/lbd-debate/stat6_confounder_checks.py`):
   - **NOT a genomic-locus artifact.** NAB2's atopic-eczema clusters (74, 90) are **genome-wide
     functional immune modules**, not 12q13 blocks: of ~67 member genes only NAB2 + TESPA1 are on
     12q13, **STAT6 is in neither cluster**, and members span the genome (FOXP1 3p13, GFI1 1p22,
     CD28 2q33, IRF4, IL4, IL10, IL22). NAB2's disease enrichment comes from co-clustering with
     bona-fide Th-effector genes, not from proximity to STAT6. **This clears the worst version of
     the confounder.**
   - **NAB2 is a stronger program regulator than STAT6 itself** (Th1-associated, Ota z=**7.71** vs
     STAT6 z=2.66; ~8×). A mere proximity-shadow would not exceed the source — this argues NAB2 is a
     genuine regulator, not an echo. The knockdown is NAB2-specific (on-target, adj-p 1e-16, no
     off-target), so the functional effect is real NAB2 loss-of-function.
   - **Residual (honest) caveat:** NAB2 and STAT6 have the **identical disease profile** in this
     data (both support exactly {asthma, atopic eczema}, same program direction). So we cannot claim
     NAB2's disease specificity is *distinct* from STAT6's — consistent with NAB2 being a genuine,
     strong **co-regulator of the same type-2/atopic axis** STAT6 masters (biologically coherent for
     neighbors), not with a pure artifact. Frame it as "NAB2 is a strong, novel regulator of the
     atopic/Th axis — the same axis STAT6 governs," not as a STAT6-independent discovery.
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

## 6. Follow-up checks — DONE (2026-07-08)
- **Locus test:** ✅ done — NAB2's atopic-eczema clusters are genome-wide functional modules, not a
  12q13 artifact; STAT6 not in them (see caveat 1). **Confounder substantially reduced.**
- **NAB2 vs STAT6 comparison:** ✅ done — same disease profile + program direction, but NAB2's
  program effect is ~8× stronger; residual caveat is shared-axis co-regulation, not artifact.
- **Still optional (mechanism):** an EGR-target-overlap check to address the EGR-mediation caveat.

## Method & sources
4 independent Claude agents (molecular / immunology / disease / genetics), each over the 155-paper
corpus + targeted Europe PMC / OpenAlex / Semantic Scholar queries, synthesized here and cross-checked
against `referee_triple` on our Perturb-seq tables. Corpus + per-agent syntheses:
`.claude/scratch/lbd-debate/nab2_*`. Tool: `src/arbiter/lit/search.py`.
