# MEMORY.md — PyZoBot Arbiter Session Index

Lean cross-session index. The narrative lives in `memory/sessions/YYYY-MM-DD.md`;
the live dashboard in `WORK_PROGRESS.md`; the handoff in `memory/NEXT_SESSION.md`.
This file is the fast scan: where we are, what's decided, what happened lately.

## Current Status
**2026-07-07 — Scaffold + PM tooling bootstrapped.** Fresh hackathon repo. Plan =
`docs/plan.md` (v6). Session-lifecycle skills (`session-start`, `session-closer`,
`freshen`, `atomic-planner`) pulled in from the sibling Halcyon / generator projects.
**Next:** stand up the deterministic Validator tool (3-hop CSV lookup + KD-QC gate)
and prove the receipt-backed NO/YES loop on one real gene. See `memory/NEXT_SESSION.md`.

## Hard constraints (never lose)
- **NEW WORK ONLY** — every file authored during the event (started 2026-07-07); git history is the compliance proof.
- **Deadline: 2026-07-13, 9:00 PM ET.** Solo builder; async, interruptible.
- **Open source, MIT.** Claude for reasoning; Voyage for embeddings. Never OpenAI.
- **Every causal edge traces to a data receipt.** Calibrated language only. See `CLAUDE.md`.

## Key decisions (ADRs)
ADRs live in `memory/decisions/adr-NNN-*.md`. None recorded yet — record the load-bearing
build decisions here as they're made (embeddings provider, agent boundaries, verdict UX).

## Recent Sessions
| Date | Focus | Key outcome |
|------|-------|-------------|
| 2026-07-07 | PM tooling bootstrap | Session-lifecycle skills + doc scaffold added; handoff migrated to `memory/NEXT_SESSION.md` |

_Last updated: 2026-07-07_
