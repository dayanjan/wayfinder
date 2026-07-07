---
name: freshen
description: Universal consistency checker. Syncs project management documents and flags drift across MEMORY.md, WORK_PROGRESS.md, ATOMIC_PLAN.md, and the workstreams directory. Use when asked to freshen, sync, check consistency, detect drift, or run a project health check.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

## Invocation modes

- `/freshen` — run all checks and apply auto-fixes
- `/freshen --check` — **dry-run**: run all checks, print the report, apply **zero** writes. Use this to audit drift before deciding whether to commit. If the invocation contains `--check`, set `DRY_RUN=true` and skip every write step.

## Process

### Step 0. Git preflight — MUST run before any write

- Detect **template mode**: if `_template/GENERATOR-PROMPT.md` exists at repo root, set `TEMPLATE_MODE=true`. In template mode the repo is the generator scaffold itself (not a generated project), so absent project-state files are expected, the PreToolUse hook intentionally targets `Bash` rather than `Write|Edit|MultiEdit`, and Step 13 has no `WORK_PROGRESS.md` to append to. The relevant per-step branches reference this flag explicitly.
- `git status --porcelain` — capture full tree state. If `WORK_PROGRESS.md` and `MEMORY.md` exist at repo root, additionally run `git diff --stat -w` on them (the `-w` flag suppresses whitespace / line-ending noise — many Windows repos throw LF→CRLF warnings that are not real drift). If they don't exist, skip the diff (do NOT pass non-existent paths to `git diff` — git treats them as revisions and errors out).
- If either file has non-whitespace uncommitted changes: flag as "pre-existing uncommitted housekeeping" in the drift report and record the diff stat. Freshen still proceeds, but the report makes clear its edits will land on top of a dirty tree.
- If `git` itself errors (not a repo): flag CRITICAL and abort auto-fixes entirely.

### Step 1. Read source-of-truth files

- `WORK_PROGRESS.md` snapshot dashboard — current phase, completed workstreams, milestones, active/resolved blockers
- `workstreams/` directory (if present) — the source of truth for what phases exist
- `ATOMIC_PLAN.md` (if present) — the source of truth for task state

### Step 2. Verify workstream / plan integrity

- Every `WS0N_*.md` file referenced in WORK_PROGRESS exists on disk
- Every workstream marked complete in WORK_PROGRESS has a matching commit in `git log` (match on commit subject, not just prefix)
- Every completed task in ATOMIC_PLAN has its "done when" file paths resolving on disk
- Flag any orphans or missing artifacts

### Step 3. Sync MEMORY.md against WORK_PROGRESS.md (narrow edits only)

WORK_PROGRESS is authoritative; MEMORY reflects it, never the reverse. Reconcile:

- Header `Current Status` / `Next:` line — must match active workstream and blockers in WORK_PROGRESS
- Recent Sessions table — bidirectional scan: every `memory/sessions/YYYY-MM-DD.md` file must have a row (append missing rows chronologically); every row must map to a session file or progress log entry (flag phantoms, never auto-delete)
- Resolved "pending" phrasing — if a decision line still says "pending" or "TODO" and WORK_PROGRESS shows the action resolved, rewrite the line **once** to reflect the resolved state. Idempotent: never re-rewrite.
- `Last updated:` timestamp — bump **only if at least one reconciliation actually fired**. Skip the bump on no-op runs.

Apply edits directly unless `DRY_RUN=true`. Do NOT restructure sections, add/remove ADRs, or rewrite gotchas. If any reconciliation is ambiguous (WORK_PROGRESS and MEMORY disagree on substance, not just staleness), leave it and flag it in the drift report.

### Step 4. Check CLAUDE.md folder structure block

Compare the fenced folder map in CLAUDE.md against actual top-level directories. Flag mismatches in the report. **Never auto-apply** — CLAUDE.md is hot-path. Ask explicitly.

### Step 5. Verify timestamps

Every WORK_PROGRESS progress log entry, session log, ADR file, and `docs/gotchas.md` entry must have a `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` timestamp. Flag undated entries with file:line.

### Step 6. Check project-specific artifacts (conditional — skip silently if absent)

The generator populates this step with artifact checks specific to the project type. Each check MUST skip silently if the artifact doesn't exist yet, to avoid drowning early-phase projects in false positives. Examples by project type:

- **Document/report target**: bibliography integrity (CSL JSON parse, required fields, duplicate IDs), citation resolution, figure path resolution, legacy citation-syntax detection
- **ML/Data Science**: notebook execution state, data checkpoint freshness, model artifact presence
- **API/Backend**: migration lineage, schema drift, OpenAPI spec consistency
- **CLI tool**: help text vs. README drift, version string consistency

### Step 7. Detect `.env` variable rename drift

Read `.env` to enumerate variable **names only** (never read or log values). Grep for env-read patterns across source directories (`src/`, `tests/`, `scripts/`, `.claude/`):

- Python: `os.environ["VAR"]`, `os.environ.get("VAR"`, `os.getenv("VAR"`
- Shell/PS: `$env:VAR`, `$VAR`, `${VAR}`
- Node: `process.env.VAR`
- Dotenv: `load_dotenv` / `dotenv.config` followed by `VAR` usage

Flag any variable referenced in code but missing from `.env` as "orphaned env reference — likely rename drift". Do not auto-fix. **Exclude `memory/`** from this scan — that directory legitimately references historical variable names for provenance, and scanning it produces false positives.

### Step 8. Check `memory/lessons-learned.md` staleness

If session log date span is ≥14 days and `lessons-learned.md` still contains only template placeholder entries, remind the user to capture template feedback during the next session-closer run.

### Step 9. Check `docs/plans/` hygiene

Walk `docs/plans/`. Flag any `.md` file older than 14 days as "review candidate — plan may be stale, completed, or orphaned". Suggest archive or delete. **Never auto-move or auto-delete** — plans may contain decisions that haven't been migrated into ADRs yet.

### Step 10. (CRITICAL) Verify hook integrity — `.claude/settings.json`

The PreToolUse hook is the deterministic enforcement layer for the entire project. Silent corruption or removal would be catastrophic, so freshen verifies the hook every run.

- Parse `.claude/settings.json` as JSON. Parse failure → CRITICAL + abort all auto-fixes (harness is broken).
- Verify `hooks.PreToolUse` exists and contains at least one entry matching `Write|Edit|MultiEdit` (or a superset matcher).
- Verify the hook command/prompt text contains the required enforcement tokens. The generator substitutes project-specific tokens at generation time, for example:
  - Document/citation projects: `[@bib-key]`, `citeproc`
  - DB-safety projects: `DROP TABLE`, `TRUNCATE`
  - Shell-hardening projects: `rm -rf`, `--force`
  - Secrets-blocking projects: `AWS_SECRET`, `.env`
- Any missing token → CRITICAL (enforcement regression).

### Step 11. Apply auto-fixes (skip entirely if `DRY_RUN=true`)

- WORK_PROGRESS `Last updated:` bump — only if at least one other sync fired
- MEMORY.md narrow-edit reconciliation from Step 3
- CLAUDE.md folder map — suggest only, never auto-apply

### Step 12. Generate report

```markdown
## /freshen results — YYYY-MM-DD HH:MM [(dry-run)]

### Synced
- [concrete thing fixed — file path + one-line what changed]

### Drift detected (needs human attention)
- [issue + file:line + suggested action]

### CRITICAL
- [hook corruption / JSON parse failure / git repo missing / enforcement regression]

### Warnings
- [stale timestamps / review-candidate plans / orphan env refs]

### Clean
- [checks that passed — one line each]
```

Omit empty sections. If the entire report is "Clean" only, skip the progress log append per the idempotency invariant.

### Step 13. Append progress log entry (skip if `DRY_RUN=true` OR clean no-op)

```markdown
### YYYY-MM-DD HH:MM — Freshen: <one-line summary>
**Synced:** <bullets of edits applied to WORK_PROGRESS and MEMORY, or "none">
**Flagged:** <bullets of drift + CRITICAL items, or "none">
**Clean:** <bullets of checks that passed, or "all non-applicable checks skipped">
```

The `**Synced:** / **Flagged:** / **Clean:**` subsections are required for grep-ability — past freshen entries must be mechanically parseable.

## Source-of-truth hierarchy (explicit)

- `workstreams/` is the source of truth for what phases exist. WORK_PROGRESS must match it.
- `WORK_PROGRESS.md` is the source of truth for session state, blockers, and current phase. MEMORY reflects WORK_PROGRESS, never the reverse.
- `ATOMIC_PLAN.md` is the source of truth for task state.
- `.env` (variable names only) is the source of truth for environment configuration. Code references that don't match are the drift.
- `CLAUDE.md` is hot-path and suggestion-only — never auto-edited.

## Invariants

- **Idempotency** (hard rule): a clean run produces zero writes, zero progress log entries, zero timestamp bumps. A second freshen run immediately after a first must find zero drift.
- **Append-only**: WORK_PROGRESS progress log entries are never modified. Freshen adds entries only.
- **Ordering**: Step 0 (git preflight) MUST run before any write. All read-only checks run before any writes. Report is generated last.
- **Never-touch list**: `.env` values (names only), ADR files, session log files, `data/raw/` files, CLAUDE.md (suggestion-only).
- **Failure modes**: `settings.json` JSON parse failure → CRITICAL + abort. Missing git repo → CRITICAL + abort. Hook missing enforcement tokens → CRITICAL (enforcement regression). All CRITICAL flags stop the relevant write path but the report is always generated.

## What freshen does NOT do

- Rewrite WORK_PROGRESS or MEMORY from scratch (narrow edits only)
- Auto-edit CLAUDE.md (suggestion-only)
- Modify session logs, ADR files, or `data/raw/` (read-only)
- Run other skills (session-start, session-closer, compile, workstream-runner)
- Make git commits or pushes (that's session-closer's or workstream-runner's job)
