# V-PRIM — method-primitive novelty audit (M2, M4, M8, M9, M10)

**Verifier:** V-PRIM · **Date:** 2026-07-12 · **Mode:** read-only + live `search_all`
**Question per claim:** is this a KNOWN primitive (→ novelty at most application-specific), or genuinely new?
**Sources read:** MASTER_REGISTER.md; `03_methods.tex` (§3.1–3.4); `04_results.tex` (§4.1, §4.1b, §4.2, §4.2b).

**Headline:** All five are **known primitives**. The manuscript does *not* claim to have invented any of
them — it presents each as a design choice, and M8/M9/M10 are actively *understated*. So the correct grade
for the primitives is NOT-NOVEL / PARTIALLY-ANTICIPATED, but the correct grade for **the manuscript's use of
them is honest, not overstated**. One improvement worth flagging: **M2 and M9 should each cite the field
they instantiate** (selective-prediction/reject-option for M2; the ML-leakage literature for M9) so a
reviewer sees the primitive is deliberately, correctly located rather than reinvented. Novelty for all five
lives at the **application** layer, and the load-bearing novelty is the M1 conjunction (V-GAP's), not any
single primitive here.

---

## M2 — QC-gated ABSTENTION (failed knockdown = *untested*, not negative) as a first-class verdict

**Restatement.** The referee returns `untested` (not `refuted`) when the knockdown fails QC at hop 0; a
third, abstain outcome sits alongside supported/refuted, so an uninterpretable experiment is never scored as
a biological negative (§3.3 Hop 0; §4.2 IL2).

**Queries:** "selective prediction reject option classifier"; "abstention uncertain prediction machine
learning biomedical"; "three-way classification abstain reject clinical".

**Key prior art**
- Geifman & El-Yaniv, *Selective Classification for Deep Neural Networks*, 2017 (925 cites), arXiv:1705.08500 — canonical modern selective-prediction / reject.
- Geifman & El-Yaniv, *SelectiveNet: A Deep Neural Network with an Integrated Reject Option*, 2019 (465 cites).
- Xin et al., *The Art of Abstention: Selective Prediction and Error Regularization for NLP*, 2021, doi:10.18653/v1/2021.acl-long.84.
- Hendrickx et al., *Machine learning with a reject option: a survey*, 2024, doi:10.1007/s10994-024-06534-x (63 cites).
- **Biomedical instances:** *Uncertainty-aware single-cell annotation with a hierarchical reject option*, 2023, Bioinformatics; *Reliable prediction of anti-diabetic drug failure using a reject option*, 2016, doi:10.1007/s10044-016-0585-4; *On the Feature Selection Methods and Reject Option Classifiers for Robust Cancer Prediction*, 2019.

**VERDICT: NOT-NOVEL (as a primitive) / application-novel.** The abstain / reject-option / "learning to
defer" family is decades old and already worked in genomics and clinical ML. Wayfinder's move — mapping the
abstain outcome onto a *deterministic experimental QC gate* (a failed knockdown is un-interpretable, so
`untested`, not `no effect`) — is a **sensible, specific instantiation**, not a new primitive. The
manuscript's IL2 framing ("refusing to read an uninterpretable knockdown as a biological result") is exactly
selective prediction under a domain-specific reject rule. **The manuscript does not claim to have invented
abstention** (no "novel verdict primitive" language survives in §3.3/§4.2), so it is not overstated — but it
also **does not cite the selective-prediction field at all**, which is a real gap: locating M2 against
Geifman/El-Yaniv would (a) pre-empt the reviewer who says "this is just a reject option" and (b) let the
paper claim the *right* novelty (a QC-derived, deterministic reject rule for hypothesis adjudication).

**Moves science forward?** As a primitive, no. As an application, mildly yes — the QC→abstain mapping is a
clean domain rule that a confirmation-shaped pipeline lacks; it is the honest part of the thesis, correctly
scoped.

---

## M4 — deterministic-tools-only division of labour (LLM never computes a receipt)

**Restatement.** Every numeric receipt (OR, p, effect count, co-mention) is a deterministic tool lookup; the
LLM does judgment/provenance only and "no model computes a receipt" (§3.1 model cast; §3.2 "Every signal is
a deterministic lookup"; §3.4).

**Queries:** "grounded tool use LLM avoid hallucination deterministic"; "retrieval augmented generation
deterministic tool scientific agent"; "LLM agent calls external tool for calculation instead of computing".

**Key prior art**
- Goodell et al., *Large language model agents can use tools to perform clinical calculations*, 2025, doi:10.1038/s41746-025-01475-8 — near-exact analog: the LLM defers numeric computation to deterministic tools rather than computing itself.
- Gou et al., *CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing*, 2023, arXiv:2305.11738 — LLM reasons, tools verify.
- Zhuang et al., *ToolQA: A Dataset for LLM QA with External Tools*, 2023, arXiv:2306.13304.
- *Small LLMs Are Weak Tool Learners: A Multi-LLM Agent*, 2024, EMNLP; *LLM-Based Agents for Tool Learning: A Survey*, 2025 — the entire grounded / tool-augmented-generation paradigm (Toolformer lineage).

**VERDICT: NOT-NOVEL (as a primitive).** "LLM plans/judges, deterministic tools compute the numbers" is the
standard grounded-tool-use / RAG-with-tools pattern; the clinical-calculations paper is essentially the same
architectural rule in medicine. This is the register's correctly-flagged **HIGH-risk** item and the risk is
confirmed. **But the manuscript is honest about it** — §3.4 presents the discipline as a *provenance
guarantee* ("all biological interpretation is confined to these models reading deterministic receipts"), not
as a novel technique, and never claims to have invented tool-grounding. So NOT overstated. The
application-specific contribution is thin here: it is best read as *rigor / an epistemic invariant for a
science referee* (no LLM-fabricated statistic can enter a receipt), which is good practice rather than a
contribution. Correctly treated as method hygiene, not a headline.

**Moves science forward?** No as a primitive; it is a well-chosen constraint that supports the *auditability*
claim (M1/M6), where the actual novelty sits.

---

## M8 — balanced novelty+effect ranking objective (min-z bridge, no obscurity reward)

**Restatement.** Eligible candidates ranked by `min(z(ab), z(bc)) + β·z(effect) − w·log1p(ac_lit) −
w2·ac_known`; the `min` makes the bridge balanced (one strong axis can't rescue a weak one) and raw
co-mention is deliberately kept out of the gate so obscurity is not rewarded (§3.2).

**Queries:** "literature-based discovery ranking ABC score mutual information"; "Swanson ABC model
literature based discovery hidden connections"; "understudied genes literature bias underexplored genome".

**Key prior art**
- Swanson-lineage LBD ranking is a whole subfield: *Indirect association and ranking hypotheses for literature based discovery*, 2019, doi:10.1186/s12859-019-2989-9; *A context-based ABC model for literature-based discovery*, 2019, doi:10.1371/journal.pone.0215313; *Prioritizing ADR and Drug Repositioning Candidates Generated by LBD*, 2016.
- Understudied-gene / literature-bias context (motivates the anti-obscurity term): Stoeger et al. lineage — *understudied genes are lost in a leaky pipeline between genome-wide assays and reporting* (2023 preprint, doi:10.1101/2023.02.28.530483) and *Accelerating biological insight for understudied genes*, 2021, doi:10.1093/icb/icab029; *GhostBuster: a Literature-Unbiased Gene Prioritization Tool*, 2025, doi:10.1101/2025.06.22.660948.

**VERDICT: PARTIALLY-ANTICIPATED (as a primitive) / understated.** "Rank LBD candidates by a combined
novelty-plus-strength score" is standard; the ABC/ranking literature is large. What is *not* off-the-shelf is
the exact objective: a **balanced min-z bridge** (a conjunction rather than a sum, so a strong A–B cannot
paper over a weak B–C) **combined with an explicit anti-obscurity guard** (co-mention out of the gate; an
`ab` percentile floor). That specific formulation is a reasonable, arguably-novel *combination* within a
known paradigm — but it is application-level, and the manuscript **understates** it (calls the objective "the
only human judgment," examines rank stability, and never claims the objective is itself novel). Not
overstated; if anything the paper could claim slightly more here (the anti-obscurity design directly answers
the Stoeger literature-bias problem).

**Moves science forward?** Modestly, at the application layer — the balanced-bridge + anti-obscurity pairing
is a thoughtful, transferable ranking design for novelty-seeking prioritization.

---

## M9 — disease-answer-free / leakage-free candidate-universe construction

**Restatement.** The candidate universe A is built from perturbation data alone (knockdown-QC + effect +
program), *before any disease information is consulted*; construction never reads the disease table T3, so
the gene list cannot be contaminated by the disease answer it is later tested against (§3.2; §4.1).

**Queries:** "data leakage prevention gene prioritization machine learning"; "target leakage feature
selection before train test split genomics"; (context) "label permutation negative control gene set enrichment".

**Key prior art**
- Kapoor & Narayanan, *Leakage and the reproducibility crisis in machine-learning-based science*, 2023, doi:10.1016/j.patter.2023.100804 (710 cites) — canonical taxonomy of leakage, including using the label to build features.
- *Overview of leakage scenarios in supervised machine learning*, 2025, doi:10.1186/s40537-025-01193-8 (52 cites); *Don't push the button! Exploring data leakage risks in ML and transfer learning*, 2025, doi:10.1007/s10462-025-11326-3.
- Domain instances: *Benchmarks in antimicrobial peptide prediction are biased due to the selection of negative data*, 2022; *Prevention of Leakage in ML Prediction for Polymer Composite Properties*, 2024; *A review of model evaluation metrics for ML in genetics and genomics*, 2024.

**VERDICT: NOT-NOVEL (as a primitive).** "Do not consult the label/answer when constructing the candidate
set/features" is textbook target-leakage avoidance; Kapoor & Narayanan formalize exactly this failure mode.
This is the register's second **HIGH-risk** item and the risk is confirmed at the primitive level. **However
the manuscript is scrupulously honest and does not overstate:** §3.2 explicitly scopes it — "**A** is
disease-answer-free, *not evidence-free*: it is preselected on the same knockdown/effect/program evidence the
referee re-reads at hops 0–2" — which is precisely the correct, self-limiting statement and pre-empts the
"you leaked the effect signal into A" objection. That candor is the right posture. The only improvement: a
one-line citation to the ML-leakage literature (Kapoor & Narayanan) would show the construction is a
*deliberate* application of a known principle to LBD, not an ad-hoc choice.

**Moves science forward?** No as a primitive; yes as *correct discipline* — many hypothesis-generation
pipelines do leak the disease answer, and the honest scoping ("answer-free, not evidence-free") is better
than most.

---

## M10 — negative-control DECOMPOSITION (label-shuffle → substrate-inherited stringency; referee's own edge = QC gate)

**Restatement.** A 2,000-permutation disease-label shuffle shows the disease hop's ~99% refutation rate is
*inherited from the enrichment study's FDR family* (null passes 0.99%, observed 0.86%), so that stringency is
**not** credited to the referee; the referee's own discriminating edge is then relocated to and quantified at
the QC gate (~1 in 6 untested), §4.1b Control 2 + §4.2b.

**Queries:** "label permutation negative control gene set enrichment"; (shared with M8/M9) LBD-ranking and
leakage batteries above.

**Key prior art**
- Label/phenotype permutation as the negative-control null is ubiquitous in gene-set enrichment: Subramanian GSEA phenotype-permutation lineage; *On testing the significance of sets of genes*, 2007, doi:10.1214/07-aoas101; *Random-set methods identify distinct aspects of the enrichment signal*, 2007; *Camera: a competitive gene set test accounting for inter-gene correlation*, 2012, doi:10.1093/nar/gks461; *Avoiding the pitfalls of gene set enrichment analysis with SetRank*, 2017.

**VERDICT: PARTIALLY-ANTICIPATED (as a primitive) / understated.** Label-permutation negative controls are
completely standard; the *permutation test itself* is not novel. What is not standard-issue is the
**decomposition move**: using the shuffle not merely to compute a p-value but to **attribute** the observed
stringency to the substrate versus the referee, and then explicitly *decline credit* for the substrate-owned
part and relocate the referee's real edge to the QC gate. That attribution-and-honest-subtraction framing —
"this discrimination is not ours; here is the part that is" — is a specific analytical/rhetorical
contribution, and it is heavily understated (the paper even refuses the tempting "rarer-than-chance"
selectivity reading because the upper-tail p is 1.0). It is application-level, not a new statistical
primitive, and it is the opposite of overstated — it actively *shrinks* the paper's own M3 falsification
claim.

**Moves science forward?** As a primitive, no. As a *methodology-honesty template* for agentic-science
evaluation (permute to separate substrate-inherited from method-supplied discrimination, then claim only the
latter), modestly yes — it is a reusable pattern for not over-crediting a referee.

---

## Summary table

| Claim | Primitive verdict | Manuscript's use | Novelty locus | Cite-gap to fix |
|---|---|---|---|---|
| M2 abstention | NOT-NOVEL | honest, uncited | QC→abstain rule (application) | **cite selective-prediction/reject-option** |
| M4 deterministic-tools-only | NOT-NOVEL | honest (rigor, not headline) | provenance invariant (application) | optional (grounded tool-use) |
| M8 min-z balanced ranking | PARTIALLY-ANTICIPATED | understated | balanced-bridge + anti-obscurity (application) | could claim slightly more |
| M9 leakage-free universe | NOT-NOVEL | honest, well-scoped | answer-free construction (application) | **cite ML-leakage lit (Kapoor & Narayanan)** |
| M10 control decomposition | PARTIALLY-ANTICIPATED | understated (self-shrinking) | substrate-vs-referee attribution (application) | none |

**Net:** No OVERSTATED or FALSE findings among the primitives. The primitives are known; the paper knows
they are known and treats them as method (M4/M9) or under-claims them (M8/M10). The two actionable items are
citation gaps (M2, M9), not novelty problems. The paper's real novelty is the **conjunction (M1)**, which is
V-GAP's to adjudicate — nothing in the primitive audit undermines it, and the honest under-claiming of
M8/M9/M10 *supports* the paper's calibrated-language thesis.

---

## Retrieved evidence appendix (M2 / M4 / M9 closest prior art)

### M2 — abstention / reject option / selective prediction
1. **Geifman & El-Yaniv, 2017** — *Selective Classification for Deep Neural Networks.* arXiv:1705.08500 (925 cites). The reference modern formulation of predict-or-abstain with a risk–coverage tradeoff. Directly anticipates "return a third, abstain outcome under an uncertainty/quality threshold."
2. **Geifman & El-Yaniv, 2019** — *SelectiveNet: A DNN with an Integrated Reject Option.* (465 cites). Reject option built into the model; establishes the abstain outcome as first-class.
3. **Xin et al., 2021** — *The Art of Abstention: Selective Prediction and Error Regularization for NLP.* doi:10.18653/v1/2021.acl-long.84. "Abstention" as first-class in generation/classification.
4. **Hendrickx et al., 2024** — *Machine learning with a reject option: a survey.* doi:10.1007/s10994-024-06534-x. Field survey — confirms maturity/breadth of the primitive.
5. **(biomedical) 2023** — *Uncertainty-aware single-cell annotation with a hierarchical reject option.* Bioinformatics. Reject option already applied in single-cell genomics — the same domain family as Wayfinder's substrate.
6. **(biomedical) 2016** — *Reliable prediction of anti-diabetic drug failure using a reject option.* doi:10.1007/s10044-016-0585-4. Reject-to-abstain in clinical prediction.

### M4 — grounded / deterministic tool-use (LLM does not compute)
1. **Goodell et al., 2025** — *Large language model agents can use tools to perform clinical calculations.* doi:10.1038/s41746-025-01475-8. Closest analog: the LLM defers numeric computation to deterministic tools rather than computing itself — the exact M4 division of labour, in medicine.
2. **Gou et al., 2023** — *CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing.* arXiv:2305.11738 (57 cites). LLM reasons; external tools supply/verify facts.
3. **Zhuang et al., 2023** — *ToolQA: A Dataset for LLM QA with External Tools.* arXiv:2306.13304. Benchmarks LLMs answering via external deterministic tools rather than internal computation.
4. **2024** — *Small LLMs Are Weak Tool Learners: A Multi-LLM Agent.* EMNLP-main.929; **2025** *LLM-Based Agents for Tool Learning: A Survey*, doi:10.1007/s41019-025-00296-9 — establishes tool-grounded generation as a standard, surveyed paradigm.

### M9 — data/target-leakage avoidance
1. **Kapoor & Narayanan, 2023** — *Leakage and the reproducibility crisis in machine-learning-based science.* doi:10.1016/j.patter.2023.100804 (710 cites). Canonical taxonomy; "using the label/answer to construct features or the sample" is a named leakage mode. M9 is a direct application of avoiding it.
2. **2025** — *Overview of leakage scenarios in supervised machine learning.* doi:10.1186/s40537-025-01193-8 (52 cites). Systematizes leakage types incl. feature-construction leakage.
3. **2025** — *Don't push the button! Exploring data leakage risks in ML and transfer learning.* doi:10.1007/s10462-025-11326-3 (51 cites).
4. **2022** — *Benchmarks in antimicrobial peptide prediction are biased due to the selection of negative data.* doi:10.1093/bib/bbac343 — genomics-domain instance of answer-contaminated set construction; the failure mode M9's answer-free construction avoids.

*All DOIs/years retrieved live via the repo `search_all` tool on 2026-07-12; citation counts are the tool's returned values at retrieval time.*
