# Claude Science — capability test plan & the `operon-cli.db` receipt store

**2026-07-08.** How we empirically verify Claude Science (CS) capabilities against our own install,
and the key discovery that makes it cheap and reliable. Produced by a 2-round repo-read codex-debate
(doctrine §22) on the testable inventory in `claude-science-demo-findings_2026-07-08.md §8`. Debate
record: `.claude/scratch/cs-capability-mining/codex/round{1,2}-codex.log`.

---

## 1. The strategy: drive with Playwright, VERIFY FROM DISK

CS has no task CLI, so we still **drive** it with the `drive-claude-science` Playwright driver
(send a prompt → auto-approve cards → poll). But for **verification** we do NOT scrape the UI (the
scraped text tail is unreliable, and the Reviewer panel / provenance tabs are UI-only). Instead we
read CS's own **on-disk receipt store**. This is doctrine §19 (prefer direct/DB over UI) and it is
on-thesis for this project: *CS keeps a receipt for every hop, and we can read the receipts.*

## 2. THE DISCOVERY — `operon-cli.db` is a fully-readable audit DB

Path: `~/.claude-science/orgs/<org>/operon-cli.db` (SQLite). It opens **read-only even while the
daemon runs**: `sqlite3.connect("file:<db>?mode=ro&immutable=1", uri=True)`. (No `sqlite3` CLI in the
WSL image — use WSL `python3`.) It is the ground truth for almost every capability:

| Table | Key columns | Verifies |
|---|---|---|
| **`host_call_log`** | `method`, `args_json`, `data_inline`, `error`, `execution_log_id` | **C1** `host.delegate`, **C2** inline model sampling, MCP calls (**C3**) — every `host.*` SDK call is logged |
| **`verification_checks`** | `claim`, `verdict`(warn/fail), `severity`, `evidence`, `rebuttal`, **`reviewer_model`**, `reviewer_kind`, `status`, `artifact_version_id`, `root_frame_id` | **C5** the **Reviewer** findings. Already holds 4 real catches from our prior runs; **`reviewer_model="claude-sonnet-5"` — this CONFIRMS the reviewer runs Sonnet 5** (the demo never stated the model) |
| **`execution_log`** | `frame_id`, `cell_index`, **`kernel_id`**, `conda_env`, `language`, `source`, `stdout`, `stderr`, `files_written`, `files_read` | **C7** kernel reuse (same `kernel_id` across cells), **C8** language (py/R), plus `host.*` usage in `source` |
| **`artifact_versions`** | `extracted_code`, `code_description`, `lineage_messages`, `environment_snapshot`, `dependency_mappings`, `version_number`, `agent_name`, `is_checkpoint` | **C11** provenance completeness (the reproducible block + env snapshot + lineage, on disk) |
| **`artifact_dependencies`** | `artifact_version_id`, `depends_on_version_id`, `reference_name` | **C11** the provenance dependency graph |
| **`frames`** | `agent_name`, **`model`**, `effort`, `delegate_name`, `specialists_used`, `total_cost`, `input/output_tokens`, `root_frame_id`, `project_id` | sub-agent/reviewer **models & cost per frame**; a `REVIEWER` frame confirms a review ran; delegate frames corroborate C1 |
| **`frame_messages`** | `frame_id`, `idx`, `msg_json` | full conversation transcript (the "lagging tail" content) |
| **`user_agents`** | `name`, `system_prompt`, `skill_names` | **C9** specialists |
| **`memories`**, **`memory_categories`** | `body`, `category_id`, `name`, `guidance` | **C12** 4-tier memory (empty by default — off unless enabled) |
| **`compaction_archives`** | `frame_id`, `summary`, `messages`, `token_count` | **C15** folding compaction |
| **`annotations`**, **`transcript_annotations`** | `target_kind`, `body` | **C14** annotations |
| **`host_grants`**, **`mcp_tool_grants`**, **`directory_attachments`** | grants + the 24 connector attachments | permission/connector state |

**Consequence:** capabilities Codex round-1 flagged as "NEEDS-DRIVER-EXTENSION" because they live in
UI tabs (C5 reviewer, C11 provenance) are in fact **DB-verifiable tonight with zero UI scraping.** The
Playwright driver's only job is to make CS *do* the work and clear approval cards.

## 3. The test artifacts (in `.claude/scratch/cs-capability-mining/`)

- **`prompts/audit-db.txt`** — one combined "capability audit" prompt (Parts A–G) that in a single CS
  session exercises **C1** (`host.delegate` → 5 personas), **C2** (inline model yes/no sampling),
  **C6** (scatter v1→v2 self-correction past 3σ), **C7** (`persistent_marker` kernel reuse), **C8**
  (Python→R ggplot), **C10** (5-persona synthesis), and **plants a 4-vs-5 persona count
  inconsistency** in a final summary to trigger the **Reviewer (C5)**; it saves `executed_code.py`
  for **C11**.
- **`prompts/audit-mcp.txt`** *(optional 2nd run)* — resolve canonical IDs for NAB2/STAT6/IL2/EGR2/
  SATB1 via the bio MCPs → verifies **C3** from `host_call_log` MCP methods + the output CSV.
- **`verify_cs_capabilities.py`** — the DB verifier. `python3 verify_cs_capabilities.py <db>
  <run_start_ms> [name_substr]`: finds the run's project (newest `projects.created_at > run_start_ms`),
  lists its frames (agents/models/cost), then prints **PASS / PARTIAL / FAIL** per capability with
  evidence, encoding the round-2 SQL.

## 4. Run procedure (drive → wait → verify)

1. Capture `run_start_ms` (now − 5s margin) and `touch ~/.cs_marker` (artifact-extraction marker).
2. Mint a login nonce (`claude-science url`), launch the driver with `--new "<name>"` + the prompt.
3. On DONE, **do not trust the scraped tail.** Extract workspace files:
   `wsl … 'find ~/.claude-science/orgs -type f -newer ~/.cs_marker'` (grep out `/artifacts/`,
   `__pycache__`), copy via the `//wsl.localhost/Ubuntu/…` UNC path.
4. Run `verify_cs_capabilities.py`. **Re-run it 2–5 min later if C5 is FAIL** — the Reviewer runs
   asynchronously and may write `verification_checks` *after* the Stop button vanishes (driver "DONE"
   means *agent stopped*, not *all receipts landed*). If still empty, send the fallback
   review-request prompt into the same project.

## 5. Driver hardening applied (`cs-drive.js`)

The demo revealed approval-card types the old regex missed. Applied (verified `node --check`):
- `APPROVE` now also matches `allow for this project`, `allow once`, `snooze` (dismisses the
  usage-velocity guard), `continue` — ordered conversation/project-scope first. **Deliberately NOT
  auto-clicking `Allow globally`** (the demo shows a big "code runs the moment Claude writes it"
  warning; conversation/project scope is enough).
- `PENDING` now also matches **MCP-use**, **network-domain**, **connector**, **usage-velocity /
  5-hour-limit / snooze** cards so the poll loop waits for them instead of declaring "done" with a
  card still open.
- **Deferred:** plan-mode dropdown click (C4). The DB makes plan mode verifiable without it, and it's
  not in tonight's set.

## 6. Capability testability summary (post-discovery)

- **DB-verifiable tonight:** C1, C2, C5, C6, C7, C8, C10, C11 (combined run); C3 (optional MCP run).
- **DB-verifiable but not exercised tonight:** C9 (`user_agents`), C12 (`memories`; off by default),
  C14 (`annotations`), C15 (`compaction_archives`) — data appears only if the feature is used.
- **Skip:** C4 plan-mode (needs driver dropdown), C13 GPU biomodel (heavy/risky unattended; we DO
  have an RTX 3090 in WSL, so it's a future single-purpose run).
- **Already demonstrated** (don't re-test): the end-to-end headless drive itself; the QC/join/referee
  YES/UNTESTED/REFUTED run (`docs/perturbseq-qc_2026-07-07/`); the independent evidence-chain
  reproduction + figure (`docs/claude-science-evidence-chain_2026-07-08/`).

*Results land in `docs/cs-capability-tests_2026-07-08/` after the run.*
