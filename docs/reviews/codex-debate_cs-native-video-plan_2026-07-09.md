# Codex debate — CS-native video plan (2026-07-09, 2 rounds, repo-read, --preserve-intent)

**Framing question:** Is the CS-native 3-minute video plan the strongest, most defensible Researcher-track
submission — and where does it overclaim, mislead, under-sell, or risk failing on Friday?

**Verdict:** the spine is sound and genuinely differentiated; the plan needed **honesty scoping baked into
the runnable narration** and **the confident NO made visible**. All accepted fixes are now applied to the
artifacts. Per-round detail in `codex-debate_cs-native-video-plan_2026-07-09/round_*`.

## Trajectory
- **R1 (Codex):** 10 findings. 2×P0 (capture-receipts-are-blockers-not-tuning; live-vs-cached too easy to
  misread), plus calibration (over-absolute "never drawn", STAT6 line over-closes) and — importantly — the
  plan **under-sells its own moat** (the confident NO is asserted, not shown).
- **R2 (Claude):** accepted 8, deferred 1 (hybrid fallback → documented contingency), partial-1 (Swanson
  timing). Revised narration for the load-bearing beats.
- **R2 (Codex):** **dropped F-006/F-009** (resolved), but **escalated the rest** with a decisive catch —
  the accepted fixes existed only in the debate text, **not in the runnable files** (F-011, P0). Raised
  F-012–F-016 (put the cached/live caption *on screen*; make the NO a *required frame*; use the revised
  wording *verbatim*; overlay rule; screenshot-source whitelist to avoid leaking stale "validated").

## Convergent findings (acted on — all applied to the artifacts)
| # | Fix | Landed in |
|---|---|---|
| F-002/F-012 | Live-vs-cached boundary as an **on-screen caption** in b5 + scoped b4 narration | `cs/narration.mjs`, `cs/scenes.mjs` |
| F-005/F-013 | **Visible NO receipt** (IL2 untested / SBF2 refuted) as a required b5 frame | `cs/scenes.mjs`, `cs/CAPTURE_PLAN.md` |
| F-003/F-014 | "six co-mentions, no direct NAB2→Th1/Th2→eczema chain" (not "never drawn") | `cs/narration.mjs` |
| F-004/F-014 | "a possible STAT6 cis-artifact refuted live; GWAS label stays a nomination" | `cs/narration.mjs`, `cs/scenes.mjs` |
| F-007 | Grounded endcap ("built the missing generation half — beside the test") | `cs/narration.mjs` |
| F-001/F-011 | **4 required frames = release blockers**, pre-capture first | `cs/CAPTURE_PLAN.md`, `SCRIPT` |
| F-008/F-015 | Overlay rule: screen-only b4/b6a; prepared artifact overlay for b5/b6b | `cs/CAPTURE_PLAN.md` |
| F-016 | Screenshot whitelist: reviewer flag from `stage5/review.json`; avoid raw loose JSON with "validated" | `cs/CAPTURE_PLAN.md` |
| F-010 | `ELLEVENLABS_API_KEY` spelling confirmed internally consistent; verify vs real .env Friday | (pre-flight) |

## Persistent disagreements
**None conceptual.** R2 was "still iterating" *only* because the fixes weren't yet in the files — now
resolved by applying them. The final Codex recommendation was explicit: **stop debating the concept; patch
the artifacts and pre-capture the four required frames.** Done (patch) + carried into Friday (frames).

## Preserve-intent check
**Spine intact — `convergence_sanding_warning: null` in both rounds.** Codex affirmed the differentiator
(generation + deterministic testing/refusal inside the workbench) is real and repo-backed, and never
drifted toward "a team that used Claude Science." Accepting F-002/F-005 *strengthened* the novel claim
(the refusal + generation both visibly live in the workbench) rather than sanding it.

## Recommended next move
Friday: pre-flight → **pre-capture the 4 required frames (blockers)** → assemble → gate → submit. The
concept is settled; execution risk is now bounded to those four screenshots + the live-CS auth refresh.
