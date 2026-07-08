# PyZoBot Arbiter — 3-minute demo video plan (v1, for codex-debate)

**Goal.** A ~3-minute narrated, screen-only demo video for the hackathon submission
(*Built with Claude: Life Sciences*). Demo is **30%** of judging (Claude Use 25% · Impact 25% ·
Depth 20%), so this is the single heaviest-weighted deliverable. Deadline 2026-07-13 9:00 PM ET.

**Track (resolved in debate R2/F-011; reframed per operator 2026-07-08).** Track = **RESEARCHER, framed
as *a researcher who also builds*** — a scientist who builds their own instruments (the referee, the LBD
question-engine, the Claude-Science automation) *to ask and answer the research questions*. The
deliverable is a **reproducible T-cell finding + how Claude Science got us there**; the tooling is the
method/vehicle, and the builder-craft is evidence of a researcher who can build to get the science done.
(`CLAUDE.md` + `AGENTS.md` updated to this framing 2026-07-08.) So the narration leads with the *finding
and the method's rigor* (the confident NO) and shows the referee working live as the instrument — a
Claude Science beat earns the "how CS got us there" credit — while the interactive build itself quietly
demonstrates the "researcher who builds" story.

**Thesis to sell in 3 minutes (do not lose this).** The edge is the **confident, receipt-backed NO** —
a referee that adjudicates a mechanistic T-cell claim, returns a receipt for every hop, and is willing
to say *refuted* or *untested* (a failed knockdown → **UNTESTED, not a negative** — the hero feature).
Falsification is the moat. The money-shot finding (NAB2 → Th1/Th2 → atopic eczema) is the proof the
referee finds real signal too.

---

## 1. Pipeline (already built + proven — we reuse, not build)

The user-level **`demo-video` skill** (`~/.claude/skills/demo-video/`) is a generic harness + a
per-project 3-file "pack." Stages: `grep → tts → record → assemble → stitch → gate`
(`node lib/run.mjs <packDir> --stage=all`).

- **Screen-only Playwright** drives a LIVE app (mouse/keyboard only; `grep_gate.mjs` forbids
  `fetch`/`page.request`/`/api/`/deep-links). Cosmetic cursor-dot + click-ripple + caption pill overlays.
- **TTS-first pacing:** narration is voiced per scene; measured `durations.json` drives the visual
  pacing (`sceneStart/untilT/sceneEnd(pad 0.9s)`). Author to **scenes, not a word budget**; render,
  read the measured seconds, trim to 180s.
- **Two-stage TTS economy:** draft everything in cheap **edge-tts** and pass the transcription gate
  FIRST → operator review → only then upgrade the approved cut to **ElevenLabs** (voice "Brian"
  `nPczCjzI2devNBz1zQrb`, `eleven_multilingual_v2`, `{stability:0.5, similarity_boost:0.75, style:0.0,
  use_speaker_boost:true}`) + background music. Key: **`ELLEVENLABS_API_KEY`** (sic, double-L) in
  `01 Dayanjan LLC Hub/.env` — set `TTS.keyEnvFile` to it + `TTS.keyVar:"ELLEVENLABS_API_KEY"`.
- **Transcription gate is the acceptance test** (`gate.py`, local `faster-whisper small.en`, threshold
  0.5): every scripted beat must be present + in order, or it FAILS. Proper-noun ASR mangling is
  cosmetic and does not fail the gate.
- **Background music** muxed post-stitch on the `-nomusic` variant, level-matched (ALPINE: −36.8 LUFS).

**Reference packs to model on:**
- **ALPINE `ep5` (single-actor browser)** — `C:/alpine/.tmp/demo/ep5/` — Playwright over a `localhost`
  app, `STORAGE_STATE` for pre-authed session, `LOGIN.loggedIn` nav landmark, 7 scenes, title+endcap
  cards, ~471 narration words. **This is our closest template.**
- **Rasitha `overview-video` (multi-actor)** — `2026-04-03 Rasitha - Halcyon/.claude/scratch/
  overview-video/demo.config.mjs` — the validated Halcyon-LIMS ElevenLabs config (shows the exact
  `TTS` block + multi-actor `STITCH.order`).

**Quality findings inherited from the Halcyon AI-ISO demo-suite codex-debate (2026-07-05):**
persuade ≠ exhaust (ONE flagship, not a coverage tour); demo-readiness preflight (screen-only ≠
demo-ready); **fixture re-runnability is the #1 effort sink** (must run clean twice); Potemkin
vigilance (show REAL state transitions, never a pre-seeded end state); redaction before any upload.

---

## 2. THE load-bearing decision — the demo surface

**PyZoBot has no web app** — only the `arbiter` Python modules (`src/arbiter/lbd`, `lit`), the
executable notebook, and the Claude Science artifacts. The screen-only pipeline needs a live browser
surface. Three options:

| Option | Surface | Pros | Cons |
|---|---|---|---|
| **A. Drive JupyterLab live** | The evidence-chain notebook running in JupyterLab (`localhost:8888`) | Zero new product scope; shows the REAL artifact; receipts literally print as cells run | Developer-y chrome; cell-run timing variance; reads as "a notebook," not "a product" |
| **B. Build a minimal REAL referee UI** | A small **Streamlit** app wrapping `referee_triple` (`localhost:8501`): choose a perturbation gene + an atlas-backed disease module + condition → **Adjudicate** → renders the REAL `referee_triple` contract (gate-fail → HOP-0-only halted chain; gate-pass → 4-hop chain), verdict badge across the full taxonomy | Interactive + product-feeling; makes the hero feature (confident NO / UNTESTED) tangible & live; perfect ep5-style screen-only demo; highest Demo score | New scope (~half day); must be REAL (backed by `referee_triple`, no Potemkin) + verified before recording |
| **C. Hybrid (recommended)** | Streamlit referee UI as the **hero**, + a short depth montage (the re-framed funnel + the STAT6 confounder check + the pre-rendered CS figure) | Best of both: the interactive hero for Demo/Impact, plus depth backing for Depth/Claude-Use | Same UI scope as B |

**Recommendation: C (Streamlit referee UI hero + depth montage).** Rationale: Demo 30% + Impact 25%
reward *showing the method work interactively*. "Choose a perturbation gene and an atlas-backed disease
module, and watch a receipt-backed verdict resolve — including a confident UNTESTED when the knockdown
failed" is the single most thesis-aligned, most memorable thing we can put on screen, and it is
**honest** (real `referee_triple`,
<1s per verdict, data already loaded). Scope is modest: the referee + data loader already exist;
Streamlit is a thin, real wrapper. The notebook (M5.1) and CS chain (M5.2) supply the depth montage.

**Fallback if the UI proves too costly in debate:** Option A (drive the notebook), which needs zero
product build and still shows real receipts.

---

## 3. Narrative arc (recommended surface — Streamlit hero, single actor, ~6 scenes, ~180s)

**Falsification is the SPINE (revised per debate R1/F-001).** Author `narration.mjs` FIRST; approve;
verify each beat live screen-only; then record. Style (per ALPINE): **literal, warm, no hype;
second-person present-tense describing exactly what's on screen**; calibrated language only (consistent
with / re-derived / refuted / untested / flagged — never "discovered/proven/definitively").

- **Title card (voiced):** "PyZoBot Arbiter — a referee for T-cell hypotheses. It answers with a
  receipt for every step, and it's willing to say a confident *no*."
- **Scene 1 — a fast YES (credibility-setter, ~20–25s, deliberately short).** Choose NAB2 + the
  atopic-eczema module → Adjudicate → the 4 hops resolve green with receipts. "Knockdown verified.
  Real on-target effect. Shifts the Th1/Th2 program. Enriched in atopic-eczema modules — every hop, a
  receipt." *Purpose: a confident NO only lands once the same machine has just shown a rigorous YES.*
- **Scene 2 — the hero catch (UNTESTED), the centerpiece (longest dwell).** Choose SATB1 + asthma →
  Adjudicate → the chain **visibly HALTS at HOP-0** (gate fail; downstream hops greyed as "not
  interpretable"). "SATB1's knockdown never took — guide expression barely moved from control. So the
  honest verdict is *untested*, not a negative. Catching the failed experiment is the whole point."
- **Scene 3 — the confident NO (REFUTED), disease-specific.** Choose **NAB2 + multiple sclerosis** →
  **refuted-for-disease** (GATE/EFFECT/PROGRAM green, DISEASE red — verified clean, unlike SLC1A5 whose
  effect hop also refutes). "The *same* NAB2 — same real knockdown, same effect — but ask about multiple
  sclerosis, and the referee says no at the disease hop. It adjudicates the specific disease, not the gene."
- **Scene 4 — the cull at scale (funnel re-framed as evidence-of-refusal).** "Behind these three: 22,039
  literature-eligible gene–disease questions. 43 held at the disease hop; **30 were clean, full-chain,
  receipt-backed** — the referee refuted the rest." *(Funnel moved AFTER the verdicts; it now proves the
  referee refuses at scale, not an opening stat.)*
- **Scene 5 — depth: the STAT6 confounder, refuted by external data (calibrated).** Cut to the
  **pre-rendered Claude Science figure** (`docs/claude-science-evidence-chain_2026-07-08/
  nab2_evidence_chain.png`) — never a live S3 run. "The sharpest confounder — that NAB2 is just STAT6's
  shadow — is *refuted by this check*: in the authors' own genome-wide data, STAT6 doesn't move under
  NAB2 knockdown."
- **Endcap card (voiced):** "Receipt-backed. Willing to refute. Independently replicated. PyZoBot Arbiter."

Rough budget: ~430–460 words → render → trim to 180s. If long, compress Scene 4 to one line; Scene 2
(the UNTESTED centerpiece) keeps its dwell.

**Arc SETTLED (debate R3, converged):** fast YES-first opener (credibility) → UNTESTED as the first
LONG dwell → REFUTED → funnel-as-evidence-of-refusal → CS-figure depth. Title card primes refusal
upfront. Rejected: cold-UNTESTED open (without a prior YES the audience can't distinguish "untested"
from "the tool is broken").

---

## 4. Build + production steps (sequenced)

1. **[if Option B/C] Build the Streamlit referee UI** — `app/streamlit_app.py`: load `referee_triple`
   + `load_referee_data()` once (`@st.cache_resource`); inputs = **gene select (A-universe / measured
   genes)** + **disease select (the 12 atlas-backed modules from `load_c()`)** + condition (default
   Stim8hr); a "try these" preset row (NAB2→eczema=YES, SATB1→asthma=UNTESTED, NAB2→multiple sclerosis=NO;
   the YES and NO share the gene to show disease-specificity). **Adjudicate** renders
   against the REAL `referee_triple` contract with **two branches** (F-002): (a) **gate-fail** (`answer
   == "untested"`) → render HOP-0 badge + the downstream hops **greyed/struck as "not interpretable —
   knockdown unverified"** (this IS the hero visual); (b) **gate-pass** → the full 4-hop chain, per-hop
   status + receipt. Verdict badge maps the FULL taxonomy (F-003): green=`supported`;
   amber=`supported_weak`/`supported_flagged`; grey=`untested`/`untested_for_c`;
   red=`refuted_for_c`/`refuted_effect`/`refuted_program`. REAL only — every value from `referee_triple`,
   no hardcoding. Stable visible labels on every control (F-009). Note `referee_triple` dynamically loads
   `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`; run the app from repo root so the import resolves.

1a. **PREFLIGHT GATE (must pass before any recording) (F-007/F-009/F-012):** (i) add `streamlit` to
   `requirements.txt`; (ii) `streamlit run app/streamlit_app.py` launches from a clean env; (iii) the
   three showcased triples render the correct verdicts live (NAB2→atopic eczema=supported 4-hop;
   SATB1→asthma=untested HOP-0-only; NAB2→multiple sclerosis=refuted_for_c with GATE/EFFECT/PROGRAM green);
   (iv) a Playwright **smoke script** drives all three screen-only
   (no fetch/API/deep-link) and **asserts on the visible result text** for supported / untested /
   refuted_for_c; (v) the smoke script passes **twice consecutively from a fresh browser context**
   (re-runnability — the Halcyon #1-effort-sink lesson; Streamlit reruns must not leave sticky state).
   Recording does not start until (i)–(v) pass.
2. **Scaffold the pack** — copy the 3 templates into `.tmp/demo-video/` (gitignored). Fill
   `demo.config.mjs` (BASE `http://localhost:8501`, single ACTOR/no-auth, TTS edge draft, TRANSCRIBE
   local, STITCH title+endcap), `narration.mjs` (the arc above), `scenes.mjs` (ep5-style: `moveTo` to
   point, `act` to click Adjudicate, `untilT` to pace to the narration, real selects — no fetch).
2a. **Calibrated-language grep gate (F-006), before recording:** grep `narration.mjs` (case-insensitive)
   for `discovered|proven|definitive|definitively|excluded|breakthrough|cure` — any hit must be reworded
   to the calibrated set (consistent with / re-derived / refuted / untested / flagged) per `CLAUDE.md`.
   In particular the STAT6 beat says "refuted by this check," never "definitively excluded."
3. **Draft pass:** `node lib/run.mjs .tmp/demo-video --stage=all` with edge-tts → **gate must PASS**.
4. **Operator review** the draft cut → approve / adjust narration or scenes → re-gate.
5. **Final pass:** flip `TTS.mode:"elevenlabs"` (Brian) + `keyEnvFile`/`keyVar` → re-render → re-gate →
   mux background music (CC-BY, level-matched) on the `-nomusic` variant.
6. **Redaction + ship:** scrub any incidental identifiers; final MP4 out-of-band; note attribution.

---

## 5. Risks & how PyZoBot differs from Halcyon

- **No live-prod state accumulation (PyZoBot is easier).** The referee is deterministic and read-only
  over local CSVs — no sign-offs/approvals to reset, no fixture corruption, re-records are trivially
  clean. The #1 Halcyon effort sink is largely absent here.
- **UI scope risk (Option B/C).** Building a real UI under deadline. Mitigation: Streamlit is thin, the
  referee exists, verdicts are <1s; timebox to ~half day; fall back to Option A (drive the notebook) if
  it slips.
- **Potemkin risk.** The badges must be computed live by `referee_triple`, never hardcoded. Verify the
  three showcased triples on the live UI screen-only before recording.
- **Pacing/timing.** JupyterLab or Streamlit render timing differs from a settled web app; use `untilT`
  generously and `sceneEnd` pad; the gate catches dropped beats.
- **Env-var double-L gotcha.** `ELLEVENLABS_API_KEY` (sic) — set `TTS.keyVar` explicitly.

---

## 6. Production watchpoints (debate resolved; these are the things to watch while building)
The 3-round codex-debate converged; the decisions above are settled. During production, watch:
1. **The falsification spine (the north star).** Does the recorded cut give **UNTESTED the first LONG
   dwell** and make the refusal **visibly live** (the chain halting at HOP-0 on camera), not merely
   narrated? If the edit lets the YES opener sprawl or the UNTESTED beat gets clipped, the thesis is lost.
2. **Fallback trigger.** If the Streamlit UI isn't preflight-green (dep + 3 live triples + two-run
   screen-only smoke) within the timebox (~half day), fall back to Option A — drive the pre-executed
   notebook (baked outputs, no live S3), Scene 5 = the pre-rendered CS figure.
3. **180s timing.** Author to scenes; render edge-tts; read `durations.json`; trim to ≤180s (compress
   Scene 4 first, never Scene 2).
4. **Screen-only + calibrated-language gates.** `grep_gate.mjs` (no fetch/API) + the step-2a
   calibrated-language grep both green before recording; transcription gate PASS is the acceptance test.
5. **Track framing (done 2026-07-08).** `CLAUDE.md` + `AGENTS.md` updated to **Researcher — a researcher
   who also builds**; the video carries the same framing (finding + method-rigor first; the live build
   quietly demonstrates the builder-craft).
