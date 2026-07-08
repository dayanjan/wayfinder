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
