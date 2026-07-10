# 3. Materials and Methods

> **DRAFT v1 — for CS actor–critic review.** Numbers here MUST be reviewer-checked against primary
> artifacts (`stage1/sweep_Stim8hr.json`, `stage1/lbd_questions_Stim8hr.json`, `src/arbiter/lbd/`).
> Honors outline v1.2: approach-not-product; two receipt classes; three liveness claims distinct;
> role/model/checkpoint self-audit; the no-API driver given weight. Calibrated language. ~1,450 words.

---

## 3.1 Materials

**Perturbation data.** All adjudication runs against the aggregated supplementary tables of a
genome-scale CRISPRi Perturb-seq study in primary human CD4+ T cells [Zhu, Dann, Yan, … Marson 2025]:
(T1) per-perturbation differential-expression statistics, including an on-target effect flag and a count
of downstream differentially expressed genes; (T2) a Th1/Th2 polarization-signature enrichment per
perturbation, reported for two independent marker contrasts; (T3) a cluster-to-autoimmune-disease
enrichment (odds ratio and FDR per module–disease pair); and (T4) per-guide knockdown efficiency with a
significance call. We work at the 8-hour stimulation condition unless noted. No raw single-cell matrices
are used; for the one confounder check that needs genome-wide differential expression, the study's
deposited matrix is read lazily from public object storage (byte-range reads, no bulk download).

**Disease and program vocabularies.** The program **B** is fixed to Th1/Th2 polarization, with two term
arms: process terms (e.g. "Th2 cells", "T helper 2") used for the gene–program signal, and marker terms
(GATA3, IL-4, IFN-γ, T-bet) additionally used for the program–disease signal, since disease literature
legitimately cites markers. The disease set **C** comprises 12 immune diseases, each pinned to a MONDO
identifier and re-verified live against Open Targets search and the EBI Ontology Lookup Service. This
verification is load-bearing: MONDO and EFO identifiers differ, and a wrong identifier makes Open Targets
report "no known association" for every gene, spuriously inflating apparent novelty everywhere.

**Literature and association sources.** Co-mention counts come from Europe PMC `hitCount` queries (all
terms quoted); curated gene→disease genetic-association scores come from the Open Targets GraphQL API.

**Model cast.** Inside the workbench (Section 3.4) the author role is an Opus-class model (Claude Opus
4.8); the independent reviewer role is a Sonnet-class model (Claude Sonnet 5), invoked at separate
verification checkpoints; lightweight inline sampling is handled by a smaller model. All
biological interpretation is confined to these models reading deterministic receipts; no model computes a
receipt.

## 3.2 Candidate generation

**An answer-free gene universe.** The candidate gene set **A** is defined from the perturbation data
alone, before any disease information is consulted. A gene enters **A** if it clears the knockdown-QC gate
(≥1 guide with a significant knockdown call in T4), has a significant transcriptional effect (an on-target
significance flag or a nonzero downstream-DE count in T1), and shows a significant Th1/Th2 shift (T2
adjusted *p* < 0.05). Construction never reads the disease table T3, so the gene list cannot be
contaminated by the answer it will later be tested against; each gene carries its downstream-DE count
forward as an effect-strength prior. At the 8-hour condition, **A** contains 3,935 genes.

**Five deterministic signals.** For each (gene A, disease C) pair we compute: `ab`, the Europe PMC
co-mention count of A with the Th1/Th2 process terms; `bc`, the co-mention count of the program terms with
C (constant per disease); `ac_known`, the Open Targets genetic-association score of A for C (zero when
absent — the novelty signal); `ac_lit`, the direct A–C co-mention count (computed only for referee
survivors, to bound API cost); and `effect`, the downstream-DE count from T1. Every signal is a
deterministic lookup.

**Gate and ranking objective.** Eligibility requires all of: `ab ≥ ab_gate` (a universe percentile,
default the median, which removes candidates that look novel only because the gene is understudied),
`bc ≥ 3`, and `ac_known ≤ 0.1` (no established genetic link). Raw `ac_lit` is deliberately *not* in the
gate — hard-gating on zero co-mention would exclude every well-studied strong regulator and reward
obscurity. Eligible candidates are ranked by a balanced objective,

```
score = min( z(log1p ab), z(log1p bc) ) + β·z(log1p effect) − w·log1p(ac_lit) − w2·ac_known,
```

with β = 1, w = 1, w2 = 3, and z-scores taken over the universe. The `min(z_ab, z_bc)` term makes the
bridge *balanced* — one strong axis cannot rescue a weak other; `β·z(effect)` is the "loud in the data"
reward; the final two terms push novel-yet-bridged candidates up without hard-excluding them. The
objective was designed offline (its structure fixed before running), the only human judgment in an
otherwise mechanical pipeline.

**Order of operations.** The sweep builds **A**, prefetches the per-disease `bc`/`ac_known` (12 calls
each) and per-gene `ab`, applies the gate, then runs the deterministic referee *first* (it is local and
free) to keep only chain-supported survivors, and only then computes `ac_lit` and the final score for
those survivors. At the 8-hour condition this funnels 3,935 genes → 22,039 eligible (gene, disease) pairs
→ 43 disease-supported → 30 clean full-chain nominations.

## 3.3 The referee

The referee adjudicates one triple at a time as a four-hop chain, each hop reading a specific receipt:

- **Hop 0 — knockdown QC.** Did the perturbation actually work (T4)? If no guide reaches a significant
  knockdown, the triple is returned **untested** — never as a negative. This is the gate that converts a
  failed experiment into an honest "we cannot say," rather than a false "no effect."
- **Hop 1 — effect.** Did the (real) knockdown produce a reproducible transcriptional effect (T1): a
  nonzero downstream-DE count, on target, without an off-target flag?
- **Hop 2 — program.** Do the downstream effects shift the Th1/Th2 program (T2)?
- **Hop 3 — disease.** Does the perturbed gene's downstream signature fall in a module enriched for the
  specific disease (T3: odds ratio, FDR)?

A triple is **supported** only if the full chain holds with a nonzero, positive effect; effect-zero chains
are demoted to **supported-weak**, off-target-flagged chains to **supported-flagged**, and a failed effect
hop yields **refuted-effect**; failure at the specific-disease hop is **refuted-for-C**. The confident *no*
lives in these demotions, all deterministically computed. One honesty point belongs in Methods, not only
in Limitations: because **A** is preselected on program-significance, *within the funnel* the program hop
is a tautology (no eligible gene can fail it), so the program hop discriminates in an individual triple's
receipt — as a reported quantity — not as an independent filter on funnel survivors.

## 3.4 The agentic loop, and how the instrument is operated

Generation, adjudication, and provenance assembly were run inside Claude Science, a persistent-kernel
agentic scientific workbench, in which an author model writes and runs analysis code and an independent
reviewer model verifies the result at separate checkpoints (Section 3.1).

**Operating an instrument that has no API.** Claude Science exposes no programmatic task-submission
interface: analyses are ordinarily driven by hand in its web interface, which makes each run a one-off,
hand-paced event rather than a reproducible procedure — human clicking becomes the bottleneck at exactly
the moment when keeping pace with the twin floods of data and literature is the whole point. To make the
workbench *scriptable*, we drive its web interface
headlessly. A browser-automation driver, orchestrated from a coding agent (Claude Code), loads a saved
authenticated session, submits the task prompt, and **auto-approves the workbench's in-loop sandbox
prompts — working-directory, code-execution, and network-access cards — for fully unattended, zero-click
operation**; it then polls the run to completion and retrieves the emitted artifacts together with the
workbench's own audit records. We are candid that this is browser automation against a user interface with
no stable public contract (Section 5.3); it is nonetheless what converts a click-once web session into a
re-runnable, audited pipeline, and it is, to our knowledge, an under-appreciated route to reproducible
*agentic* science: where no direct API exists, principled UI automation is the honest substitute.

**Provenance and self-audit.** Every run is captured in the workbench's own audit store, from which we
draw model identities, per-step costs, and the reviewer's checks. The reviewer verifies each reported
number against the underlying artifacts and enforces calibrated language on the author's output; in this
work it flagged overstated words ("validated", "definitive") and they were removed. We characterize this
independence precisely: it is *role, model, and checkpoint* independence — a distinct reviewer model at
distinct verification points — within a single model family, not independence across vendors.

**Three claims about liveness, kept distinct.** We separate what ran live from what was replayed, because
conflating them would overstate the result. (i) *Full-scale reproduction*: the generation pipeline ran
unchanged over the entire 3,935-gene universe inside the workbench, but against a workbench-local cache of
previously captured literature/association responses, under a guard that raises on any live network call
(cache delta zero) — a faithful recomputation, not a live crawl. (ii) *Live authorship*: in a separate,
smaller run the workbench was given only the method and wrote its own generator from scratch, making live
Europe PMC and Open Targets calls; the headline gene did not appear in that small run's top candidates, so
nothing was cherry-picked, and a Stage-0 probe independently confirmed live external access from the
kernel. (iii) *Cross-family independence*: replication with a different vendor's models is kept external
by design (Section 4.6). Reported this way, the workbench supplies generation, data-grounded
adjudication, and a language self-audit; cross-model independence is supplied from outside it.
