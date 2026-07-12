# NEW EXPERIMENTS — closing the reconciliation's gaps (Step 3, 2026-07-12)
Derived from `RECONCILIATION.md`. Each item traces to the claim it serves, the gap it closes, and the source
data it needs. Status is tracked in `docs/CLAIMS_EVIDENCE_LEDGER.md`. Priority = G1 ≫ G2 > G3.

## G1 — A REAL EVALUATION WITH A BASELINE  *(the publish gate; closes the audit's central FATAL)*
> **STATUS 2026-07-12: DE-RISKED → GO Option A** (Europe PMC as-of-T windowing verified; positive class
> ~1,469/22,039, CI floor 807; `docs/spikes/heldout-eval-feasibility_2026-07-12.md`) **+ codex-debate-hardened**
> (converged 3 rounds, repo-verified, no sanding; `docs/reviews/codex-debate_heldout-eval-plan_2026-07-12.md`).
> **Build to the frozen spec** `docs/plans/heldout-eval-implementation-plan_2026-07-12.md` (v3). **CS-driver
> health-check PASSED 2026-07-12** (drivable on port 8000; driver defaults 8765 — override). Next:
> enumerate frame + count manifest → 6 rankers + 2 co-primary contrasts → run in CS.
**Serves:** M1/M3/M8/M10, R2/R4 — converts "SUPPORTED-BY-EXP (demonstration)" into "measured decision quality."
**Why it's the gate:** every existing run is execution/reproduction; nothing measures precision/recall vs a
baseline (`recon_analyses.md`). Without this the method is unpublishable as an *evaluated* method.

**Option A (primary) — time-sliced held-out evaluation.** Already scoped in
`docs/plans/heldout-eval-scope_2026-07-12.md`: freeze literature at cutoff T, generate as-of-T, measure
recovery of post-T-established links; Wayfinder vs baselines (literature-rarity / effect-only / enrichment-only /
random); report precision@k, MAP, recall. **Source:** S5 (Europe PMC, as-of-T windowing — feasible per
`sources.europepmc_count`). **CS-native:** yes — generation already runs in CS (S10); the metric harness can run
in CS or locally.
**Option B (fallback) — promote `hard_negatives` to a metric.** It is already baseline-*shaped* (a frozen
curated-association nominator, S6); add a labelled gold set and compute precision/recall on the referee's culls.
Weaker than A (no time element) but cheaper. **Source:** S4/S6.

**DE-RISK FIRST (do this next):** a live-network spike (main-thread, not Codex-sandbox) that (1) confirms
Europe PMC date-windowing behaves and (2) **sizes the post-T positive class** at T ∈ {2016,2018,2020}. If the
positive class is too small → pivot to Option B. Output → `docs/spikes/heldout-eval-feasibility_<date>.md`.
Effort: ~½ session. **[CLAUDE — needs live network]** → then build **[CODEX-RESCUE]** → integrate **[CLAUDE]**.

## G2 — 12q13 COLOCALIZATION  *(the one open biology confounder; B5)*
**Serves:** B5 (OPEN-GAP) — the GWAS eczema-label LD-inheritance question the substrate cannot settle.
**Method:** variant-level colocalization / summary-data Mendelian randomization (coloc/SMR) between the 12q13
atopic-dermatitis GWAS and CD4⁺ T-cell *NAB2* vs *STAT6* eQTLs — tests whether the eczema association is
NAB2-specific or an LD shadow of STAT6. **Source:** external AD GWAS summary stats (S1 lists the study; the
GWAS sumstats are external) + a CD4⁺ eQTL resource (external, e.g. DICE/eQTL Catalogue).
**CS-native feasibility: UNCERTAIN — needs a feasibility check first.** Requires (a) obtaining GWAS sumstats +
eQTL data and (b) coloc/SMR tooling; and it "presupposes a detectable NAB2 cis-eQTL in CD4⁺ T cells" (§4.4b) —
which may not exist, in which case even variant data can't separate NAB2 from STAT6. **First step:** a CS/Claude
spike to check whether a NAB2 CD4⁺ cis-eQTL exists at all (if not, G2 is not resolvable and B5 stays OPEN — which
is itself a publishable, honest statement). Effort: 1 session if data reachable. **[CODEX-SPIKE then CLAUDE]**.

## G3 — FROZEN RECEIPT FOR EGR-DISTINCTNESS  *(cheap; R5)*
**Serves:** R5 — currently script-only (`nab2_egr_mechanism_check.py`), no committed output receipt.
**Method:** re-run the script, save the output JSON (NAB1 paralog-opposition = the load-bearing D3 fact; both
contrasts significant), commit it as a receipt like the other analyses. Reframe the manuscript arg around D3
(not the weak cross-cohort D2). **Source:** S4. Effort: <½ session. **[CLAUDE — small]**.

## MANUSCRIPT FIXES (not experiments — apply from `RECONCILIATION.md`'s 9 honesty flags)
Track as edits, not new work; each is a wording/number correction:
1. M6 "byte-for-byte" → "value-identical / digit-for-digit" (files differ by newline only).
2. M5 "flagged and removed" → note one word ("validated") was flagged and retained by design.
3. R2 funnel: reconcile 395 vs 406 (referee-alone supported count).
4. M8/R4: state rank stability conditions on NAB2 surviving the gate (culled 9/27 cells).
5. B6: T/NK −0.57 is n.s. (p 0.11) → "partial," not "confirmed per-cell."
6. Retire the buggy `[74,90]` confounder script; cite only the corrected 90/100 derive-clusters path.
7. Cosmetic: stale "1.9 kb" (old headers) → "~43 kb" (already corrected in the manuscript body).
8. M7: "reproduced every headline number" → "reproduced all but two, which it corrected."
9. B7: add the EGR2-is-STAT6-driven-pro-type-2 sign-flip caveat to §5.2.

## Recommended sequence
1. **G1 de-risk spike** (next) — decides Option A vs B; the only gap that gates publication.
2. Apply the 9 manuscript fixes (cheap, independent, honest-record hygiene).
3. **G3** frozen receipt (cheap).
4. **G2 eQTL-existence spike** — determines whether B5 is resolvable or stays a foregrounded-open (both are honest).
5. Build the chosen G1 eval → integrate → the method becomes *measured*, at which point re-assess publishability.
