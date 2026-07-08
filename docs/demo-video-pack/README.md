# Demo-video pack — the reproducible recipe (M5 part 3)

The 3-file pack that produced the ~112s narrated product-demo video via the user-level `demo-video`
skill (`~/.claude/skills/demo-video/`). The rendered MP4 + the music MP3 are **out-of-band** (large,
gitignored under `.tmp/`); this pack is the recipe to regenerate them.

## Files
- `demo.config.mjs` — single actor, **no auth** (`user:""`), BASE `http://localhost:8501`, ElevenLabs
  "Brian" TTS (final) / edge-tts (draft), title + endcap cards.
- `narration.mjs` — the falsification-first script (calibrated language): fast YES → **UNTESTED**
  (centerpiece, halts at the gate) → confident NO (disease-specific) → the funnel → Claude Science depth.
- `scenes.mjs` — the screen-only Playwright scenes driving the live Streamlit app across its three screens.
- `CREDITS.txt` — CC-BY attribution for the background music (Kevin MacLeod, "Deliberate Thought").

## Regenerate
1. Run the app from repo root: `streamlit run app/streamlit_app.py --server.port 8501`
2. Copy this pack into a working dir (e.g. `.tmp/demo-video/`) and run the pipeline:
   `node ~/.claude/skills/demo-video/lib/run.mjs .tmp/demo-video --stage=all`
   (draft = edge-tts; flip `TTS.mode` to `elevenlabs` for the final — key `ELLEVENLABS_API_KEY` in the
   LLC-Hub `.env`). Then mux the music bed (−20 dB, faded, `amix normalize=0`) per `CREDITS.txt`.
3. Acceptance = the transcription gate PASS (held at ~94% mean coverage, voice clear over the music bed).

Plan of record: `docs/plans/demo_video_plan_2026-07-08.md` (debate-hardened). App design source:
`app/DESIGN_SOURCE.md`.
