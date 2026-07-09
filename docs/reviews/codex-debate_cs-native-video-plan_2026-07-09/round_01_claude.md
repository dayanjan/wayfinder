# Round 1 — Claude's opening position

**Framing question:** Is the CS-native 3-minute video plan (spine, narrative arc, beat sheet,
honesty/calibration, and feasibility against the built assets + the actual CS conversations) the
strongest, most defensible Researcher-track submission — and where does it overclaim, mislead,
under-sell, or risk failing on Friday?

## The position (what the plan claims)

1. **Spine.** Scientists face two exponential floods — literature (>1M papers/yr) and omics (millions
   of measurements/sample) — and discoveries hide in the gap. Literature-based discovery (Swanson ABC)
   surfaces implicit gene→program→disease hypotheses; large-scale omics has the mirror problem (answers
   with no questions). The differentiator: build the **LBD-generation half INSIDE Claude Science**, so
   hypothesis *generation* and *testing* run on one platform, each answering the other's central
   criticism (LBD's untestable-hypothesis flood; omics' question-less answers).

2. **Exemplar + moat.** Demonstrated on the Marson-lab CD4 T-cell Perturb-seq data: 22,039 machine-
   generated hypotheses → a deterministic referee culls with a receipt at every hop and confidently says
   **NO** (failed knockdown → *untested*, not false-negative) → 30 survive. Standout: **NAB2 → Th1/Th2 →
   atopic eczema**, a connection the literature never drew; the hardest confounder (STAT6 cis-artifact)
   refuted live against the authors' own genome-wide data; and the platform **self-checks** (a Sonnet-5
   Reviewer killed a calibrated-language overclaim).

3. **Format.** A 3-min screen-only video, entirely **CS-native** (skip the Streamlit app), assembled via
   the existing demo-video harness (STORAGE_STATE auth to CS), ElevenLabs "Brian", transcription-gate
   acceptance. 6 beats: two-floods → core-facility pain → Swanson graphic → CS-builds-LBD-live → referee-
   culls+NAB2 → self-check. Submit **EOD Friday**.

4. **Honesty posture.** NAB2 is a **nomination** (never "proven/discovered"); the therapeutic direction
   (brake/UP-modulate) stays OUT of the cut; the "CS builds LBD live" beat uses the **micro-sweep**
   (genuinely live, independently re-verified), never implying the full 3,935-gene sweep was a live
   crawl; context stats kept soft.

## Risks I already see (self-identified — attack these harder, and find the ones I missed)
- (a) The full sweep was a **cached replay**; the "live" beat must be scoped to the micro-sweep only.
- (b) Beat-4's conversation shows **"Review — blocked"** (ultra-mode off) — so the self-check must be
  tied to the stage5 conversation (b6b), not the micro-sweep.
- (c) Two live-UI capture mechanics (**open-at-bottom**, **wheel-doesn't-scroll**) need artifact-open
  workarounds (documented in `cs/CAPTURE_PLAN.md`).
- (d) **1-day timeline** with a live-CS capture dependency; auth (`cs_state.json`) can expire.

## What I want Codex to attack
Is the spine genuinely differentiated, or a dressed-up "we used Claude Science"? Does the narrative
overclaim NAB2 or the "live" framing anywhere? Is the 6-beat / 3-min arc feasible AND compelling for the
judging weights (Demo 30 / Claude 25 / Impact 25 / Depth 20)? What would sink it on Friday that I haven't
listed? **Verify claims against the repo** — open `docs/demo-video-pack/cs/*`, the asset HTML in
`docs/demo-video-pack/assets/*`, `docs/cs-full-pipeline_2026-07-09/README.md`, and
`docs/lbd_finding_nab2_2026-07-08.md` to check the plan against reality.
