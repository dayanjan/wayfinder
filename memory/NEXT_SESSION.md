# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-09 19:12 (full-close)

**Current state**: Full-close, tree clean, all pushed. **Submission strategy pivoted to a CS-native
3-minute video** (new spine: *when you don't know what to ask, use LBD to surface the data's implicit
hypotheses — built directly in Claude Science; the library and the lab on one bench*). **Deadline moved
up to EOD Friday 2026-07-10** (operator out of town Sat–Mon; Monday too close). Tonight banked ALL design +
de-risk + plan-hardening: spine, narration, 3 visual assets, verified on-screen capture plan, the CS-native
demo pack, and a 2-round repo-read codex-debate whose accepted fixes are applied. **Friday = capture +
assemble + submit only** — no design left. The Streamlit app + prior demo video remain the fallback MVP,
so this is upside, not gating.

**Next action** `[CLAUDE]` (skill-orchestration — demo-video harness + CS driving + transcription gate;
not Codex-delegable): execute the CS-native video per `docs/demo-video-pack/cs/README.md`. **Order matters:**
(1) pre-flight (confirm CS port via `claude-science status`; refresh `cs_state.json` auth by running the
tracer once); (2) **PRE-CAPTURE THE 4 REQUIRED FRAMES FIRST (release blockers)** — live micro-sweep proof,
funnel+NAB2 receipt, one concrete NO receipt (IL2→untested or SBF2→refuted), reviewer overclaim flag
(stage5/review.json); confirm each is crisp before assembling; (3) `node <demo-video>/lib/run.mjs
.tmp/demo-cs --stage=all`; (4) gate PASS → mux CC-BY music → repo public + light scrub → submit
(video + repo + 100–180w summary, all in the SCRIPT doc).

**Prerequisites**: CS daemon up (was port **8000**, pid 487 — do NOT restart it). `cs_state.json` auth fresh
(re-mint via drive-claude-science if the tracer prints NEED_NONCE). ElevenLabs key `ELLEVENLABS_API_KEY` in
the LLC-Hub `.env` (verify spelling). Deps: edge-tts, imageio-ffmpeg, faster-whisper (see demo-video SKILL).

**Open questions**: (1) Do the b5 on-screen cached/live caption + scoped narration fully resolve the
live-vs-cached read, or should the visible NO become the centerpiece rather than a beat? (from the debate —
F-002/F-005). (2) For b5 (funnel/NAB2) and b6b (reviewer flag): live capture vs prepared static artifact
overlay — decide at the pre-capture step (overlay is preferred per CAPTURE_PLAN.md; CS opens at bottom +
mouse-wheel doesn't scroll the transcript). (3) Does the 3-min budget hold after adding the NO receipt +
tightening Swanson (beat 3)?

**Do not touch**: never commit `.env`, `data/*.csv`, `cs_state.json`, `.claude/scratch/`, raw codex logs
(`docs/reviews/codex-debate_*/*_raw.log` + `*_prompt.txt` — gitignored). **Do NOT restart the CS daemon**
(pid 487; an "Update available" toast offers Restart — dismiss it). Don't re-run completed sweeps. Don't
"un-fix" the debate-hardened calibration (NAB2 = nomination; scoped live-vs-cached).

**Context to preload**: `docs/demo-video-pack/cs/README.md`; `docs/demo-video-pack/cs/CAPTURE_PLAN.md`;
`docs/demo-video-pack/cs/scenes.mjs`; `docs/demo-video-pack/cs/narration.mjs`;
`docs/demo-video-pack/SCRIPT_cs-native_2026-07-09.md`;
`docs/reviews/codex-debate_cs-native-video-plan_2026-07-09.md`;
`C:/Users/wijesingheds/.claude/skills/demo-video/SKILL.md`; `WORK_PROGRESS.md`; `MEMORY.md`.

**Estimated budget**: ~1 day (Friday). Video is upside; submission MVP already exists. If Friday runs short,
the fallback is the existing Streamlit demo video (already gate-passed).

---

## Mirror of this handoff is appended to memory/sessions/2026-07-09.md by session-closer.
