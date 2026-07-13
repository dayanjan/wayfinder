# CLAIMS ↔ EVIDENCE ↔ SOURCE — canonical living ledger
> **THE single source of truth** for what the manuscript claims, what evidence backs each claim, where the
> original source is, and the current status. **Read this FIRST** before any claim audit, review, revision,
> or new experiment. It exists because on 2026-07-12 a literature-only audit forgot that CS experiments had
> already tested the NAB2/STAT6 confounder and over-generalized a critique — this ledger prevents that recurring.

## ⚠ ANTI-AMNESIA PROTOCOL (mandatory)
1. **Any claim audit / review / referee-response MUST reconcile against BOTH (a) the literature AND (b) the
   experiment corpus indexed here** — never literature-or-manuscript alone. Literature tells you if a claim is
   *novel*; the experiments tell you if it's *supported*. The 2026-07-12 miss was checking only novelty.
2. **This file is the LIVING INDEX; the dated files are the IMMUTABLE EVIDENCE.** Update *this* table when a
   claim's status changes; never edit the dated records (`docs/reviews/contribution-novelty-audit_2026-07-12/`,
   `docs/claims-vs-experiments_2026-07-12/`) — cite them.
3. **Every status change records: date · what changed · which artifact · which source.** No status without a
   traceable artifact + source ID.
4. `session-closer` checks this file is current at close; `session-start` preloads it. It is listed in
   `memory/NEXT_SESSION.md` "Context to preload."

## Status vocabulary
`SUPPORTED-BY-EXP` (an experiment backs it) · `SUPPORTED-AS-SCOPED` (holds within its stated hedge) ·
`NOVEL-NARROW` (novel but narrow/integration-only) · `KNOWN-PRIMITIVE` (prior art; app-only novelty) ·
`OPEN-GAP` (no experiment yet — candidate for new work) · `NEEDS-FIX` (a wording/number defect to correct).

## The ledger (last full reconciliation: 2026-07-12)
| ID | Claim (short) | § | Status | Evidence artifact (repo) | Source | Panel critique → resolution | Last verified |
|----|---------------|---|--------|--------------------------|--------|-----------------------------|---------------|
| M1 | LBD + deterministic non-LLM referee vs held substrate + receipts + abstain + refute | 2.4 | NOVEL-NARROW | cs-full-pipeline/stage1, cs-capability-tests/tracer-artifacts | S1,S4,S10 | novel-but-narrow; cite Popper/VERITAS → still valid | 2026-07-12 |
| M2 | QC-gated abstention (untested≠negative) | 3.3 | SUPPORTED-BY-EXP · KNOWN-PRIMITIVE | Control 1 (2,430/2,430 untested); hard_negatives | S4 | selective-prediction prior art → cite it | 2026-07-12 |
| M3 | Falsification / confident "no" as deliverable | 4.2 | SUPPORTED-AS-SCOPED | tracer (SLC1A5); hard_negatives (~1-in-6) | S4,S10 | self-bounded by M10; partly-anticipated | 2026-07-12 |
| M4 | Deterministic tools only; LLM never computes a receipt | 3.1 | SUPPORTED-BY-EXP · KNOWN-PRIMITIVE | tracer referee.py; replay-guard sweep | S4,S10 | grounded tool-use prior art | 2026-07-12 |
| M5 | Actor–critic self-audit enforces calibrated language | 4.5 | SUPPORTED-BY-EXP · **NEEDS-FIX** | cs-capability-tests/final_summary_with_planted_inconsistency.md, stage5/review.json | S10 | real catch; "flagged & **removed**" half-true (one word retained) → reword | 2026-07-12 |
| M6 | Headless driving of API-less workbench; reproduction | 3.4 | SUPPORTED-BY-EXP · **NEEDS-FIX** | drive-claude-science skill; cs-reproduction COMPARE; tracer | S10 | capability real, not novel *science*; **"byte-for-byte" false** (CRLF/LF, value-identical) → reword | 2026-07-12 |
| M7 | Cross-family adversarial replication lab | 4.6 | SUPPORTED-BY-EXP · **NEEDS-FIX** | replication_report_2026-07-08.md; replication/ | S1,S4 | QA not novel; "reproduced every number" vs "caught errors" → "all but 2, corrected" | 2026-07-12 |
| M8 | Balanced novelty+effect ranking objective | 3.2 | SUPPORTED-BY-EXP · KNOWN-PRIMITIVE | gate_grid_results.json | S4,S5,S6 | understated; rank conditions on survival (9/27 cull) | 2026-07-12 |
| M9 | Disease-answer-free (leakage-free) construction | 3.2 | SUPPORTED-BY-EXP · KNOWN-PRIMITIVE | stage1 sweep JSONs | S4 | standard leakage avoidance | 2026-07-12 |
| M10 | Label-shuffle: disease-hop stringency substrate-inherited | 4.1b | SUPPORTED-BY-EXP | Control 2 (406 vs 467.7±10.9, z −5.645) | S4 | the honest self-limit; permutation controls standard | 2026-07-12 |
| B1 | NAB2 is a Th1/Th2 (Th2) regulator | 4.3 | SUPPORTED-BY-EXP | lbd_finding_nab2; replication (D-set); tracer | S1,S4,S3 | novel for **polarization** (NAB2 has other T-cell roles); add EGR2/3 adjacency | 2026-07-12 |
| B2 | NAB2 → atopic eczema nomination | 4.3 | SUPPORTED-AS-SCOPED | evidence-chain; sweep | S4,S6 | thin, LD-plausibly STAT6, but honestly scoped as a nomination | 2026-07-12 |
| B3 | STAT6 cis-effect ruled out at expression level | 4.4 | SUPPORTED-BY-EXP | **stage3_cis.json** (STAT6 +0.087/p0.79; NAB2 −3.08); nab2_stat6_definitive_check.py | S3 | adversary conceded "cannot attack"; panel under-credited | 2026-07-12 |
| B4 | Eczema modules genome-wide (STAT6 absent), not 12q13 artifact | 4.4b | SUPPORTED-BY-EXP | replication (74→90/100 correction); corrected derive-clusters | S4 | only verifier = replication; cite corrected script only | 2026-07-12 |
| B5 | 12q13 LD disease-label cannot be discharged | 4.4b | **OPEN-GAP** | — (needs variant-level coloc) | S1(GWAS)+ext | genuine open confounder; foregrounded correctly → **G2** | 2026-07-12 |
| B6 | NAB2 down in lesional AD skin | 5.2 | SUPPORTED-BY-EXP · **NEEDS-FIX** | nab2-direction-geo (bulk −0.32/FDR0.002; scRNA keratinocyte −0.51/p0.027) | S7,S8 | a real DE result, not "unverifiable"; T/NK −0.57 is n.s.(p0.11) → say partial | 2026-07-12 |
| B7 | NAB2 = Th2 brake → restore not knockdown | 5.2 | SUPPORTED-AS-SCOPED | nab2-direction-geo/per_arm.json; depmap-check | S7,S8,S9 | direction unsettled (1/4 arms); keep hedge; add EGR2-STAT6 sign-flip caveat | 2026-07-12 |
| R1 | Funnel 3,935→22,039→43→30 | 4.1 | SUPPORTED-BY-EXP | stage1/sweep_Stim8hr.json; live-fullsweep-loose | S4 | reproduced exactly incl. cold-cache live (NAB2 rank 4) | 2026-07-12 |
| R2 | Referee-alone supports 395/47,220 | 4.1 | **NEEDS-FIX** | sensitivity_results.json | S4 | **number discrepancy: text 395 vs JSON 406 → reconcile** | 2026-07-12 |
| R3 | Control 1: 2,430 failed-KD all untested (100%) | 4.1b | SUPPORTED-BY-EXP | Control-1 output | S4 | no leakage | 2026-07-12 |
| R4 | Flagship rank stable (1–8 wt / 1–5 gate, med 4) | 4.1b/c | SUPPORTED-BY-EXP | gate_grid_results.json | S4,S5,S6 | conditions on NAB2 surviving gate (culled 9/27) | 2026-07-12 |
| R5 | NAB2 distinct from EGR (NAB1 paralog opposition) | 4.3 | SUPPORTED-BY-EXP | **egr_distinctness_results.json** (G3 receipt, `opposition_confirmed=true`); nab2_egr_mechanism_check.py | S4 | **G3 DONE 2026-07-13**: frozen receipt committed; §4.3 now leads with D3 (NAB2 Th1 vs NAB1 Th2 both contrasts sig) | 2026-07-13 |

**The central item (publish gate) — now EXECUTED (2026-07-12).** G1, the time-sliced held-out evaluation, is
built and run: it measures whether the method ranks future-established gene→program→disease links above
baselines within a literature-novel-as-of-2016 frame (22,437 pairs, 5,570 positives). **Result: a NULL at the
pre-registered primary** — C_broad (Wayfinder − lit-rarity) = +0.20 [−0.20, +0.65]; C_mech (Wayfinder −
disease-hop-only) = −0.15 [−0.35, +0.30]; joint outcome `broad_null` (precision@20, gene-and-disease two-way-
clustered bootstrap). Wayfinder leads on the secondary metrics (precision@5 = 0.80 and MAP = 0.287, both best
of six rankers) but neither is the primary, and the disease-hop-only baseline matches/exceeds it at
precision@20 — empirically confirming the "substrate-inherited stringency" reading (M8/M10). This CLOSES the
audit's FATAL (method now *measured*, not merely demonstrated) and is reported straight in §4.7.
**Independently reproduced in Claude Science (2026-07-13, blind + headless):** precision table + both
co-primary points (+0.20 / −0.15) exact, same `broad_null` verdict, concordant CIs
(`data/eval_out/cs_verify_result.json`). Evidence:
`data/eval_out/count_manifest_full_T2016_k5.json` (committed receipt), `eval_results_T2016_k5.json`,
`src/arbiter/eval/`, `docs/g1-build-log_2026-07-12.md`, `docs/reviews/diff_g1-harness_2026-07-12.md`.

## Manuscript honesty fixes — status (2026-07-13)
The 9 honesty flags from `docs/claims-vs-experiments_2026-07-12/RECONCILIATION.md` are now all resolved.
**Applied 2026-07-13** (reconciled against the current manuscript, not the list): **M6** "byte-for-byte" →
"value-identical" (abstract + §4.5 caption + §5.1); **M5** "both removed" → "removed from the manuscript-facing
output; ``validated'' persists in the raw-log free-text field"; **M7** "reproduced every number" → "reproduced
every headline receipt while catching+correcting two of our own errors"; **B6** T/NK −0.57 now stated n.s.
(p 0.11) → "partial per-cell confirmation" (§5.2); **B7** EGR2-is-STAT6-driven pro-type-2 sign-flip caveat added
to §5.2. **Already resolved in prior revisions** (verified present): R2 (395/406 reconciled in §4.1), M8/R4 (rank
stability conditioned on gate survival, §4.1b/c), the buggy [74,90] script (narrative uses corrected 90/100),
stale "1.9 kb" (already "~43 kb"). Also **2026-07-13**: abstract + §1 reframed to state the method is now
*measured* (G1 held-out eval, null reported straight), not only demonstrated.

## Sources appendix (trace every claim to its origin)
| ID | Source | Locator |
|----|--------|---------|
| S1 | Perturb-seq study (Zhu, Dann, … Marson), the substrate | DOI **10.64898/2025.12.23.696273** (bioRxiv); `references.bib` `zhu2025` |
| S2 | Authors' analysis repo | **github.com/emdann/GWT_perturbseq_analysis_2025** |
| S3 | Genome-wide DE matrix (cis-test) | **s3://genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad** (anon S3, lazy read) |
| S4 | Aggregated supplementary tables T1–T4 (KD-eff, DE, program, disease-enrichment) | via `src/arbiter/lbd/referee_triple.load_referee_data()` (repo cache) |
| S5 | Europe PMC (co-mention counts) | `src/arbiter/lbd/sources.europepmc_count` |
| S6 | Open Targets GraphQL (association scores) | `src/arbiter/lbd/sources.opentargets_*` |
| S7 | GEO bulk AD datasets (direction) | accessions in `docs/nab2-direction-geo_2026-07-09/` |
| S8 | GEO scRNA AD dataset (direction) | GSE204762 + accessions in `docs/nab2-direction-geo_2026-07-09/arm_d_scrna/` |
| S9 | DepMap (target essentiality) | `docs/nab2-depmap-check_2026-07-09/` |
| S10 | Claude Science (agentic workbench) audit store | `operon-cli.db`; runs in `docs/cs-full-pipeline_2026-07-09/`, `docs/cs-capability-tests_2026-07-08/` |
| S11 | MONDO / OLS4 (disease id resolution) | `src/arbiter/lbd/verify_disease_ids.py` |

## Detailed evidence records (immutable — cite, don't edit)
- Literature novelty audit: `docs/reviews/contribution-novelty-audit_2026-07-12/` (VERDICT.md + 15 agent files)
- Claims↔experiments reconciliation: `docs/claims-vs-experiments_2026-07-12/` (RECONCILIATION.md + 6 recon + CLAIMS_LEDGER.md)
- New-experiment plan (gaps G1–G3): `docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md`
- Held-out-eval (G1): scope `docs/plans/heldout-eval-scope_2026-07-12.md`; **frozen build spec (v3, debate-hardened)**
  `docs/plans/heldout-eval-implementation-plan_2026-07-12.md`; de-risk `docs/spikes/heldout-eval-feasibility_2026-07-12.md`;
  codex-debate (converged, GO Option A) `docs/reviews/codex-debate_heldout-eval-plan_2026-07-12.md`

## Maintenance
On any change that affects a claim (new experiment, manuscript edit, a fix applied), update the row's Status +
Last-verified + note the artifact/source. Keep the dated records immutable. `session-closer` verifies currency.
