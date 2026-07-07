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
