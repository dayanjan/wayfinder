# The full LBD→NAB2 pipeline — exhaustive inventory + Claude Science mapping

**2026-07-09.** Part 1 is an exhaustive, ordered inventory of *everything we did* to go from "rich
dataset, no question" to the receipt-backed **NAB2 → Th1/Th2 → atopic-eczema** nomination. Part 2
maps each step to Claude Science: can it be done there, how, and what can't. Reconstructed from the
actual code/artifacts by a 3-agent recon (LBD engine · data+referee · validation gauntlet); the
long-form backups are those agents' notes. CS mapping uses the 2026-07-08 capability findings
(`cs-capability-tests_2026-07-08/RESULTS.md`).

**Verdict key:** ✅ CS-native (as good or better) · 🟡 CS-partial (needs the Delegation toggle, or
loses cross-model independence) · ❌ not in CS (needs OpenAI/Codex, i.e. a second model family).

---

## PART 1 — Exhaustive inventory (30 steps, 6 stages)

### A. Setup & entities
- **A1. Cached deterministic HTTP + `.env` layer** — `_http.py`: SHA1 cache key → on-disk JSON cache
  (`data/lbd_cache/`), 0.34 s politeness, keyless where possible. Makes the whole run offline-reproducible.
- **A2. Disease→ontology map + reproducible ID verification** — `entity_maps.DISEASES` (12 eligible
  MONDO diseases incl. atopic eczema `MONDO_0004980`) re-resolved live against **Open Targets GraphQL
  search + EBI OLS4** (`verify_disease_ids.py`). Load-bearing: MONDO≠EFO — a wrong id would make Open
  Targets return "no known association" for every gene and falsely inflate novelty everywhere.
- **A3. Program keyword arms + asymmetric term policy** — `entity_maps.PROGRAM`: Th1/Th2 process +
  marker arms; A-B uses process-only (don't inflate on marker proximity), B-C keeps markers.

### B. LBD Swanson-ABC proposer (generates the questions)
- **B1. Answer-free A-universe build** — pandas over T4 (KD gate) ∩ T1 (significant effect) ∩ T2
  (program-significant) → **3,935 genes**; never touches any disease table.
- **B2. A-B co-mention** (gene↔Th1/Th2) — Europe PMC `hitCount`, all terms quoted.
- **B3. B-C co-mention** (program↔disease) — Europe PMC `hitCount`.
- **B4. A-C known-association fetch (the set to EXCLUDE)** — Open Targets GraphQL disease→targets,
  paginated (page 3000), score floor 0.05; absent gene ⇒ novelty signal. One call/disease (12).
- **B5. A-C literature co-mention** — Europe PMC; deferred to referee survivors for API cost.
- **B6. Preflight go/no-go** — bounded sample × 12 diseases; confirm disjoint survivors exist (GO: 10/216).
- **B7. Gated + balanced scoring objective** — gate: `ab≥pctile ∧ bc≥3 ∧ ac_known≤0.1`; rank:
  `min(z_ab,z_bc)+β·z(effect)−w·log1p(ac_lit)−w2·ac_known`. (Objective *designed* via Codex consult
  + 3-round codex-debate — see F2/F3.)
- **B8. Full sweep → gate → referee-cull-first → score/rank → emit** — `propose.sweep`; Stim8hr funnel
  22,039 eligible → 43 disease-supported → **30 clean full-chain**; emits `sweep_/lbd_questions_*.json`.

### C. Data substrate + 4-hop referee (answers the questions)
- **C1. Ingest 4 Perturb-seq supplementary tables** (Marson/Pritchard genome-scale CD4+ CRISPRi;
  aggregated CSVs, CPU-only, no 22M-cell matrix): T4 guide-KD, T1 DE_stats, T2 Th1/Th2 signature,
  T3 cluster-disease enrichment.
- **C2. QC each table** — drop 933 null-ENSG guides; exclude 924 negative-control disease rows;
  `ast.literal_eval`-explode T3 `intersecting_genes`; treat sparse reproducibility cols as
  "not reported," not failure.
- **C3. Build + verify the join-map** — `pyzobot_join_spec.json`; 4 joins (ENSG+condition, SYMBOL,
  SYMBOL-in-list ×2) verified by key overlap (e.g. gate 11,422 ENSG).
- **C4. Pre-index** — ENSG↔SYMBOL Rosetta from T1; HOP-0 gate aggregate (`n_signif>0`); T3 explode.
- **C5. HOP-0 knockdown-QC gate (the hero)** — failed knockdown ⇒ **UNTESTED**, halt chain; a null
  downstream is uninterpretable, never "no effect." Only past a passed gate can a null be **REFUTED**.
- **C6. HOP-1 effect / HOP-2 program (BOTH contrasts) / HOP-3 disease (condition-matched)** — each a
  table lookup with an OR/p/effect-size **receipt**.
- **C7. Rule-based calibrated verdict synthesis** — vocabulary `supported/refuted/untested/flagged`
  only; `_synthesize_overall`; never "proven/discovered."
- **C8. 3 worked demo verdicts** — EGR2 = receipt-backed **YES**; IL2@Rest = **UNTESTED** (barely
  expressed, nothing to knock down); SLC1A5 = **REFUTED** (in 9 disease sets, none FDR<0.05).
- **C9. 602-candidate batch ranking + exact-disease adapter** — `chain_score` + novelty bonus
  (`pyzobot_referee_batch.py`); `referee_triple` re-does HOP-3 for one exact disease, no new stats.

### D. The finding
- **D1. NAB2 → Th1/Th2 → atopic eczema @ Stim8hr** — near-novel (`ac_lit=6`, no Open Targets assoc),
  every hop supported: gate 2/2 (expr 0.056 vs 0.567), effect −16.9/301 downstream, program Ota
  z=7.71, disease clusters 90&100 (OR 3.90 FDR 0.0028 / OR 3.43 FDR 0.0224). Calibrated as a
  re-derived chain "the literature has not made."

### E. Validation gauntlet (make it survive scrutiny)
- **E1. 4-agent multi-source literature novelty audit** — Europe PMC + OpenAlex + Semantic Scholar
  (`src/arbiter/lit/search.py`), 155-paper NAB2 corpus, 4 domain-lens agents → **0 direct papers** on
  either link; surfaced the STAT6-12q13 and EGR-mediation confounders.
- **E2. In-data confounder scripts** — STAT6 locus-artifact (cytobands via MyGene: sig clusters 90/100
  are genome-wide modules, STAT6 absent), EGR-mediation (paralog NAB1 opposes → not generic EGR biology),
  cis proxy + cross-guide/donor reproducibility. Pandas over the 4 tables.
- **E3. Source-paper method-provenance read** — 63-page Zhu 2025 preprint; established the disease label
  = Open Targets **GWAS genetic evidence, no LD/coloc control** → reframe to **nomination**; paper never
  mentions NAB2; supplied STAT6 as competing gene + the reproducibility bar.
- **E4. Definitive STAT6 cis-check vs the authors' deposited genome-wide DE** — **lazy anonymous S3
  read** (`s3fs anon` + `h5py`) of one NAB2@Stim8hr row from a 16.8 GB `GWCD4i.DE_stats.h5ad`; STAT6
  **log2FC +0.09, adj-p 0.79 → cis/shadow artifact DEFINITIVELY EXCLUDED**.
- **E5. 5-agent CROSS-MODEL adversarial replication** — frozen claim-set; **Opus×3** (receipt / funnel
  clean-room / confounder-steelman) **+ Codex×2** (code audit / clean-room re-impl); **unanimous PASS**;
  every count reproduced; cluster-ID bug found independently by 2 agents; 7 issues fixed, none touched
  the science.
- **E6. Cross-agent confirmation + issue register + corrections applied** (`docs/replication/`).

### F. Provenance & process
- **F1. Raw-working-trail provenance capture** — `docs/provenance/` (52 verbatim files; secret-scanned;
  third-party abstracts stripped to metadata).
- **F2. 3-round repo-read codex-debate hardening the LBD spec** (v1→v2, 9→3→0 findings).
- **F3. Codex consults** — designed the balanced scoring objective; fixed the full-chain classification
  bug (answer was being set from the disease hop alone).

---

## PART 2 — Can Claude Science do it?

| # | Step | CS | How in CS / caveat |
|---|---|---|---|
| A1 | Cached HTTP/env | ✅ | Kernel `requests`, or `host.mcp` (CS auto-caches tool results in `tool-results/`). |
| A2 | Disease→MONDO + verify | ✅ | `host.mcp("genes-ontologies"/OpenTargets/OLS)` — **proven 2026-07-08 to return real IDs**. |
| A3 | Program keyword arms | ✅ | Config/judgment; trivial. |
| B1 | Answer-free A-universe | ✅ | Persistent kernel pandas (CS home turf). |
| B2 | A-B co-mention | ✅ | Literature connector (`host.mcp` Europe PMC / Literature Graph) or kernel HTTP. |
| B3 | B-C co-mention | ✅ | Same. |
| B4 | A-C known assoc (exclude) | ✅ | Open Targets connector. |
| B5 | A-C lit co-mention | ✅ | Same as B2. |
| B6 | Preflight go/no-go | ✅ | Kernel. |
| B7 | Scoring objective (exec) | ✅ | Kernel. *Design* used Codex (see F3) — in CS you'd design with Claude + its Reviewer (no cross-model check). |
| B8 | Full sweep + cull + emit | ✅ | Kernel orchestration; parallel per-condition via `host.delegate` **if Delegation enabled**. |
| C1 | Ingest 4 Perturb-seq tables | ✅✅ | Kernel pandas — and CS can pull Perturb-seq from **GEO/CELLxGENE connectors** natively (arguably better). |
| C2 | QC tables | ✅ | Kernel pandas. |
| C3 | Join-map + verify | ✅ | Kernel pandas. |
| C4 | Pre-index (Rosetta/gate/explode) | ✅ | Kernel pandas. |
| C5 | HOP-0 KD-QC gate (hero) | ✅ | Kernel pandas; pure logic. |
| C6 | HOP-1/2/3 lookups + receipts | ✅ | Kernel pandas. |
| C7 | Calibrated verdict synthesis | ✅+ | Kernel; **CS's own Reviewer would independently audit the calibrated language** (bonus). |
| C8 | 3 demo verdicts | ✅ | Kernel. |
| C9 | Batch ranking + exact-C adapter | ✅ | Kernel. |
| D1 | NAB2 receipt chain | ✅ | Falls out of B+C in CS. |
| E1 | 4-agent lit novelty audit | 🟡→✅ | Lit connectors + multi-persona via `host.delegate` (**Delegation toggle**) or `host.llm_batch`; CS Reviewer adds a pass. All-Claude agents map fine. |
| E2 | In-data confounder scripts | ✅ | Kernel pandas + MyGene connector for cytobands. |
| E3 | Source-paper read (63-pg PDF) | ✅ | CS **`pdf-explore` skill + vision-grounded annotations** read PDFs natively — a showcase CS use. |
| E4 | Definitive S3 cis-check (h5ad) | ✅✅ | Kernel `h5py`+`s3fs anon` + one **network-domain approval card** for the S3 host; CS is **built for h5ad/scanpy** — a showcase use. |
| E5 | 5-agent **cross-model** replication | ❌ (partial 🟡) | The **Opus agents + clean-room re-impls run in CS** (delegation); the **Codex×2 / second-model-family independence is impossible** — CS is Anthropic-only (Opus/Sonnet/Haiku). **This is THE gap.** |
| E6 | Cross-agent confirm + issues | 🟡 | Within-Claude via CS agents + Reviewer; cross-model corroboration lost. |
| F1 | Provenance capture | ✅✅ | **CS does this natively and better** — `operon-cli.db`, immutable artifact versions, `extracted_code` repro blocks, dependency graph, `verification_checks`. (Except external codex-debate logs.) |
| F2 | 3-round codex-debate (spec) | ❌ | OpenAI Codex; not in CS. CS's own multi-round Reviewer/agents partially substitute — but not cross-model. |
| F3 | Codex consults (design/bugfix) | ❌ | Same — no OpenAI in CS. |

---

## Tally & the one real gap

- **✅ Fully CS-native (≈25/30)** — all of Setup (A1–A3), the entire LBD proposer (B1–B8), the entire
  data substrate + 4-hop referee (C1–C9), the finding (D1), the in-data confounder checks (E2), the
  source-paper read (E3), the definitive S3 cis-check (E4), and provenance (F1). Several are **better**
  in CS: scRNA-seq is CS's home turf (Alec's own field), CELLxGENE/GEO/Open Targets/MyGene are native
  connectors, `host.mcp` returns real IDs, PDFs/h5ad are first-class, and **provenance + an independent
  Sonnet-5 Reviewer come for free** — the Reviewer *is* our referee/falsification discipline.
- **🟡 CS-partial (≈3/30)** — the multi-agent steps (E1, E5-partial, E6): doable within-Claude via the
  Delegation toggle + `host.llm_batch` + specialists, but you lose a second model family.
- **❌ Not in CS (≈2/30, + the cross-model half of E5)** — anything that needs **OpenAI Codex**: the
  3-round codex-debate spec-hardening (F2) and the Codex design/bug-fix consults (F3).

**The single real limitation:** Claude Science is **Anthropic-only** (Opus primary, Sonnet reviewer,
Haiku inline). It cannot give you **cross-model / second-model-family independence** — which was the
load-bearing property of our adversarial replication ("a bug both model families miss is rarer than
one either misses") and of the codex-debate that hardened the spec. Everything else — the receipts,
the referee logic, the compute, the databases, the provenance, and even an independent reviewer — CS
can do, most of it as well or better.

**Implication for tomorrow:** the whole *scientific instrument* can live inside Claude Science (one
workbench: MCP receipts → kernel referee → its Reviewer auditing → provenance in `operon-cli.db`).
Keep **Codex as the external cross-model auditor** for the one thing CS structurally can't be: a
different model family. That hybrid — CS as the instrument, Codex as the independent second opinion —
is the honest, strongest architecture.
