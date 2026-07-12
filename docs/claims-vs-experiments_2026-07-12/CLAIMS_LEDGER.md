# Claims ledger — the manuscript's novelty/contribution statements AS THEY STAND
**Step 1 of the claims ↔ CS-experiments reconciliation (2026-07-12).** Manuscript-faithful: each row is
what the paper *actually asserts* and how it scopes it — NOT the audit's verdict (that's the panel files)
and NOT the experimental reconciliation (that's Step 2, `RECONCILIATION.md`, still to come). IDs continue
the audit's `MASTER_REGISTER.md` for traceability. The "CS/experiment evidence to check" column is a
*scaffold for Step 2* — where the already-run evidence lives — not a judgement.

## METHOD claims
| ID | Novelty/contribution statement (as the paper makes it) | § | Paper's own scope/hedge | CS/experiment evidence to check (Step 2) |
|----|--------------------------------------------------------|---|-------------------------|------------------------------------------|
| **M1** | The contribution is receipt-backed *prioritization* of machine-generated hypotheses via an LBD front-end + a **deterministic, non-LLM referee** scoring each triple against a **held, pre-existing** Perturb-seq substrate, with per-hop **experimental** receipts, QC-gated **abstention**, and **falsification** as first-class verdicts (the §2.4 "we are not aware of a system that does this combination"). | 2.4, abs, 1, 5.4 | "we are not aware of" (not proven absence); "narrow and specific"; the contribution is the method, "not a demonstration of predictive correctness" | cs-full-pipeline stage1 (generation), tracer-artifacts (native referee), perturbseq-qc (validator built in CS) |
| **M2** | QC-gated **abstention**: a failed knockdown is reported *untested*, never a negative — "an artifact caught rather than a false negative recorded." | abs, 3.3, 4.2 | scoped to knockdown-QC (T4); shown out-of-funnel because within-funnel hops 0–2 are pre-gated | perturbseq-qc; cs-full-pipeline; hard_negatives_results.json (IL36RN/TREX1/PADI4 untested); Control 1 (2,430 genes 100% untested) |
| **M3** | **Falsification / "confident receipt-backed no"** is the deliverable (vs plausibility-optimizing generators). | abs, 4.2, 5.1 | §4.1b/§4.2b: the referee's *own* no is the QC gate (~1 in 6); the disease-hop no is substrate-inherited | tracer (SLC1A5 refuted), hard_negatives, Control 2 label-shuffle |
| **M4** | Division of labour: every data receipt is deterministic code; the LLM interprets/assembles but **never computes a receipt**. | 2.3, 3.1 | objective weights + interpretation are human/model judgment (§5.3) | cs-full-pipeline (deterministic sweep under replay guard), tracer referee.py |
| **M5** | Actor–critic **self-audit** enforcing calibrated **language** on the platform's own output — an independent reviewer model flagged & removed "validated"/"definitive". | 3.4, 4.5 | "language hygiene + receipt-consistency," NOT epistemic verification of biology; within-family, not cross-vendor | cs-capability-tests (Reviewer caught a planted inconsistency); cs-full-pipeline stage5/review.json |
| **M6** | **Headless scripting of an API-less agentic workbench** (Claude Science) → "replicable-in-principle agentic science"; funnel reproduced digit-for-digit, sensitivity panel **byte-for-byte**. | 3.4, 4.5, 5.1 | "subject to the platform's UI"; full-scale run is a cache replay under a no-live-call guard, "not a live crawl" | cs-full-pipeline stage1 (replay, cache delta 0), manuscript/analysis/cs-reproduction/sensitivity_results.cs.json vs sensitivity_results.json, drive-claude-science skill |
| **M7** | **Cross-family adversarial clean-room replication lab** (5 agents incl. cross-vendor Codex) reproduced every headline number and caught real errors. | 4.6 | "computational robustness, not biological validity"; not every member checked every number | replication/ + replication_report_2026-07-08.md (incl. the 74→90/100 catch) |
| **M8** | Balanced novelty+effect **ranking objective** (min-z bridge; no obscurity reward). | 3.2 | weights set priority not verdict; robust (§4.1b/c) | gate_grid_results.json (rank stability); sensitivity_results.json |
| **M9** | **Disease-answer-free** (leakage-free) candidate-universe construction. | 3.2, 4.1 | "answer-free, not evidence-free"; hops 0–2 pre-gated | cs-full-pipeline stage1 (universe build), sweep JSONs |
| **M10** | Negative-control **decomposition**: label-shuffle shows the disease-hop stringency is *substrate-inherited*; the referee's own edge is the QC gate. | 4.1b, 4.2b | self-limiting; "we do not claim rarer-than-chance selectivity" | Control 2 (2,000 permutations); hard_negatives; gate_grid |

## BIOLOGY claims
| ID | Novelty/contribution statement (as the paper makes it) | § | Paper's own scope/hedge | CS/experiment evidence to check (Step 2) |
|----|--------------------------------------------------------|---|-------------------------|------------------------------------------|
| **B1** | **NAB2 is a Th1/Th2 (Th2) regulator** — a re-derived regulatory role the literature has not made (2/2 guides, effect −16.9, 301 DE, Ota z 7.71). | abs, 4.3 | "consistent with / re-derived"; novelty "in the surfaced literature"; not sig in Höllbacher | lbd_finding_nab2, replication (opus_confounder D-set), tracer verdicts |
| **B2** | **NAB2 → atopic eczema** — a literature-novel *genetic-association nomination* (modules OR 3.90/3.43). | abs, 4.3 | "GWAS-based label, no coloc/LD control"; a nomination, not causality | claude-science-evidence-chain, cs-full-pipeline, replication C-set |
| **B3** | The STAT6 **cis-effect is ruled out at the expression level** — STAT6 unmoved under NAB2-KD (log2FC +0.087, p 0.79). | 4.4 | "one aggregate Stim8hr null … not every conceivable cis channel" | **stage3_cis.json**, nab2_stat6_definitive_check.py, nab2_cis_artifact_check.py |
| **B4** | NAB2's eczema modules (clusters 90/100) are **genome-wide functional immune modules** (STAT6 absent), not a 12q13 artifact. | 4.3, 4.4b | rejects the cluster-membership artifact only | replication/opus_confounder (90/100 correction), nab2_stat6_confounder_check.py |
| **B5** | The **12q13 LD-inherited disease label cannot be discharged** — foregrounded, not resolved. | 4.4b, 5.3 | explicitly open; needs variant-level coloc | (no experiment — GAP; needs external genetics) |
| **B6** | **NAB2 reads down in lesional AD skin** (per-cell: keratinocyte −0.51, T/NK −0.57). | 5.2 | exploratory; outside the referee substrate | nab2-direction-geo_2026-07-09/ (arm_d_scrna, per_arm.json) |
| **B7** | **NAB2 = "Th2 brake"** lost in chronic lesions → restore/up-modulate, not knockdown. | 5.2 | a directional *question* to test, not a finding; sign unsettled | nab2-direction-geo, nab2-depmap-check, codex-debate_nab2-direction |

## Empirical / result claims (used as demonstrations)
| ID | Statement | § | CS/experiment evidence to check |
|----|-----------|---|---------------------------------|
| **R1** | Funnel: 3,935 genes → 22,039 eligible pairs → 43 supported → 30 clean survivors (Stim8hr). | 4.1 | cs-full-pipeline stage1 sweep_Stim8hr.json; live-fullsweep-loose |
| **R2** | Referee alone supports 395/47,220; novelty gate culls 395→43. | 4.1, 4.1b | gate_grid / hard_negatives / sweep JSONs |
| **R3** | Control 1: all 2,430 failed-knockdown genes returned *untested* (100%, no leakage). | 4.1b | Control-1 output (in analysis/) |
| **R4** | Flagship rank stable: NAB2 rank 1–8 (median 4) over weights; 1–5 over gate cells. | 4.1b, 4.1c | gate_grid_results.json |
| **R5** | EGR mechanism: NAB2 is a *distinct* regulator, not a swappable EGR corepressor (NAB1 paralog opposition). | 4.3 (implied) | nab2_egr_mechanism_check.py, replication D-set |

## How Step 2 will read this ledger (proposed)
For each claim: locate the already-run CS/experiment evidence → classify **SUPPORTS / REFUTES /
COMPLICATES / PARTIAL / NO-EXPERIMENT(gap)**, and cross it against the **panel's critique** (from
`docs/reviews/contribution-novelty-audit_2026-07-12/`). Two things Step 2 must not miss:
1. **Experiments that answer a panel critique the panel under-credited** (e.g. B3/B4 vs the STAT6 attack).
2. **Experiments that REFUTE or COMPLICATE a manuscript claim** (intellectual-honesty priority — e.g. the
   replication's "8× is really 3×", the wrong-cluster QC, the direction work's brake reversal).
Output → `RECONCILIATION.md`. Gaps with no experiment → Step 3 `NEW_EXPERIMENTS.md` (CS-native where possible).
