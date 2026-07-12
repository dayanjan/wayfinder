# Independent Cross-Check (Claude) — Contribution & Novelty Audit

**Role:** Phase-D independent cross-checker. Fresh queries, different phrasing from the obvious, formed BEFORE reading sibling finding files (no anchoring). Tool: live Europe PMC + OpenAlex + Semantic Scholar via `src.arbiter.lit.search`.

**Epistemic caveat applied throughout:** a query that fails to surface a paper proves "not surfaced in my queries," NOT "proven absent." Negatives below are flagged accordingly.

---

## X1 — Prior-art threat: Popper / VERITAS / MOOSE-Chem3

### Queries run
- `agentic sequential falsification hypothesis validation error control`
- `Automated Hypothesis Validation Agentic Sequential Falsifications` (abstract pull)
- `VERITAS multi-agent co-scientist hypothesis supported refuted underpowered` (+ abstract pull)
- `MOOSE-Chem3 ... experiment feedback chemistry hypothesis`; `MOOSE-Chem ... rediscovering chemistry hypotheses`

### Key papers (all CONFIRMED to exist, abstracts pulled)
| Paper | Year | DOI | Index cites |
|---|---|---|---|
| **Popper** — "Automated Hypothesis Validation with Agentic Sequential Falsifications" | 2025 | 10.48550/arxiv.2502.09858 | 6 (see note) |
| **VERITAS** — "A Multi-Agent Co-Scientist for Verifiable Image-Derived Hypothesis Testing" | 2026 | 10.48550/arxiv.2604.12144 | — |
| **MOOSE-Chem3** — "Toward Experiment-Guided Hypothesis Ranking via Simulated Experimental Feedback" | 2025 | 10.48550/arxiv.2505.17873 | — |
| MOOSE-Chem — "LLMs for Rediscovering Unseen Chemistry Scientific Hypotheses" | 2024 | 10.48550/arxiv.2410.07076 | — |

**Popper (2502.09858) — decisive questions, from its abstract, all YES:**
- (a) LLM-hypothesis overproduction/hallucination? **YES** — verbatim: "the rise of hypothesis generation from Large Language Models ... prone to hallucination and produce hypotheses in volumes that make manual validation impractical."
- (b) falsification/abstention against data as first-class? **YES** — "Guided by Karl Popper's principle of falsification ... agents that design and execute falsification experiments ... whether drawn from existing data or newly conducted procedures."
- (c) empirically evaluated / error control? **YES** — "sequential testing framework ensures strict Type-I error control ... six domains ... robust error control, high power, and scalability ... comparable performance to human scientists."

**VERITAS (2026)** is an even closer conceptual neighbor on the *taxonomy + receipts* axis: it "mechanically classifies outcomes as **Supported, Refuted, Underpowered, or Invalid**," produces a "**fully auditable evidence trail, tracing every conclusion through executable outputs**," and explicitly motivates the Underpowered label with "**non-significant results often reflect insufficient sample size rather than absent effects**" — which is the *general form* of the manuscript's "failed knockdown = untested, not negative" hero feature, and of its "receipt for every hop" framing.

**MOOSE-Chem3 / MOOSE-Chem** are near-neighbors in the AI-co-scientist family but are hypothesis *generation/ranking* systems (simulated experimental feedback), NOT refutation-with-abstention referees — weaker threat than Popper/VERITAS.

**Verdict: CONFIRM the threat is real; Popper is a genuine, evaluated near-neighbor that MUST be cited; VERITAS is arguably the closer neighbor on taxonomy + auditable-receipts and must also be cited.**

**Does any COLLAPSE the manuscript's novelty ("deterministic non-LLM referee + held pre-existing substrate + abstain + refute")?** **No — but they narrow it, and more than a single-paper framing admits.** The manuscript's *four-part* differentiator survives:
1. **Deterministic, non-LLM adjudication core.** Popper and VERITAS both use *LLM agents* to design/run/judge; the manuscript's referee is a deterministic tool with LLM confined to interpretation. Genuine distinction.
2. **Held, pre-existing substrate** (re-derivation over a fixed public Perturb-seq table) rather than agent-designed/newly-run experiments. Genuine distinction vs Popper (designs experiments) and MOOSE-Chem3 (simulates feedback).
3. **Abstain (untested) as first-class** — **NOT novel in kind.** VERITAS's "Underpowered/Invalid" and Popper's Type-I control both instantiate it. Novelty here is application-only.
4. **Confident receipt-backed refute** — **NOT novel in kind.** VERITAS "Refuted," Popper falsification. Application-only.

So the honest position: the *combination* + the *deterministic-referee-over-held-substrate* is defensible as novel; the *abstain/refute-as-outcomes* and *receipt-per-hop* framing are prior art (VERITAS/Popper) and should be presented as **application/instantiation**, not invention. **If the manuscript currently claims abstain-or-refute-as-outcomes as a conceptual first, that is OVERSTATED and 2502.09858 + VERITAS falsify the claim at the concept level.**

**Note on cite count:** the brief cites Popper at ~41 cites; this merged index reports **6**. Likely index undercount for a 2025 preprint — I could not reproduce 41. Does not change the threat (existence + relevance are what matter), but the manuscript should not lean on a specific citation number I can't confirm.

---

## X2 — Is NAB2 a named 12q13 AD causal gene, or is STAT6 the driver?

### Queries run
- `atopic dermatitis 12q13 locus causal gene fine-mapping`
- `STAT6 atopic dermatitis susceptibility variant Th2`
- `NAB2 allergic disease asthma eczema GWAS variant`
- `Triangulating Molecular Evidence Prioritize Candidate Causal Genes Atopic Dermatitis Loci` (abstract pull)

### Findings
- **STAT6** recurs as the recognized 12q13 allergy/AD candidate: 2004 STAT6 haplotype↔elevated IgE; 2018 STAT6 variants↔food allergy (DBPCFC). STAT6 (12q13.3) is the canonical Th2/IL-4/IL-13-signaling driver.
- The systematic fine-mapping paper — **"Triangulating Molecular Evidence to Prioritize Candidate Causal Genes at Established Atopic Dermatitis Loci" (2020)** — ran 103 molecular-QTL/functional resources across 25 AD loci. Single-gene resolution at 8 loci (IL6R, ADO, PRR5L, IL7R, ETS1, INPP5D, MDM1, TRAF3); "less familiar" candidates at 6 more (SLC22A5, IL2RA, MDM1, DEXI, ADO, STMN3). **Neither STAT6 nor NAB2 appears in either prioritized list** — 12q13 was evidently NOT resolved to a single gene by triangulation.
- **NAB2 never surfaced** as a named candidate in any AD/allergic-disease GWAS query (the big shared-allergy GWAS — 2017 asthma/hayfever/eczema, 2018 "eleven loci," 2020 "76 variants" — none name NAB2 in title/surfacing).

### Verdict: **CONFIRM, with a REFINE.**
NAB2 is literature-absent as a *named* AD causal gene in my queries (not surfaced → consistent with passenger status), and STAT6 is the recognized/canonical driver — the eczema signal is LD-plausibly STAT6's. **REFINE:** state STAT6 as the *recognized/canonical candidate*, not a *fine-mapped-to-single-gene certainty* — the best systematic triangulation did not cleanly resolve 12q13, so a "STAT6 is the proven fine-mapped driver" phrasing would be OVERSTATED. The manuscript's actual claim (LD-plausibly STAT6's; NAB2 a passenger) is well-supported and correctly hedged.

---

## X3 — Is NAB2 absent from Th1/Th2 polarization lit, and are EGR2/EGR3 established Th switch regulators?

### Queries run
- `NAB2 NGFI-A binding protein T helper cell Th2 differentiation`
- `EGR2 EGR3 transcription factor Th1 Th2 T cell differentiation polarization`
- `NAB2 EGR corepressor transcriptional immune regulation lymphocyte`

### Findings
- **EGR2/EGR3 ARE established immune / T-cell regulators — CONFIRM strongly:** 1998 "Egr-3 Regulates Fas Ligand Expression"; 2001 "Fas Ligand in Th1 and Th2 Cells ... Regulated by Early Growth Response Gene"; 2003 "EGR + NFAT heterodimers"; **2008 "Opposing regulation of T cell function by Egr-1/NAB2 and Egr-2/Egr-3"**; 2014 "EGR2 is critical for peripheral naïve T-cell differentiation." EGR2/EGR3 are documented regulators of T-cell activation, tolerance/anergy, and differentiation.
- **NAB2 is NOT entirely absent from T-cell literature.** The **2008 "Opposing regulation of T cell function by Egr-1/NAB2 and Egr-2/Egr-3"** paper names NAB2 explicitly in a T-cell-function axis (Egr-1/NAB2 vs Egr-2/Egr-3). NAB2 is the corepressor of EGR proteins and appears in T-cell *activation/tolerance* literature — but I found **no paper placing NAB2 specifically as a Th1/Th2 polarization/switch regulator.**

### Verdict: **REFINE (leaning CONFIRM on the load-bearing point).**
- The precise claim "**NAB2 absent from the Th1/Th2 *polarization* literature**" is defensible — not surfaced in my queries as a Th1/Th2-switch regulator.
- But "**novel-for-NAB2**," if read as "NAB2 has no T-cell literature," is **OVERSTATED** — NAB2 has a documented T-cell-function role (Egr-1/NAB2 axis, 2008). 
- **This actually STRENGTHENS the plausibility bridge, not weakens it:** the Egr-1/NAB2 vs Egr-2/Egr-3 T-cell axis is *already documented*, so extending NAB2 (EGR corepressor) to the Th1/Th2 switch is a short, well-motivated hop — while the switch-specific role remains genuinely unclaimed. Recommend the manuscript frame it as "NAB2 has an established T-cell-function role via the EGR axis but is unstudied in Th1/Th2 polarization specifically," which is both more accurate and more persuasive.
- **On EGR2/EGR3:** CONFIRM as established T-cell regulators; minor REFINE — their canonical role is activation/tolerance/anergy (with Th1/Th2-linked outputs like Fas ligand), not the textbook Th1/Th2 master switch (T-bet/GATA3). The "plausibility bridge" framing holds.

---

## X4 — Is QC-gated abstention ("failed knockdown = untested") a known primitive?

### Queries run
- `selective prediction reject option classification abstain confidence`
- `CRISPR screen quality control filter knockdown efficiency exclude negative`

### Findings
Selective prediction / reject-option classification is a **mature, well-established ML primitive:** 2015 "Agnostic Pointwise-Competitive Selective Classification"; 2018 "Classification with Reject Option Using Conformal Prediction"; 2019 "SelectiveNet"; 2021 "Optimal strategies for reject option classifiers," "The Art of Abstention," "Machine Learning with a Reject Option: A survey"; 2024 survey. Separately, CRISPR/RNAi-screen QC filtering ("from a Pool to a Valid Hit," 2018) is standard practice. The manuscript's gate = composition of two known primitives.

### Verdict: **CONFIRM (prior art; manuscript novelty is application-only).**
Abstention/reject-option is unambiguously prior art. The manuscript should claim novelty only in the *application* — a knockdown-QC validity gate that converts a failed perturbation to "untested" rather than "negative" — not in the abstention primitive itself. Any "we introduce abstention" framing would be OVERSTATED.

---

## X5 — Does CRISPRi dCas9-KRAB distance-dependent spreading lit exist; does it prove 43 kb "safe"?

### Queries run
- `CRISPRi dCas9 KRAB chromatin spreading distance repression range`
- `KRAB zinc finger H3K9me3 heterochromatin spreading domain silencing genomic distance`
- `CRISPRi neighboring gene repression proximity off-target dCas9-KRAB local`

### Findings
- Distance/locality literature **exists:** 2016 "Optimizing sgRNA position markedly improves ... dCas9-mediated repression" (effect is TSS-proximal, position-dependent); 2017 "Ten principles of heterochromatin formation" (spreading is a real property); 2021 CRISPRoff "Genome-wide programmable transcriptional memory" (heritable KRAB-based methylation).
- **Double-edged key paper:** **2010 "KRAB–Zinc Finger Proteins and KAP1 Can Mediate Long-Range Transcriptional Repression through Heterochromatin"** + 2011 "Retrotransposon-Induced Heterochromatin Spreading" — these show KRAB/KAP1 repression **can extend long-range**, not merely a tidy short local footprint.

### Verdict: **CONFIRM the finding as stated ("makes 43 kb plausible, does NOT prove it safe"); flag mild DISPUTE against any stronger reading.**
The literature supports that dCas9-KRAB acts *predominantly* TSS-proximally (geometric plausibility for a 43 kb-distant neighbor being spared), so the manuscript's geometric cis-argument is *literature-plausible*. **But it is NOT proof:** the 2010 long-range-KRAB-repression result is exactly what a hostile reviewer would cite to argue 43 kb is not guaranteed safe. If the manuscript anywhere states 43 kb is "safe" rather than "geometrically plausible / expected-but-not-guaranteed to spare," that is OVERSTATED — recommend explicit hedging + cite the long-range KRAB paper as the counter-consideration it addresses.

---

## Cross-check summary of over/under-statements to flag to the master register
- **X1:** If the manuscript claims *abstain-or-refute-as-outcomes* or *receipt-per-hop* as conceptual firsts → OVERSTATED; Popper (2502.09858) + VERITAS instantiate both. Must cite both; reframe those as application/instantiation. The deterministic-referee-over-held-substrate combination survives as the real novelty.
- **X2:** "STAT6 is the fine-mapped/proven driver" → mildly OVERSTATED (triangulation didn't resolve 12q13 to one gene). "NAB2 = passenger" is well-supported.
- **X3:** "NAB2 is novel / absent from T-cell literature" → OVERSTATED (Egr-1/NAB2 T-cell axis documented, 2008). The narrower "absent from Th1/Th2 *polarization* lit" is supported and stronger.
- **X4:** No overstatement risk if framed application-only; would be OVERSTATED if abstention is claimed as invented.
- **X5:** "43 kb is safe" → OVERSTATED; "geometrically plausible, not proven" is correct and supported.

*Negatives are "not surfaced in my independent queries," not proofs of absence.*
