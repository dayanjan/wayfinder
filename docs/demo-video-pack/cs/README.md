# CS-native demo pack — Friday runbook

The CS-native re-cut of the 3-min submission video. New spine: *when you don't know what to ask, use
LBD to surface the data's implicit hypotheses — built directly in Claude Science.* Drives our `file://`
slide assets (beats 1–3) + the **live Claude Science UI** (beats 4–6), screen-only, scene-timed to
ElevenLabs "Brian". Full script + beat→conversation map: `../SCRIPT_cs-native_2026-07-09.md`.

This pack supersedes the parent `../demo.config.mjs` (Streamlit cut), which stays as the fallback recipe.

## Files (standard demo-video pack names)
- `demo.config.mjs` — 1920×1080, `STORAGE_STATE`=`cs_state.json` (CS auth), Brian TTS, title/endcap cards.
- `narration.mjs` — the 6-beat script (`TURNS.walk`) + voiced `CARDS`.
- `scenes.mjs` — beats 1–3 = `file://` slides; beats 4–6 = live CS (home → click conversation → scroll).
- Assets consumed: `../assets/slide-two-floods.html`, `slide-feature-matrix.html`, `swanson-graphic.html`.

## Pre-flight (do these first, Friday)
1. **CS daemon up + port.** `wsl -- bash -lc "claude-science status"` → confirm `running` + `port`.
   If not 8000, update `CS` in `scenes.mjs` and `BASE` in `demo.config.mjs`. **Do NOT restart CS.**
2. **Refresh CS auth.** The saved `cs_state.json` session can expire. Run the tracer once to re-auth:
   `node <scratch>/cs-capture-tracer.js --out .` — if it prints `SIGNED_IN: true`, `cs_state.json` is fresh.
   If it prints `NEED_NONCE`, re-mint via the `drive-claude-science` skill (marker + `claude-science url`).
3. **Confirm conversation titles** match `scenes.mjs` (`Live LBD Literature Question Generator`,
   `Literature-Based-Discovery Loose Gene Universe Sweep`, `Stage3: NAB2-STAT6 Cis-Artifact Verification`).
4. **Deps** (once): `edge-tts`, `imageio-ffmpeg`, `faster-whisper` (see the skill SKILL.md), ElevenLabs
   key `ELLEVENLABS_API_KEY` in the LLC-Hub `.env`.

## Run
```bash
SKILL="C:/Users/wijesingheds/.claude/skills/demo-video"
mkdir -p .tmp/demo-cs && cp docs/demo-video-pack/cs/{demo.config.mjs,narration.mjs,scenes.mjs} .tmp/demo-cs/
node "$SKILL/lib/run.mjs" .tmp/demo-cs --stage=all      # grep -> tts -> record -> assemble -> stitch -> gate
```
Iterate one stage at a time if needed (`--stage=record --turn=walk`, then `assemble`, `stitch`, `gate`).
The **`//TODO Fri`** lines in `scenes.mjs` are scroll-target tunings — watch the recorded `walk` clip and
adjust `rec.wheel(...)` amounts so each CS beat lands on its receipt (live calls / funnel+REFUTED /
STAT6-unmoved + Reviewer flag).

## Acceptance
Done only when `gate.py` prints `RESULT: PASS` (all 6 beats + 2 cards present, in order, above threshold).
Then mux the CC-BY music bed (−20 dB, faded) per `../CREDITS.txt`. Final MP4 → `.tmp/demo-cs/out/` (out-of-band).

## Then submit
Repo public + light identifier scrub → upload video + repo + the 100–180w summary (in the script doc).

## Calibration guardrails (do not overclaim)
NAB2 = nomination (never proven/discovered). Therapeutic direction stays OUT of the cut. The "CS builds
LBD live" beat uses the **micro-sweep** (genuinely live) — never imply the full sweep was a live crawl.
