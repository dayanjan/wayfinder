---
name: session-closer
description: End-of-session housekeeping. Writes session log, syncs MEMORY.md and WORK_PROGRESS.md, creates the handoff file for the next session, then either commits housekeeping (full-close) or leaves a checkpoint (mid-workstream). Use at end of session, or when asked to wrap up, log progress, close out, or save learnings.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

**Dual-mode operation** (the skill decides automatically — never asks the user):
- **Full-close** — active workstream's Done Criteria are satisfied AND the working tree contains no WIP workstream artifacts. Skill writes housekeeping files, makes a single commit, leaves tree clean.
- **Checkpoint** — workstream is mid-flight (Done Criteria not yet satisfied) OR tree contains WIP that shouldn't be bundled into a session-close commit. Skill still writes the session log and handoff file (these are required for next session to resume), but does NOT commit. WIP stays in place.

## Process

### Step 0. Git preflight + secrets refusal (before any writes)

- Run `git status --porcelain`.
- Classify every changed/untracked file into buckets:
  - **Housekeeping** (committable in full-close): `memory/sessions/*`, `MEMORY.md`, `WORK_PROGRESS.md`, `docs/gotchas.md`, `memory/patterns.md`, `memory/NEXT_SESSION.md`, `memory/lessons-learned.md`
  - **Workstream artifacts** (never in a session-close commit): files under `src/`, `tests/`, `data/`, `figures/`, `reports/`, `notebooks/`, and any project-specific output directories
  - **Secrets — HARD REFUSAL**: any of `.env*`, `*.key`, `*.pem`, `*.p12`, `id_rsa*`, `credentials*`, `*.secret`, `*token*.json`. If any are staged or modified, ABORT the skill immediately with a clear error. **No override flag exists.** User must unstage and re-run.

### Step 1. Detect mode

- Read the active workstream file (if any). If all Done Criteria are checked AND no workstream artifacts remain in the tree → **full-close**. Otherwise → **checkpoint**.
- Record the chosen mode in the session log header.

### Step 2. Write session log — `memory/sessions/YYYY-MM-DD.md`

- Header: `# Session: YYYY-MM-DD HH:MM` with `Mode: full-close | checkpoint`
- Structured sections: What was accomplished, Decisions made (link to ADR if created), New gotchas discovered, New patterns noted, Open questions for next session
- If today's session log file already exists, **append a new block** — never rewrite previous blocks (session log blocks are append-only within a day).

### Step 3. Update MEMORY.md (narrow edits only)

- Append row to Recent Sessions table (date, focus, key outcome)
- Bump `Last updated:` timestamp
- If full-close and a workstream completed: update `Current Status` / `Next:` header line
- Do NOT restructure sections, add/remove ADRs, or rewrite gotchas.

### Step 4. Update WORK_PROGRESS.md

- Update snapshot dashboard in place (current phase, completed workstreams, blockers)
- Append progress log entry: `### YYYY-MM-DD HH:MM — Session close ([mode]): [one-line summary]`

### Step 5. Record new gotchas

Append to `docs/gotchas.md` with `Added: YYYY-MM-DD`.

### Step 6. Note new patterns

Append to `memory/patterns.md` with `Noted: YYYY-MM-DD`.

### Step 7. Write handoff file (dual-location mirror)

Primary: `memory/NEXT_SESSION.md` (overwrites previous). Mirror: append the same block to the bottom of today's session log. The mirror exists so session-start can fall back to the session log if NEXT_SESSION.md is missing, deleted, or stale.

Handoff schema (every field required; use "none" if empty):

```markdown
## Next session priorities — written YYYY-MM-DD HH:MM

**Current state**: [one-line status — phase, workstream, full-close or checkpoint]
**Next action**: [single concrete first step for the next session]
**Prerequisites**: [what must be true before the next action can run]
**Open questions**: [questions to resolve before proceeding]
**Do not touch**: [files or areas that are in-flight or off-limits]
**Context to preload**: [up to 10 file paths the next session should read first]
**Estimated budget**: [rough turns or hours for the next action]
```

### Step 8. Check for unscrubbed deliverables

If any deliverable-directory files (reports/, figures/, external-facing docs) were written, remind the user to run `/scrub-internals` before sharing.

### Step 9. Prompt for lessons learned

Ask if anything about the project scaffolding (structure, skills, agents, hooks, conventions, workflows) worked particularly well or should be improved. If yes, append to `memory/lessons-learned.md` with timestamp, category, details. This flows back to the generator template repo.

### Step 10. Suggest CLAUDE.md improvements

Based on session learnings, suggest edits in the closing report. Never auto-apply; CLAUDE.md is hot-path.

### Step 11. Commit (full-close mode ONLY)

- Stage ONLY housekeeping files, by explicit file list. Never use `git add .` or `git add -A`.
- Single commit: `Session close: YYYY-MM-DD — [one-line summary]`
- Never bypass hooks (`--no-verify`). If a pre-commit hook fails, do NOT retry or amend — leave files staged, report the failure, let the user fix the root cause.
- **Checkpoint mode skips this step entirely.** No commit happens under any circumstances in checkpoint mode.

### Step 12. Push decision

Never push without explicit user confirmation, even in full-close mode.

## Invariants

- **Idempotency**: re-running session-closer within the same minute on unchanged state is a true no-op. The session log block for the current minute is detected by header timestamp and skipped. No duplicate progress log entries.
- **Append-only**: session logs, WORK_PROGRESS progress log, lessons-learned, gotchas, and patterns files are append-only. Previous entries are never rewritten.
- **Hard refusal on secrets**: no override flag exists. Secrets detection aborts the skill before any writes.
- **Mode is automatic**: never ask the user to pick checkpoint vs full-close. Inspect workstream state and tree state; decide.
- **Checkpoint never commits**: housekeeping files are written (required for handoff to work) but the git commit step is skipped entirely.

Note: Claude's built-in auto-memory (/memory) handles cross-session context automatically — this skill focuses on structured project-specific logs, handoff, and commit boundary decisions.
