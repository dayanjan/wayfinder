# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-09 07:20 (full-close)

**Current state**: **The full LBD→NAB2 instrument now runs natively in Claude Science** — the MVP
(Stage 0/1/3/5) is COMPLETE, all PASS, verified-from-DB, honesty-audited, and archived to
`docs/cs-full-pipeline_2026-07-09/` (README + provenance + 4 stage dirs; ~$6.41 CS spend). Generation (LBD
sweep, cached-receipt replay under a pure-replay guard), referee (native, from the tracer), and falsification
(native anon-S3 STAT6 cis-check, cis refuted) all live in CS; provenance in `operon-cli.db`; cross-model
independence stays external (Codex). Tree clean after this close. The demo/app/notebook remain the submission
MVP; this native-in-CS reproduction is a strong **Claude Use / Depth** capability artifact.

**Next action**: **Decide the submission surface for the native-in-CS pipeline** (deadline 2026-07-13). Top
pick `[CLAUDE]`: fold a tight "the whole instrument runs inside Claude Science" section into the submission
narrative (README/notebook/app "Claude Science" screen or the demo video) — cite the funnel 3935/22039/43/30,
NAB2 rank 4, the cis-refutation +0.087/0.79, and the Reviewer's live calibrated-language enforcement, all
pointing at `docs/cs-full-pipeline_2026-07-09/`. Judging weights Claude Use 25% + Depth 20% — this is the
highest-leverage place to spend remaining hours. Second option `[CLAUDE]`/`[CODEX-RESCUE]`: build **Stage 2**
(confounder checks — dynamically-derived FDR clusters 90 & 100 + cytoband via MyGene/`host.mcp`), the only
unbuilt stretch stage (plan §5 Stage 2).

**Prerequisites**: CS daemon up on :8765 — run the binary DIRECTLY:
`wsl -d Ubuntu --cd "~" -- /home/dayanjan/.local/bin/claude-science status` (do NOT `export PATH=$HOME/...:$PATH`
— the inherited Windows PATH has `(x86)` parens that break `bash -lc`). Nonce URL:
`wsl -d Ubuntu --cd "~" -- bash -c '$HOME/.local/bin/claude-science url'`. Driver + auth at
`~/.claude/skills/drive-claude-science/` (`cs-drive.js` + `cs_state.json`). Stage-1 staging tree persists at
`/home/dayanjan/pyzobot-cs-stage1/` (re-run `.claude/scratch/cs-capability-mining/stage1_prep.sh` via
`MSYS_NO_PATHCONV=1 wsl -- bash <path>` to refresh). Verifiers: `cs_verify.py` / `cs_provenance.py`.

**Open questions**: Surface the native-in-CS pipeline as a submission headline or keep as a depth artifact?
Is Stage 2 worth building before the deadline, or is the MVP + submission-polish the better spend?

**Do not touch**: never commit `.env`, `data/*.csv`, `data/lbd_cache/`, `data/lbd_out/`, `references/*.pdf`,
`.claude/scratch/`, `.tmp/`. CS's store `~/.claude-science/` is CS's private data (copy only audit artifacts
into `docs/`). Don't re-run Stage 0/1/3/5 — all PASS and archived. The Stage-1 staging tree
`/home/dayanjan/pyzobot-cs-stage1/` is disposable scaffolding (regenerable), not a source of truth.

**Context to preload**: `docs/cs-full-pipeline_2026-07-09/README.md` (the whole run at a glance);
`docs/cs-full-pipeline_2026-07-09/provenance.md`; `docs/cs-full-pipeline_2026-07-09/stage5/receipt_chain.md`
(the CS-authored end-to-end chain); `docs/plans/full-pipeline-in-cs-plan_2026-07-09.md` (§5 Stage 2 = the
stretch); `WORK_PROGRESS.md`; `MEMORY.md`; `docs/gotchas.md` (the 2026-07-09 CS gotchas: S3 virtual
addressing, workspace=OPERON-frame, Git-Bash→WSL quote mangling).

**Estimated budget**: ~0.5 day for the submission-surface fold; +0.5–1 day if Stage 2 is built.

---

## Mirror — same handoff block appended to today's session log by session-closer.
