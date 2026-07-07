# MEMORY.md — PyZoBot Arbiter Session Index

Lean cross-session index. The narrative lives in `memory/sessions/YYYY-MM-DD.md`;
the live dashboard in `WORK_PROGRESS.md`; the handoff in `memory/NEXT_SESSION.md`.
This file is the fast scan: where we are, what's decided, what happened lately.

## Current Status
**2026-07-07 (PM) — Track=RESEARCHER; Claude Science live; Validator BUILT (P0 loop hit Day 1).**
Plan = `docs/plan.md` (v7 Researcher reframe, §0). Claude Science 0.1.16 installed under WSL,
sandbox verified, and **driven headlessly via Playwright** (no task CLI exists). Through it, the
**referee/Validator was built and demonstrated** with real receipts: EGR2 = YES, IL2@Rest = the
UNTESTED artifact-catch, SLC1A5 = REFUTED. Artifacts in `docs/perturbseq-qc_2026-07-07/`.
**Next:** build the thin **LBD question-proposer** (`docs/lbd-proposer-spec.md`) — LBD generates the
untested questions, the referee answers them; also vet anchor biology + confirm judging weights.
See `memory/NEXT_SESSION.md`.

## Hard constraints (never lose)
- **NEW WORK ONLY** — every file authored during the event (started 2026-07-07); git history is the compliance proof.
- **Deadline: 2026-07-13, 9:00 PM ET.** Solo builder; async, interruptible.
- **Open source, MIT.** Claude for reasoning; Voyage for embeddings. Never OpenAI.
- **Every causal edge traces to a data receipt.** Calibrated language only. See `CLAUDE.md`.

## Key decisions (ADRs)
ADRs live in `memory/decisions/adr-NNN-*.md`. None recorded yet — record the load-bearing
build decisions here as they're made (embeddings provider, agent boundaries, verdict UX).
- [Hardware + Claude Science placement](memory/decisions/hardware-and-claude-science-placement.md) — RTX 3090 works in WSL; runtime on C:(SSD), bulk data on D:(HDD), G:/H: are cloud. `.wslconfig` raised 8→32 GB.
- [Hackathon track + facts](memory/decisions/hackathon-track-and-facts.md) — **track committed: RESEARCHER** (finding-first via Claude Science); prizes/deadline/rules from kickoff transcript; Claude Science now critical path.
- [LBD question-engine reframe](memory/decisions/lbd-question-engine-reframe.md) — **the strategic heart:** LBD *generates the questions* (fills the "rich dataset, no question" cold-start gap), Claude Science + data *answers* them. Spec: `docs/lbd-proposer-spec.md`.

## Recent Sessions
| Date | Focus | Key outcome |
|------|-------|-------------|
| 2026-07-07 | PM tooling + repo | Session-lifecycle skills + doc scaffold; handoff → `memory/NEXT_SESSION.md`; API key verified active; private repo `dayanjan/pyzobot-arbiter` created & pushed |
| 2026-07-07 (PM) | Claude Science + Validator | Researcher-track commit; Claude Science installed on WSL + driven via Playwright; QC/join-map + referee (Validator) built through it — YES/UNTESTED/REFUTED demonstrated with receipts; 6 artifacts in `docs/perturbseq-qc_2026-07-07/`; hardware fully characterized; 3-round codex-debate + independent Fable review on the install plan |

_Last updated: 2026-07-07 19:30 (session close)_
