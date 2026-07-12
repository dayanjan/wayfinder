# Recon — NAB2 DIRECTION / TARGET cluster (B6, B7) vs the direction-GEO / scRNA / DepMap experiments

**Scope:** reconciles ledger claims **B6** (NAB2 reads down in lesional AD skin) and **B7** (NAB2 =
"Th2 brake" → restore, not knockdown) against what the 2026-07-09 direction work actually ran, and
against the panel's B6/B7 critique (`verify_dir.md`, `VERDICT.md`). Read-only; sources cited inline.

## Exec summary (~150 words)
**B6 → SUPPORTS (with a caveat).** The direct expression mining is real and on-point: bulk GSE330551
NAB2 log2FC −0.32 / FDR 0.002, anti-correlated with Th2 (ρ −0.34, p 3.6e-6, n 174); scRNA GSE204762
pseudobulk confirms per-cell down in keratinocyte −0.51 (**p 0.027**) and myeloid −0.59 (p 0.049),
with keratinocyte *proportion* UP → not dilution. This **under-credited experiment answers the panel**:
the panel could only reach "UNVERIFIABLE-BY-LIT" because it searches abstracts, not supplements — the
mining makes B6 a *re-derived DE result*, not a mere nomination. **Caveat / honesty flag:** T/NK −0.57
is cited as confirmed but is **p 0.11 (n.s.)**; the arm's own verdict is "CONFIRMED_PER_CELL_**PARTIAL**."
**B7 → PARTIAL / COMPLICATES.** Direction is genuinely mixed (1 significant voting arm of 4; cytokine
arm null; T ambiguous). The brake **sign is not settled** by these data — the manuscript's hedge is
right. Residual gap: the EGR2-is-STAT6-driven-pro-type-2 sign-flip risk is unaddressed.

---

## B6 — "NAB2 reads DOWN in lesional AD skin (per-cell: keratinocyte −0.51, T/NK −0.57)"

### (1) What was actually run + key numbers
- **ARM-A bulk, GSE330551** (`per_arm.json` arms.A): lesional-vs-non-lesional, patient fixed effect.
  NAB2 **log2FC −0.32, FDR 0.00178, p 3.8e-5** (n 174; 57 primary samples). Type-2 ρ **−0.34**
  (p 3.6e-6); robust across three type-2 scores (full −0.31, detection-filtered −0.34, chemokine/
  receptor −0.37). STAT6 also down (−0.14, FDR 0.031). Arm call **DOWN**.
- **scRNA ARM-D, GSE204762** (`arm_d_scrna/report.md`, `arm_d.json`): 39 human samples, dataset's own
  `obs:Cell type` labels, pseudobulk NAB2 by cell-type × condition; per-sample processing (each h5ad
  decompressed then deleted). Within-cell-type lesional-vs-non-lesional log2FC:
  **keratinocyte −0.5135 (paired p 0.027)**, **T/NK −0.5706 (p 0.11)**, myeloid −0.595 (p 0.049),
  VEC −0.20, Pericyte −0.02.
- **Composition check:** keratinocyte *proportion* is **UP** in lesional (0.439 vs 0.338), immune
  proportion up → the bulk NAB2-down is **not** an infiltrate-dilution artifact. This is the analysis
  that removed the load-bearing composition caveat flagged in `SUMMARY.md`.

### (2) Classification vs CLAIM: **SUPPORTS**
Every number in the B6 claim traces to a receipt (bulk −0.32/FDR 0.002; kera −0.51; T/NK −0.57;
composition resolved). The direction is internally concordant (bulk DOWN + ρ −0.34 + per-cell DOWN in
the disease-relevant compartments). The arm's own verdict is **CONFIRMED_PER_CELL_PARTIAL**.

### (3) vs PANEL CRITIQUE — the direct mining is UNDER-CREDITED
Panel (`verify_dir.md` B6): **UNVERIFIABLE-BY-LIT (lean PARTIALLY-ANTICIPATED), hedge ADEQUATE** —
because `search_all` indexes titles/abstracts, not supplementary DE tables, so it *cannot confirm or
deny* whether NAB2-down already sits buried in an AD supplement. **The direct expression experiment
does what the literature search could not:** it establishes, on public data, that NAB2 *is* down in
lesional AD per-cell. So B6 is more than a literature nomination — it is a **re-derived experimental
result**. **Important boundary:** the experiment answers the *factual* question ("is NAB2 down?" — yes),
NOT the *priority/novelty* question the panel actually raised ("is this already in someone's
supplement?"). The mining cannot discharge the priority concern; it only removes the "is it even true"
doubt. So: SUPPORTS the fact, under-credited as evidence — but does not convert UNVERIFIABLE-BY-LIT
into NOVEL.

### (4) HONESTY FLAG — T/NK is cited as confirmed but is not significant
The claim (and manuscript §5.2) lists "**T/NK −0.57**" beside "keratinocyte −0.51" as the per-cell
confirmation. In the receipt, **T/NK paired p = 0.11 (not significant)**; only keratinocyte (0.027) and
myeloid (0.049) cross p<0.05. The arm verdict is deliberately "CONFIRMED_PER_CELL_**PARTIAL**." The
manuscript drops the "PARTIAL" and states the composition confound is *resolved* ("confirmed this is a
per-cell reduction … rather than a shift in cell-type composition") while quoting the n.s. T/NK effect
without its p-value. **Mild over-statement of per-cell confidence** — clean fix: cite T/NK's −0.57 with
"p 0.11, direction-only" or lead with the significant keratinocyte/myeloid compartments.

---

## B7 — "NAB2 = Th2 brake lost in chronic lesions → restore/up-modulate, not knockdown"

### (1) What was actually run + key numbers
The full 4-arm voting structure + STAT6 test + DepMap (`per_arm.json`, `report.md`, DepMap README):
- **Voting-arm split — bulk triangulated call = NO-CALL.** A (GSE330551) **DOWN**; T (GSE32959, CD4
  Th2-vs-Th1) **AMBIGUOUS** (probes sign-discordant: 212803_at +0.15 / 216017_s_at −0.05); B (GSE292848,
  ex-vivo cytokine) **NO-CALL** — **IL-4/IL-13 do NOT induce NAB2** (IL4_IL13 vs control −0.11, FDR 0.73);
  C (GSE130588, dupilumab reversal) **AMBIGUOUS**. Decision rule (≥2 concordant arms, cytokine-arm
  privileged) **not met**.
- **STAT6 direct test (GSE17851):** NAB2's IL-4 response is **not STAT6-dependent** (Control_Act+IL-4
  −0.089/FDR 0.82; interaction 0.069/FDR 0.97). Consistent with B3.
- **DepMap:** NEGATIVE as a cancer target (CRISPR 4/1208, RNAi 1/710, no tractability), **non-
  contradictory** for an immune-regulator role; **no EGR co-dependencies** → no network corroboration.

### (2) Classification vs CLAIM: **PARTIAL / COMPLICATES**
The "brake" is a *directional reading*, and the experiments **do not settle its sign**. Only one voting
arm is significant; the on-point CD4 T-cell arm (T) is ambiguous; the cytokine arm actively shows IL-4/13
do not induce NAB2. Expression tracks *association direction*, not effector-vs-brake (stated ceiling in
every artifact). So B7 remains an **unsettled hypothesis**, exactly as scoped — the experiments COMPLICATE
any strong directional/therapeutic reading and leave the sign open.

### (3) vs PANEL CRITIQUE — is the brake settled? NO. Is the hedge right? YES.
Panel (`verify_dir.md` B7): **PARTIALLY-ANTICIPATED (mechanism: EGR2/3 are textbook inflammation brakes) +
NOVEL (the specific NAB2-as-Th2-brake AD nomination), hedge "precisely calibrated."** The direct
experiments **do not resolve** the sign — they corroborate the panel: the direction is genuinely mixed.
The manuscript hedges B7 as "the directional *question* to test rather than an established concordance"
and states "the substrate's directional metrics do not by themselves settle" the sign — **that hedge is
correct**, endorsed independently by (a) the experiment (NO-CALL / one significant arm) and (b) the panel
(hedge adequate). The hedge is *not* an over-cautious dodge; it matches the data.

### (4) HONESTY FLAG — over-reach on therapeutic direction + the EGR2 sign-flip
- **"Backwards therapy / restore NAB2" framing — manuscript is well-calibrated; the internal SUMMARY is
  hotter.** `SUMMARY.md`'s revised call ("naive hypothesis is likely BACKWARDS … topical-KNOCKDOWN idea
  is contra-indicated by the data") leans harder than the mixed evidence warrants. The **manuscript §5.2
  does NOT over-reach**: it says topical knockdown is "*likely* backwards," restoration is "the direction
  to *test*," flags "voting-arm evidence was mixed (one significant arm)," and states "only a perturbation
  … can convert this brake hypothesis into a directional therapeutic claim." That is honest. Keep the
  manuscript language; do not let SUMMARY.md's stronger phrasing migrate into the paper.
- **EGR2-is-a-STAT6-driven-pro-type-2 sign-flip risk (present, unaddressed).** The panel's operator
  caution: EGR2 is a **direct STAT6 target and linchpin of IL-4-driven type-2 polarization** (Genes Dev
  2020, `10.1101/gad.343038.120`) → EGR2 can be *pro*-type-2, which would route NAB2's net sign
  differently and (worse) **ties the brake module back to STAT6** — the very gene B2/B3's 12q13/cis
  confounder concerns. The direction experiments do **not** resolve this; the manuscript's "sign
  unsettled" hedge survives it but **does not mention it**. Recommended (panel-endorsed): add a
  half-sentence in §5.2 acknowledging "EGR2 is itself a STAT6-driven pro-type-2 factor in some
  compartments, so the module's net sign is context-dependent." Pre-empts the reviewer objection and
  reads as even-handed.

---

## Bottom line for RECONCILIATION.md
- **B6 → SUPPORTS** (re-derived experimental result; under-credited vs the panel's abstract-limited
  UNVERIFIABLE grade). Honesty fix: qualify the n.s. T/NK −0.57 (p 0.11); the confirmation is
  keratinocyte/myeloid, T/NK is direction-only. Priority/novelty concern remains open (not an experiment
  question).
- **B7 → PARTIAL / COMPLICATES** (direction mixed; sign not settled; brake stays a hypothesis). The
  manuscript's hedge is accurate and should be preserved. Two residual honesty items: (a) keep the
  calibrated §5.2 language over SUMMARY.md's hotter "contra-indicated"; (b) add the EGR2/STAT6
  pro-type-2 sign-flip caveat, currently missing.
