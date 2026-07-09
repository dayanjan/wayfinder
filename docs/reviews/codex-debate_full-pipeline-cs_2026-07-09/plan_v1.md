# Plan — rebuild the full LBD→NAB2 pipeline inside Claude Science (v1, pre-debate)

**2026-07-09.** Goal: reproduce the *entire* instrument + finding natively in Claude Science (CS),
as a clean-room reproduction (the external result is already validated). Method for every stage:
**drive CS headlessly (`drive-claude-science`) → verify from `operon-cli.db` + workspace files**
(doctrine §19), never UI-scrape. This v1 goes into a 3-round repo-read codex-debate; the open
questions in §7 are the debate's job.

## 1. What's already proven (don't redo)
The **tracer** (`docs/cs-capability-tests_2026-07-08/tracer-artifacts/TRACER-RESULTS.md`) already
reproduced the **4-hop referee + the NAB2 finding digit-for-digit natively in CS**, from the raw
tables in `/home/dayanjan/pyzobot-data/`, with CS's own pandas, plus an unprompted in-kernel
self-audit. So **Stage C+D of the pipeline is DONE in CS.** This plan covers the rest: the **LBD
proposer (A–B)**, the **confounder checks (E2)**, the **definitive S3 cis-check (E4)**, optional
**in-CS multi-agent validation (E1/E5)**, and pulling the **whole receipt chain + provenance**.

## 2. Environment facts (known)
- CS daemon up on :8765 (WSL); Opus-4.8 primary + Sonnet-5 Reviewer; inline `host.llm_batch` = Haiku 4.5.
- Data: 4 tables + `join_spec.json` already in `/home/dayanjan/pyzobot-data/` (ext4). Referee reads them
  with **no connectors** (pure pandas) — proven.
- Real `host` API (from `host_call_log`): `mcp("<connector>","<tool>",{args})`, `llm_batch`, `delegate`
  (**gated** behind the session Delegation toggle), `query_db`, `artifacts`/`artifact_path`.
- Connectors present in our install (from the `_mcp-*` workspaces): literature, genes-ontologies,
  human-genetics, clinical-genomics, biomart, expression, genomes, variants, drug-regulatory, regulation,
  protein-annotation, rna, omics-archives, cancer-models, structures-interactions, chemistry, ketcher,
  zinc, research-resources, cellguide. **Open Targets exact coverage = OPEN QUESTION (§7).**
- Async gotchas: driver "DONE" ≠ receipts landed; Reviewer findings + `extracted_code` provenance backfill
  on frame completion — **poll `operon-cli.db` after each run.**

## 3. The one load-bearing design decision (needs the debate)
The LBD needs **co-mention COUNTS** (Europe PMC `hitCount` — a single integer) and **Open Targets
association scores**, not document lists. Two ways in CS:
- **(a) `host.mcp` connectors** — cleanest if the literature/genetics connectors expose a count/score
  tool. Risk: the literature MCP may return *documents*, not a `hitCount`; Open Targets may not be a
  connector at all.
- **(b) kernel HTTP** — CS's Python kernel calls Europe PMC `search?...&resultType=idlist` (read
  `hitCount`) and Open Targets GraphQL directly, exactly like our `src/arbiter/lbd/sources.py`, behind a
  **network-domain approval card** (auto-approved by the driver). Robust, mirrors the validated code, zero
  connector-shape risk.
- **Recommendation (pre-debate): default to (b) kernel HTTP** (port `sources.py` into the CS kernel), and
  use `host.mcp` only where a connector cleanly returns the exact scalar. Debate should confirm.

## 4. Staged build (each stage = 1 driven CS run + a DB verify)
**Stage 0 — connector/feasibility recon (~10 min, cheap).** One CS run: from the kernel, (i) list
capabilities (`host.capabilities()` / the featured connectors), (ii) attempt a literature `hitCount`
BOTH via `host.mcp("literature",…)` and via a kernel HTTP call to Europe PMC, (iii) attempt an Open
Targets association lookup both ways, (iv) confirm a network-domain approval is granted headlessly.
Decide (a) vs (b) per §3 from the receipts. **Accept:** we can obtain a Europe PMC hitCount and an Open
Targets score for one (gene,disease) pair, logged in `host_call_log`/`execution_log`.

**Stage 1 — LBD proposer in CS.** Port `entities.build_a_universe` + `cooccur`/`propose` into the CS
kernel (our code, adapted): build the **answer-free A-universe** (pandas over T4∩T1∩T2 → 3,935), compute
the 5 signals (co-mention via the §3 winner; `effect`=n_downstream), apply the **gate + balanced score**,
run the **referee-cull-first** (reuse the tracer's `referee.py`), emit the funnel. **Accept (verify from
files + DB):** funnel reproduces **3,935 → 22,039 → 43 → 30 clean**; **NAB2→atopic eczema present with
ac_lit≈6, ac_known≈0.038, referee=supported**; save `sweep_Stim8hr.json` + `lbd_questions_Stim8hr.json`.

**Stage 2 — confounder checks in CS.** Port `nab2_stat6_confounder_check.py` (+ EGR + cis-proxy): derive
the FDR<0.05 clusters, map members to cytobands (MyGene / `host.mcp("genes-ontologies")`), show sig
clusters 90&100 are genome-wide modules with STAT6 absent; NAB1 paralog opposition. **Accept:** clusters
**90 & 100**, STAT6 absent, NAB1 opposes — matches `docs/replication`.

**Stage 3 — definitive S3 cis-check in CS.** Kernel `s3fs(anon)` + `h5py` lazy read of the single
NAB2@Stim8hr row from `s3://genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad`, behind
a network-domain approval for the S3 host. **Accept:** **STAT6 log2FC ≈ +0.09, adj-p ≈ 0.79** (cis
excluded); NAB2 on-target ≈ −3.08. (CS is built for h5ad — showcase.)

**Stage 4 — in-CS multi-agent validation (OPTIONAL; needs Delegation toggle).** With Delegation ON, use
`host.delegate` to run a small internal replication panel (receipt / funnel / confounder personas) +
CS's Reviewer. **Explicitly Claude-only** — this does NOT replace the external Codex cross-model pass.
**Accept:** the panel independently re-derives the NAB2 receipt; findings in `verification_checks`.

**Stage 5 — assemble the receipt chain + provenance.** One writeup artifact tying HOP-0→HOP-3 receipts +
the funnel + the confounder closures; request a CS Reviewer pass; pull the full provenance
(`host_call_log`, `execution_log`, `artifact_versions`, `verification_checks`) from `operon-cli.db` into
`docs/cs-full-pipeline_<date>/`. **Accept:** end-to-end chain reproduced with CS-native provenance.

## 5. What stays EXTERNAL (the one thing CS can't be)
- **Codex cross-model replication** + the **codex-debate** spec-hardening: CS is Anthropic-only, so
  second-model-family independence lives outside CS. Architecture = **CS is the instrument; Codex is the
  external auditor.** Keep the existing `docs/replication/` (Opus×3 + Codex×2) as the cross-model record.

## 6. Sequencing, cost, verification
- Order 0→1→2→3→(4)→5; each is completable + independently verified (finish-what-you-start, §14).
- Cost estimate: ~$2–4 per driven CS run (from prior runs); Stage 1 may be longer (co-mention volume) —
  consider a **reduced sweep** (one condition, or a gene subset) to prove reproduction cheaply, then scale.
- Every stage: capture `run_start_ms`, drive with `--new`, extract files, **poll `operon-cli.db`** for the
  reviewer/provenance backfill, verify the accept-criteria numbers against the known values.

## 7. OPEN QUESTIONS for the 3-round codex-debate
1. **Connector vs kernel-HTTP for co-mention/OpenTargets (§3):** does our install expose an Open Targets
   connector + a literature `hitCount` tool, or is kernel HTTP the reliable path? Verify against the repo's
   `sources.py` (the exact endpoints/params) and the known `_mcp-*` list.
2. **Europe PMC call volume (~4.4k `ab` calls):** headless via CS kernel — rate-limit/politeness, caching
   (CS `tool-results/`? or a kernel-side cache like `data/lbd_cache/`?), and whether a **reduced sweep**
   is the right first proof. What's the smallest run that still surfaces NAB2?
3. **Delegation toggle headlessly:** can the driver enable Delegation (Settings) for Stage 4, or must the
   operator flip it? Is Stage 4 worth it given it's Claude-only (does it add evidence over Stage 1's
   deterministic referee + CS Reviewer)?
4. **S3 network approval + data-access:** will the driver's auto-approver clear the network-domain card for
   the S3 host? Any compliance concern reading the authors' public anon-S3 h5ad from CS?
5. **Provenance completeness:** given `extracted_code` backfills only on frame completion (headless doesn't
   trigger), how do we guarantee we capture the reproducible blocks — an explicit end-of-run step, or a
   post-run poll window?
6. **Scope realism vs the deadline (2026-07-13):** is full-pipeline-in-CS the best use of remaining time
   vs. a tighter "Stage 1 + Stage 3 + Stage 5" MVP that proves *generation → definitive-check → provenance*
   natively? Recommend the minimal set that tells the strongest true story.

## 8. Acceptance (whole plan)
The LBD proposer, confounder checks, and definitive S3 check all run **natively in CS** and reproduce the
known numbers (funnel 30 clean; NAB2 receipt; STAT6 +0.09/0.79), with the full receipt chain + provenance
pulled from `operon-cli.db`, and the external Codex cross-model record intact. Then: the instrument, the
generation of the question, the answer, the falsification, and the provenance **all live in the workbench**.
