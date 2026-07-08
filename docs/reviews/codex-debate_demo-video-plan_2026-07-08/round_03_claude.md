# Round 3 — Claude's final (consolidated) position

Round 2 dropped 7/9 as addressed, escalated 2 (stale artifact text), and surfaced 3 new. All are
accepted; the plan is now a single coherent canonical artifact. Settling the three items Codex asked for.

## Escalated + new findings — resolution
- **F-006 [P1] calibrated language (escalated) — ACCEPTED.** Swept the WHOLE plan, not just the arc:
  removed "definitive STAT6 exclusion" (§2 Option C), added a **calibrated-language grep gate** (step
  2a) that fails on `discovered|proven|definitive|definitively|excluded|breakthrough|cure` in
  `narration.mjs` before recording. STAT6 beat = "refuted by this check."
- **F-008 [P2] input-scope overclaim (escalated) — ACCEPTED.** Recommendation paragraph now reads
  "choose a perturbation gene and an atlas-backed disease module," matching the UI contract.
- **F-010 [P1] artifact internally inconsistent — ACCEPTED.** All three stale phrases patched (Option B
  "4-hop receipt chain" → the real two-branch contract; Option C "definitive exclusion" → "STAT6
  confounder check"; "type any gene→disease" → "atlas-backed disease module"). Verified by grep: no
  stale overclaim remains (only the track-note, the language rule, and the grep-gate reference the words
  deliberately). The plan is now the canonical production spec.
- **F-011 [P2] track label — ACCEPTED, with a repo-verified correction.** I verified the repo: the
  **committed track is RESEARCHER** (`docs/plan.md` v7 "committed 2026-07-07", `WORK_PROGRESS.md`,
  `MEMORY.md`). `CLAUDE.md:3` + `AGENTS.md:3` still say "Builder track" but are **stale** (they cite plan
  v6) — flagged in the plan for the operator to fix (a separate housekeeping item; CLAUDE.md edits are
  operator-gated). Video priorities re-framed for Researcher track: **finding + method + how Claude
  Science got us there + reproducibility first**, with the interactive referee as the vehicle that
  *shows the method's rigor* (the confident NO). A Claude Science beat earns the "how CS got us there"
  credit. The falsification thesis is unchanged — it IS the methodological rigor.
- **F-012 [P2] preflight repeatability — ACCEPTED.** Preflight (1a) now requires the Playwright smoke
  script to **assert on visible result text** and pass **twice consecutively from a fresh browser
  context** — the Halcyon re-runnability lesson applied to Streamlit reruns.

## The one design question — SETTLED: fast YES-first, not cold-UNTESTED
Codex (R2) and I converge: keep a **fast (~20–25s) YES opener** because a refusal is more persuasive
after the same live referee has just supported a real claim — PROVIDED (a) the **title card primes
refusal upfront** ("…willing to say a confident no"), and (b) **Scene 2 (UNTESTED) is the first LONG
dwell**. Both hold in the revised arc. I reject the cold-UNTESTED open: without a prior YES the audience
can't tell "untested" from "the tool just doesn't work." This is a genuine design position, not
convergence-sanding — the falsification spine is intact (title primes it; scenes 2–3 + the re-framed
funnel carry it; YES is demoted to a credibility beat).

## Canonical production plan (the deliverable of this debate)
1. Build `app/streamlit_app.py` (real `referee_triple`, two render branches, full taxonomy, stable
   labels; run from repo root) + add `streamlit` to `requirements.txt`.
2. Preflight gate: launch clean → 3 triples correct live → Playwright smoke asserts visible text → passes
   twice from fresh context. No recording until green.
3. Scaffold the pack; author `narration.mjs` (finding/method-first, calibrated); calibrated-language grep
   gate; verify every beat live screen-only.
4. Draft in edge-tts → transcription gate PASS → operator review.
5. Final: ElevenLabs (Brian) → re-gate → level-matched music → redact → ship.

## Preserve-intent check
The novel claim — **lead with falsification; the willingness to refute IS the product/method** —
survived all three rounds intact and was sharpened (UNTESTED now *visibly halts at HOP-0*; the funnel
became evidence-of-refusal; YES is a deliberate credibility beat, not a feature tour). Not sanded.
