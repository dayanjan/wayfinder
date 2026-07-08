# Round 2 — Codex re-critique (repo-read)

**Position:** Claude’s revision addresses the substantive repo-contract problems: the HOP-0-only branch, full answer taxonomy, funnel numbers, CS figure path, and demo-video harness assumptions check out. I would not force a cold UNTESTED opener: a very short YES-first beat is defensible because it teaches that the same referee can support claims before it refuses them, but only if the handoff artifact stops carrying stale overclaims and the final script gives UNTESTED the first real dwell.

**Convergence:** still iterating

## All findings this round
### F-006 [P1] Calibrated-language fix is incomplete in the actual plan artifact
- sev4/lik4 correctness
- evidence: Claude says the video drops definitive/excluded wording, but the checked-in plan still says the hybrid montage includes “the definitive STAT6 exclusion” at docs/plans/demo_video_plan_2026-07-08.md:62. Repo memory/work-progress files also still contain “DEFINITIVELY EXCLUDED,” but the demo plan is the production-critical artifact.
- action: Patch the actual demo plan everywhere, not just the scene text: use “STAT6 confounder check” or “cis-artifact explanation refuted by this check,” and add a final script grep for discovered/proven/definitive/excluded before recording.

### F-008 [P2] Input-scope overclaim remains in the recommendation paragraph
- sev3/lik4 correctness
- evidence: Claude accepted the fix, but docs/plans/demo_video_plan_2026-07-08.md:64-66 still says “Type any gene→disease,” while the detailed build step later constrains disease selection to atlas-backed modules and gene selection to the A/measured universe.
- action: Replace the stale recommendation sentence with “choose a perturbation gene and an atlas-backed disease module,” matching the UI contract.

### F-010 [P1] The revised plan artifact is internally inconsistent with Claude’s accepted fixes
- sev4/lik4 correctness
- evidence: The actual plan still contains stale production guidance: Option B says the UI renders “the 4-hop receipt chain” at docs/plans/demo_video_plan_2026-07-08.md:61 even though SATB1 must render one HOP-0 card; Option C still says “definitive STAT6 exclusion” at line 62; the recommendation still says “Type any gene→disease” at lines 64-66; and the open questions still ask whether “leading with the funnel (Scene 1)” is best at lines 166-167 even though the revised arc no longer leads with a funnel.
- action: Before round 3 convergence, require one canonical patched plan with stale phrases removed and a single scene order. Treat the prose revision as not production-ready until the file itself is coherent.

### F-011 [P2] Builder-track positioning is contradicted by the demo plan’s Researcher-track label
- sev3/lik3 correctness
- evidence: The user/AGENTS framing says this is a hackathon Builder-track entry, but docs/plans/demo_video_plan_2026-07-08.md:3-4 labels it “Researcher track.”
- action: Correct the track label and explicitly map the video priorities to Builder scoring: live product interaction first, science depth second.

### F-012 [P2] The preflight gate proves one pass, but not repeatability under Streamlit reruns
- sev3/lik4 correctness
- evidence: The demo-video skill emphasizes fixture re-runnability and real screen-only actions; harness.mjs supports visible locator actions via act() at lines 178-184 and timing via sceneStart/untilT/sceneEnd at lines 114-128, while grep_gate.mjs forbids fetch/page.request/API shortcuts at lines 19-25. Claude’s preflight requires a Playwright smoke script clicking all three cases once, but does not require a second clean run or explicit waits for Streamlit rerun completion/results text.
- action: Make preflight require two consecutive screen-only smoke runs from a fresh browser context, with waits on visible result text for supported, untested, and refuted_for_c before recording.

## Dropped (addressed): F-001, F-002, F-003, F-004, F-005, F-007, F-009
## Escalated:
- F-006: Claude fixed the intended Scene 5 wording, but not all production-facing wording in the actual plan artifact; the stale “definitive STAT6 exclusion” phrase remains in the recommended surface table.
- F-008: Claude accepted the narrower input-scope language, but the checked-in plan still says “Type any gene→disease” in the recommendation paragraph.

**Next:** For final round 3, Claude should settle the canonical production plan: patch the stale artifact text, explicitly choose YES-first versus cold-UNTESTED, and define the repeatable two-run Streamlit preflight that must pass before recording.