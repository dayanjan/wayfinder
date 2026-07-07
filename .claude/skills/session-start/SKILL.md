---
name: session-start
description: Initialize a fresh work session. Reads the handoff written by session-closer, cross-checks against current project state, eagerly preloads referenced docs, detects between-session drift, and presents a scannable briefing. Use at start of a new session, or when asked "what's next", "where did we leave off", "session start", or after /clear.
allowed-tools: Read, Grep, Glob, Bash
---

**Read-side of the session lifecycle.** Paired with `session-closer` (write-side). Their shared interface is `memory/NEXT_SESSION.md` plus the mirrored handoff block at the bottom of the latest session log.

**Strictly read-only.** Writes no files. Makes no commits. Runs no git mutation commands. The first write of the new session belongs to whatever workstream the user chooses to run.

## Process

### Phase 1 — Gather context

1. **Read `memory/NEXT_SESSION.md`** (primary handoff). If present and parseable, extract all fields. If missing, empty, or malformed, fall back to parsing the `## Next session priorities` block at the bottom of the latest session log (`memory/sessions/YYYY-MM-DD.md`, highest date). If both are missing: record `NO_HANDOFF` and degrade gracefully (see Edge Cases).

2. **Read the latest session log for narrative continuity** — extract the "What was accomplished" and "Decisions made" bullets. Note the session log's date and compute age in days relative to today.

3. **Read `WORK_PROGRESS.md`** snapshot dashboard — `Last updated:` timestamp, active workstream indicator, milestone statuses, active/resolved blockers.

4. **Read `MEMORY.md`** header — `Current Status` / `Next:` line and the most recent 2–3 Recent Sessions rows. Should agree with WORK_PROGRESS and the handoff; any disagreement is drift.

5. **Git state check** (read-only, never mutates):
   - `git status --porcelain` — any uncommitted changes?
   - `git log --oneline -5` — last 5 commits
   - `git remote -v` — is a remote configured?
   - If a remote exists: `git fetch --dry-run 2>&1` — is the local branch behind?

   **Never run** `git pull`, `git fetch` (without `--dry-run`), `git merge`, `git rebase`, `git reset`, `git stash`, `git checkout <branch>`. All are forbidden; session-start is strictly read-only.

### Phase 2 — Verify & detect drift

6. **Cross-check handoff vs. current state** — does the handoff's "Current state" reference a workstream matching WORK_PROGRESS's active phase indicator? If not, flag "handoff vs. WORK_PROGRESS divergence" and trust WORK_PROGRESS as source of truth.

7. **Handoff staleness** — compute age from the handoff's `written YYYY-MM-DD HH:MM` timestamp. Flag at ≥7 days ("stale handoff — recommend /freshen before starting"). Flag more strongly at ≥30 days ("very stale — review WORK_PROGRESS manually").

8. **Detect between-session git drift** — compare the last commit in `git log` to the expected post-close commit. If there are commits ahead of the expected session-close commit, flag "unexpected commits since handoff" with a list. If `git status` shows dirty files not listed in the handoff's "Do not touch" section, flag "unexpected dirty state" and ask the user to reconcile before proceeding.

9. **Checkpoint resume detection** — if the handoff's "Current state" indicates checkpoint mode (workstream in progress), switch to **checkpoint-resume mode**:
   - Do NOT suggest starting a new workstream.
   - Re-read the handoff's "Do not touch" section carefully — these are the mid-flight files.
   - Verify each mid-flight file still exists.
   - Present a resume briefing instead of a start briefing.

10. **Remote behind detection** — if `git fetch --dry-run` showed remote commits ahead of local, note the count in the report. **Do not auto-pull.** Present the fact and let the user decide — pull is a write action.

### Phase 3 — Eagerly preload context

11. **Read every file listed in the handoff's "Context to preload" section.** This is the single biggest productivity lever of session-start: the first substantive turn should already have the relevant docs loaded. Don't make the user ask "please read X first."
    - Cap at 10 files. If the handoff lists more, preload the first 10 and report the rest as "not loaded — load manually if needed."
    - If a listed file no longer exists, flag "preload file missing" and continue with the others.
    - Also preload, unconditionally: `CLAUDE.md`, `WORK_PROGRESS.md` (already read in Phase 1), and the workstream file for the active phase (`workstreams/WS0N_*.md`) if applicable.

### Phase 4 — Present the briefing

12. Print the session dashboard. Scannable, fits on one screen, leads with state and next action:

```markdown
## Session start — YYYY-MM-DD HH:MM

### Where we are
[Current state sentence — from handoff, verified against WORK_PROGRESS]

### Last session — YYYY-MM-DD (N days ago)
- [Key finding/decision #1]
- [Key finding/decision #2]
- [Key finding/decision #3]

### Next concrete action
1. [first thing — literal command or file to open]
2. [second thing]
3. [third thing]

### Prerequisites
- [met, verified now]
- [unmet — action needed]

### Context preloaded
I've read these into the session already:
- [path] — [why it matters]
- [path] — [why it matters]

### Workstream status
[CLEAN start | CHECKPOINT RESUME from mid-flight in WSNN]

### Tree state
[clean | dirty: list of files]
[branch: main | N commits behind origin]

### Warnings
- [stale handoff (N days) → recommend /freshen]
- [unexpected commits since last session close → review with git log]
- [unexpected dirty files → reconcile before starting]

### Suggested first move
[Literal text to paste or command to run]
```

Omit empty sections. If Warnings is empty, omit it.

## Edge cases

- **No handoff exists** — skip Phase 2; preload only CLAUDE.md, WORK_PROGRESS.md, and the active workstream file; synthesize next action from WORK_PROGRESS's active phase. Warn: "No handoff found — consider running session-closer at the end of this session."
- **First session ever** — treat as no-handoff; briefing focuses on WORK_PROGRESS and CLAUDE.md/README.md; friendly tone.
- **Handoff says checkpoint** — switch to resume mode (step 9). Do NOT suggest `/clear` or a new workstream.
- **Handoff references a completed workstream** — flag as superseded; find the next unchecked workstream from WORK_PROGRESS and suggest that instead. The old handoff's preload list may still be relevant; preload anyway but note it's from a superseded context.
- **Remote behind** — report the count, suggest `git pull` manually, never auto-pull.
- **Uncommitted changes at start** — if they match the handoff's "Do not touch" list, proceed in resume mode. If they don't, flag "unexpected dirty state" and ask the user to reconcile.

## Source-of-truth precedence

When files disagree:
1. `WORK_PROGRESS.md` wins for current phase, milestones, blockers.
2. The handoff wins for narrative continuity and preload hints.
3. `git log` wins for "what's actually committed."
4. The filesystem wins for "does this file actually exist?"
5. Flag every divergence in the briefing so the user knows the state isn't perfectly consistent.

## Invariants

- **Strictly read-only**: no file writes, no commits, no git mutations. If a fix is needed, flag the condition and suggest the appropriate skill (`/freshen`, `/session-closer`) — never run it from here.
- **Eager preload is the point**: skipping Phase 3 reduces session-start to a `/next-workstream` wrapper. Always preload.
- **Idempotency**: running session-start twice in a row produces the same briefing. No state accumulates.
- **Brevity**: the briefing fits on one screen. Details live in the preloaded files, not in the briefing text.
