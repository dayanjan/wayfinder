# Plan — reproduce the LBD→NAB2 pipeline natively in Claude Science (v3 — FINAL / codex-debate SHIP)

> **Status: SOLIDIFIED.** 3-round repo-read codex-debate (2026-07-09) → **SHIP** ("executable and
> honest," no material findings in round 3). Trajectory: 11 findings (r1, all accepted) → 8
> spec-completions (r2, 0 re-escalations) → 0 (r3). Record:
> `docs/reviews/codex-debate_full-pipeline-cs_2026-07-09/`. **Ready to implement next session.**

**2026-07-09.** Goal: run the *scientifically load-bearing* stages of the instrument **natively in
Claude Science (CS)** and reproduce the known numbers, with receipts + provenance pulled from
`operon-cli.db`. **This is a NATIVE PORT with receipt verification** (we port our validated code into
the CS kernel and check its output) — NOT a clean-room re-derivation (that was the tracer, which wrote
its own referee from rules). The honest winning architecture: **CS is the instrument (generation →
referee → provenance); Codex stays external as the cross-model auditor** — cross-model independence is
structurally outside CS, and no CS stage changes that. Every stage: **drive CS headlessly → verify from
saved kernel files + `operon-cli.db`** (doctrine §19). Rev history: v1 + round-1 critique in
`docs/reviews/codex-debate_full-pipeline-cs_2026-07-09/`.

## 1. Already proven (do not redo)
The **tracer** reproduced the **4-hop referee + NAB2 finding digit-for-digit natively in CS** from the
raw tables, CS writing its own referee (`docs/cs-capability-tests_2026-07-08/tracer-artifacts/`). So the
data-substrate + referee (pipeline C+D) is DONE in CS. This plan covers **generation (LBD proposer)**,
the **definitive S3 cis-check**, and **provenance assembly** — the MVP — plus an optional confounder stage.

## 2. Scope (MVP — round-1 re-scoped for the 2026-07-13 deadline)
- **Stage 0** — feasibility probe (kernel HTTP + S3 micro-probe). ~10 min.
- **Stage 1** — LBD proposer natively (kernel HTTP + CS-local cache) → reproduce the funnel + NAB2 row.
- **Stage 3** — definitive STAT6 cis-check natively (anon S3 + h5py lazy read).
- **Stage 5** — assemble the end-to-end receipt chain + provenance from files + `operon-cli.db`.
- **Stage 2** (confounder checks) = **stretch**, only if time remains.
- **Stage 4** (in-CS multi-agent) = **EXCLUDED** — `host.delegate` is gated and the driver cannot enable
  the Delegation toggle headlessly; `host.llm_batch` adds no independent evidence over referee+Reviewer.
  Cross-model replication stays in Codex (existing `docs/replication/`).

## 3. THE design decision — RESOLVED: kernel HTTP (not connectors)
Verified from `src/arbiter/lbd/sources.py`: Europe PMC co-mention = a simple **GET** to
`.../europepmc/webservices/rest/search` (`query`, `format=json`, `pageSize=1`) reading the scalar
**`hitCount`** (sources.py:17,30); Open Targets known-assoc = a **GraphQL POST** to `/api/v4/graphql`,
disease-side `associatedTargets(page:{index,size})` pagination (sources.py:56,61). Neither is a
connector shape; the `_mcp-*` list only proves a MyGene-backed `genes-ontologies`. → **Port `sources.py`
+ `_http.py` into the CS kernel and call these endpoints directly** behind a network-domain approval
(auto-approved by the driver). Use `host.mcp("genes-ontologies",…)` only where a connector cleanly
returns the exact scalar (e.g. cytoband for Stage 2). **Do NOT call `host.capabilities()` — not a real
method;** in Stage 0, probe real `host.mcp(...)` + list the workspace `_mcp-*` connectors instead.

## 4. Global rules (apply to every stage)
1. **Provenance is first-class from the kernel, not the DB.** Each stage explicitly saves, from inside
   the kernel: `executed_code.py` (the real code), the result **JSON**, and a **receipt.md**. Treat DB
   `extracted_code` as *corroboration only* — it backfills on frame completion, which headless runs may
   not trigger.
2. **CS-local cache.** Mirror `_http.py`'s SHA1-of-`{m,u,p}` (sorted keys, 20-hex) → JSON cache (0.34 s
   politeness) inside the CS workspace (`lbd_cache/<sha1>.json` + a `lbd_cache/manifest.jsonl`) so the run
   is offline-replayable and each rate-limited endpoint is hit once. Do NOT rely on CS `tool-results/`
   caching (won't match request payloads). **Caveat:** the kernel teardown at session end does NOT defeat
   a workspace *disk* cache, but a fresh `--new` project gets a fresh workspace — so to replay in a new
   project, **first copy the prior `lbd_cache/` into the new workspace** (extract it in Stage 5, re-import
   at the next run's start).
3. **Per-stage deterministic verifier** keyed by `run_start_ms`: expected files exist, expected JSON
   fields match, expected `operon-cli.db` rows present. Poll `verification_checks` + `frames.status`
   AFTER the driver's "DONE" (receipts land late).
4. **Drive → wait → verify**; capture `run_start_ms`, `--new` project, extract files, poll DB.

## 5. Stages

### Stage 0 — feasibility probe (one driven run)
From the CS kernel: (a) GET Europe PMC hitCount for one pair (e.g. `"NAB2" AND "atopic eczema"` → expect
6) and `"NAB2" AND Th2 terms`; (b) POST Open Targets GraphQL for asthma disease→targets (expect a
paginated score list); (c) **S3 micro-probe**: `import s3fs, h5py`; open
`s3://genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad` anon, read only obs/var
labels, close; (d) list the workspace `_mcp-*` connectors. Save `stage0_probe.json` + `executed_code.py`.
Save the **exact query strings** used (for audit). **Distinguish two failure modes:** (i) *missing
package* (`s3fs`/`h5py` not in CS's lean base env — `requirements.txt` has them but CS base may not) →
`micromamba/pip install` into the workspace env and continue; (ii) *S3/network blocked* → real blocker.
**Accept:** a real `hitCount` integer (with its query string) + an Open Targets score + the S3 file opens
and yields obs/var labels, all in saved files + `host_call_log`/`execution_log`. **Only if (ii) → Stage 3
uses the external fallback** (run `nab2_stat6_definitive_check.py` outside CS, import the receipt).

### Stage 1 — LBD proposer natively (port sources.py+cooccur+propose)
Port the answer-free A-universe (T4∩T1∩T2 → 3,935) + the 5 signals (kernel HTTP + CS-local cache;
`effect`=n_downstream) + the **gate** (`ab≥ab_gate ∧ bc≥3 ∧ ac_known≤0.1`; **`ac_lit` is NOT in the gate**
— cite `propose.py:68`, not the stale `cooccur.py:11` docstring) + the **balanced score** + the
**referee-cull-first** (reuse the tracer's `referee.py`). Emit `sweep_Stim8hr.json` +
`lbd_questions_Stim8hr.json` + `executed_code.py`.
- **Plumbing smoke first (cheap):** a `max_genes` slice that FORCE-INCLUDES NAB2 to prove the HTTP+cache+
  score+referee plumbing end-to-end — but this is **plumbing only, NOT funnel reproduction** (NAB2 need
  not be in a natural top-N slice).
- **Then the real proof — full Stim8hr sweep.** **Accept (exact, checkable):** `a_genes=3935`,
  `eligible_pairs=22039`, `disease_c_supported_total=43`, `clean_supported=30`, `pure_disjoint_clean=1`,
  `ab_gate_value=26`; and the **NAB2→atopic eczema** row present with `ab=66`, `bc=2184`, `ac_lit=6`,
  `ac_known=0.0376`, `effect=301`, `referee_answer=supported`, **rank 4**.

### Stage 3 — definitive STAT6 cis-check natively (or external fallback)
Port `nab2_stat6_definitive_check.py`: anon `s3fs` + `h5py`, lazy-read the single **NAB2@Stim8hr** row,
report STAT6 + neighbor selected-gene values. Save JSON + receipt.md + `executed_code.py`.
**Accept:** imports `s3fs`/`h5py` OK, **no 16.8 GB download** (lazy read only), **STAT6 log2FC ≈ +0.09,
adj-p ≈ 0.79** (cis excluded), NAB2 on-target ≈ −3.08. **Fallback if S3 blocked headless:** run the
script externally, import the receipt into the CS writeup, and label it "external-data step."

### Stage 5 — assemble receipt chain + provenance
One CS writeup artifact tying HOP-0→HOP-3 receipts + the funnel + the S3 cis-exclusion; request a CS
Reviewer pass on it; pull the full provenance (`host_call_log`, `execution_log`, `artifact_versions`,
`verification_checks`) from `operon-cli.db` into `docs/cs-full-pipeline_<date>/`. **Accept:** end-to-end
chain reproduced natively with kernel-saved receipts + DB corroboration; ≥1 Reviewer finding row (or a
clean pass) captured.

### Stage 2 — confounder checks (STRETCH)
Port `nab2_stat6_confounder_check.py` (+ EGR): **derive** the FDR<0.05 clusters dynamically (do NOT
hardcode; the repo notes a stale `[74,90]`), map members to cytobands (MyGene / `host.mcp`).
**Accept:** derived significant clusters = **90 & 100**, **`STAT6 present: False`**, a cytoband-evidence
artifact (not just prose), NAB1 paralog opposition.

## 6. What stays EXTERNAL
Codex cross-model replication + the codex-debate: CS is Anthropic-only, so second-model-family
independence lives outside CS. Keep `docs/replication/` (Opus×3 + Codex×2) as the cross-model record.

## 7. Cost / sequencing
Order 0→1→3→5→(2); each completable + independently verified (§14). ~$2–4 per driven run; Stage 1 full
sweep is the long one (cache makes it replayable). Deadline 2026-07-13 → the MVP (0/1/3/5) is the
committed scope; Stage 2 only if time.

## 8. Acceptance (whole MVP)
The **LBD proposer** (generation) runs **natively in CS** over the full 3,935-gene A-universe and
reproduces the known funnel (3935/22039/43/30) with the **NAB2 row incl. rank 4 & bc=2184**; the
**definitive STAT6 cis-check** reproduces **STAT6 +0.09 / adj-p 0.79** (cis excluded) — **natively in CS
IF the S3 in-CS path succeeds (Stage 0-(ii) passed); otherwise via the labelled external-data fallback**.
Provenance (kernel-saved receipts + `operon-cli.db` corroboration) is captured, and the Codex cross-model
record stays intact. **Conditional claim:** *if* Stage 3 ran in-CS, then the question's generation, the
answer, its hardest falsification, and the provenance **all live in the workbench**; *if* the fallback was
used, the phrasing is "generation + provenance in the workbench; the hardest external-data check run
alongside" — never overstate. Codex remains the honest external second opinion (cross-model independence).

## 9. Runnable checklist (write-for-the-weaker-model — next-session executor)

**Fixed facts.** Daemon on :8765 (`wsl -d Ubuntu -- bash -lc 'export PATH=$HOME/.local/bin:$PATH; claude-science status'`).
Data: `/home/dayanjan/pyzobot-data/` (4 CSVs + join_spec.json). Driver: `~/.claude/skills/drive-claude-science/cs-drive.js`
(auth `cs_state.json` beside it). Org/DB: `/home/dayanjan/.claude-science/orgs/741d6512-1f39-4a9e-b5bb-9663fd77e1a5/operon-cli.db`
(read via WSL `python3`, `file:<db>?mode=ro&immutable=1` — no `sqlite3` CLI). Scratch scripts + prompts:
`.claude/scratch/cs-capability-mining/`.

**Per driven stage (generic recipe):**
```bash
REPO="C:/Users/wijesingheds/Documents/04 Fun with Coding/2026-07-07 PyZoBot-Arbiter"
SKILL="C:/Users/wijesingheds/.claude/skills/drive-claude-science"
SCR="$REPO/.claude/scratch/cs-capability-mining"
RUN_MS=$(python -c "import time;print(int(time.time()*1000)-5000)"); echo "$RUN_MS" > "$SCR/run_start_ms_<stage>.txt"
wsl -d Ubuntu -- bash -lc 'touch ~/.cs_marker_<stage>; sleep 1'
NONCE=$(wsl -d Ubuntu -- bash -lc 'export PATH="$HOME/.local/bin:$PATH"; claude-science url' | grep -oE 'http://localhost:8765/\?nonce=[a-f0-9]+')
cd "$SKILL" && node cs-drive.js --new "PyZoBot <stage> 20260710" --url "http://localhost:8765/" \
  --prompt-file "$SCR/prompts/<stage>.txt" --nonce "$NONCE" --max-min 25   # backgrounded
# after DONE: extract (OPERON frame id = the workspace dir name; find its project via the Stage-5 SQL)
wsl -d Ubuntu -- bash -lc "find ~/.claude-science/orgs/741d6512-*/workspaces/<OPERON_FRAME>/<outdir> -type f -newer ~/.cs_marker_<stage>"
# then VERIFY: run the DB queries below keyed by $RUN_MS; check the stage's accept JSON fields in the
# extracted files. POLL verification_checks + frames.status ~5-10 min AFTER "DONE" (reviewer/backfill async).
```
Prompts to author (one per stage) live in `$SCR/prompts/`: `stage0-probe.txt`, `stage1-lbd.txt`,
`stage3-s3.txt`, `stage5-provenance.txt`. Each prompt MUST end by saving `executed_code.py` + result
JSON + `receipt.md` inside the workspace (global rule §4.1).

**Stage 5 provenance SQL** (run read-only; `?`/`(...)` = `run_start_ms` / the run's frame ids):
```sql
-- 1) the run's project
SELECT id, name, created_at FROM projects WHERE created_at > ? OR lower(name) LIKE ? ORDER BY created_at DESC LIMIT 1;
-- 2) frames (models/effort/cost — proves OPERON+REVIEWER ran)
SELECT id, root_frame_id, agent_name, model, effort, delegate_name, specialists_used, status, input_tokens, output_tokens, total_cost, created_at FROM frames WHERE project_id = ? ORDER BY created_at;
-- 3) execution_log (the actual code + files read/written)
SELECT cell_index, kernel_id, language, source, stdout, stderr, files_read, files_written, created_at FROM execution_log WHERE frame_id IN (...) ORDER BY created_at, cell_index;
-- 4) host_call_log (every host.* call: mcp/llm_batch/…)
SELECT h.method, h.args_json, h.data_inline, h.error, h.created_at, e.frame_id, e.cell_index FROM host_call_log h LEFT JOIN execution_log e ON e.id = h.execution_log_id WHERE h.created_at > ? AND e.frame_id IN (...) ORDER BY h.created_at;
-- 5) artifact_versions (immutable versions + repro-block lengths)
SELECT artifact_id, version_number, language, agent_name, is_checkpoint, length(extracted_code) ec_len, length(code_description) cd_len, length(lineage_messages) lin_len, length(dependency_mappings) dep_len, created_at FROM artifact_versions WHERE created_at > ? ORDER BY created_at;
-- 6) artifact_dependencies (provenance graph)
SELECT artifact_version_id, depends_on_version_id, reference_name, created_at FROM artifact_dependencies WHERE created_at > ?;
-- 7) verification_checks (the Reviewer's findings)
SELECT claim, verdict, severity, evidence, rebuttal, reviewer_model, reviewer_kind, status, artifact_version_id, root_frame_id, created_at FROM verification_checks WHERE created_at > ? ORDER BY created_at;
```
"Provenance captured" = queries 2–5 + 7 return non-empty rows for the run, extracted to
`docs/cs-full-pipeline_<date>/`. Reuse `.claude/scratch/cs-capability-mining/verify_cs_capabilities.py`
+ `probe_tracer.py` as starting points.
