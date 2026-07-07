# Patterns — PyZoBot Arbiter

Append-only. Reusable patterns discovered during the build (data-lookup shapes,
receipt/provenance structures, agent-boundary conventions). `session-closer` appends here.

---
<!-- patterns appended below, newest last, each with: Noted: YYYY-MM-DD -->

## Inspect secrets masked; source from `.env`, never echo
**Noted: 2026-07-07.** When verifying a key: read `.env`, print only `len` + `prefix…suffix`
(never the full value); load it into the environment via `set -a; source .env; set +a` and
reference `$VAR` in curl so the secret stays out of the transcript and shell history.

## Pre-push safety gate before any first push
**Noted: 2026-07-07.** Before creating/pushing a repo: (1) `git add -A --dry-run` to preview
exactly what `.gitignore` lets through; (2) `git check-ignore` the sensitive paths (`.env`,
data, private notes) to prove they're excluded; (3) run the secret-grep on `git diff --cached`
as its own inspected step; (4) after push, `git ls-tree -r origin/main` and grep for the
sensitive patterns to confirm nothing leaked. Cheap, catches the irreversible mistake.
