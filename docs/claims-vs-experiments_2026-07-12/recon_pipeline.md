# Recon — CS PIPELINE cluster (claims M1, M2, M3, M4, M6-repro, M9, R1, R2, R3, B3)

**Agent:** CLAIMS↔EXPERIMENTS reconciliation, cluster = CS PIPELINE · **Date:** 2026-07-12 · **Mode:** read-only.
Read the PRIMARY experiment artifacts (JSON / receipt.md / provenance / QC), not the manuscript's summaries.
Classification per claim: (1) which experiment ran + key numbers; (2) vs the CLAIM; (3) vs the PANEL CRITIQUE;
(4) HONESTY FLAG.

---

## The load-bearing distinction up front (applies to M1/M4/M6/M9/R1)

Every "full pipeline in CS" run (stage0/1/3/5, live-microsweep, live-fullsweep-loose, cs-reproduction) is an
**EXECUTION / REPRODUCTION / LIVENESS** artifact — the code ran natively, the numbers re-derived, receipts
verified, Reviewer passed. **None of them is an EVALUATION** in the panel's sense (no precision, recall,
baseline, held-out benchmark, false-refutation / false-abstention rate). A cache-replay reproduction (Stage 1)
and even a 100%-live cold-cache reproduction (fullsweep-loose) prove the *instrument runs and reproduces*;
they do **not** measure whether the *ranking is scientifically useful*. So the panel's central "**method is
demonstrated, never evaluated**" critique (VERDICT "WHAT DOES NOT CLEAR THE BAR #1"; adversarial_codex #1;
adversarial_claude H4) **STILL STANDS** after every artifact in this cluster. These runs answer
"reproducible?" and "runs in an agentic workbench?" — not "is it good?" I flag this once here and reference it
per-claim rather than re-typing it.

**One place the panel UNDER-CREDITED the evidence** (detail under M6/R1): the VERDICT and adversarial_codex #8
describe the reproduction as "a cache replay" and the only live run as "a different 12-gene exercise that did
not recover NAB2." That is **stale** — `live-fullsweep-loose/` is a **100%-live, cold-cache (0→9,557 live
calls) full-universe sweep across all 3 conditions** that **recovered NAB2 → atopic eczema at rank 4/43 with
byte-identical raw signals**. The panel appears not to have seen it. This rebuts the *"only-a-cache-replay"*
and *"live-run-didn't-recover-NAB2"* sub-attacks — but NOT the "not evaluated" attack (liveness ≠ evaluation).

---

## M1 — the method conjunction (LBD → deterministic non-LLM referee → held substrate → per-hop receipt → QC-abstention → falsification)
- **Experiment(s):** whole cs-full-pipeline: Stage 0 probe (4 external-access paths live: Europe PMC GET
  NAB2×eczema=6, Open Targets asthma=7403 targets, anon S3 lazy read of 16.8 GB `.h5ad`, 24 MCP connectors);
  Stage 1 generation (funnel reproduced); tracer = native referee (digit-for-digit, prior work); Stage 3
  falsification (STAT6 cis); Stage 5 provenance+review. Ran natively in CS, OPERON=Opus 4.8 + REVIEWER=Sonnet 5,
  total ~$6.41.
- **vs CLAIM: SUPPORTS (existence/execution).** Every element of the conjunction demonstrably executes
  end-to-end inside one workbench with receipts pulled from CS's own audit store. The integration is real and
  runs.
- **vs PANEL: does NOT move the needle; critique STANDS.** V-GAP already graded M1 **NOVEL-but-narrow** (the
  durable wedge = "deterministic referee over a held substrate"); this run demonstrates the wedge *operates*
  but is EXECUTION, not the evaluation the panel demands. Does not touch the "cite VERITAS / Popper" or
  "unevaluated implementation distinction" findings.
- **HONESTY FLAG:** none new — the README's "we are not aware of" framing matches V-GAP's hedge. Consistent.

## M2 — QC-gated abstention (failed knockdown = *untested*, never a negative)
- **Experiment(s):** tracer IL2@Rest → **untested** (0/2 guides significant, guide expr 0.031 vs NTC 0.036 —
  nothing to knock down; referee halts at HOP-0). `hard_negatives_results.json`: panel A **1,914/11,415
  (16.8%) untested** out of an arbitrary out-of-funnel gene set; panel B — of 600 frozen *high-curated-
  association* disease nominations, **75 untested** incl. IL36RN/psoriasis (ac_known 0.819), TREX1/SLE (0.78),
  PADI4/RA (0.676), all `in_A:false`. QC report: KD gate queried FIRST; no-signif-KD gene → UNTESTED by design.
- **vs CLAIM: SUPPORTS.** The abstain outcome fires exactly as claimed — a failed/absent knockdown returns
  `untested`, and genuinely disease-associated genes are abstained-on rather than scored negative.
- **vs PANEL: mechanism shown, but the RATE critique STANDS.** V-PRIM grades M2 a **known primitive**
  (selective-prediction/reject-option; honest but uncited). These artifacts show the gate *works*; they do NOT
  measure a **false-abstention rate** (how often it wrongly abstains on a real effect), which is what an
  evaluation would need. Note `hard_negatives`/`sensitivity` live in `docs/manuscript/analysis/`, i.e. local
  ground truth — the CS-native surface for M2 is the tracer only.
- **HONESTY FLAG:** none — the untested-not-negative behaviour is exactly as advertised.

## M3 — falsification / "confident receipt-backed no" as the deliverable
- **Experiment(s):** tracer SLC1A5@Stim8hr → **refuted** (disease hop: 9 clusters, none FDR<0.05, best 0.054);
  Stage 3 STAT6 cis → **refuted**; `hard_negatives_results.json` panel A **own_edge_cull_rate = 0.1693**
  (1,932/11,415 culled by the referee's own effect/program hops = ~**1 in 6**), panel B own_edge_cull 0.157.
- **vs CLAIM: SUPPORTS but self-COMPLICATES.** Refutation fires and is receipt-backed (SLC1A5, STAT6). But the
  referee's *own* discriminating edge is only **~1 in 6**; the bulk of the disease-hop stringency is
  substrate-inherited (Control 2, below) — the manuscript's own M10 already discloses this.
- **vs PANEL: PARTIALLY-ANTICIPATED (unchanged).** V-GAP: the falsification-first *concept* is converging in
  2026 (VERITAS's Refuted/Underpowered labels); Wayfinder's differentiator is the coupling to a deterministic
  held-substrate referee. These runs are a concrete instance, not a priority claim. Critique stands.
- **HONESTY FLAG:** the ~1-in-6 own-edge rate is a genuine *shrink* of the "moat" — but it is disclosed, not
  hidden. Consistent with calibrated framing.

## M4 — deterministic-tools-only division of labour (LLM never computes a receipt)
- **Experiment(s):** Stage 1 ran the **real `arbiter.lbd.propose.sweep` unchanged** under a **pure-replay
  guard** (HTTP layer monkeypatched to raise on any live call; cache 4685→4685, **delta 0**) — every receipt
  came from deterministic code, not the model. Stage 3 = deterministic `s3fs`+`h5py` row read. Stage 5 =
  OPERON assembles prose but every number cited traces to `chain.json`.
- **vs CLAIM: SUPPORTS.** The delta-0 guard is direct evidence that no LLM fabricated a statistic during the
  sweep; receipts are code-produced.
- **vs PANEL: honest primitive (unchanged).** V-PRIM: NOT-NOVEL (standard grounded-tool-use), honest, rigor
  not headline. Execution supports the invariant; does not make it a contribution.
- **HONESTY FLAG:** none.

## M6-repro — headless scripting of an API-less workbench; funnel reproduced digit-for-digit, sensitivity byte-for-byte
- **Experiment(s):** Stage 1 receipt: **ALL 16 acceptance checks PASS** (funnel 3935/22039/43/30, NAB2 rank 4,
  ab 66/bc 2184/ac_lit 6/ac_known 0.0376/effect 301/score −1.137), pure-replay guard delta 0. **cs-reproduction
  `COMPARE.md`:** the §4.1b sensitivity panel run inside CS is **byte-identical (sha256 match, json.load
  equality True)** to local ground truth — including the seeded 2,000-perm null (`null_mean 467.727 ± 10.935`)
  reproduced to the digit, on **two** script versions. **live-fullsweep-loose:** 100%-live cold cache
  (0→9,557 calls) reproduced the identical 30 clean-supported + NAB2 rank 4/43.
- **vs CLAIM: SUPPORTS (this is the one claim whose scope IS reproduction).** Digit-for-digit and
  byte-for-byte both verified natively in CS.
- **vs PANEL: ANSWERS an under-credited critique.** adversarial_codex #8 / VERDICT call the reproduction "a
  cache replay" and the live run "a 12-gene exercise that did not recover NAB2." The **live-fullsweep-loose**
  artifact (fresh live acquisition, full universe, recovered NAB2 rank 4 exactly) **rebuts that specific
  sub-attack** — the panel did not credit it. However adversarial_codex's deeper point ("byte-identity of
  deterministic outputs from identical inputs is expected, not a contribution") **still stands** for the
  cache-replay + byte-for-byte parts.
- **HONESTY FLAG:** the README is scrupulous — it labels the main Stage-1 sweep a cached-receipt replay and
  isolates the 10 plumbing-smoke cache adds (4675→4685) from the funnel. No overstatement. The live-fullsweep
  strengthens, not contradicts, the claim.

## M9 — disease-answer-free (leakage-free) candidate-universe construction
- **Experiment(s):** Stage 1 builds A from perturbation data only (KD-QC + effect + program) before any
  disease table is read (3,935 A-genes). `hard_negatives` panel B **stratum_not_in_A**: high-curated-
  association disease genes (IL36RN, TREX1, PADI4 …) are **`in_A:false`** — i.e. A did not pull them in *via*
  their disease answer; they enter only as frozen external nominations.
- **vs CLAIM: SUPPORTS.** The universe demonstrably does not consult the disease answer; disease-famous genes
  are absent from A unless they earned it on perturbation evidence.
- **vs PANEL: honest primitive (unchanged).** V-PRIM: NOT-NOVEL (textbook target-leakage avoidance, Kapoor &
  Narayanan), but "answer-free, not evidence-free" is the correct self-limiting scope. Cite-gap only.
- **HONESTY FLAG:** none — the "not evidence-free" caveat (A is preselected on the same effect/program signal
  the referee re-reads) is stated and true.

## R1 — Funnel: 3,935 genes → 22,039 eligible pairs → 43 supported → 30 clean survivors (Stim8hr)
- **Experiment(s):** Stage 1 `sweep_Stim8hr.json` / receipt: a_genes **3935**, eligible_pairs **22039**,
  disease_c_supported_total **43**, clean_supported **30**, pure_disjoint_clean 1; chain_classes
  {refuted_for_c 21995, supported 30, supported_weak 10, supported_flagged 3, refuted_effect 1}. All acceptance
  checks ✅. Independently reproduced 100%-live in fullsweep-loose (Stim8hr chain classes: refuted_for_c 49261 /
  supported 30 … — same 30).
- **vs CLAIM: SUPPORTS exactly.** Every funnel number verified twice (replay + live).
- **vs PANEL: numbers verified, but "funnel ≠ quality" STANDS.** adversarial_codex #1: "the funnel merely
  proves thresholds remove candidates"; #9: the 30 survivors "are not 30 independently validated chains"
  (selection uses KD/effect/program, then the referee re-reads them — partial circularity). Verifying the
  counts does not answer either. Critique stands.
- **HONESTY FLAG:** none on the counts; the circularity is a framing concern the manuscript partly concedes
  (M9 "answer-free, not evidence-free").

## R2 — Referee alone supports 395/47,220; novelty gate culls 395→43
- **Experiment(s):** `sensitivity_results.json` control2: pair_space_AxC **47,220** (3935×12 diseases),
  **observed_disease_hop_supported = 406**, observed_rate 0.0086. Stage 1 confirms the post-novelty-gate
  disease_c_supported_total = **43**.
- **vs CLAIM: PARTIAL / minor discrepancy.** The pair space (47,220) and the 43-after-gate are confirmed. But
  the pre-gate referee-supported count in the artifact is **406, not 395** as the ledger states R2. The 43
  survivor count is solid; the exact pre-gate figure the manuscript cites should be re-checked against the
  source it was drawn from (406 here vs 395 claimed — an 11-count gap worth reconciling before publication).
- **vs PANEL: the "no baseline" critique STANDS** — showing a gate culls 406→43 is a threshold effect, not
  evidence the surviving 43 beat effect-alone / FDR-alone / random ranking (adversarial_codex #1).
- **HONESTY FLAG:** ⚠ **395 (claimed) vs 406 (sensitivity_results.json).** Not a large gap and possibly a
  different cut/condition, but a numeric mismatch on a headline funnel figure — verify the provenance of "395".

## R3 — Control 1: all 2,430 failed-knockdown genes returned *untested* (100%, no leakage)
- **Experiment(s):** `sensitivity_results.json` control1: n_failed_kd_genes **2430**, n_untested **2430**,
  fraction_untested **1.0**, `leaks: []`. Byte-identically reproduced in CS (`sensitivity_results.cs.json`,
  COMPARE.md; Reviewer verbatim-verified).
- **vs CLAIM: SUPPORTS exactly.** 100% of failed-KD genes abstained; zero leaked through as negatives.
- **vs PANEL: this is the CLEAN part.** It is the strongest direct demonstration of the M2 hero gate and the
  panel does not dispute it. It is still a *behavioural demonstration* (the gate does what it's built to do),
  not a decision-quality evaluation — so it supports M2's honesty, not the missing benchmark.
- **HONESTY FLAG:** none — clean, reproduced, leak-free.

## B3 — STAT6 cis-effect ruled out at the expression level (log2FC +0.087, p 0.79)
- **Experiment(s):** Stage 3 `stage3_cis.json` / receipt, **live anon S3 read** of the 16.8 GB deposited DE
  matrix: under NAB2-KD @Stim8hr, **STAT6 log2FC +0.0870, adj_p 0.7884, not significant** (|log2FC| rank
  5,444/10,282); **NAB2 self −3.0783, adj_p 7e-60** (knockdown worked); 302 genes moved (≈ referee effect=301).
  7/7 assertions PASS.
- **vs CLAIM: SUPPORTS exactly.** The hardest confounder (guide ~1.9 kb from STAT6) is refuted at the
  expression level — STAT6 mRNA is unmoved while the on-target knockdown is strong.
- **vs PANEL: the panel CREDITED this AND under-credited it.** VERDICT "WHAT SURVIVES #3": both adversaries
  steelmanned B3 and "could not break it" — a reusable cis-artifact-falsification template. This CS-native live
  S3 run is that competent, honest test executed natively. BUT adversarial_codex #10's scope caveat STANDS and
  is *disclosed*: it rules out a **steady-state expression** decrease only — not STAT6 isoforms, chromatin,
  transcriptional interference, or downstream STAT6 activity. The manuscript's own hedge ("one aggregate
  Stim8hr null … not every conceivable cis channel") matches this exactly.
- **HONESTY FLAG:** none — B3 is scoped correctly ("ruled out at the expression level," not "STAT6 excluded").
  The calibrated wording aligns with the reviewer's calibrated-language edit (Stage 5 removed "definitive" from
  the Stage-3 heading; review.json flags it).

---

## Cross-cutting honesty flags (for Step-2 orchestrator)
1. **⚠ R2 numeric mismatch:** ledger says referee-alone supports **395**/47,220; `sensitivity_results.json`
   says **406**. Reconcile the "395" provenance before it appears in the manuscript funnel.
2. **Execution ≠ evaluation (M1/M4/M6/M9/R1/R3):** every CS-pipeline run is reproduction/liveness. The panel's
   FATAL "demonstrated-not-evaluated" finding is untouched by this cluster — do NOT let a green ALL_PASS /
   byte-identical / Reviewer-passed run be read as answering it.
3. **Under-credited by the panel — surface it:** `live-fullsweep-loose/` (100%-live, cold-cache, full-universe,
   recovered NAB2 rank 4/43) rebuts adversarial_codex #8's "only a cache replay / live run didn't recover
   NAB2." Worth citing back at that critique.
4. **M3 self-shrink is real and disclosed:** referee own-edge cull ~1 in 6 (own_edge_cull_rate 0.1693);
   Control 2 shows the disease-hop stringency is substrate-inherited (observed 406 vs null_mean 467.7, fold
   0.87, empirical_p 1.0 — *not* rarer-than-chance). The moat is honestly narrow.
</content>
</invoke>
