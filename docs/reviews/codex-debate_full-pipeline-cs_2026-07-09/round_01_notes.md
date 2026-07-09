# Round 1 — Codex critique + Claude accept/reject log

Full critique: `.claude/scratch/cs-capability-mining/codex/debate-round1.log` (tail). All findings
repo-verified with file:line. Disposition below (accept/reject/defer, no silent drift).

| # | Codex finding (repo-verified) | Disposition | v2 change |
|---|---|---|---|
| OQ1 | Europe PMC = simple GET reading scalar `hitCount` (sources.py:17,30); Open Targets = GraphQL POST disease-side pagination (sources.py:56,61); `_mcp-*` list only proves MyGene, not these. → **kernel HTTP default; Stage 1 must not depend on connectors.** | ACCEPT | §3 rewritten: kernel HTTP is the path; connectors only opportunistic in Stage 0. |
| OQ2 | Full-sweep volume is ~3935 AB + 12 BC + ≤60 OT pages + **43** AC-lit (survivors only, propose.py:89), NOT 3935×12. Needs a CS-local cache mirroring `_http.py` SHA1/0.34s. A reduced/forced-NAB2 run is **plumbing only**, not funnel reproduction (NAB2 may not be in a top-N slice). | ACCEPT | Corrected math; mandate CS-kernel cache; separate "forced-NAB2 smoke" from "full funnel proof". |
| OQ3 | `host.delegate` gated; driver can't enable Delegation headlessly. `host.llm_batch` adds no independent evidence over referee+Reviewer. | ACCEPT | Stage 4 **dropped from acceptance** (operator-manual only). |
| OQ4 | S3 not yet proven headless. Add a Stage 0 S3 micro-probe (import s3fs/h5py, open, read obs/var labels, close). If it fails, Stage 3 degrades to "run externally, import receipt", don't block. | ACCEPT | Stage 0 gets an S3 micro-probe; Stage 3 has a documented fallback. |
| OQ5 | Provenance mitigation under-specified. `extracted_code` backfills on frame completion (headless may not). **Every stage must save `executed_code.py`+JSON+receipt.md from inside the kernel**; DB = corroboration, not the repro source. | ACCEPT | Made a global rule; DB reframed as corroboration. |
| OQ6 | Full 0→5 not the best use pre-deadline. MVP = Stage 0 + Stage 1 + Stage 3 + Stage 5; Stage 2 next-best; Stage 4 excluded. | ACCEPT | Plan re-scoped to the MVP; Stage 2 = stretch. |
| Acc | Add accept numbers: `bc=2184`, `effect=301`, `ab_gate_value=26`, **NAB2 rank 4** (else a reshuffled run passes). Stage 2: derived clusters + `STAT6 present: False` + cytoband artifact. Stage 3: import checks + no 16.8 GB download. | ACCEPT | Accept-criteria tightened per stage. |
| Miss1 | `host.capabilities()` is NOT a verified method — would waste a run. Real: delegate/llm_batch/mcp/query_db/agent_list/list_artifacts/artifact_path/artifacts. | ACCEPT | Removed `host.capabilities()`; Stage 0 uses real `host.mcp` probes + workspace connector listing. |
| Miss2 | "clean-room" vs "native port": Stage 1 ports our code → it's a **native port with receipt verification**, not clean-room (the tracer was clean-room). | ACCEPT | Terminology fixed throughout. |
| Miss3 | Stop treating "full pipeline in CS" as intrinsically stronger; honest architecture = CS for generation/referee/provenance, Codex external auditor. | ACCEPT | Framing corrected; goal statement rewritten. |
| Bug | Repo doc-staleness: `cooccur.py:11` docstring says `ac_lit<=max_ac` is in the gate, but impl excludes ac_lit (only penalizes; propose.py:68). | ACCEPT (note) | Plan cites `propose.py`; logged as a repo doc-fix for later (not blocking). |

Net: 11/11 accepted, 0 rejected. Round 1 converged hard (repo-verified findings are cheap to accept).
