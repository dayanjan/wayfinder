# V-GAP — novelty audit of M1 (the §2.4 conjunction) and M3 (falsification-as-deliverable)

Verifier: V-GAP · Date: 2026-07-12 · Tool: `src.arbiter.lit.search.search_all` (live Europe PMC + OpenAlex + Semantic Scholar)
Scope: read-only literature adjudication of the load-bearing novelty crux. I cannot prove a negative; below I distinguish "no prior art surfaced across 17 queries" from "proven novel."

---

## Queries run (17)

1. AI co-scientist hypothesis validation Gottweis
2. FutureHouse Robin assay data hypothesis agent autonomous
3. hypothesis prioritization held-out experimental dataset validation
4. CRISPR screen retrospective validate LLM hypothesis perturbation
5. PaperQA2 scientific claim verification citation
6. SciAgents knowledge graph hypothesis critic multi-agent
7. PerturbQA perturbation question answering benchmark language model
8. language model plausibility perturbation diverges CRISPR ground truth
9. literature-based discovery experimental validation grounding omics evidence
10. deterministic referee scoring hypothesis experimental data abstain refute
11. gene disease hypothesis scoring Perturb-seq atlas prioritization T cell
12. AI scientist automated hypothesis generation refutation negative result falsification
13. autonomous chemistry Coscientist Boiko experiment execution
14. LLM hypothesis validation against held-out single-cell perturbation ground truth
15. rerank prioritize literature-based discovery candidates with experimental omics filter
16. knowledge graph hypothesis validation transcriptomics evidence support refute per edge
17. VERITAS / rbio1 / Robin targeted abstract pulls

---

## M1 — the headline conjunction

**Claim restatement (§2.4, verbatim spine):** Wayfinder occupies a gap defined by the *conjunction* of: (a) an LBD front-end that generates candidate A–B–C triples; (b) a **deterministic, non-LLM referee** that scores each hypothesis against a **held, pre-existing** experimental substrate (a genome-scale CRISPRi Perturb-seq resource that predates and is blind to the triples); (c) a **per-hop experimental receipt** — OR / p-value / effect size — for every causal edge; (d) a **QC-gated abstention** (failed knockdown → *untested*, not *negative*); and (e) **falsification** as a first-class verdict. The paper claims this specific combination is distinct from AI co-scientist, Robin/PaperQA2, SciAgents, Coscientist, AI Scientist, and PerturbQA, and hedges only "we are not aware of a system that does the specific combination."

**How each named neighbour actually behaves (confirmed by retrieval):**

| System | What it does | Why it is NOT the conjunction |
|---|---|---|
| **Google Co-Scientist** (Gottweis, *Nature* 2026, `10.1038/s41586-026-10644-y`, 49 cites) | Tournament of simulated scientific debate; ranks hypotheses; reports wet-lab-validated hits | LLM debate + **new** wet-lab validation; no held pre-existing substrate; no deterministic referee; no abstention/refutation taxonomy |
| **Robin** (arXiv 2025, `10.48550/arxiv.2505.13400`) | Multi-agent system that generates and analyses **new** assay data in the loop | Generates fresh experiments, does not adjudicate against a held substrate |
| **PaperQA2 / language-agent synthesis** (`10.48550/arxiv.2409.13740`) | Superhuman synthesis of scientific knowledge; receipts are **literature citations** | Literature-derived evidence, not an experimental receipt; no data test |
| **SciAgents** (`10.1002/adma.202413523`; `10.48550/arxiv.2409.05556`) | Multi-agent reasoning over an ontological knowledge graph with a critic | KG reasoning, not a deterministic data referee; no experimental receipt per hop |
| **Coscientist / AI Scientist** (Boiko, `10.1038/s41586-023-06792-0`; Emergent, `10.48550/arxiv.2304.05332`) | Autonomous chemistry that **runs its own** experiments | New-experiment execution; no held substrate, no abstention |
| **PerturbQA / rbio1 / SynthPert / PerturBench** (`10.48550/arxiv.2408.10609`; `10.1101/2025.08.18.670981`; `10.48550/arxiv.2509.25346`) | Benchmark LLM **prediction accuracy** on perturbation outcomes; rbio1 uses "soft verifiers" to train a predictor | Frame the task as prediction, exactly as §2.4 says — not a referee that abstains and refutes with a receipt |

**Closest genuine near-neighbour surfaced (not cited in the manuscript):**
**VERITAS** — *A Multi-Agent Co-Scientist for Verifiable Image-Derived Hypothesis Testing* (2026, preprint, doi none, 0 cites). This is the single most threatening hit. It introduces "an epistemic evidence label framework that mechanically classifies outcomes as **Supported, Refuted, Underpowered, or Invalid** by jointly evaluating significance, effect direction, and study power," explicitly because "non-significant results often reflect insufficient sample size rather than absent effects." That is a strikingly parallel articulation of Wayfinder's *support / refute / untested-abstain* taxonomy and the failed-knockdown-≠-negative distinction. **However**, it does NOT collapse the carve-out: VERITAS (i) operates on **medical-imaging** data, not an LBD-generated triple; (ii) uses **LLM multi-agent** role-players that **run new statistical analyses** on the data they are handed — it is not a *deterministic, non-LLM* referee; (iii) has **no LBD front-end** and **no held, pre-existing perturbation substrate**; (iv) produces a single verdict per hypothesis, not a **per-hop** receipt chain. It anticipates the *verdict-vocabulary* element of M1, in a different domain and by a different mechanism, concurrently (2026).

**VERDICT — M1: NOVEL (defensible carve-out), with a required citation caveat.**

Across 17 queries no prior or prior-art system was surfaced that performs the *full conjunction* — an LBD front-end feeding a deterministic non-LLM referee that adjudicates each hypothesis against a held, pre-existing experimental substrate with a per-hop experimental receipt, QC-gated abstention, and falsification. Every named neighbour genuinely does something else (new experiments, literature ranking, KG reasoning, or prediction accuracy), and the retrieval corroborates the paper's characterisations of them. The "we are not aware of a system that does the specific combination" hedge therefore **holds** — it is a hedge, correctly, not an absolute-priority claim.

Caveat that keeps the hedge honest: the **individual components are each well-established** (grounded tool-use, selective prediction/abstention, permutation controls — see V-PRIM), so M1's novelty is entirely *integrative*, and the manuscript is right to frame it that way. The abstention+refutation **verdict-taxonomy** sub-element is independently and **concurrently** anticipated by VERITAS. Recommend the authors **cite VERITAS** (and ideally the SoundnessBench / "Sound Agentic Science Requires Adversarial Experiments" cluster) so the "we are not aware" hedge cannot be read as having missed the nearest neighbour. Doing so *strengthens* the paper — the differentiators (deterministic referee, LBD front-end, held perturbation substrate, per-hop receipts) survive the comparison cleanly.

**Moves science forward?** Yes, modestly and honestly. The specific integration — a cheap, CPU-feasible, deterministic experimental back-end that closes the LBD *triage* loop and can return a receipt-backed *no* — is a genuinely useful and, on this evidence, un-anticipated combination for the discovery-informatics reader.

---

## M3 — falsification / "confident receipt-backed no" as the deliverable

**Claim restatement (§4.2, 5.1):** Unlike plausibility-optimising generators, Wayfinder's headline deliverable is the confident, receipt-backed **no** — refuting a plausible claim with a real experimental receipt, and catching artefacts (failed knockdown → *untested*, not *negative*). Falsification, not confirmation, is the moat.

**Retrieval findings:** The *conceptual primitive* — treating refutation and "underpowered/abstain" as first-class outcomes of an agentic science system, and warning that plausibility ≠ truth — is **present and active in the concurrent 2026 literature**, not unique to Wayfinder:
- **VERITAS** (2026) already makes **Refuted** and **Underpowered** first-class, mechanically-assigned verdict labels.
- The critique cluster — *SoundnessBench: Can Your AI Scientist Really Tell Good Research Ideas from Bad Ones?* (2026, 3 cites), *Sound Agentic Science Requires Adversarial Experiments* (2026), *AI scientists produce results without reasoning scientifically* (2026) — is explicitly organised around the failure of plausibility-optimising generators and the need for refutation/soundness.
- The paper's own cited motivation (`plausibility2026`: LLM perturbation plausibility diverges from held-out CRISPR ground truth) is itself a refutation-of-plausibility result.

What remains **specific to Wayfinder**: falsification framed as *the product* (not a byproduct), tied to a *held experimental substrate* and a *deterministic* gate, and delivered with a *per-hop receipt*. That framing is legitimate and I found no exact twin — but it is an *emphasis/positioning* novelty layered on a primitive that others are converging on simultaneously. It is also **self-bounded by M10**: the manuscript's own negative-control decomposition shows the referee's *own* falsification edge fires ~1 in 6 and the disease-hop stringency is substrate-inherited — i.e., the paper honestly shrinks the very moat M3 asserts.

**VERDICT — M3: PARTIALLY-ANTICIPATED.**
The idea that an agentic scientific system should refute and abstain (power-gated) as first-class verdicts is independently and concurrently in the 2026 literature (VERITAS; the soundness/adversarial-experiments critique cluster). Wayfinder's differentiator is not the primitive but its *coupling to a deterministic held-substrate referee with per-hop receipts* — real, but narrow, and appropriately hedged. Not overstated in the manuscript as written (the language is "the deliverable here is the confident, receipt-backed no," a positioning claim, not a priority claim), and M10 keeps it honest.

**Moves science forward?** Yes as *demonstration*, less so as *concept*. The concept (falsification-first agentic science) is in the air; Wayfinder's contribution is a concrete, reproducible instance of it grounded in a held perturbation substrate — valuable, but the authors should not imply they originated the falsification-first framing.

---

## Bottom line for the orchestrator
- **M1: NOVEL** as an integrative conjunction; carve-out survives retrieval; **must cite VERITAS** to keep the "we are not aware" hedge airtight.
- **M3: PARTIALLY-ANTICIPATED**; the falsification-first *primitive* is converging in concurrent work; Wayfinder's *instantiation* (deterministic referee + held substrate + per-hop receipt) is the honest, defensible part.
- No result surfaced that **falsifies** M1's central claim. This is "no prior art found in 17 queries," not "proven novel."

---

## Retrieved evidence (closest-neighbour appendix for Phase-D re-adjudication)

1. **VERITAS: A Multi-Agent Co-Scientist for Verifiable Image-Derived Hypothesis Testing** (2026, preprint, doi none). *"…introduces an epistemic evidence label framework that mechanically classifies outcomes as Supported, Refuted, Underpowered, or Invalid by jointly evaluating significance, effect direction, and study power. This distinction is critical … where non-significant results often reflect insufficient sample size rather than absent effects … produces a fully auditable evidence trail, tracing every conclusion through executable outputs from analysis plan to … final verdict."* → **Closest neighbour on verdict taxonomy**; differs in domain (medical imaging), mechanism (LLM agents running new analyses, not a deterministic referee), and absence of an LBD front-end / held perturbation substrate. Concurrent (2026).

2. **Accelerating scientific discovery with Co-Scientist** (Gottweis et al., *Nature* 2026, `10.1038/s41586-026-10644-y`, 49 cites). Tournament of simulated debate + ranking; reports wet-lab-validated hits. → New-experiment validation, LLM-judged; no held substrate, no abstention/refutation primitive.

3. **Robin: A multi-agent system for automating scientific discovery** (2025, `10.48550/arxiv.2505.13400`). Generates and analyses **new** assay data in-loop. → New experiments, not adjudication against a held substrate.

4. **Language agents achieve superhuman synthesis of scientific knowledge** (PaperQA2, 2024, `10.48550/arxiv.2409.13740`). Receipts are **literature citations**. → No experimental data test; cannot abstain on data-quality or return a data-grounded *refuted*.

5. **SciAgents: Automating Scientific Discovery Through … Multi-Agent Intelligent Graph Reasoning** (2025, `10.1002/adma.202413523`; arXiv `10.48550/arxiv.2409.05556`). KG reasoning with an explicit critic. → Ontology/graph reasoning, not a deterministic experimental referee.

6. **Autonomous chemical research with large language models** (Coscientist; Boiko et al., *Nature* 2023, `10.1038/s41586-023-06792-0`). Runs its **own** chemistry experiments. → New-experiment execution.

7. **rbio1 — training scientific reasoning LLMs with biological world models as soft verifiers** (2025, `10.1101/2025.08.18.670981`). SOTA on **PerturbQA prediction** via soft (world-model) verifiers used at *training* time. → Prediction accuracy, not a refereeing/abstaining system; corroborates §2.4's "PerturbQA frames it as prediction" characterisation.

8. **SynthPert** (2025, `10.48550/arxiv.2509.25346`) and **PerturBench** (2024, `10.48550/arxiv.2408.10609`). LLM/ML **prediction** of cellular perturbation outcomes. → Prediction benchmarks; not referees.

9. **SoundnessBench: Can Your AI Scientist Really Tell Good Research Ideas from Bad Ones?** (2026, 3 cites) and **Sound Agentic Science Requires Adversarial Experiments** (2026). → Evidence that refutation/soundness-first framing is an active, concurrent theme — relevant to M3's "partially anticipated" verdict.

10. **Tracking biological hallucinations in single-cell perturbation predictions using scArchon** (2025, `10.1101/2025.06.23.661046`). Consistency check on perturbation predictions. → Hallucination-detection on predictions, not an LBD-fed referee with per-hop experimental receipts.

*(No system surfaced across queries 1–17 performs Wayfinder's full conjunction. Negative-search result, not a proof of novelty.)*
