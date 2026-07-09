# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## Next session priorities — written 2026-07-09 06:15 (full-close)

**Current state**: Claude Science exploitation is planned and de-risked. The **CS tracer already reproduced
the 4-hop referee + NAB2 finding natively, digit-for-digit** (`docs/cs-capability-tests_2026-07-08/tracer-artifacts/`),
and the **full-pipeline-in-CS plan is SOLIDIFIED** — 3-round repo-read codex-debate → **SHIP**
(`docs/plans/full-pipeline-in-cs-plan_2026-07-09.md` v3). Architecture: **CS = the instrument (generation →
referee → provenance); Codex = the external cross-model auditor.** Tree clean after this close (plan +
debate committed). M5 submission artifacts (notebook + app + demo video) remain the fallback MVP.

**Next action**: **Implement the plan's §9 runnable checklist in CS**, starting with **Stage 0 (feasibility
probe)** — one driven CS run that, from the kernel, (a) GETs a Europe PMC `hitCount` (e.g. `"NAB2" AND "atopic
eczema"` → expect 6), (b) POSTs an Open Targets GraphQL disease→targets query, (c) S3 micro-probe (anon
`s3fs`+`h5py` open of `GWCD4i.DE_stats.h5ad`, read obs/var labels, close), (d) lists `_mcp-*` connectors.
Then Stage 1 (LBD proposer, full 3,935 sweep via kernel HTTP + workspace cache) → Stage 3 (S3 cis-check) →
Stage 5 (provenance from `operon-cli.db`). `[HYBRID]` — Claude drives + verifies-from-DB; author each stage
prompt into `.claude/scratch/cs-capability-mining/prompts/`.

**Prerequisites**: CS daemon up on :8765 (`wsl -d Ubuntu -- bash -lc 'export PATH=$HOME/.local/bin:$PATH; claude-science status'`);
data at `/home/dayanjan/pyzobot-data/` (4 CSVs + join_spec.json); hardened driver `~/.claude/skills/drive-claude-science/cs-drive.js`
(auth `cs_state.json` beside it; re-mints nonce); DB `operon-cli.db` under `~/.claude-science/orgs/741d6512-…/`
(read via WSL `python3`, no `sqlite3` CLI). Reuse `verify_cs_capabilities.py` + `probe_tracer.py` as verifier seeds.

**Open questions**: Does the S3 in-CS path clear the network-domain approval headlessly (Stage 0-(ii))? If not
→ documented external fallback for Stage 3. Are `s3fs`/`h5py` in CS's base env or need workspace install?
Smallest honest Stage-1 proof = the FULL 3,935 sweep (a forced-NAB2 reduced run is plumbing only, not "CS
generated the question").

**Do not touch**: never commit `.env`, `data/*.csv`, `data/lbd_cache/`, `data/lbd_out/`, `references/*.pdf`,
`.claude/scratch/`, `.tmp/`. CS's store `~/.claude-science/` is CS's private data (copy only the audit
artifacts we produce into `docs/`). Don't re-run the tracer (referee+NAB2 already proven native).

**Context to preload**: `docs/plans/full-pipeline-in-cs-plan_2026-07-09.md` (esp. §9 checklist + §5 stages);
`docs/reviews/codex-debate_full-pipeline-cs_2026-07-09/final_synthesis.md`; `docs/cs-capability-tests_2026-07-08/tracer-artifacts/TRACER-RESULTS.md`;
`docs/claude-science-test-plan_2026-07-08.md` (operon-cli.db map); `docs/pipeline-inventory-and-cs-mapping_2026-07-09.md`;
`src/arbiter/lbd/sources.py` + `_http.py` (the code to port); `docs/lbd-methods-explainer.md`; `WORK_PROGRESS.md`; `MEMORY.md`.

**Estimated budget**: ~0.5–1 day for the MVP (Stage 0/1/3/5); Stage 1 full sweep is the long one (cache makes it replayable).
