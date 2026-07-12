# V-AUDIT — agentic-methodology novelty audit (M5, M6, M7)

Owner: V-AUDIT. Scope: the three agentic-methodology claims (self-audit language critic;
headless scripting of an API-less workbench; cross-family adversarial replication lab).
Tool: `src.arbiter.lit.search.search_all` (live, Europe PMC / OpenAlex-class), 3–7 queries per claim.
Read: MASTER_REGISTER.md, §3.4 (methods), §4.5 + §4.6 (results).

**Framing note that governs all three verdicts.** M5/M6/M7 are, by the project's own thesis
(`CLAUDE.md`: "the tooling is the method/vehicle"), *supporting craft*, not the headline. The load-bearing
novelty is M1 (the referee conjunction) + the biology (B1/B2). The right referee question for each is not
"is this a new algorithm?" but "is this a **scientific contribution** or a **well-executed engineering /
QA practice**?" On the evidence below, all three are the latter — and, importantly, **the manuscript already
says so**, in unusually calibrated language. So the dominant risk is *not* that the text overstates; it is
that a referee discounts M5–M7 as plumbing. The defense is to keep them framed as method/vehicle and let
M1+biology carry the contribution. Where the text drifts toward implying these are novel *methods*, flag it.

---

## M5 — Actor–critic self-audit that enforces calibrated LANGUAGE on the platform's own output

**Restatement.** An independent reviewer model (Sonnet-class), at separate checkpoints, verified each
reported number against artifacts AND enforced calibrated scientific language on the manuscript-facing
output — flagging "validated"/"definitive" as overclaiming and removing them. Claimed distinct from
generic LLM-as-judge because the critic polices *hedging / calibrated language*, not *correctness*.

**Queries.** "LLM as judge scientific claims overclaiming"; "self-critique self-refine language model
output"; "Reflexion verbal reinforcement agent self-reflection"; "hedging overclaiming detection scientific
text calibrated language"; "actor critic verification LLM output constitutional AI reviewer model";
"speculative hedge detection scientific writing exaggeration press release".

**Key papers.**
- *Self-Refine: Iterative Refinement with Self-Feedback* (2023, arXiv:2303.17651, ~214c) — the canonical self-critique-then-revise loop.
- *Reflexion: Language Agents with Verbal Reinforcement Learning* (2023, arXiv:2303.11366, ~4260c) — verbal self-feedback agent.
- *Self-critiquing models for assisting human evaluators* (Saunders et al., 2022, arXiv:2206.05802, ~47c) — a model critiquing model output, the direct ancestor.
- *CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing* (2023) and *A Survey on LLM-as-a-Judge* (2024, arXiv:2411.15594; 2026 *Innovation* survey) — the LLM-as-judge field is mature and large.
- **Calibrated-language / overclaiming detection as an established NLP task** (this is the real hit): *An NLP Analysis of Exaggerated Claims in Science News* (2017, W17-4219, ~33c); *Can ChatGPT Understand Causal Language in Science Claims?* (2023, WASSA); *Recognizing Speculative Language in Research Texts* (2013); the CoNLL-2010 hedge-detection shared task; *RIGOURATE: Quantifying Scientific Exaggeration with Evidence-Aligned Claim Evaluation* (2026, findings-acl.1699); *Saying More Than They Know: A Framework for Quantifying Epistemic-Rhetorical Miscalibration in LLMs* (2026); *The Calibration Turn in AI-Assisted Research* (2026); *Refute-or-Promote: An Adversarial Stage-Gated Multi-Agent Review Methodology* (2026).

**VERDICT: PARTIALLY-ANTICIPATED (as method); NOT OVERSTATED (as written).**

**Reasoning.** Every *component* is prior art: (a) an independent LLM reviewer checking another LLM's output
= LLM-as-judge / self-critiquing models (2022–2024, huge literature); (b) the *specific* target — detecting
overclaiming / enforcing hedged, calibrated scientific language — is itself an established NLP task with a
decade of work (exaggeration-in-science-news 2017, hedge/speculation detection 2010–2013, and 2026 revivals
RIGOURATE / epistemic-rhetorical-miscalibration). So the claimed distinction — "critic polices calibrated
LANGUAGE, not correctness" — does **not** carve out virgin territory; it names a task other people already
study, just applied here to the pipeline's own manuscript-facing text in-loop. The only genuinely
under-published corner is the *combination*: an actor–critic pair inside one agentic scientific run where the
critic's job is language hygiene + receipt-consistency on the run's own report. That is a reasonable, narrow,
novel-in-combination bit of engineering discipline — not a novel algorithm or scientific finding.

**Scientific contribution or engineering practice?** Engineering / QA practice. It is *disciplined authorship
hygiene* implemented with a second model. It produces no new knowledge; it prevents the pipeline from
overstating knowledge. Referees will read it exactly that way.

**Moves science forward?** Marginally, and only as method. Its real value is rhetorical-integrity insurance
for *this* paper (n=1 anecdote: two words flagged and removed). It is not a result. The manuscript is candid
about all of this — it explicitly scopes the claim to "language hygiene plus receipt-consistency … not an
independent epistemic verification that the underlying biology is correct," and to "role, model, and
checkpoint independence … not independence across vendors." **That candor is why M5 is not OVERSTATED as
written.** Recommendation: keep the current hedged framing; do NOT let any downstream summary/abstract phrase
promote it to "a novel self-audit method for calibrated scientific language" — that phrasing *would* be
OVERSTATED against the 2017/2010 prior art. Present it as applied practice + honesty demonstration.

---

## M6 — Headless scripting of an API-less agentic workbench → replicable-in-principle agentic science

**Restatement.** Claude Science exposes no task-submission API; the loop drives its web UI headlessly
(browser automation, auto-approving sandbox cards), polls to completion, retrieves artifacts + audit records
— converting a click-once web session into a re-runnable, audited pipeline, with the full-scale run
reproduced "byte-for-byte" natively (against a workbench-local cache under a raise-on-live-call guard).

**Queries.** "reproducibility LLM agent scientific workflow analysis"; "browser automation reproducible
research pipeline web interface scraping"; "reproducibility of large language model outputs nondeterminism
scientific".

**Key papers.**
- *LMR-BENCH: Evaluating LLM Agent's Ability on Reproducing Language Modeling Research* (2025, arXiv:2506.17335, ~20c) — reproducibility of agentic LLM research is a benchmarked subfield already.
- *PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows* (2025) and *LLM Agents for Interactive Workflow Provenance* (2025) — provenance/audit for agentic workflows.
- *Replicating a High-Impact Scientific Publication Using Systems of LLMs* (2024, biorxiv 2024.04.08.588614).
- Nondeterminism-of-LLM-output line: *An Empirical Study of the Non-Determinism of ChatGPT in Code Generation* (2024, ~149c); *Defeating Nondeterminism in LLM Inference* (2025); *Understanding and Mitigating Numerical Sources of Nondeterminism in LLM Inference* (2025).
- **Browser/UI automation via LLM is a whole active area**: *MacroBench* (web-automation scripts, 2025); *AutoQALLMs: Automating Web Application Testing Using LLMs and Selenium* (2025); *DiLogics* (2023); *WebUI dataset* (2023); *LLMs applied to web scraping and web crawling: a systematic review* (2026).
- **The "is it science?" mirror**: *Workflow Closure Is Not Scientific Closure in Auto-Research Systems* (2026); *AI-Assisted Computational Reproducibility on the FABRIC Testbed* (2026); ReScience-C tradition.

**VERDICT: PARTIALLY-ANTICIPATED / ENGINEERING PLUMBING (LOW prior-art on the exact artifact, HIGH on the capability class).**

**Reasoning.** There is no paper on headless-scripting *Claude Science specifically* — that exact artifact is
new (it barely exists). But the *capability* — driving an API-less web app via browser automation to make it
scriptable/reproducible — is textbook Selenium/Playwright engineering (MacroBench, AutoQALLMs, DiLogics, a
2026 systematic review of exactly this). And "reproducibility of agentic-LLM scientific analyses" is not a gap
either: it is an actively benchmarked field (LMR-BENCH, PROV-AGENT, replication-with-LLM-systems, the whole
LLM-nondeterminism literature). So M6 sits at the intersection of two well-populated areas; the specific
mash-up is new only because the target platform is new.

**Scientific contribution or engineering practice?** Engineering plumbing, unambiguously. It is a driver +
auto-approver + poller + artifact-puller. Valuable, competent, reusable — but it is instrumentation, not a
scientific result or a scientific method. The paper's own words ("browser automation against a user interface
with no stable public contract") concede this.

**Moves science forward?** As enabling infrastructure, modestly — it makes *this* analysis re-runnable and
audited, which is genuinely good practice. The "byte-for-byte native reproduction" line needs a caveat the
text already supplies but a referee will still push on: the full-scale reproduction ran **against a local
cache under a raise-on-live-call guard (cache delta zero)** — i.e., a deterministic *re-computation of cached
inputs*, not a live re-derivation. That is a legitimate and honestly-labeled reproducibility check, but it is
the *weaker* of the two senses of "reproduce," and calling it "byte-for-byte native reproduction" risks
sounding stronger than "recomputed identical outputs from cached inputs." The live-authorship 12-gene run
(fresh generator, live APIs, flagship absent) is the more scientifically interesting liveness claim; lean on
that. Recommendation: keep M6 explicitly framed as method/vehicle (it is); resist any phrasing that implies
"replicable-in-principle agentic science" is a *new scientific paradigm* rather than good instrumentation.

---

## M7 — Cross-family adversarial clean-room replication lab as a verification method

**Restatement.** Five agents (3 Opus-class + 2 cross-vendor Codex), each re-deriving the finding from raw
supplementary tables under an adversarial mandate, two doing clean-room re-implementations importing none of
the pipeline code; unanimous pass; the adversarial process caught+corrected real errors (cluster-ID
misalignment, effect-size overstatement).

**Queries.** "multi-agent adversarial code replication reproducibility audit"; "cross-model ensemble
verification LLM different vendors agreement"; "clean room independent reimplementation computational
reproducibility verification".

**Key papers.**
- *When LLMs Agree, Are They Right? Auditing Self-Consistency and Cross-Model Agreement as Confidence Signals* (2026) — **directly** proposes cross-model agreement as a verification/confidence signal.
- *MEDLEY: a multi-model approach harnessing bias in medical AI* (2026) and *A Hashgraph-Inspired Consensus Mechanism for Reliable Multi-Model Reasoning* (2025) — multi-model / cross-vendor ensembling for reliability.
- *Diverse LLMs vs. Vulnerabilities: Who Detects and Fixes Them Better?* (2025); *Evaluating Multi-Agent AI Systems for Automated Bug Detection and Code Refactoring* (2025) — multi-agent code review.
- *From Reproduction to Replication: Evaluating Research Agents with Progressive Code Masking* (2025, arXiv:2506.19724); *LMR-BENCH* (2025); *An Agentic Approach Towards Replication Package Quality Evaluation* (2026); *Rollout Cards: A Reproducibility Standard for Agent Research* (2026) — agentic reproduction/replication as a method.
- *ReScience-C: A Journal for Reproducible Replications in Computational Science* (2018) — the human clean-room-replication tradition M7 automates.

**VERDICT: PARTIALLY-ANTICIPATED / WELL-EXECUTED PRACTICE.**

**Reasoning.** Each ingredient is prior art: cross-model / cross-vendor agreement as a verification signal
(When-LLMs-Agree 2026, MEDLEY, hashgraph consensus); multi-agent adversarial code review (bug-detection /
refactoring multi-agent systems 2025); clean-room independent re-implementation as a reproducibility gold
standard (ReScience-C since 2018; From-Reproduction-to-Replication 2025). M7 assembles these into a 5-agent
lab pointed at one finding. The assembly is sensible and the *cross-vendor* twist (Codex vs Claude) is a nice
hedge against single-family blind spots — but "ensemble across vendors to verify" is precisely the
When-LLMs-Agree / MEDLEY thesis, so the twist is anticipated, not novel.

**Scientific contribution or engineering practice?** QA / verification practice. It is a reproducibility audit
executed by agents. It establishes *computational robustness* of the reported numbers — which the manuscript
correctly says is "not biological validity." That is exactly the scope of a replication audit; it is not a new
verification *method* so much as an application of known ones.

**Moves science forward?** As evidence for *this* paper's numbers, yes and usefully — a hostile independent
re-derivation reproducing every headline number and *fixing* two real errors (the 74/90 → 90/100 cluster-ID
bug materially changed a confounder conclusion) is the single most credibility-earning thing in the
methodology section. But it is n=1 (one finding, one lab) and it is verification, not discovery. As a
*general method* it is PARTIALLY-ANTICIPATED and would not, on its own, clear a methods-venue novelty bar.
Recommendation: present M7 as *this finding's robustness evidence* (strong, keep it prominent) rather than as
"a new cross-family adversarial replication *method*" (weak claim against 2025–2026 prior art). The current
§4.6 text mostly does this ("evidence of computational robustness, not of biological validity") — hold that line.

---

## Bottom line for the operator (blunt)

None of M5/M6/M7 is a **standalone novel scientific contribution**. In referee terms:
- **M5** = disciplined authorship hygiene via a second model (LLM-as-judge + overclaiming-detection, both mature). Engineering/QA. n=1 anecdote.
- **M6** = browser-automation instrumentation of a new-but-generic web app (web-automation + agentic-reproducibility, both mature fields). Plumbing.
- **M7** = an agent-run reproducibility/verification audit (cross-model-agreement + clean-room replication, both prior art). QA. n=1 lab.

**They are real, competent, and honestly described** — the manuscript's calibrated wording keeps every one of
them from being OVERSTATED *as written*. Their legitimate role is exactly what `CLAUDE.md` says: method/vehicle
that makes the *biology* (B1/B2) and the *referee architecture* (M1) reproducible, audited, and honestly
hedged. That is a defensible and even admirable posture for a "researcher-who-builds" track. The failure mode
to guard against is any abstract/summary sentence that *promotes* M5–M7 from "how we kept ourselves honest and
reproducible" to "novel methodological contributions" — against the prior art retrieved here, that promotion
would draw a fair referee's "this is good engineering, not new science" rejection of the *novelty* claim
(though not of the paper, if M1+biology hold). Keep them as scaffolding; let M1 + the biology be the contribution.

---

## Retrieved evidence appendix — closest M5 (LLM-as-judge / calibrated-language) papers

| Year | Title | DOI / arXiv | Cites | Why it bounds M5 |
|---|---|---|---|---|
| 2022 | Self-critiquing models for assisting human evaluators (Saunders et al.) | arXiv:2206.05802 | 47 | Direct ancestor: a model critiques model output to help evaluators. M5's actor–critic is this pattern. |
| 2023 | Self-Refine: Iterative Refinement with Self-Feedback | 10.48550/arXiv.2303.17651 | 214 | Canonical self-critique→revise loop; M5 is a role-separated instance of it. |
| 2023 | Reflexion: Language Agents with Verbal Reinforcement Learning | 10.48550/arXiv.2303.11366 | 271/4260 | Verbal self-feedback agent; the "critic revises the run" primitive. |
| 2023 | CRITIC: LLMs Can Self-Correct with Tool-Interactive Critiquing | 10.48550/arXiv.2305.11738 | 57 | Critic + tools correcting LLM output. |
| 2024/26 | A Survey on LLM-as-a-Judge | arXiv:2411.15594 / 10.1016/j.xinn.2025.101253 | 38/— | Establishes LLM-as-judge as a mature, surveyed field — M5's genus. |
| 2017 | An NLP Analysis of Exaggerated Claims in Science News | 10.18653/v1/w17-4219 | 33 | **Overclaiming detection in science text is a decade-old NLP task** — the exact "calibrated language" target M5 claims as its distinction. |
| 2013 | Recognizing Speculative Language in Research Texts | — | 2 | Hedge/speculation detection in research writing (with CoNLL-2010 shared task) — same target as M5. |
| 2023 | Can ChatGPT Understand Causal Language in Science Claims? | 10.18653/v1/2023.wassa-1.33 | 8 | LLM judging calibration of causal/hedged language in science claims. |
| 2026 | RIGOURATE: Quantifying Scientific Exaggeration with Evidence-Aligned Claim Evaluation | 10.18653/v1/2026.findings-acl.1699 | 0 | Contemporary system for exactly "does this claim overstate its evidence?" |
| 2026 | Saying More Than They Know: Quantifying Epistemic-Rhetorical Miscalibration in LLMs | — | 0 | Frames overclaiming-vs-evidence as measurable miscalibration — M5's problem, named. |
| 2026 | The Calibration Turn in AI-Assisted Research | — | 0 | Positions calibrated/evidence-licensed language as a research-methods concern. |
| 2026 | Refute-or-Promote: Adversarial Stage-Gated Multi-Agent Review | — | 0 | Adversarial multi-agent review gating claims — neighbor to M5+M7. |

Cross-checkable by a different model: every row above is a real `search_all` hit from the queries listed
under M5; DOIs/arXiv IDs as returned by the tool.
