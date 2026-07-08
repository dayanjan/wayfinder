# Round 3 — Codex final critique (repo-read)

**Position:** The repo checks mostly support Claude's round-3 claims: the high-risk stale phrases around “any gene” and “4-hop receipt chain renders” are gone, the Researcher-track pivot is real in `docs/plan.md`, and the planned UI branches match the current `referee_triple` answer taxonomy. One production-facing inconsistency remains in the actual demo-plan artifact: it still carries obsolete debate-open-question text after Claude says the arc is settled.

**Convergence:** still iterating | sanding warn: None

**Dropped (addressed):** F-006, F-008, F-011, F-012
**Escalated:** F-010

### F-010 [P2] Canonical plan still contains stale open-question text after the arc was supposedly settled
- evidence: `docs/plans/demo_video_plan_2026-07-08.md` still says “Open question still on the table (debate R2)” at line 118 and still asks whether “leading with the funnel (Scene 1)” is best at line 182, even though the chosen arc no longer leads with a funnel and Claude's round-3 position explicitly settles fast YES-first over cold-UNTESTED.
- action: Remove the debate-open-question block and replace section 6 with final production watchpoints only: Streamlit-vs-notebook fallback trigger, 180s timing, and screen-only two-run preflight. State fast YES-first + long UNTESTED dwell as the settled arc.

**Production watchpoint:** the single thing to watch during production: does the recorded cut preserve the falsification spine by giving UNTESTED the first long dwell and making the refusal visibly live, not just narrated?