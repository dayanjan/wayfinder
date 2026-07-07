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

## Drive Claude Science headlessly via Playwright (automate the UI-only workbench)
**Noted: 2026-07-07.** Claude Science has no task-submission CLI, but its local web UI is fully
drivable — the meta-capability that lets an orchestrator run the research workbench. Recipe
(Playwright 1.60 from the `demo-video` skill's `node_modules`; scripts in `.claude/scratch/cs-drive/`, gitignored):
1. **Auth:** `NONCE=$(wsl -d Ubuntu -- bash -lc 'export PATH=$HOME/.local/bin:$PATH; claude-science url' | grep -oE 'http://localhost:8765/\?nonce=[a-f0-9]+')`; chromium `goto(NONCE)`, **click the "Sign in" button** (the nonce alone does NOT authenticate), then `ctx.storageState({path:'cs_state.json'})` and reuse it on later runs.
2. **Send a prompt:** target `[contenteditable="true"]`, `click({force:true})` (input is disabled while the agent generates), `keyboard.insertText(text)` then `keyboard.press('Enter')`. NEVER type a multi-line prompt key-by-key — a mid-prompt Enter submits early; `insertText` inserts newlines as text.
3. **Approve code:** click **"Allow for this conversation"** once -> auto-approves every subsequent sandboxed code card in that conversation (otherwise it stops on each).
4. **Stop/redirect a wandering agent:** `button[aria-label*="stop" i]` to interrupt, then send the correcting prompt.
5. **Read latest state:** scroll to bottom, `innerText.slice(-2600)` (slice(0,N) returns the OLD top). A "working/thinking/writing/installing" token = still busy.
6. **Extract artifacts to the repo:** plain files under `~/.claude-science/orgs/<org>/workspaces/<ws>/`; copy from the Windows side via `//wsl.localhost/Ubuntu/home/<user>/.claude-science/.../` (dodges MSYS spaced-path mangling).

## Referee verdict structure (the Validator contract)
**Noted: 2026-07-07.** `referee(gene, condition)` -> structured verdict, one hop per evidence
table, driven by `pyzobot_join_spec.json`:
- **HOP 0 GATE first (T4 knockdown-QC):** pass only if >=1 guide `signif_knockdown=True`. Fail -> whole verdict `untested`, STOP. Never report an absent downstream effect as "no effect" when the knockdown failed. This is the artifact catch / hero feature.
- HOP 1 EFFECT (T1); HOP 2 PROGRAM (T2, faceted by BOTH Ota & Hollbacker contrasts — never collapsed to one); HOP 3 DISEASE (T3, `intersecting_genes` ast.literal_eval-exploded, negative-control rows excluded, `supported` requires FDR<0.05).
- Per-hop calibrated status (**supported / refuted / untested / flagged**), each carrying the **exact table value** (OR / p-value / effect size / KD flag) as its receipt. Assert nothing not in the tables. Reference impl: `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`.
