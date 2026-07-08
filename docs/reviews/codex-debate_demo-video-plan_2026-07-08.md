# Codex-debate synthesis — PyZoBot Arbiter demo-video plan (2026-07-08)

**Framing question.** How best to improve the quality of PyZoBot Arbiter's 3-minute demo video before
putting the pipeline into production — the demo-surface decision, the narrative arc, and the
production/preflight/Potemkin/timing risks. Solo builder; deadline 2026-07-13; hackathon judged
Demo 30% / Claude Use 25% / Impact 25% / Depth 20%.

**Mode.** 3 rounds, `--preserve-intent`, **repo-read** (Codex ran from the repo with read-only file
access and verified every claim against `referee_triple.py`, the notebook, `sweep_Stim8hr.json`, the CS
figure, the `demo-video` skill, and `CLAUDE.md`/`AGENTS.md`). Per-round artifacts in
`docs/reviews/codex-debate_demo-video-plan_2026-07-08/`.

## Trajectory
- **R1 — 9 findings** (2 P0, 5 P1, 2 P2), all repo-verified. The two big ones: **F-001** the arc
  contradicted its own falsification-first thesis (opened with funnel + YES); **F-002** the real
  `referee_triple` returns *only HOP-0* on gate failure, so the UNTESTED case must **visibly halt at
  HOP-0** (a gift — the hero feature made literal). Plus: incomplete `answer` taxonomy (F-003), Option A
  not zero-risk (live S3 cell in the notebook, F-004), funnel over-compression (F-005), uncalibrated
  "definitively excluded" (F-006), missing streamlit dep/preflight (F-007), "any gene→disease" overclaim
  (F-008), unproven screen-only automation (F-009).
- **R2 — dropped 7/9 as addressed**, escalated 2 (stale overclaim text still elsewhere in the artifact),
  surfaced 3 new: artifact internally inconsistent (F-010), **track-label contradiction** (F-011 —
  plan/repo say Researcher, CLAUDE.md/AGENTS.md say Builder), two-run repeatability preflight (F-012).
- **R3 — converged.** Dropped 4/5, zero new substantive findings, one residual P2 bookkeeping nit
  (stale "open question" text after the arc was settled) — now patched.

## What changed in the plan (accepted, all verified)
1. **Arc re-spined around falsification** (F-001): title primes refusal → **fast YES** (credibility,
   ~20–25s) → **UNTESTED centerpiece, first long dwell, visibly halting at HOP-0** → REFUTED → funnel
   re-framed as *evidence-of-refusal at scale* → CS-figure depth.
2. **UI contract matched to the real code** (F-002/F-003): two render branches (gate-fail HOP-0-only vs
   gate-pass 4-hop) + the full `answer` taxonomy badge mapping.
3. **Honesty/calibration** (F-004/F-005/F-006/F-008): Scene 5 uses the pre-rendered CS figure (no live
   S3); funnel narrated at the true grain (22,039 → 43 → 30); "definitively excluded" → "refuted by this
   check" + a calibrated-language grep gate; "any gene→disease" → "atlas-backed disease module."
4. **Preflight hardened** (F-007/F-009/F-012): streamlit dep + launch + 3 live triples + Playwright smoke
   asserting visible text + **two consecutive fresh-context runs** before recording.
5. **Track resolved** (F-011): committed track is **RESEARCHER** (plan v7); CLAUDE.md/AGENTS.md "Builder"
   are stale (flagged for operator). Video priorities re-framed finding/method/Claude-Science-first.

## Persistent disagreement — resolved, not sanded
The one live design question (cold-UNTESTED open vs fast-YES-then-UNTESTED) **converged with reasoning
on both sides**: keep the fast YES opener because a refusal only means something after the same live
referee has supported a real claim — *provided* the title primes refusal and UNTESTED gets the first
long dwell. This is a defended design position, not consensus-drift.

## Preserve-intent check — PASSED
The novel claim (**lead with falsification; the willingness to refute IS the product/method**) survived
all three rounds and was *sharpened*, not sanded: UNTESTED now visibly halts at HOP-0, the funnel became
evidence-of-refusal, and the YES was consciously demoted to a credibility beat. No sanding warning fired
in any round.

## The production north star (Codex's final watchpoint)
> Does the recorded cut preserve the falsification spine by giving **UNTESTED the first long dwell** and
> making the refusal **visibly live** (the chain halting at HOP-0 on camera), not just narrated?

## Recommended next move
The plan (`docs/plans/demo_video_plan_2026-07-08.md`) is production-ready. Build order: Streamlit referee
UI → preflight gate (green twice) → pack + narration (finding/method-first, calibrated) → edge-tts draft
→ transcription gate → operator review → ElevenLabs final + music → redact + ship. Fallback to Option A
(drive the pre-executed notebook) if the UI misses its timebox.
