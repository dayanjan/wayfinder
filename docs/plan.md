# PyZoBot — "Built with Claude: Life Sciences" hackathon build plan (v6)

**Status:** domain + substrate LOCKED · rules reconciled · **track committed: RESEARCHER** · **Date:** 2026-07-07
**Lineage:** v1 (harness stack) → v2 (deploy-first, de-scoped, Codex debate) → v3 (validation-not-generation thesis, grant-critique) → v4 (Perturb-seq substrate + "hypothesis referee") → v5 (winning strategy, Fable review — "receipt-backed NO") → v6 (official rules reconciled: new-work-only clean-room, open-source, team≤2, judging map) → **v7 (Researcher-track pivot: finding-first via Claude Science; tool = the method/vehicle)**

## 0. v7 — Researcher-track reframe (committed 2026-07-07)
**This section governs where it conflicts with the Builder-framed sections below (esp. §1, §6, §7, §11, §12); those are being re-aimed, not deleted.**

- **Track = RESEARCHER (committed), framed as *a researcher who also builds* (operator, 2026-07-08).** Operator applied as Researcher. Per the kickoff transcript the track is technically set at the *Submit* button (not hard-locked at application), and an independent Fable 5 review argued Builder is the stronger fit for a *referee tool* — but the operator has committed to Researcher. **The reframe resolves the tension without hedging:** we are a researcher who builds their own instruments (the referee, the LBD question-engine, the Claude-Science automation) *to ask and answer the research questions*. Finding-first stays the spine; the substantial builder-craft is presented as *evidence of a scientist who can build to get the science done*, not as a separate Builder pitch. Decision recorded; we execute finding-first and do **not** hedge (hedging is the only thing that triggers the "between two stools" risk).
- **Deliverable shift.** Researcher track asks for *"a discrete finding / trained model / analysis others can reproduce, and how Claude Science got you there"* (kickoff). So the deliverable is a **reproducible T-cell Perturb-seq FINDING**, derived **through Claude Science**, that another scientist can re-run. The **PyZoBot Arbiter referee is the METHOD/vehicle** that produces and presents the finding — shown as *how the finding was reached*, not as a product to adopt.
- **What carries over UNCHANGED (the moat is intact):** the thesis (**falsification / the receipt-backed NO**), the 3-hop validation chain (§3), the two anchors (known-true + non-obvious), the **knockdown-QC rigor gate**, and calibrated language. These are *more* persuasive to Researcher/Gladstone judges than to a demo-driven Builder panel.
- **What CHANGES under Researcher:**
  1. **Claude Science is REQUIRED and on the critical path** (the track mandates it). Install + placement runbook: `docs/claude-science-wsl-install-plan_2026-07-07.md` (debate-hardened; GATE-0 docs confirmed). Because there is no "just use pandas" fallback, a VCU managed-endpoint block is a **Day-1 escalation risk** — de-risk first.
  2. **Reproducibility is the product.** Lean on Claude Science's native provenance (code + environment + full message history per artifact) as the "others can reproduce" evidence. The finding must re-run from the receipts.
  3. **Video/README lead with the FINDING**, not a tool tour. The "NO with a receipt" is presented as a **scientific result** ("we refuted claim X against real Perturb-seq data; we caught artifact Y as *untested*, not *negative*"), with the Claude-Science workflow shown as the how. Infra/UI ~invisible.
  4. **Judging aim = Researcher rubric** (real reproducible finding + genuine Claude Science use + scientific rigor), plus the **track-agnostic Gladstone Special Prize** ("most potential to advance science overcoming disease") — very reachable with a real autoimmune-relevant gene→program→disease result. Note: the kickoff named explicit prize $ for the Builder track ($30k/$10k/$5k); Researcher has its own top-3 + the Gladstone award.
  5. **Compute unchanged in scale** (CPU pandas on the aggregated CSVs); Claude Science is the *workbench/orchestration + provenance* layer. The local RTX 3090 (24 GB, CUDA 13.2 in WSL) is an *optional* deeper-analysis bonus (embeddings), gated by GATE-GPU — NOT required for the finding.
- **Efficiency guardrails (Fable review):** timebox the Claude Science stand-up to ~half a day with a hard escalate-the-endpoint exit; skip persistence/GPU gold-plating; keep the anchor-biology validation as the scarce-attention sink.

## 1. Goal & posture
- **Event:** *Built with Claude: Life Sciences* (Anthropic × Gladstone), global virtual hackathon **July 7–13, 2026**, $100k credits, **Build track**.
- **Hard stop:** submit **July 13, 9:00 PM ET** (via CV platform); operator travels July 14. Effective window ≈ 6.5 days from the July 7 12:30 PM ET kickoff. **Play to win.**
- **True prize (operator, 2026-07-07):** finish a real problem to a *publishable* result. **Winning is the bonus; a paper is the floor.** Posture: **brave — explore and learn.**
- **Track:** Builder ("Build Beyond the Bench"). Datasets are listed as Researcher-track examples but are public and usable by a Builder tool; the referee still yields a *finding* as a byproduct (the paper).

## 1b. Rules compliance (from the official Participant Guide)
- **NEW WORK ONLY (strict):** everything submitted must be built from scratch during the event; no pre-existing work. → **Fresh repo, `git init` after the July 7 12:30 PM ET kickoff — the commit history is the compliance proof.** PyZoBot POC = *mental reference only, zero file reuse*. **No lifting** Halcyon `.deploy.yaml` or R01_Template `tools/`. Re-author fresh OR use maintained third-party libs (`pyzotero`, Biopython/Entrez). Third-party OSS libraries (LangChain, LlamaIndex, Streamlit, pandas, Voyage SDK) and public datasets ARE allowed.
- **OPEN SOURCE:** entire submission published under an approved OSS license (MIT/Apache-2.0). Commercialization is a *later*, separate concern — not this repo.
- **TEAM ≤ 2 → SOLO (operator's choice, 2026-07-07).** A human teammate is a coordination liability given the operator's async, snatched-time caregiving schedule. The **Claude Code + Codex agent fleet is the "team"** (interruption-tolerant force multiplication). Named user = an *archetype*, not a teammate; anchor validation = operator's grasp + data-driven receipts + Claude-drafted candidates to vet. Solo raises the stakes on ruthless scope + Day-1 money-shot insurance — both already in the plan.
- **Submission:** 3-min demo video (YouTube/Loom) + open GitHub repo + 100–200-word summary.
- **Banned:** rights-violations / unlicensed code, data, or assets.

## 2. The thesis (locked)
The NIH R01 (1R01LM015392-01) was ND — killed by one critique across all 3 reviewers: *"LBD generates an enormous number of hypotheses, almost none of which ever get followed up; the preliminary win came from expert review + experimental validation, which the proposed work drops."*

**We invert the flaw into the product.** PyZoBot v2 is not a hypothesis *generator* — it is a **hypothesis REFEREE**: given a mechanistic claim (from literature, or a researcher's hunch), Claude *agents* adjudicate it — gather literature evidence, then **validate each hop against real experimental data**, and return a **ranked verdict with a receipt for every hop**. The tool's job is *culling and grounding*, not spawning. This is simultaneously the winning demo, the "Built with Claude" story, the rebuttal to the killer critique, and a publishable method.

**The actual winning edge (sharpened, Fable review 2026-07-07): the confident, receipt-backed NO.** Every serious entry will "validate." The moat is *refuting a plausible-sounding claim live, with an experimental receipt* — including catching artifacts (failed knockdown → "untested," not "negative"). Falsification, not confirmation, is what a skeptical Gladstone audience trusts and what no copycat replicates. **Promote the knockdown-efficiency QC gate from a table row to a HERO feature** — distinguishing "no effect" from "knockdown failed" is the tell that a real scientist built this.

## 3. The validation substrate (LOCKED — T-cell Perturb-seq)
Domain = human CD4+ T-cell immunology. Spine = the **Marson/Pritchard genome-scale CD4+ T-cell Perturb-seq** dataset (22M cells; every expressed gene perturbed; Rest/Stim8hr/Stim48hr). We use the **precomputed, aggregated supplementary tables** (auth-free CSVs on GitHub, ~25 MB total, already downloaded) — NOT the 22M-cell raw matrices.

A complete **3-hop validation chain lives in these tables alone**, each hop with an experimental receipt:

| Hop | Table | Validates |
|---|---|---|
| 1. Gene → effect | `DE_stats.suppl_table.csv` (33,983 perturbation×condition rows: up/down genes, on-target effect, cross-donor/guide reproducibility) | Does perturbing gene G do something real & reproducible? |
| 2. Gene → program | `Th2_Th1_polarization_signature_DE_results...csv` (37,289 rows: per-gene log_fc/zscore/p in Th1/Th2 contrast) | Do G's effects shift a real T-cell program? |
| 3. Program → disease | `cluster_autoimmune_enrichment_results.suppl_table.csv` (5,237 rows: cluster→disease odds ratios + intersecting gene lists) | Does G's downstream cluster enrich for autoimmune disease/asthma/etc.? |
| QC gate | `guide_kd_efficiency.suppl_table.csv` (73,766 rows: `signif_knockdown`) | Distinguishes "no effect" from "knockdown failed" — the rigor point reviewers demanded. |

**Hop 3 is the payoff:** it is a *gene→disease association*, experimentally grounded — the heart of PyZoBot's thesis, but with a real receipt instead of a literature assertion.

**Optional bonus hops (time-permitting only):** Pollard DNA-regulatory-activity (regulatory DNA → gene) and Krogan PPI (protein → protein) — corroborating layers *where genes overlap*. Not required; Perturb-seq alone is a complete entry.

## 4. Compute (confirmed light)
Core loop = **pandas lookups on aggregated CSVs — CPU-only, laptop-scale, no GPU, no raw-cell download, no auth.** Colab Pro (GPU) is **stretch-only** (raw single-cell re-analysis, Pollard DL models, cell embeddings) and NOT on the critical path. Literature/KG embeddings are API-based (Voyage), not GPU. **Compute is a non-issue for the win** → the whole week goes to the agentic referee + demo, not data engineering.

## 5. The agent cast (the "Built with Claude" story)
Visible, adversarial agency — the operator's own red-team doctrine applied to science:
- **Proposer** — floats a mechanistic hypothesis from the literature (or takes the researcher's hunch).
- **Skeptic** — tries to *refute* it from the literature (adversarial; kills weak claims). *Real judgment → visible agency.*
- **Validator** — **calls the Perturb-seq tables as deterministic TOOLS** for the 3-hop receipts + KD-efficiency gate. *Deterministic, not an "agent" — this is what makes it trustworthy to scientists and kills the "why an LLM for a pandas lookup?" objection.*
- **Adjudicator** — issues the ranked verdict: supported / refuted / untested per hop, with calibrated confidence + a persistent **"what would falsify this"** line. *Real judgment → visible agency.*

Reserve *visible agency* for where real judgment lives (Skeptic, Adjudicator); the data checks are deterministic tool calls. The demo *shows the agents culling weak hypotheses live* — overproduction solved on screen. **Every causal edge on screen traces to a data receipt (OR / p-value / table row); Claude interprets receipts, it never asserts the biology.** De-emphasize the knowledge graph (minimal, legible 3-node provenance only — no hairball); the *verdict* is the UI.

## 6. Harness stack (clean-room — all written fresh this week)
Under NEW-WORK-ONLY, nothing is *lifted* from prior projects. Prior work contributes *knowledge/patterns only*; every submitted file is authored during the event. What we use:
| Layer | Built from | Role |
|---|---|---|
| Scaffolding | Kickstarter generates *fresh* files at event time (defensible: new files) — or a plain `git init` | Session/memory discipline. Policy = "Claude for reasoning/generation; Voyage for embeddings." |
| Deploy | **Simple managed host written fresh** (Streamlit Community Cloud / HF Spaces / Render) — NOT the Halcyon harness | Public demo URL + smoke check. **Video-first**; infra ≤ ~5s of video, not judged highly. |
| Product brain | Fresh Claude-native pipeline; PyZoBot POC = *reference only, no file reuse* | GraphRAG shape, re-authored. |
| Agentic referee | Claude agents (§5), written fresh | The star: adversarial validation/prioritization. |
| Validation data | Perturb-seq CSVs (§3) — public data, allowed | The experimental receipts. |
| Provenance | Maintained third-party libs (`pyzotero`, Biopython/Entrez) — NOT R01_Template tools | Literature receipt: title + DOI + source chunk per claim. |

Retrieval/persistence = LlamaIndex on-disk / SQLite. Third-party OSS libs (LangChain/LlamaIndex/Streamlit/pandas/Voyage) are allowed dependencies. Entire repo open-sourced (MIT/Apache-2.0).

## 7. Build order (7 days → July 13)
- **Day 0 (today):** ✅ data downloaded; confirm hackathon rules/portal + Build-track dataset eligibility; pick the anchor hypothesis (see §8).
- **Day 1 — walking skeleton + referee tracer:** password-gated Streamlit URL live + prod smoke; **stand up the Validator's 3-hop lookup against ONE real gene** end-to-end (proves the loop with real receipts, not a placeholder).
- **Days 2–4 (P0):** the full agent cast (Proposer/Skeptic/Validator/Adjudicator) live behind the URL; **select & lock the anchor pre-vetted discovery**; per-hop provenance + verdict UI; scripted ~90s video recordable.
- **Day 5 (P1):** generalizable "referee any claim" workflow; deploy hardened; fallback video recorded.
- **Day 6 (P2):** optional Pollard/Krogan corroboration hop; graph polish (no hairballs); second anchor.
- **Day 7:** deploy-verify + submission (video + repo + README) with buffer.

## 8. What we still need from the operator (domain brain)
1. **The named user (an archetype — no teammate needed):** name the Gladstone-adjacent user the tool serves (e.g. *"an immunologist with 22M Perturb-seq cells and no way to referee a mechanistic claim against them in 30 seconds"*). Solo is fine; the user is who the tool serves, not who builds it. *Optional-if-reachable:* an async gut-check from any scientist contact before submit.
2. **TWO anchor hypotheses** (not one), both operator-pre-vetted for biological truth:
   - a **known-true** one → the tool *re-derives* it (proves it works),
   - a **non-obvious** one → the wow ("recovers what we know AND surfaces what we didn't").
   Form: *"regulator gene G shifts program P implicated in autoimmune disease D."*
3. Confirm hackathon **rules/portal** (Build-track use of the dataset; submission format).

## 9. Scope ladder
- **P0 (by Day 4):** one agentic, builder-verified, non-obvious 3-hop discovery with per-hop experimental + literature receipts; scripted 90s narrative; recordable video.
- **P1 (by Day 5):** generalizable "referee any claim" workflow; deployed password-gated URL (video-first); prod smoke of the real query path.
- **P2 / cut:** Pollard/Krogan bonus hop, richer graph interactivity, second discovery, pgvector.
- **Hard cut:** not-P0 by Day 4 → dropped. Day 6 polish. Day 7 submit with buffer.

## 10. Execution model & risks
One linear builder thread; delegate mechanically-specifiable chunks (deploy skeleton, CSV-lookup Validator, provider adapters) to Codex. Builder's scarce attention → biomedical validation of the anchor.
Risks: (a) anchor hypothesis must be genuinely non-obvious AND true → operator pre-vets; (b) Claude extraction edges can be wrong → Skeptic agent + per-hop receipts are the correctness gate; (c) POC dependency reconstruction → frozen stack + deterministic fallback; (d) scope creep into Pollard/Krogan → they are P2 only.

## 11. Winning strategy (Fable review, 2026-07-07)

**The 90-second video arc (show, don't tell):**
- **0–10s — the wound:** on-screen, the actual NIH critique + grant number (1R01LM015392-01): *"generates hypotheses nobody ever validates. They were right. So I built the opposite."*
- **10–25s — a claim goes in** (plain English: gene → program → autoimmune disease).
- **25–55s — the cull (money shot):** feed N claims; the Skeptic + Validator **REFUTE** a plausible one with a real Perturb-seq receipt, OR flag a failed-knockdown as **UNTESTED** (not negative). Real table values on screen; verdict flips live. **2 of N survive.**
- **55–75s — the survivor:** supported hops with receipts; a real gene→disease edge grounded in experiment; persistent "what would falsify this."
- **75–90s — the turn:** "The tool the grant should have proposed. Live, open, referees any claim in this dataset today." Flash URL.
- **Single most memorable moment:** the tool saying **NO** with a receipt. Capture this rough on **Day 1** as insurance — don't let it depend on Day-4 polish.

**High-leverage moves (fold into build):**
- **"What would falsify this"** as a persistent UI element — a Popper flex this audience rewards.
- **README = mini method-paper** (doubles as the publishable-result skeleton — the true prize) with the R01 critique + grant number quoted verbatim.
- **Calibrated language everywhere:** "consistent with / re-derived / flagged for follow-up" — never "discovered/proven." One overclaim poisons the entry with scientists.
- **Infra ≤ ~5s of video.** Deploy/tunnel is a reliability signal, not a selling point to a science audience.
- **One independent scientist watches the 90s before submit** — cheapest signal on whether the wow lands with the target audience vs. engineering pride.
- **Tie prize→mission:** "with the credits, this scales from one dataset to every Perturb-seq atlas."

**To win:** make the tool say **NO** to a plausible claim, live, with a real receipt (incl. a failed-knockdown catch), opened by the dead grant's own critique, aimed at a named researcher. Lead with falsification + data receipts; keep graph and infra nearly invisible; two anchors (known-true + non-obvious).
**To lose:** an impressive 4-agent GraphRAG system, 60s of architecture, one happy-path success over a big graph, a claimed "discovery," and video time on the deploy pipeline.

## 12. Judging map (official criteria → our answer)
Aim every hour at the weights:
- **Demo — 30% (largest):** the live **NO-with-a-receipt** money shot; "genuinely cool to watch" + "findings you trust." 3-min video, tight arc (§11).
- **Claude Use — 25%:** the adversarial **agent cast** — Skeptic refuting, Adjudicator calibrating — "did they surface capabilities that surprised even us?" This is why the agency must be *visible where judgment lives* and *deterministic tools where it's a lookup* (§5).
- **Impact — 25%:** the **named user** (immunologist who must referee claims against 22M cells) + "could this become something people use." The generalizable "referee any claim" workflow proves the finding was reached with a reusable *method* a researcher built — not a one-off — which is exactly the "researcher who also builds" story.
- **Depth & Execution — 20%:** falsification rigor, the **knockdown-QC gate**, calibrated language, two anchors (known-true + non-obvious) — "pushed past the first idea… real craft."
