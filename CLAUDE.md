# PyZoBot Arbiter — project map

Hackathon build (*Built with Claude: Life Sciences*, **Researcher track — a researcher who also builds**). A **hypothesis referee**: Claude agents adjudicate a mechanistic T-cell claim and return a verdict with a **receipt for every hop**. The framing: a researcher who builds their own instruments — the referee, the LBD question-engine, and the Claude-Science automation are tools built *to ask and answer the research questions*. The deliverable is a **reproducible T-cell finding + how Claude Science reached it**; the tooling is the method/vehicle, and the builder-craft is evidence of a scientist who can build to get the science done. Full plan: `docs/plan.md` (v7). This file is the lean map.

## The thesis (don't lose this)
The edge is the **confident, receipt-backed NO** — refuting a plausible claim with a real experimental receipt, and catching artifacts (failed knockdown -> *untested*, not *negative*). Falsification, not confirmation, is the moat. The knockdown-QC gate is a **hero feature**, not a footnote.

## Hard constraints
- **NEW WORK ONLY.** Every submitted file is authored during the event (started July 7, 2026). No reuse of prior projects (PyZoBot POC is *reference only*, zero file copy). Git history is the compliance proof.
- **Open source, MIT.** Entire repo is public.
- **Deadline: July 13, 2026, 9:00 PM ET.** Solo builder; async, interruptible workflow — keep `memory/NEXT_SESSION.md` current so any session resumes cleanly.
- **Claude for reasoning/generation; Voyage for embeddings** (Anthropic has no embedder). Never OpenAI.

## Conventions
- **Every causal edge shown traces to a data receipt** (OR / p-value / effect size). Claude interprets receipts; it never asserts biology.
- **Calibrated language only:** "consistent with / re-derived / refuted / untested / flagged." Never "discovered/proven."
- **Data lookups are deterministic tools**, not "agents." Visible agency is reserved for judgment (the Skeptic weighing literature, the Adjudicator calibrating confidence).
- Compute is CPU-only (pandas over the aggregated CSVs). No GPU, no 22M-cell raw matrices.

## Structure
```
docs/plan.md            # the v6 build plan (thesis, agent cast, 3-hop substrate, judging map)
data/                   # public Perturb-seq supplementary tables (fetch via fetch_data.sh; gitignored)
src/arbiter/            # the tool (fresh code)
tests/
memory/NEXT_SESSION.md  # async handoff — canonical (read/written by session-start & session-closer)
MEMORY.md               # lean session index (status, decisions, recent sessions)
WORK_PROGRESS.md        # live dashboard (phase, milestones, blockers, progress log)
memory/                 # sessions/, decisions/ (ADRs), lessons-learned.md, patterns.md
```

## Session workflow (PM skills)
Async, interruptible, solo. Use the session-lifecycle skills at the boundaries:
- **`/session-start`** — at the top of a session: reads the handoff, cross-checks state, briefs you.
- **`/session-closer`** — at the end: writes the session log, syncs `MEMORY.md`/`WORK_PROGRESS.md`, refreshes `memory/NEXT_SESSION.md`, commits housekeeping (or checkpoints).
- **`/freshen`** — drift check across the PM docs.
- **`/atomic-planner`** — decompose a workstream into 1–3h testable task cards.

Codex delegation + review skills (`codex-rescue`, `codex-review-diff`, `codex-spike`, …) are user-level and already available.

## Judging weights (aim every hour here)
Demo 30% - Claude Use 25% - Impact 25% - Depth 20%. See `docs/plan.md` section 12.

## Delegation
Solo + agent fleet. Delegate mechanically-specifiable chunks (data-lookup tools, provider adapters, deploy) to Codex; keep judgment (anchor vetting, verdict UX) local. Cross-agent brief: `AGENTS.md`.
