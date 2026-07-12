# Wayfinder — project map

Hackathon build (*Built with Claude: Life Sciences*, **Researcher track — a researcher who also builds**). A **hypothesis referee**: Claude agents adjudicate a mechanistic T-cell claim and return a verdict with a **receipt for every hop**. The framing: a researcher who builds their own instruments — the referee, the LBD question-engine, and the Claude-Science automation are tools built *to ask and answer the research questions*. The deliverable is a **reproducible T-cell finding + how Claude Science reached it**; the tooling is the method/vehicle, and the builder-craft is evidence of a scientist who can build to get the science done. Full plan: `docs/plan.md` (v7). This file is the lean map.

## Hackathon + what we're doing now
- **Event:** *Built with Claude: Life Sciences* hackathon (organized by **Cerebral Valley**), **Researcher track** ("a researcher who also builds").
- **Timeline:** started **July 7, 2026**; deadline **July 13, 2026, 9:00 PM ET** (see Hard constraints). Solo builder; async/interruptible.
- **Deliverable:** a reproducible T-cell finding (NAB2 → Th1/Th2 → atopic eczema, receipt-backed) + how Claude Science reached it — the referee, the LBD question-engine, and the headless Claude-Science automation are instruments built to get the science done.
- **Submission status: BUILT + FIRE-READY.** Repo `dayanjan/wayfinder` (private); say **"scrub and flip"** to run `SUBMIT_CHECKLIST.md` and flip it public. Demo video + 3-screen Streamlit app = the MVP.
- **Current post-hackathon thread:** a **manuscript for FRMA** (`docs/manuscript/latex/main.pdf`) hardened by a 13-agent **contribution/novelty audit** and a **claims↔experiments reconciliation** (below). Live state: `WORK_PROGRESS.md` + `memory/NEXT_SESSION.md`.

## Claims ↔ evidence traceability (READ-FIRST for any claim work)
`docs/CLAIMS_EVIDENCE_LEDGER.md` is the canonical **living index**: every manuscript claim (M1–M10, B1–B7, R1–R5) → status → the experiment artifact that supports/refutes it → primary source (S1–S11) → review-panel critique + resolution.
- **Anti-amnesia protocol (mandatory):** any claim audit / review / referee-response / revision reconciles against **BOTH** the literature **AND** the experiment corpus the ledger indexes — literature tells you if a claim is *novel*, the experiments tell you if it is *supported*; never one alone. (This exists because a 2026-07-12 literature-only audit forgot the Claude-Science confounder experiments and over-generalized the NAB2/STAT6 critique — 2 of 3 confounder channels were already experimentally closed.)
- Dated records under `docs/reviews/contribution-novelty-audit_2026-07-12/` and `docs/claims-vs-experiments_2026-07-12/` are **immutable evidence** (cite, don't edit); the ledger is the living index you update. Open gaps → `docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md` (G1 held-out eval = the publish gate).

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
