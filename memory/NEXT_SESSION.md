# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-08 18:02 (full-close)

**Current state**: **M5 COMPLETE.** All three submission artifacts shipped — the executable
evidence-chain **notebook** (`notebooks/pyzobot_arbiter_evidence_chain.ipynb`), the **Claude Science
evidence chain** (`docs/claude-science-evidence-chain_2026-07-08/`), and the interactive **Streamlit
"Researcher's Workbench"** (`app/streamlit_app.py` — Referee / Hypothesis Engine / Claude Science,
implementing a Claude co-design imported via DesignSync) + the **final demo video** (~112s, ElevenLabs
"Brian" + CC-BY music bed, transcription gate PASS 94%; recipe `docs/demo-video-pack/`, MP4 out-of-band).
Two 3-round repo-read codex-debates hardened the demo + workbench plans. Track = **"Researcher who also
builds"**. Tree clean; all committed (commits ready to push). **The demo + app are the fallback MVP.**

**Next action**: **READ THE PRODUCT-DEMO TRANSCRIPT FIRST**, then do a deeper dive into **Claude
Science** based on it — what CS capabilities / workflow it revealed and how to push the finding or the
product further with CS:
`C:\Users\wijesingheds\Downloads\Voice 260708_115846 Claude Science demo_20260708_171006_timestamped-notes.md`
**[CLAUDE]** (synthesis + exploration; drive CS via `drive-claude-science` if we run it).

**Prerequisites**: the transcript exists at the path above (read it before anything else). If we drive
Claude Science again: the WSL daemon reachable + `~/.claude/skills/drive-claude-science/` (needs
`/design-login`-style setup? no — CS uses its own login; DesignSync is separate). App runs from repo
root: `streamlit run app/streamlit_app.py`.

**Open questions**: what the transcript surfaces about CS capabilities worth exploiting next; whether to
deepen the finding (new CS-driven analysis), wire the app's live-CS lane for real, or something else the
transcript points to.

**Do not touch**: never commit `.env`, `data/*.csv`, `data/lbd_cache/`, `data/lbd_out/`,
`references/*.pdf`, `.claude/scratch/`, `.tmp/` (demo MP4/MP3 — now gitignored).

**Context to preload**: the transcript above (FIRST); `docs/claude-science-evidence-chain_2026-07-08/README.md`;
`docs/claude-science-capabilities.md`; `~/.claude/skills/drive-claude-science/SKILL.md`;
`app/DESIGN_SOURCE.md`; `docs/demo-video-pack/README.md`; `WORK_PROGRESS.md`; `MEMORY.md`.

**Estimated budget**: ~0.5–1 day (transcript read + Claude Science exploration).
