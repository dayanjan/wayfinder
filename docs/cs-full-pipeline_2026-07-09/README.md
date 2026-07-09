# LBD→NAB2 pipeline — the instrument stages reproduced natively in Claude Science (cross-model audit external) (2026-07-09)

The scientifically load-bearing stages of the PyZoBot Arbiter instrument were run **natively inside
Claude Science (CS)** — Anthropic's local scientific workbench — and reproduced the known numbers with
receipts pulled from CS's own audit store (`operon-cli.db`). Driven headlessly via the
`drive-claude-science` skill (zero-click; the driver auto-approves CS's folder / code / network cards).

**Architecture (decided by a 3-round repo-read codex-debate → SHIP):**
**CS is the instrument** (generation → referee → provenance falsification); **Codex stays external as the
cross-model auditor.** Second-model-family independence is structurally outside CS, so cross-model
replication (Opus×3 + Codex×2, `docs/replication/`) remains the external record. Plan of record:
`docs/plans/full-pipeline-in-cs-plan_2026-07-09.md`.

**Honesty framing (verbatim, do not overstate):** Claude Science ran the LBD generator natively over the
full 3,935-gene Stim8hr universe using the same deterministic code path, **replaying previously captured
Europe PMC / Open Targets JSON receipts from a workbench-local cache**, and reproduced the exact funnel and
the NAB2→atopic-eczema rank. A **separate Stage 0 probe** demonstrated the same CS kernel can make **live**
Europe PMC GET + Open Targets GraphQL POST calls, and **Stage 3 read the authors' deposited genome-wide DE
matrix live from public S3**. The full Stage-1 sweep itself was a cached-receipt replay (verified: zero live
calls, via a guard that raises on any network access), **not** a fresh live web crawl.

Prior work (do not redo): the **tracer** already had CS write its *own* referee from rules and reproduce
the 4-hop verdict + NAB2 finding digit-for-digit (`../cs-capability-tests_2026-07-08/tracer-artifacts/`).
This run is the **native port with receipt verification** of the remaining stages: generation, the
S3 STAT6 cis-check, and provenance assembly.

Provenance store: `~/.claude-science/orgs/741d6512-…/operon-cli.db`. Every driven run =
**OPERON = Opus 4.8** (the scientist) + **REVIEWER = Sonnet 5** (the critic). "Reviewer · No issues found"
on every stage.

---

## Stage 0 — feasibility probe · PASS
`proj_9bbb495de66b` · workspace `0c391ac5-…` · artifacts in `stage0/`
Proved all four external-access paths work natively from the CS kernel:
- **Europe PMC GET** (`hitCount`): `("NAB2") AND ("atopic eczema")` → **6** (= the finding's `ac_lit`); Th2 query → 31.
- **Open Targets GraphQL POST**: asthma `MONDO_0004979` → **7403** associated targets (FLG 0.744, IL4R 0.744, IL33, TSLP, IL5, IL13…).
- **Anon S3 lazy read** of the 16.8 GB `GWCD4i.DE_stats.h5ad` → **opened, no download** (byte-range reads of obs/var labels). Self-healed a proxy 403 by switching to **virtual addressing** (bucket-qualified host).
- **24 `mcp-*` connectors** enumerated (literature, pubmed, human-genetics, expression, …).
→ **Resolves the plan's open question: Stage 3's S3 cis-check runs natively in-CS; no external fallback needed.**

## Stage 1 — LBD proposer (generation), full 3,935-gene sweep · PASS (ALL_PASS = True)
`proj_4f40ad0d829b` · OPERON frame `ea4d8563-…` (Opus 4.8, ~$1.23) · artifacts in `stage1/`
The real `arbiter.lbd.propose.sweep()` was imported **unchanged** from a repo-shaped staging tree
(`/home/dayanjan/pyzobot-cs-stage1`) and run under a **pure-replay guard** (HTTP layer monkeypatched to
raise on any live call). Reproduced the exact funnel:

| metric | value |
|---|---|
| A-universe genes | **3935** |
| eligible pairs (post-gate) | **22039** |
| chain classes | refuted_for_c 21995 · supported 30 · supported_weak 10 · supported_flagged 3 · refuted_effect 1 |
| disease-C-supported | **43** · clean full-chain **30** · pure-disjoint clean **1** |
| ab_gate value | **26** |
| **pure-replay guard** | cache 4685 → 4685, **delta 0** (zero live calls during the sweep) |

**NAB2 → atopic eczema — rank 4 of 30** clean supported: ab 66 · bc 2184 · ac_lit 6 (near-novel) ·
ac_known 0.0376 · effect 301 · score −1.137 · referee_answer **supported**.
All 16 acceptance checks ✅. (The 10 cache files added before the sweep, 4675→4685, are the explicitly
**guard-free plumbing smoke**'s live `ac_lit` calls — separate from the funnel reproduction.)

## Stage 3 — STAT6 cis-check (falsification), native S3 · PASS
`proj_ea76f1a08006` · OPERON frame `fb886080-…` (Opus 4.8, ~$0.70) · artifacts in `stage3/`
Ported `nab2_stat6_definitive_check.py`: anon `s3fs`+`h5py` **lazy** read of the NAB2@Stim8hr row from the
16.8 GB deposited DE matrix (no download). The hardest confounder — NAB2's guide sits ~1.9 kb from STAT6 —
is **refuted**:

| gene (under NAB2-KD, Stim8hr) | log2FC | adj_p | significant |
|---|---:|---:|:--:|
| **STAT6** (neighbor under test) | **+0.0870** | **0.7884** | no → **UNMOVED** |
| **NAB2** (self / on-target) | **−3.0783** | 7.2e-60 | yes → knockdown worked |

10,282 genes measured; 302 significantly moved by NAB2-KD (≈ the referee's effect=301). STAT6 |log2FC|
rank 5444/10282 (less-affected half). → **the CRISPRi cis-artifact is refuted; the observed Th2/eczema-linked
signal is consistent with NAB2 perturbation rather than STAT6 bleed.**

## Stage 5 — end-to-end receipt chain + provenance · PASS (Reviewer did real work)
`proj_99ccc044f003` · OPERON frame `4473ddef-…` (Opus 4.8, ~$0.94) · **3 Sonnet-5 REVIEWER frames** (~$0.78) · artifacts in `stage5/`
OPERON assembled `receipt_chain.md` (HOP-0→3 + cis-exclusion + honesty framing + "what ran where" +
calibrated verdict) and `chain.json`. The Reviewer then produced **4 `verification_checks`** (the only run
where CS's audit `verification_checks` table surfaced non-empty — the others' reviewer rows backfill async):
- **PASS** — every numeric receipt cited matches `chain.json` (funnel 3935→22039→43→30; NAB2 ab=66/bc=2184/ac_lit=6/ac_known=0.0376/effect=301; STAT6 +0.09/adj_p 0.79).
- **PASS** — final verdict + "what ran where" table match the source of truth.
- **PASS** — the Reviewer **flagged "validated" (title) and "definitive" (Stage-3 heading) as calibrated-language violations; both were edited out** — the falsification/receipt-discipline thesis enforced live by an independent critic model.
- **WARN (resolved)** — a cosmetic `—` escape artifact in `review.json`.

**Total run cost across Stage 0/1/3/5: ~$6.41** (OPERON Opus 4.8 + REVIEWER Sonnet 5). Full frame/cost/checks
breakdown in `provenance.md`.

---

### What ran where
| layer | where | evidence |
|---|---|---|
| generation (LBD proposer) | **CS native**, cached-receipt replay | Stage 1 (guard delta 0) + Stage 0 live-access proof |
| referee (4-hop + KD-QC gate) | **CS native**, own pandas | tracer (digit-for-digit) |
| falsification (STAT6 cis) | **CS native**, live public S3 | Stage 3 |
| provenance / audit | **CS native** | `operon-cli.db` (OPERON Opus 4.8 + REVIEWER Sonnet 5) |
| cross-model independence | **external** (by design) | `docs/replication/` (Opus×3 + Codex×2) |

**Bottom line:** the question's *generation*, its *answer*, and its *hardest falsification* all live in the
workbench; provenance is captured in CS's own audit store; and cross-model independence is kept honestly
external. Verdict reproduced: a novel, reproducible **nomination** that NAB2 is a Th1/Th2 regulator (the
atopic-eczema link is Open-Targets GWAS-genetic, flagged as such).

---

## Addendum — fully-live LBD micro-sweep authored from scratch in CS · PASS
`proj_64a5e671c715` · OPERON frame `2b61c815-…` (Opus 4.8) · artifacts in `live-microsweep/`
Stage 1 was a *port* replaying cached receipts. To prove CS can **set up an LBD workflow from scratch, live**,
we drove a fresh project where CS was given only the *method* (Swanson ABC + a gate + a novelty score) — **no
staged code, no cache** — and had it write its own generator and run it against live APIs. It:
- built its own 12-gene A-universe from the granted tables (top-effect KD-gated genes: CD3E, LAT, ZAP70,
  VAV1, CD3D/G, PLCG1, LCP2, TADA2B…; **NAB2's effect was too low to rank top-12, so it did not appear** — no cherry-picking),
- made **live** Europe PMC GET + Open Targets GraphQL POST calls for all five signals,
- applied a self-authored gate + `min(z_ab,z_bc)+z(effect)−log1p(ac_lit)−3·ac_known` score,
- generated **22 eligible candidate questions** (top: CD3E→Th1/Th2→atopic eczema; ac_lit 21, ac_known 0.0022),
  labelled explicitly as *candidates to referee next, not findings*. Sonnet-5 Reviewer: no issues.

**Liveness independently verified:** re-querying CS's exact recorded queries against the live Europe PMC API
returned the identical counts — `ab` TADA2B = **7/7**, `ac_lit` TADA2B×asthma = **82/82**, `bc` program×asthma
= **30473/30473** (TADA2B was never in our cache). → **CS can author and run an LBD generator live, from
scratch** — the generation layer is not merely portable to CS, it is natively *constructible* there.
