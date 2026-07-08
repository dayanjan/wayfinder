# MEMORY.md — PyZoBot Arbiter Session Index

Lean cross-session index. The narrative lives in `memory/sessions/YYYY-MM-DD.md`;
the live dashboard in `WORK_PROGRESS.md`; the handoff in `memory/NEXT_SESSION.md`.
This file is the fast scan: where we are, what's decided, what happened lately.

## Current Status
**2026-07-08 (full-close) — M3+M4 DONE; finding REPLICATED + all confounders CLOSED (incl. definitive STAT6).**
LBD question-proposer built end-to-end (`src/arbiter/lbd/`; spec v2 debate-hardened; MONDO ids;
`referee_triple` adapter). Full Stim8hr sweep: **22,039 → 30 clean supported**; headline
**NAB2 → Th1/Th2 → atopic eczema**. **Independently replicated** (5-agent lab, unanimous PASS,
`docs/replication/`). Confounders stress-tested; the **DEFINITIVE STAT6 cis-check** (authors' deposited
genome-wide DE via lazy S3 read — `docs/nab2_stat6_definitive_check.py`) shows **NAB2-KD leaves STAT6
unmoved (log2FC +0.09, p 0.79) → cis/shadow EXCLUDED**. Verdict = genuine, novel, NAB2-specific Th1/Th2
regulator (nomination re causality, per the paper). Full provenance trail committed (`docs/provenance/`).
**Next:** M5 submission artifacts — evidence-chain **Jupyter notebook** + **Claude Science evidence chain**
+ 3-min demo video (fresh session). See `memory/NEXT_SESSION.md`.

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
| 2026-07-08 | LBD proposer + finding (autonomous) | Spec hardened v1→v2 (3-round repo-read codex-debate, 9→3→0); fresh tool layer `src/arbiter/lbd/` (verified); disease ids MONDO-resolved; `referee_triple` exact-disease adapter; Codex consult fixed scoring+full-chain bug; full Stim8hr sweep 22,039→30 clean supported; **finding NAB2→Th1/Th2→atopic eczema** (near-novel, receipt-backed) |
| 2026-07-08 | Validation + source-paper vetting | 4-agent literature audit (new `src/arbiter/lit/`) → both links 0-papers novel; STAT6/EGR/cis confounders stress-tested & argued-against; **5-agent independent replication unanimous PASS** (`docs/replication/`); source-paper read → **reframed as novel reproducible NOMINATION, disease link flagged**; paper in `references/` + analysis repo recorded; ~8 commits |
| 2026-07-08 | Definitive STAT6 check + provenance (full-close) | Preserved full raw provenance trail (`docs/provenance/`, 52 artifacts); **definitive STAT6 cis-check** via lazy S3 read of authors' genome-wide DE → **NAB2-KD leaves STAT6 unmoved → cis/shadow EXCLUDED**, verdict upgraded to genuine novel NAB2-specific regulator; decided M5 = evidence-chain notebook + Claude Science chain + demo video |

_Last updated: 2026-07-08 (full-close)_
