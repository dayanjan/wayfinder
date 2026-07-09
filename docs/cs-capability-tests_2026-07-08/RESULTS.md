# Claude Science capability tests — RESULTS (2026-07-08, live on our install)

Empirically driven against our own CS install (WSL daemon, `0.1.16-dev`, Opus 4.8) with the hardened
`drive-claude-science` Playwright driver, then **verified from `operon-cli.db` + the extracted
workspace files** (doctrine §19 — not UI scraping). Method + strategy: `../claude-science-test-plan_2026-07-08.md`.
Extracted artifacts: `./artifacts/` (run 1) and `./artifacts-mcp/` (run 2). Run 1 project
`proj_f73a77807d02` (combined audit, ~$3.17); run 2 project `proj_431a9b7f838a` (MCP gene lookup).

## Scorecard (combined audit run 1)

| Cap | Verdict | Evidence (DB + file) |
|---|---|---|
| **C2** host inline model sampling | **PASS** | Two `host.llm_batch` calls in `host_call_log` (no error); `inline_sampling_results.csv` labels all 4 chunks correctly (NAB2 knockdown→yes, dashboard→no, p-value→yes, "interesting"→no). Inline model = **`claude-haiku-4-5`** (per `persona_synthesis.md`). |
| **C5** Reviewer catches error | **PASS (strong)** | `verification_checks` (DB) holds **2** Sonnet-5 findings for the run: a **FAIL** — *"final_summary…line 14 asserts 'The delegation used exactly four personas' while the table immediately below it lists five"* (the planted inconsistency, caught) — and a **WARN** on the delegation→`host.llm` substitution. The reviewer reads the actual saved artifacts to ground its evidence. **Timing:** the FAIL committed to the DB **~10 min after** the driver's "DONE" (reviewer is async). |
| **C6** self-sight figure correction | **PASS** | `scatter_v1.png`→`scatter_v2.png`; `self_correction_note.md`: computed per-axis z-scores, flagged the |z|>3 point (x=8.5,y=−7.2,z_x=4.16), highlighted+labeled it in v2, noted the leverage/robust-estimator caveat. |
| **C7** persistent kernel reuse | **PASS** | `execution_log` cells 7→8→9→15 all kernel `1b2697cb…`; cell 8 reuses `persistent_df`/`persistent_marker` from memory (`assert … in dir()`), no CSV re-read; marker value exact. |
| **C8** R/Python interop | **PASS** | Languages this run: python, r, bash; `ggplot` in R source; `python_to_r_plot.png` produced. **Nuance:** R & Python are **separate processes sharing only the workspace FS — handoff via CSV**, not a shared kernel (`r_interop_note.md`). |
| **C10** multi-persona synthesis | **PASS** | All 5 personas present in `host.llm_batch` args + `delegation_results.csv`; `persona_synthesis.md` synthesizes the 5 lenses to a convergent "knockdown-validation" theme. |
| **C1** `host.delegate` fan-out | **PRESENT-BUT-GATED** | `host_call_log` has a `delegate` call, but it **errored**: *"host.delegate(): delegation is not enabled for this session (ultra mode is off). Enable it via the session's delegation toggle, or use host.llm() for single-shot model calls."* The agent fell back to `host.llm_batch` and disclosed it. → **Programmatic sub-agent delegation requires the session Delegation toggle (off by default in a driver-created project).** |
| **C11** provenance | **PARTIAL — versioning+graph immediate; repro-block deferred** | Immediate: 14 immutable `artifact_versions` (v1, agent=OPERON, language-tagged) + `artifact_dependencies` = 7 rows (the dependency graph). Deferred: the reproducible `extracted_code` block **did NOT backfill** for the driven run even ~15 min later (0/14), while the OPERON frame stayed `processing`. It **does** populate in general (48 prior, interactively-closed artifacts carry it, e.g. 22 KB) → **reconstruction is tied to frame/session completion, which headless driving doesn't trigger.** `environment_snapshot` is NULL even on old artifacts → the repro receipt is `extracted_code`, not env_snapshot. |
| **C3** MCP-as-skill DB lookup *(run 2)* | **PASS (strong)** | `host_call_log` method **`mcp`**, one batched call `host.mcp("genes-ontologies","query_genes",{terms:[5 genes],fields:"…ensembl.gene",species:human})`. `gene_id_lookup.csv` → all 5 **correct real Ensembl IDs** (NAB2 ENSG00000166886, STAT6 …888, IL2 …109471, EGR2 …122877, SATB1 …182568), taxid 9606, all `success`, none fabricated. MyGene.info-backed. Confirms the demo's "MCP-as-skill invoked programmatically in one loop, filter-before-context." |

## Key empirical discoveries (for tomorrow)

1. **`operon-cli.db` is a fully-readable receipt store** — every `host.*` call (`host_call_log`),
   every cell (`execution_log`), every artifact version + provenance (`artifact_versions`,
   `artifact_dependencies`), every reviewer finding (`verification_checks`), and per-frame model +
   token + cost (`frames`). This is the single biggest lever for scripting/auditing CS. Details +
   table map: `../claude-science-test-plan_2026-07-08.md §2`.
2. **Real `host` SDK method names** (from `host_call_log`): `delegate`, `llm_batch`, `mcp`,
   `query_db`, `agent_list`, `list_artifacts`, `artifact_path`, `artifacts`. (Demo said "`host.delegate`
   / `host` samples the LLM" — concretely: inline sampling = **`host.llm_batch`**; MCP/connector calls
   = **`host.mcp("<connector>","<tool>",{args})`** (batched — 5 genes in one call); artifact CRUD =
   `host.artifacts`/`host.artifact_path`.)
3. **`host.delegate` is gated behind a session Delegation ("ultra mode") toggle**, off by default.
   `host.llm_batch` (batched cheap-model sampling) is the ungated path and does the RLM-style
   fan-out. To test true sub-agent delegation we must enable delegation in the session config
   (not exposed by the current headless driver — a future driver extension or a manual toggle).
4. **Actor-critic architecture confirmed live**: OPERON primary = **claude-opus-4-8, effort=high**;
   Reviewer = **claude-sonnet-5**, run as **3 separate REVIEWER frames** (checkpoints + end, exactly
   as the demo described). The reviewer READS the saved artifacts to ground its findings and catches
   real inconsistencies — directly validating our project's referee/falsification thesis with an
   independent product.
5. **Inline cheap model = Haiku 4.5** (`claude-haiku-4-5-20251001`).
6. **Per-frame cost accounting is in the DB.** This ~8-min combined audit cost ≈ **$3.17** (OPERON
   $2.08 + three Sonnet reviewers $0.31+$0.46+$0.28). OPERON input tokens = **1.55M** (reflects
   cache reads / the folding-compaction the demo showed) for 19.5K output. Useful for cost-modeling
   any CS-in-the-loop feature: **the reviewer roughly doubles a run's model spend** (consistent with
   the demo's "~20% of context" telemetry once cache pricing is considered).
7. **Provenance reconstruction is async/deferred** (tied to frame completion), and `environment_snapshot`
   is not populated — the durable repro receipt is `artifact_versions.extracted_code` + the
   `artifact_dependencies` graph. When scripting a "pull the receipts" step, wait for frame
   completion (or poll) before reading `extracted_code`.
8. **The Reviewer runs asynchronously AFTER the driver's "DONE"** (Stop button gone ≠ receipts
   landed). Findings + provenance land minutes later. Any automation must poll `verification_checks`
   / `frames.status` post-run rather than trust the Playwright done-signal.

## Driver hardening — validated live
The hardened `cs-drive.js` auto-approved **2 cards** ("allow for this conversation") cleanly and
polled to a correct DONE with **no hang and no misfire** on the broadened regexes. The added
MCP-use / usage-velocity / snooze patterns didn't spuriously match anything in this run. (Change:
added `allow for this project`/`allow once`/`snooze`/`continue`; broadened `PENDING`; deliberately
**not** auto-clicking "Allow globally".)

## Caveats / method notes
- The DB verifier's C7 "PARTIAL" and C11 "FAIL" are **heuristic artifacts**, not real failures:
  C7 mixed the `host-tool`/`skill-sidecar` pseudo-kernels into the kernel-id set (the real python
  kernel is single + reused); C11 filtered on a literal that didn't match + on the unused
  `environment_snapshot`. Manual inspection resolves both to PASS/confirmed.
- One combined run exercised 6 capabilities + triggered the reviewer — the "combined live-fire"
  doctrine (§3) worked: ~8 min + ~$3 verified what would have been 6 sequential runs.
