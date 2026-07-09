# Claude Science — intelligence mined from the 2026-07-08 live demo

**Source `[DEMO]`:** the Wednesday hackathon live session — **Alec Tarashansky** (product
development lead, Claude Science; PhD bioengineering / cross-species scRNA-seq; ex-CZI Cell-by-Gene
4 yrs), hosted by **Jason Bigman** (community team). ~63 min, "Built with Claude: Life Sciences."
Transcript: `01-hackaton details/Voice 260708_115846 Claude Science demo_..._timestamped-notes.md`
(4,318-line turbo voice transcription). Version on stage: same `0.1.16-dev.20260707` line as ours,
launched at `localhost:9700`.

This doc is the **net-new + correcting** intelligence from that demo (the source our main
`claude-science-capabilities.md` §15 had flagged as "not yet mined"). It was produced by a 5-agent
parallel pass over the transcript (lenses: demo-narrative / orchestration / skills-connectors-compute
/ artifacts-provenance-UI / deltas-QA-limits; raw notes in `.claude/scratch/cs-capability-mining/`).
Every claim carries a `[hh:mm:ss]` transcript timestamp so it's re-checkable.

> **Confidence convention:** `[DEMO]` = stated/shown on stage. Where the demo *corrects* or *can't
> confirm* a main-doc claim, it's called out. Voice-transcription guesses are flagged `⚠`.

> **✓ EMPIRICALLY CONFIRMED 2026-07-08** — much of this was then verified live against our own install
> (`cs-capability-tests_2026-07-08/RESULTS.md`): reviewer **= Sonnet 5** (DB-confirmed), primary **=
> Opus 4.8/high**, inline model **= Haiku 4.5**; the reviewer **caught a planted count inconsistency
> (fail)**; MCP-as-skill programmatic lookup returned **real Ensembl IDs**; `host.delegate` is **gated
> behind a session Delegation toggle** (`host.llm_batch` is the ungated path). Full receipts via the
> **`operon-cli.db`** audit store — see `claude-science-test-plan_2026-07-08.md`.

---

## 1. Headline net-new primitives (not in the main doc)

### 1.1 The `host` kernel SDK — the core orchestration primitive `[00:50:48–00:53:00]`
Delegation and harness-control happen **through the kernel**, via a built-in object **`host`**
available to every kernel/agent — "a bridge that lets the agent interact with its harness
programmatically… honestly why the harness is so powerful."
- **`host.delegate(...)`** spawns sub-agents **programmatically** and **collects their results
  programmatically** (live demo: "spawn 50 sub-agents that write a haiku" → the execution log shows
  a `host.delegate` fan-out + gather in one loop).
- `host` also **calls MCPs**, **creates/publishes skills** to your claude.ai account, and does
  **artifact rename/delete** — all composable in code.
- **`host` can sample the LLM directly** `[00:52:24]`: chunk a 100-page PDF into ~200 pieces, fire a
  **Haiku** yes/no-relevance call per chunk, filter programmatically → "RLM-shaped search." A cheap
  inline map-reduce that never pollutes the main context.

**Why it matters for us:** this is the mechanism behind both "deterministic DB lookups" and
"programmatic sub-agent fan-out." A referee built *inside* CS would route its Skeptic/Adjudicator
delegation and its receipt-fetching through `host` in kernel code.

### 1.2 MCPs are represented as SKILLS, invoked programmatically `[00:22:29–00:23:14]`
"MCPs are actually represented as **skills instead of tools**, and the agent invokes them
programmatically." Fetching 100 genes from Ensembl/BioMart in Claude Code = 100 tool calls; in CS =
**one for-loop that filters before anything enters context** ("very RLM style"). Every MCP ships a
synthesized skill with instructions for programmatic invocation. This is the scaling story — "scales
to a very large number of capabilities" with good **search primitives** over skills/MCPs.

### 1.3 "Folding" compaction + full context telemetry `[00:36:00–00:39:20]`
A per-session graph plots, per turn, **blue = tokens actually sent to the API** vs **red =
counterfactual total context**. Shown session: **red = 4.7M tokens, live context never exceeds
~400K.** Compaction "gradually folds earlier parts of the conversation while maintaining coherence"
— no discontinuity, finite context, "incredibly long" sessions.
- **Context breakdown telemetry:** ~6% assistant prose, **~60% tool calls**, ~5% compaction,
  **~20% the automated reviewer**, ~6% artifact-provenance generation, ~0.4% memory extraction.
  (Cost note: reviewer ≈ 1/5 of token spend.)

### 1.4 Forced self-sight → visual self-correction `[00:06:46–00:07:21]`
"We force the agent to **see everything it produces**." When it makes an image, that image is
**auto-injected into the next LLM turn**, so it self-corrects (e.g. doing QC, sees a cluster just
past a threshold → nudges the threshold on its own). This is the concrete "compute, don't
confabulate" mechanism — look at real output rather than assert.

### 1.5 Reviewer mechanics, made concrete `[00:53:53–00:57:17]` — directly on our thesis
- Forks a reviewing agent at **checkpoints during the run AND at the very end**; operates on
  **short, small conversation windows**; checks **factual accuracy of claims AND artifact quality**
  (prose + artifacts).
- On an issue it **injects a finding** — a **warning** or a **hard fail** — that the agent responds
  to, **fixes, version-bumps the artifact**, and the finding shows **resolved**.
- **Live catch:** "the rebuilt deck states **8 of 10** targets have small-molecule chemistry, but
  the slide's own compound table lists only **seven**" → agent corrects to seven, version-bumps,
  resolved. *(This is exactly the falsification/receipt-check pattern our referee is built around.)*
- **Custom rubric** layers on top of the built-in reviewer (owl icon); reviewer's own transcript is
  viewable. The demo didn't state the reviewer's *model*, but our 2026-07-08 live test **confirms it
  from the DB: `verification_checks.reviewer_model = "claude-sonnet-5"`** (3 separate REVIEWER frames
  ran at checkpoints; the primary OPERON ran `claude-opus-4-8`, effort high). So Opus-primary +
  Sonnet-reviewer is now first-hand + DB-confirmed.
- **Roadmap:** a **parallel "shadow" reviewer** that watches the *whole* session for on-plot /
  long-horizon-goal drift (not just factual accuracy) — not released yet. On-thesis for a referee.

### 1.6 Sub-agents do the *science*; configurable/dynamic sub-agent model `[00:48:26–00:50:41]`
Sharpest architectural framing of the demo: **in Claude Science, sub-agents run the actual
analyses** (his project has **200 executed**), while a **root coordinating agent stays free to
chat** and orchestrates — the **inverse** of Claude Code (where sub-agents do low-level
explore/search). Settings › General exposes **effort level (default High)**, **default session
model**, and a **sub-agent model** (default = parent; Sonnet 5 selectable). Claude "can dynamically
choose the model it delegates to." Endorsed pattern: **Opus parent supervising Sonnet-5 workers**
against very detailed briefs (Sonnet = strong instruction-follower) — i.e. our own tiered-manager
pattern, native inside CS.

### 1.7 Specialists = full-CRUD, Claude-authored agent profiles `[00:23:50–00:29:19]`
"Skills, connectors, and specialists are the three holy-grail primitives." A **specialist** = a
custom agent with restricted skills + restricted connectors + custom instructions (incl.
communication style — "write to me as if you were a cat"; "talk to me only through HTML dashboards +
SVGs"). Claude has **create/rename/update/delete** on specialists and can **spawn one on the fly,
delegate, then tear it down**. **Skills can encode multi-agent behavioral state machines** — demo:
a **"brainstorming skill" spins up 20 differentiated agent profiles, delegates for varied POVs,
synthesizes, then tears them down** (our six-hats/red-team pattern, expressible inside CS).

### 1.8 Fully-interruptible harness + unified annotation steering `[00:16:57–00:19:07]`
- **Any message interrupts** a mid-sentence agent; mid-code-execution, it **backgrounds the cell**;
  sub-agents (and the parent steering them) are equally interruptible.
- **Annotations unify across ALL artifact types** — figures, PDFs, markdown, **individual
  HTML-dashboard elements**, and **the transcript itself** — into one tray, **drained to the agent
  on the next message**. Vision-grounded (asked "what is this?" of an unlabeled UMAP point to prove
  it sees pixel location). Pins are drag-droppable; send can target the **existing OR a new
  session**. Workflow tip: read output as a **"lagging tail,"** annotate to steer while it runs.

### 1.9 Other net-new
- **Reproducible-block provenance is LLM-reconstructed, ~99.9% byte fidelity** `[00:07:53]`, with a
  fallback chain: standalone block → execution log → raw message history (+ frozen conda env
  snapshot). Quantifies the doc's "reproducible by construction."
- **Memory = 4 default tiers** (global / project / session / artifact) **+ user-defined categories**
  (demo made a "foot gun" category) `[00:40:00]`. Plus a **per-compute-provider memory** where
  Claude notes infra foot-guns and learns to work around them `[00:13:33]`.
- **Live kernel introspection** `[00:10:29]`: the notebook panel is an IPython-like input — type
  `print(lin)` to read the agent's live variables ("careful not to step on its toes").
- **Register conda envs from GitHub repos** incl. **editable-mode installs** `[00:31:59]`.
- **Version diff view** (V1↔V2) for text/markdown/LaTeX `[00:19:31]`.
- **Files view + remote-filesystem browsing** (SSH host / Modal machine / cloud bucket) `[00:32:51]`.
- **Usage-velocity guardrail** `[00:53:00]`: "~43% of your 5-hr limit per hour" → snooze / stop
  sessions (stopped sessions resumable).

---

## 2. Corrections / refinements to `claude-science-capabilities.md`

| # | Main-doc claim | Demo correction | ts |
|---|---|---|---|
| 1 | §10 "No native Windows — WSL2 only" | **Native Windows imminent — "next week or two"** (≈ mid-July 2026). Changes our install story. | `01:00:22` |
| 2 | §5 leads with "uv-managed `.venv`/micromamba" | Presenter is **conda-first** throughout ("managing your **conda** environments"; R+Python chosen for conda support). uv may coexist but was never mentioned. | `00:14:56` |
| 3 | §9 "no task CLI; web UI only" | **Explicitly confirmed** — "someone could run Claude Science headlessly, which is currently **not supported**." Validates the `drive-claude-science` Playwright approach as the only scripting path today. | `00:46:39` |
| 4 | (right panel assumed Jupyter) | **Not Jupyter** — "nothing to do with Jupyter beyond there being cells… very custom, limited, no plugins." | `00:11:56` |
| 5 | §1 "plan comes with a confidence estimate" | **No confidence estimate shown** in this demo (not contradicted; sourced from keynote). | `00:20:57` |
| 6 | §1 reviewer "distinct model (Sonnet 5)" | Demo confirms a **forked agent** but **does not state a separate model**. Keep "Sonnet 5" tagged `[OURS]`, not presenter-confirmed. | `00:54:20` |
| 7 | §4 SSH hosts (key-based) | **Password-protected SSH = in progress**, not yet supported. And **remote SSH forfeits the persistent kernel** (batch only, "more frictionful"). | `00:13:10` / `00:34:24` |
| 8 | §12 seed projects | Demo used a **different** live corpus: an AnnData h5ad ("analyze this data"), a **CELLxGENE liver** plan-mode pipeline, and his real **138-species** paper. His personal project holds **5,613 artifacts**. | `00:05:37` / `00:20:51` / `00:57:58` |

---

## 3. Q&A digest (audience question → answer)

1. Right panel Jupyter + plugins? → **No**, custom viewer, no plugins `[00:11:47]`.
2. Large sequencing data / HPCC? → Customize › Compute: **Modal / NVIDIA BioNeMo / any SSH host**
   (reads `~/.ssh/config`); Claude submits+manages jobs; per-provider memory. Password SSH in
   progress `[00:11:23]`.
3. More languages (Rust/Julia)? → **Python + R only** today (conda-driven; R↔Python interconvert);
   Julia "great option," Rust unsure `[00:14:07]`.
4. Git best practices / auto-connect repo? → Credentials › **GitHub** (auto-detect or PAT); grant a
   r/w folder; Claude does all git ops; can register venvs from repos `[00:29:22]`.
5. MacBook: local or Anthropic servers? max data size? → Runs **wherever you launch it**; all
   code+files local; scale out via AWS/SLURM/pod over SSH (loses persistent kernel) `[00:33:29]`.
6. Where are papers/literature stored? → hidden **`~/.claude-science`** `[00:35:47]`.
7. Context/memory/data limits? → the **folding graph** (4.7M→400K) — effectively finite context,
   very long sessions `[00:36:47]`.
8. Local data-access rules (e.g. UK Biobank can't be shared)? → **DEFERRED** — "I'm not a lawyer…
   will follow up in **Discord**." (Open compliance question.) `[00:36:56]`
9. Connect CS directly to Claude Code CLI? → Works internally, **not productized**; easiest =
   **Claude Code remote connector** `[00:43:07]`.
10. What can Claude Code do that CS can't? → "Very little — it's a matter of **token efficiency**.
    For **pure coding** use Claude Code; **everything else → Claude Science**" (CS has bash +
    edit-file) `[00:44:05]`. **[TIP]**
11. Terminal/CLI version of CS? → **No CLI planned**; *might* add a terminal *inside* CS to launch
    Claude Code; long-term = "**Science SDK**" `[00:45:53]`.
12. CS ↔ Claude "Design" links? → Both visual-artifact/HTML-annotatable; CS lacks Design's
    render-and-iterate HTML primitives (may add) `[00:46:55]`.
13. Opus-delegator steering Sonnet-workers? → **Yes**, Settings › sub-agent model; can work well
    given detailed briefs; "don't be surprised if outputs are worse" — try & report `[00:48:15]`.
14. How to ensure output is correct? → **the reviewer** (§1.5; the 8-vs-7 catch) `[00:53:42]`.
15. One-click publication export (data+code)? → **ROADMAP**; his 138-species paper written entirely
    in CS with a full provenance dependency graph; "download script" approximates it; "we're very
    close, no promises on robustness" `[00:57:23]`.
16. Windows + roadmap? → §2 + §4 `[01:00:08]`.

---

## 4. Roadmap / coming-soon
- **Native Windows — "next week or two"** `[01:00:22]`.
- **Parallel "shadow" reviewer** watching the whole session for on-plot / long-horizon drift `[00:55:36]`.
- **Team/lab collaboration** — shared infra; shape TBD `[01:00:44]`.
- **Claude auto-builds & registers custom MCP servers** (wrap any API, zero manual work) `[01:01:30]`.
- **Custom artifact renderers + an artifact-renderer marketplace** (genome browser / physics sim /
  CAD / breadboard) `[01:02:05]`.
- **"Science SDK"** — headless CS powering science apps like the Agent SDK powers agent apps `[00:45:53]`.
- Better **artifact organization + export/download** (admitted rough edges) `[00:59:49]`.
- Next live session: **Friday, Sukrit Silas (Gladstone Institute)** `[01:03:04]`.

---

## 5. Limitations / gotchas (admitted on stage)
- **Artifact sprawl** — 5,613 artifacts in one project; star-artifacts broke live; Cmd-K search is
  the workaround `[00:16:37]`.
- **Storage is a deliberately hidden `~/.claude-science`** dir (stops renames that break
  provenance); export UX rough (a download button visibly failed) `[00:33:57]`.
- **Remote SSH loses the persistent kernel**; **Python+R only**; **key-based SSH only**;
  **compliance guidance deferred**.
- **Provenance reconstruction not guaranteed perfect**; export-graph robustness "no promises."
- **Multi-agent = high token burn** (velocity guardrail exists; reviewer ≈20% of tokens).
- **Beta instability** — several demo features glitched (version not regenerating, star, download,
  orphaned provenance IDs from a cloned DB).

---

## 6. Best-practice TIPs
- **Steer continuously via annotations while it runs** — fully interruptible; don't wait on a 3-hr cell.
- **Plan-first for big multi-step tasks** — the plan is an iterable artifact + live dashboard.
- **Build specialists** to fix scope + communication style; let Claude author them.
- **Turn on the reviewer and customize its rubric** — "one of the most load-bearing pieces."
- **Import skills from a GitHub repo; use memory tiers + custom categories** for a persistent partner.
- **Choose permission scope deliberately** (Once / conversation / project / Global-with-warning).
- **Curate the network allowlist** for sensitive data (anti-exfiltration).
- **Leave the walled garden** via Download script / notebook (reproducible zip).

---

## 7. Playwright automation cheat-sheet (for `drive-claude-science`)
- App at a **localhost port** (ours 8765; demo 9700). Left = chat/transcript; right =
  notebook/artifact viewer.
- **Composer** has: upload, **plan dropdown**, send. **Sending any message interrupts** a running agent.
- **Locate artifacts via Cmd-K** search; project default view = **Artifacts**, with a **Files** toggle.
- **Approval cards can appear anytime** — code / **MCP-use** / **network-domain** / **usage-velocity**.
  Scope labels are **exactly**: `Allow once` / `Allow for this conversation` / `Allow for this project`
  / `Allow globally` (Global shows a big warning). The current `cs-drive.js` `APPROVE` regexes cover
  "allow for this conversation/session", "always allow", "allow", "approve", "yes," — **verify they
  also catch the MCP-use and usage-velocity cards** (see Phase-3 hardening task).
- **Provenance** opens from an artifact → tabs Messages / Code / Execution Log / Environment / Review.
- **Known-flaky:** star, download menu — don't hard-depend.
- **Ground truth = artifact files** under `~/.claude-science/orgs/<org>/workspaces/<ws>/`, not the
  scraped text tail.

---

## 8. TESTABLE-CAPABILITY INVENTORY (the bridge to Phases 2–3)

What we can actually verify by driving our own install headlessly. Legend for **Testability**:
**T1** = drive a prompt, verify from produced artifacts (cleanest); **T2** = drive a prompt, verify
from a UI screenshot/scrape (state we can't get as a file); **T3** = needs UI state our headless
driver reads poorly — may need a `cs-drive.js` extension; **N/A** = can't test on our hardware/plan.
This is a *draft* for Codex to refine in Phase 2.

| # | Capability | Test | Verify | Testability |
|---|---|---|---|---|
| C1 | `host.delegate()` programmatic fan-out | Prompt: "in the kernel, use `host.delegate` to spawn 5 sub-agents that each return one immune-cell fact; collect + tabulate." | Execution log shows `host.delegate`; a table artifact with 5 rows. | T1 |
| C2 | `host` inline LLM sampling (Haiku map-reduce) | Prompt: "chunk this text into N; call the model per chunk for a yes/no; filter." (supply a small text) | Artifact/log shows per-chunk calls + filtered result. | T1 |
| C3 | MCP-as-skill programmatic DB lookup | Prompt: "for these 5 genes fetch canonical IDs from a gene DB in one loop; return a table." | Table with 5 resolved IDs; log shows a loop, not 5 tool calls. | T1 |
| C4 | Plan mode → approve → execute w/ parallel sub-agents | Send a 4-step prompt via the **plan dropdown**; approve. | Plan artifact (multi-phase); sub-agent briefs+outputs; final artifacts. | T2/T3 (needs plan-dropdown click) |
| C5 | Reviewer catches a planted inconsistency | Turn reviewer on; prompt a summary that will contain a self-inconsistent count. | A **finding** (warning/fail) + agent fix + version bump. | T2 (reviewer UI) |
| C6 | Forced self-sight self-correction | Prompt: "make a scatter; if any point is an outlier past 3σ, notice it and adjust." | Two figure versions + text noting the self-correction. | T1 |
| C7 | Persistent kernel reuse | Prompt A loads/derives a variable; prompt B (same session) reuses it without recompute. | Log shows reuse, no reload. | T1 |
| C8 | R ↔ Python interconvert | Prompt: "compute X in Python, hand the dataframe to R for a ggplot." | A ggplot artifact + both-language log. | T1 |
| C9 | Specialist create → delegate → teardown | Prompt: "create a single-cell specialist, ask it one question, then remove it." | Specialist appears/disappears; its answer. | T2/T3 |
| C10 | Skill-encoded multi-agent state machine (mini "brainstorm") | Prompt: "spin up 4 differentiated persona sub-agents on a question, synthesize, tear down." | Synthesis artifact citing 4 POVs; log shows fan-out+teardown. | T1 |
| C11 | Provenance completeness (repro block + env + review) | After any figure, open its provenance. | Standalone code block + env snapshot present + runnable. | T1 (repro block downloadable) |
| C12 | 4-tier memory write/read | Create a custom memory category; later session reads it. | Memory persists across sessions. | T3 (memory UI) |
| C13 | GPU biomodel via skill (we have RTX 3090 in WSL) | Prompt a light ESMFold/ESM-2 embed on a short peptide. | Structure/embedding artifact; env installs torch+CUDA. | T1 but heavy — **de-risk cost first** |
| C14 | Interruptibility / annotation steering | Start a long task; send a steering message mid-run. | Task redirects; cell backgrounds. | T2/T3 (timing-sensitive) |
| C15 | Compaction on a long session | Run a long multi-step task; open the context graph. | Red≫blue, live context bounded. | T2 (context UI) |

**Phase-2 question for Codex:** which of C1–C15 are worth spending live CS runs on tonight vs
noting as "confirmed-by-demo, low marginal value to re-verify"; the best *single* combined prompt
that exercises several T1 capabilities in one run (per the "combined live-fire" doctrine); and how
to harden `cs-drive.js` for the new card types (MCP-use, usage-velocity) and the plan-dropdown.

---

*Companion to `docs/claude-science-capabilities.md` (the full curated list). Raw per-lens notes:
`.claude/scratch/cs-capability-mining/pass-{A,B,C,D,E}-*.md`.*
