# Adversarial review — Claude hostile reviewer (live-literature)

**Mandate:** argue, as hard as the evidence honestly allows, that this manuscript does not make a
real contribution and should not be published — but back every attack with a real literature search,
and steelman anything I cannot break. Live tools: Europe PMC + OpenAlex + Semantic Scholar via
`src.arbiter.lit.search`. All searches below were run from the repo on 2026-07-12.

**One-line verdict:** a scrupulously honest, competently executed hackathon *demonstration* whose own
Limitations section concedes away every ingredient of a publishable contribution — with the single
closest published neighbor (an agentic falsification-validation system) left uncited.

---

## PRIORITIZED HOSTILE FINDINGS

### H1 — The load-bearing novelty is a gerrymandered 5-way conjunction, and its closest published neighbor is uncited. **[MAJOR]**
**Target:** M1 (§2.4, abstract, §1, §5.4) — "a *deterministic, non-LLM* referee that scores each
hypothesis against a *held, pre-existing* experimental substrate and returns a per-hop *experimental*
receipt … with a QC-gated *abstention* and a *falsification* as first-class verdicts," claimed distinct
from AI co-scientist, Robin/PaperQA2, SciAgents, Coscientist, AI Scientist, and PerturbQA.

**The attack.** The contribution is defined by a conjunction of five clauses (deterministic-not-LLM ∧
held-not-newly-generated substrate ∧ per-hop receipt ∧ abstention ∧ refutation). Each neighbor is
excluded on exactly one clause: AI co-scientist / Robin / Coscientist generate *new* experiments (fails
"held"); PerturbQA scores prediction accuracy (fails "abstain/refute"); classical LBD scores literature
(fails "data test"). But **every individual clause is prior-arted**, so the novelty rests entirely on
the intersection being "interesting," which is a judgment a referee can decline. Worse, the single most
on-point neighbor is **absent from the manuscript's bibliography**:

- **Huang, Zou et al., "Automated Hypothesis Validation with Agentic Sequential Falsifications," 2025,
  arXiv 2502.09858 — 41 citations** (verified uncited: `grep` of `references/references.bib` for
  `falsif|2502.09858|sequential` returns nothing). Its abstract states the *identical* motivating
  problem — "hypothesis generation from LLMs, which are prone to hallucination and produce hypotheses in
  volumes that make manual validation [infeasible]" — and its solution is agentic **sequential
  falsification against data with rigorous Type-I-error / e-value control**. That is falsification +
  abstention + data-grounding as first-class, published and *benchmarked*. Wayfinder's only clean
  differentiator is "the test is a fixed deterministic referee rather than an LLM-designed test," which
  is a narrow implementation distinction, not a new category.
- Adjacent, also uncited: **MOOSE-Chem3, "Experiment-Guided Hypothesis Ranking via Simulated
  Experimental Feedback," 2025, arXiv 2505.17873**; and the 2026 wave — **"Sound Agentic Science
  Requires Adversarial Experiments," arXiv 2604.22080** — showing the "adjudicate hypotheses against
  experimental feedback" space is actively filling.

**Severity MAJOR, not fatal:** the *exact* 5-way combination does appear unoccupied, and the
held-substrate framing is a real (if narrow) distinction. But a novelty that survives only by
conjunction, while omitting its nearest published relative, is exactly what a methods referee flags as
"contribution engineered to be empty of neighbors."
**What would rebut me:** cite Popper/2502.09858 and MOOSE-Chem3, and show a concrete task the
held-substrate deterministic referee does that sequential-falsification agents provably cannot — or
demonstrate the combination yields measurably better triage (which requires H4's missing evaluation).

### H2 — The flagship biology is 12q13 locus-adjacency to STAT6, and the manuscript concedes the disease claim is undischargeable. **[MAJOR]**
**Target:** B1/B2 (abstract, §4.3) — "NAB2 → Th1/Th2 → atopic eczema is a literature-novel regulatory
nomination."

**The attack.** NAB2 sits tail-to-tail with **STAT6** (~43 kb) inside the **12q13 atopy locus** — the
single best-established atopic-dermatitis/atopy locus in human genetics. Live searches:
- **STAT6 is the recognized 12q13 driver.** "Human germline heterozygous gain-of-function *STAT6*
  variants cause severe allergic disease," 2023, doi 10.1084/jem.20221755 (114 cites); "Regulation of
  Skin Barrier Function via … IL-13/IL-4–JAK–STAT6," 2020, doi 10.3390/jcm9113741 (152 cites);
  "Interactive effect of STAT6 and IL13 gene polymorphisms on eczema status," 2013, doi
  10.1186/1471-2350-14-67. The IL-4/IL-13→STAT6 axis *is* the canonical atopic-dermatitis pathway.
- **The 12q13 AD locus is old news:** "A genome-wide association study of atopic dermatitis identifies
  loci with overlapping effects on asthma and psoriasis," 2013, doi 10.1093/hmg/ddt317 (208 cites);
  "Dense mapping of chromosome 12q13.12-q23.3 and linkage to asthma and atopy," 1999, doi
  10.1016/s0091-6749(99)70398-2; "Fine-mapping of IgE associated loci 1q23, 5q31 and 12q13," 2014.
- **NAB2 is absent from the AD/eczema and the asthma-TWAS/eQTL literature.** Targeted searches
  ("NAB2 atopic dermatitis eczema"; "NAB2 asthma allergy TWAS eQTL 12q13 candidate causal gene")
  returned **zero** NAB2 hits. That is the tell: NAB2's "literature-novelty" is exactly what an
  **LD passenger of a named driver** looks like — novel because STAT6 is the gene everyone assigns the
  locus to, not because a real NAB2 signal was overlooked.

The manuscript's own §4.4b(iii) concedes this precisely: the LD-inherited disease label "we **cannot**
settle," it needs variant-level colocalization the substrate cannot perform, and that colocalization
"itself presupposes a detectable NAB2 *cis*-eQTL in CD4⁺ T cells, without which even variant-level data
cannot cleanly separate NAB2 from STAT6." In plain terms: **the flagship's disease hop is confounded
beyond what any available data can repair, and the authors say so.** For the paper's designated "hero
feature," the disease nomination is therefore unfalsifiable-in-practice.

On B1 specifically: NAB2's *only* described T-cell role is as an EGR-family corepressor (the paper cites
Collins 2008), and **Egr2/Egr3 are already established Th regulators** — "Early growth response 2 and
Egr3 are unique regulators in immune system," 2017, doi 10.5114/ceji.2017.69363; "Egr2 and 3 control
inflammation … PD-1^high memory T cells," 2020, doi 10.26508/lsa.202000766; "Regulatory polymorphisms in
EGR2 … systemic lupus," 2010, doi 10.1093/hmg/ddq092. So "NAB2 as a Th2 regulator" is a short step along
the *already-known EGR2/NAB2 axis* — family-adjacency stacked on locus-adjacency.

**Severity MAJOR.** The one worked discovery deflates to "NAB2 perturbs the Th program in this one
dataset" (real, receipt-backed) plus "an atopic-eczema label that is admittedly an LD shadow of STAT6."
**What would rebut me:** a NAB2 CD4⁺ *cis*-eQTL + colocalization against the 12q13 AD GWAS separating it
from STAT6 — which the manuscript itself lists as *future* work (§5.3b), i.e. not in this paper.

### H3 — Steelman-defeated but honest: the STAT6 *cis*-test survives; it just doesn't rescue the disease claim. **[MINOR — I cannot break this part]**
**Target:** B3/B4 (§4.4). The expression-level STAT6 *cis*-falsification is *competent and real*: 302/10,282
genes move under NAB2-KD, STAT6 is not among them (log₂FC +0.087, p 0.788), tested against the study
authors' own genome-wide DE matrix, with the geometry argument (dCas9–KRAB promoter-proximal spread,
STAT6 promoter ~43 kb away — "CRISPRi spread" is real: Lensch 2022). This is exactly the kind of honest
artifact-check the field usually skips, and the cross-model replication even *caught and fixed* a
cluster-ID mislabeling (74/90 → 90/100). I cannot honestly attack this as wrong. **But** it only excludes
the *perturbation-signal* confound; it does nothing for the *disease-label* LD confound (H2), and the
manuscript correctly refuses to let it. So it is good practice that leaves the flagship's central claim
exactly as undischargeable as before.

### H4 — No evaluation: the method is demonstrated (n=1), never measured — and the paper admits it. **[MAJOR, approaching FATAL for a methods framing]**
**Target:** M3/M10, §4.1, §5.3, §5.3b. The manuscript's contribution is "the method." A methods paper is
judged on the method being *measured*. This one reports **no precision, no recall, no held-out
evaluation, no external ground-truth panel** — and §5.3b concedes every one of these as *future* work,
explicitly: "They do *not* establish that the referee *decides correctly at scale* — there is no external
validation and no precision or recall against a ground truth, and we make no such claim." The
"discrimination" that remains after §4.1b's honest label-shuffle control is (a) substrate-inherited
disease-hop stringency (not the referee's) and (b) a **knockdown-QC gate that flags ~1 in 6 genes** —
i.e. "did the experiment work?", a standard screen QC filter, not a discovery engine. The abstention
primitive it is built on is itself deep prior art: **"Machine learning with a reject option: a survey,"
2024, doi 10.1007/s10994-024-06534-x (63 cites); "The Art of Abstention: Selective Prediction …," 2021,
doi 10.18653/v1/2021.acl-long.84; "Agnostic Pointwise-Competitive Selective Classification," 2015** — the
reject-option/selective-prediction lineage runs back to Chow (1970). The domain instantiation
("a failed knockdown is *untested*, not a negative") is a genuinely useful discipline, but it is one QC
rule, not a measured method.

Compounding: the headline "reproduction" is a **cache replay** under a no-network guard (§4.5, conceded
"a faithful recomputation, not a live crawl"), and the cross-model replication re-derives numbers from
CSVs — "evidence of computational robustness, not of biological validity" (the paper's own words, §4.6).

**Severity MAJOR→FATAL for a Frontiers/bioinformatics *methods* submission:** the exact deliverable a
methods referee needs is the one the paper says it will produce later. And H1's uncited neighbor
(2502.09858) *did* run the FDR-controlled evaluation — so the missing rung is not merely absent, it is
absent relative to a published system.
**What would rebut me:** execute §5.3b step (1) or (2) — a time-sliced held-out or an external
known-true/known-false panel with precision/recall on the *refuted* and *untested* classes. That would
convert demonstration into contribution. It is not in this manuscript.

### H5 — The agentic-workbench methods trick is real but modest, and the honesty framing cannot itself be the contribution. **[MINOR]**
**Target:** M6/M7 (§3.4, §4.5, §5.1). Headless scripting of an API-less agentic workbench + an
independent language-critic that stripped "validated"/"definitive" is a genuine, under-explored trick
(H-steelman below). But the manuscript over-relies on it: with the biology deflated (H2) and the method
unmeasured (H4), the *self-audit language hygiene* risks becoming the paper's main novelty — and
"our LLM removed two overstated words from its own output" is a process anecdote (n=2 words), not a
scientific result. The replicability-over-a-UI-with-no-stable-contract point is honestly flagged as
fragile (§5.3). Reads as an engineering note, not a finding.

---

## STEELMAN — the strongest honest case FOR publishing

There *is* a real, small contribution here, and it would be dishonest to deny it. Three things survive
my attack. **First**, the domain discipline "a failed knockdown must be reported as *untested*, never as
a biological negative" is correct, under-practiced in screen-mining, and cleanly operationalized — a lot
of Perturb-seq re-analysis genuinely does record failed perturbations as null effects, and naming this as
a first-class verdict has teaching value even if selective-prediction theory is old. **Second**, the
STAT6 *cis*-test (H3) is a competent, honest confounder falsification against the authors' own
genome-wide data, and the adversarial cross-model replication that *caught its own cluster-ID bug* is a
model of the reproducibility hygiene the field lacks. **Third**, the whole artifact is
radically calibrated: it foregrounds the confounder it cannot discharge, labels its reproduction a cache
replay, and refuses precision/recall claims it did not earn. As a **methods-and-norms perspective piece**
— "here is a disciplined, receipt-backed, abstention-aware way to triage LLM/LBD hypotheses against held
perturbation data, demonstrated end-to-end inside an agentic workbench, with the honesty apparatus made
load-bearing" — it is more rigorous than most of the 2025–26 "AI co-scientist" papers it cites. A venue
that publishes methodology-and-practice notes could reasonably take it *if* reframed as demonstrated
(not evaluated) and the missing neighbors (2502.09858, MOOSE-Chem3) are engaged.

---

## BOTTOM LINE

**Do-not-publish in the current form; at most major-revision as an explicitly-scoped methods/perspective
note, not as a discovery.** The manuscript is honest to a fault, and that honesty is its undoing for a
publication decision: by §5.4 it has conceded that its biological flagship is an undischargeable LD
shadow of STAT6 in the 12q13 atopy locus (H2), that its referee's own edge reduces to a ~1-in-6
knockdown-QC gate whose disease-hop stringency is substrate-inherited (H4), that its reproduction is a
cache replay (H4), and that it has no precision/recall or external validation (§5.3b) — while its single
closest published neighbor, an *evaluated* agentic sequential-falsification validator built for the
identical LLM-hypothesis-overproduction problem (arXiv 2502.09858, 41 cites), goes uncited (H1). What is
left after the hedging is a competent, teachable *demonstration* on n=1 gene — real craft, real honesty,
a genuinely nice STAT6 artifact-check — but not a result that moves science, and not a method that has
been measured. Given the stated preference for "don't publish" over adding a forgettable paper, the
honest call is **do-not-publish**: the paper that *would* move science (H4's held-out evaluation + H2's
colocalization) is the one the authors correctly describe as future work.

---

## Retrieved evidence (papers cited above, for independent re-adjudication)
- Huang/Zou et al., Automated Hypothesis Validation with Agentic Sequential Falsifications, 2025, arXiv **2502.09858**, 41 cites — **uncited** by manuscript (verified). Abstract confirms LLM-hypothesis-overproduction + hallucination motivation; agentic sequential falsification vs data with error control.
- MOOSE-Chem3: Experiment-Guided Hypothesis Ranking via Simulated Experimental Feedback, 2025, arXiv **2505.17873**, 5 cites — uncited.
- Sound Agentic Science Requires Adversarial Experiments, 2026, arXiv **2604.22080** — uncited.
- Human germline GoF STAT6 variants cause severe allergic disease, 2023, **10.1084/jem.20221755**, 114 cites.
- Regulation of Skin Barrier Function via … IL-13/IL-4–JAK–STAT6/STAT3, 2020, **10.3390/jcm9113741**, 152 cites.
- Interactive effect of STAT6 and IL13 polymorphisms on eczema status, 2013, **10.1186/1471-2350-14-67**.
- GWAS of atopic dermatitis, overlapping effects on asthma/psoriasis, 2013, **10.1093/hmg/ddt317**, 208 cites.
- Dense mapping of chromosome 12q13.12-q23.3, linkage to asthma and atopy, 1999, **10.1016/s0091-6749(99)70398-2**.
- Fine-mapping of IgE associated loci 1q23, 5q31 and 12q13, 2014, **10.1183/13993003/erj.44.suppl_58.p4215**.
- NAB2 vs atopic dermatitis / asthma-TWAS/eQTL: **zero** hits across two targeted searches (LD-passenger tell).
- Egr2/Egr3 unique regulators in immune system, 2017, **10.5114/ceji.2017.69363**.
- Egr2/Egr3 control inflammation, PD-1^high memory T cells, 2020, **10.26508/lsa.202000766**.
- Regulatory polymorphisms in EGR2 associated with SLE, 2010, **10.1093/hmg/ddq092**.
- Machine learning with a reject option: a survey, 2024, **10.1007/s10994-024-06534-x**, 63 cites.
- The Art of Abstention: Selective Prediction …, 2021, **10.18653/v1/2021.acl-long.84**, 38 cites.
- Agnostic Pointwise-Competitive Selective Classification, 2015, **10.1613/jair.4439**.
- Neighbors the manuscript DOES cite and engages fairly: gottweis2025 (Co-Scientist), robin2025, sciagents2025, perturbqa2025, plausibility2026.
