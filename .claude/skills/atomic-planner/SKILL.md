---
name: atomic-planner
description: Break a workstream or feature into atomic tasks (1-3 hours each, single-purpose, testable). Writes a markdown plan AND creates a native Task List for compaction-survival. Use when planning a workstream, decomposing a complex effort, or when the user asks "break this down" or "what are the steps".
allowed-tools: Read, Write, Edit, Grep, Glob
---

# atomic-planner

## When to use

- A task is too large to execute in one session.
- Multiple independent pieces of work need parallel handling.
- A complex synthesis needs sub-tasks.
- The user asks "break this down" or "what are the steps".

## Process

1. **Read context** — `docs/plan.md` (the plan of record, v6), `memory/NEXT_SESSION.md` (current handoff), `WORK_PROGRESS.md`, and any in-flight task. For data-lookup / receipt / agent work, read `data/README.md` and the affected `src/arbiter/*.py`.

2. **Decompose into atomic tasks**. Each task must be:
   - **Atomic** — single concern, completable in 1-3 hours.
   - **Testable** — has a "done when" criterion.
   - **Independent** — minimal coupling to other in-flight tasks.
   - **Concrete** — not "research X", but "produce file Z" or "run command Q".
   - **Honest about runtime-error causes** — if a card names the root cause of a *runtime* error (a traceback, crash, or wrong output) that you inferred from a static read, tag it **"hypothesis — reproduce before fixing"**, not as fact. The bug's true location only reveals itself at runtime; the implementing session must falsify the hypothesis cheaply (probe/traceback) before the first edit.

3. **Write task cards** to `docs/plans/<topic>_atomic.md` using `references/task-template.md`.

4. **Create a native Task List in parallel.** After writing the markdown plan, use TaskCreate for each AT-NNN. Dual representation is the point.

5. **Map dependencies.** Annotate parallel-eligible tasks. Default to parallel-eligible when two tasks don't share inputs, outputs, or side effects.

6. **Report**: total tasks, parallel count, recommended first task, estimated total time.

## Anti-patterns (reject during decomposition)

- ❌ Tasks longer than 3 hours — break further.
- ❌ Tasks without a "done when" — not atomic.
- ❌ Vague verbs ("research", "look into", "explore") — replace with deliverables.
- ❌ Re-creating tasks already enumerated in `docs/plan.md` or an existing `docs/plans/*_atomic.md` — extend the existing card instead.
- ❌ Markdown plan without a native Task List — breaks under compaction.
- ❌ Stating a statically-inferred root cause of a runtime error as fact — tag it "hypothesis — reproduce before fixing".

## Output

- `docs/plans/<topic>_atomic.md` (markdown plan, human-readable)
- Native Task List (runtime state)
