# Codex-debate synthesis — CS-native demo video (multimodal, frame-grounded)

**Date:** 2026-07-10 · **Rounds:** 2 (converged, no sanding warning) · **Mode:** `codex exec` with a 12-frame
storyboard attached (`-i`) + transcript + captions + audio metadata, read-only repo access, `--preserve-intent`.
**Framing question:** having *watched* the rendered 2:52 video (as frames), is the six-agent panel's fix
register correct, complete, and correctly prioritized — and does the actual video surface anything the
text-only panel missed? Per-round artifacts: `codex-debate_cs-native-video_2026-07-10/round_0{1,2}_*`.

**Honest boundary (Codex flagged it too, F-125):** Codex saw the VISUAL track + read the transcript/captions;
it could NOT hear the cloned voice or music mix. Voice timbre / naturalness / music intelligibility / actual
caption-dwell are a **human listen-through QA item before upload**, not covered here.

---

## Headline

The panel and Codex **agree on substance**; Codex's contribution is **runtime discipline**. The video is
already 2:52 under a hard 3:00 cap, so the panel's full Tier-1 list can't all be *added* — and applying it all
would flatten the clean arc into "a list of qualifications" (live/cached → nomination → confounder → reviewer
→ R01). Codex re-scoped the register into a **minimal, mostly-free, SWAP-not-ADD** set that captures ~80% of
the judging gain while protecting the spine.

**Spine preserved (preserve-intent check):** the confident-NO moat, "the library and the lab on one bench,"
and the calibrated honesty all survived — Codex explicitly protected them (F-105) and warned against
over-correcting into a flashier or more defensive cut. No novel claim was sanded off.

**Convergence caveat:** Claude accepted ~all of round 1 (zero rejects), so round 2 was framed to *break* the
plan, not agree more. It did — the runtime re-scoping + two new scoping risks (F-130, F-135) are the value.

---

## FINAL merged pre-submission action list

### Tier 0 — repo integrity, before the repo goes public (P0; panel + Codex unanimous)
1. **Rewrite the stale README** — lead with the finding + Claude Science role + video link + reproduce steps +
   full data citation. (Async judges land here first.)
2. **Purge "validated"** repo-wide → "re-derived"/"receipt-backed" (`pyzobot_referee.py` `_synthesize_overall`,
   `receipt_chain.md`); then grep the whole repo for banned certainty terms *and* `C:/Users/…` paths.
3. **Fix the stale "Th1-associated" → "Th2-associated"** label in `receipt_chain.md`.
4. **Scrub personal Windows paths** from the demo-video configs + `app/smoke_referee.mjs`.
5. **Reconcile the dataset-license wording** (dataset = public-dataset provision, not "MIT").
6. **At publish:** CC-BY music credit + full data citation in the upload description; final secret-grep → public.

### Tier 1 — ONE video re-cut, minimal high-ROI subset (in ROI order; SWAP, don't ADD — stay < 3:00)
1. **[must-do, ~free] Frame-8 scope fix (F-095).** Change "referee verdict: supported" → **"program hop
   supported · eczema nomination inherited"** (split label: *Perturb-seq-backed: NAB2→Th1/Th2* vs *inherited
   nomination: eczema*). Zero runtime; protects the central calibration claim. **Highest ROI of all.**
2. **[must-do, SWAP] IL2 cold-open (F-015).** Open with **5–6s of IL2→UNTESTED** *before* a **shortened** title
   (cut title narration ~10s→~5s; trim one sentence across b1–b3 to hold < 3:00). Puts the distinctive refusal
   in the first 10s of triage. Must REPLACE, not insert.
3. **[must-do, ONE callout] STAT6 legibility (F-025).** Add a single zoom/callout on **frame 10** making
   **STAT6 +0.09 / adj_p 0.79 & NAB2 self −3.08** readable (the live receipts are currently too small at
   laptop scale). If time allows, frame-5 live-HTTP-counts second. **Drop the frame-6 callout.**
4. **[must-do, ~free] Scope "Thirty survive" (F-135).** → **"Thirty clean candidates survive the referee
   gates"** (pairs with #1 so "survive" ≠ disease-level discovery).
5. **[must-do if text-only swap] Replace the dense equals-chain caption (F-065).** Two plain captions:
   *"Live micro-sweep: generator + receipt path."* then *"Full 22,039 sweep: cached replay, same deterministic
   referee."* No new dwell.
6. **[must-do, ~free] Soften "hardest confounder" → "one key confounder" (F-055).** Narration only; keep the
   caption's "GWAS label stays a nomination."
7. **[nice-to-have, no new beat] Tighten the reviewer line (F-045).** Keep frame-11 dwell; revise the spoken
   line to *"Anthropic's scientific workbench checked the claim, flagged 'validated' and 'definitive', and I
   cut them."* Do NOT expand into a separate scene.
8. **De-number frame 8 but keep receipt texture (F-035 + F-115).** Cut AB/BC/AC_KNOWN/score/rank; keep
   22,039→30, ac_lit 6, effect 301, ALL_PASS, and the `stage1/receipt.md` receipt-strip cue. Folds into #1.

### CUT from the video (Codex overrides the panel here)
- **R01-rejection hook → SUMMARY ONLY (F-075/F-130).** Under the hard cap it's lower ROI than the items above
  and risks the "list of defenses" flattening. Keep it as one line in the **written summary**, not the video.

### Summary rewrite (non-video)
Lead with the confident-NO / the LBD-follow-up answer; add the eczema = GWAS-nomination honesty line; treat
"30" as illustrative and lean on the NAB2 receipt; carry the R01 sentence here.

### QA before upload (F-125)
Human listen-through: voice naturalness, intelligibility over the −20 dB music bed, and that each lower-third
stays on screen long enough to read.

---

## What Codex changed vs the six-agent panel
- **De-escalated the R01 hook** out of the video (panel Demo+Impact wanted it in; Codex: summary only, ROI).
- **One callout, not "make the live frames legible" broadly** — prioritized the STAT6 evidence frame.
- **Reviewer beat = a sharper line, not a new beat** (panel Claude-Use wanted "its own beat").
- **Added two scoping must-dos the panel implied but didn't localize:** frame-8 split label (F-095) and
  "thirty survive" wording (F-135) — both nearly free and both protect the calibration claim on-screen.
- **Elevated the meta-constraint:** the cumulative fixes must not turn the cut into qualifications; every
  caveat is a precision LABEL, not an apology.

## Provenance
Six-agent Claude panel (`judging-panel_cs-native-video_2026-07-10.md`) → 2-round frame-grounded codex-debate
(`round_0{1,2}_{claude.md,codex.json}` + `video-context.md` in `codex-debate_cs-native-video_2026-07-10/`).
Storyboard: `.claude/scratch/codex-video-debate/storyboard/*.png` (gitignored). MP4 out-of-band.
