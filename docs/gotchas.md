# Gotchas — PyZoBot Arbiter

Append-only running list of traps, surprises, and non-obvious fixes. `session-closer`
appends here at close; check it before debugging something that "should just work."

---
<!-- gotchas appended below, newest last, each with: Added: YYYY-MM-DD -->

## `freshen` references `ATOMIC_PLAN.md`, but this project uses `docs/plan.md`
**Added: 2026-07-07.** The `freshen` skill was copied from the generator and still names
`ATOMIC_PLAN.md` / `workstreams/` as task-state sources. This project has neither — it uses
`docs/plan.md` (plan of record) and `docs/plans/*_atomic.md` (from `atomic-planner`). Those
checks are guarded by "(if present)" so `freshen` degrades gracefully and still validates
`MEMORY.md`/`WORK_PROGRESS.md`. Not a bug; just don't expect the ATOMIC_PLAN checks to fire.

## Check an Anthropic key's validity without spending tokens
**Added: 2026-07-07.** `GET https://api.anthropic.com/v1/models` (with `x-api-key` +
`anthropic-version: 2023-06-01`) returns 200 + the model catalog and consumes zero tokens —
use it as the auth check. A key can list models yet still be blocked on inference, so also
fire one minimal `POST /v1/messages` (`max_tokens:5`) to confirm end-to-end before trusting it.

### Reading one cell of a huge deposited h5ad without downloading it — Added: 2026-07-08
The authors' genome-wide DE (`GWCD4i.DE_stats.h5ad`) is 16.8 GB on a public no-creds S3 bucket
(`s3://genome-scale-tcell-perturb-seq/marson2025_data/`). To read a single (perturbation, gene) value
(e.g. STAT6 under NAB2-KD) do NOT download it: `s3fs.S3FileSystem(anon=True).open(url)` → `h5py.File(fo)`
reads only the chunks needed (obs categoricals, var names, one matrix slice) via range requests. anndata
is NOT required (and its pin conflicts with typing_extensions here) — raw h5py suffices. See
`docs/nab2_stat6_definitive_check.py`. Raw single-cell matrices (`D*_*.assigned_guide.h5ad`, ~140 GB each)
are the off-limits big data; the DE results are the CPU-feasible slice.

### `offtarget_flag` in DE_stats already encodes a cis-neighbor check — Added: 2026-07-08
The DE_stats `offtarget_flag` = "a gene with TSS within 10 kb of the guide is significantly down-regulated."
So a False flag on a perturbation already means no 10 kb neighbor is cis-repressed — a cheap partial answer
to any "did the guide hit a neighbor?" (e.g. NAB2 guide vs STAT6 1.9 kb away) before pulling the full DE.

## Claude Science operational gotchas — Added: 2026-07-09
- **`host.delegate` is gated** behind a session Delegation ("ultra mode") toggle — OFF by default and NOT
  reachable via the headless driver. Programmatic sub-agent fan-out fails with "delegation is not enabled";
  use `host.llm_batch` (inline Haiku-4.5 sampling) instead. Real host API: `mcp`/`llm_batch`/`query_db`/
  `delegate`/`agent_list`/`list_artifacts`/`artifact_path`/`artifacts`. (`host.capabilities()` is NOT real.)
- **The driver's "DONE" ≠ receipts landed.** CS's Sonnet-5 Reviewer commits `verification_checks` and the
  `extracted_code` provenance block backfills only on FRAME COMPLETION — headless runs may leave the OPERON
  frame "processing" for 10+ min. Poll `operon-cli.db` after DONE; save receipts from the kernel, don't rely
  on DB backfill.
- **CS base env is lean** — `s3fs`/`h5py` (and other bio stacks) may need install into the workspace env;
  distinguish "missing package → install" from "S3/network blocked" when a data-access step fails.
- **LBD in CS = kernel HTTP, not connectors.** Europe PMC `hitCount` (GET) + Open Targets GraphQL (POST) are
  plain HTTP in `sources.py`; CS's `_mcp-*` connectors don't expose those exact scalars. Port `sources.py`/
  `_http.py` into the kernel with a workspace SHA1 cache (a fresh `--new` project resets the workspace → copy
  `lbd_cache/` in before replay).

## Claude Science full-pipeline-native gotchas — Added: 2026-07-09
- **Anon S3 in CS needs VIRTUAL addressing.** `s3fs.S3FileSystem(anon=True)` works headless for the public
  bucket, BUT path-style `s3.amazonaws.com` is proxy-denylisted (403). CS self-heals by switching to the
  bucket-qualified host `genome-scale-tcell-perturb-seq.s3.amazonaws.com` (virtual addressing); the driver
  auto-approves the network-domain card. So the 16.8 GB `GWCD4i.DE_stats.h5ad` opens + lazy-reads in-CS with
  NO download — the S3 cis-check runs natively (no external fallback). Proven Stage 0 + Stage 3 (2026-07-09).
- **A CS run's workspace dir == the OPERON frame id**, at
  `~/.claude-science/orgs/<org>/workspaces/<OPERON_FRAME>/`. Get the OPERON frame from `frames` WHERE
  project_id + agent_name='OPERON'. NOTE: `find` sometimes cannot traverse the workspace (overlay/perms);
  a DIRECT `wsl -d Ubuntu --cd "~" -- cat /abs/path/...` reads it fine.
- **Git-Bash → WSL nested-quote mangling (recurring, wastes runs).** A multi-line `wsl -- bash -c '...'`
  carrying `$VAR=` assignments, `$(...)` subshells, or heredocs silently yields EMPTY variables (symptom:
  `mkdir: cannot create directory '/src'` = `$DST` empty; or literal quotes in error paths). FIXES: (a) put
  the script in a FILE and run `MSYS_NO_PATHCONV=1 wsl -d Ubuntu --cd "~" -- bash /mnt/c/.../script.sh`;
  (b) for one-offs use a single direct command with NO shell vars (`wsl --cd "~" -- cat /abs/path`);
  (c) always `MSYS_NO_PATHCONV=1` when a `/mnt/c/...` arg is present (else Git-Bash prepends its install root).
- **CS `verification_checks` surface only when a review is EXPLICITLY requested AND the OPERON frame
  completes.** Stage 5 (which asked for a review) populated 4 rows; Stage 0/1/3 were async-empty at capture
  even though a REVIEWER frame ran — the driver-tail "Reviewer · No issues found" is the corroboration. To
  guarantee captured findings, end the prompt with an explicit "request a review of <file>" and poll the DB
  after "DONE".
