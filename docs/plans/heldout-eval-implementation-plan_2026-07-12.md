# G1 — Time-sliced held-out evaluation: implementation plan (v2, codex-debate-hardened R1)
De-risk: **GO — Option A** (`docs/spikes/heldout-eval-feasibility_2026-07-12.md`). Closes the audit FATAL
(method *demonstrated, never measured*, `docs/reviews/contribution-novelty-audit_2026-07-12/VERDICT.md`).
**v2 folds in Codex debate round 1** (`docs/reviews/codex-debate_heldout-eval-plan_2026-07-12/round_01_codex.json`,
13 findings). Codex confirmed the design is **not circular** (fixed-2025 data vs post-2016 literature labels are
distinct signals); the fixes below make it a defensible measurement.

## Estimand (F-010 — precise wording; NOT "prospective prediction")
**Retrospective literature time-slicing against a contemporary fixed substrate.** Among gene→Th1/Th2→disease
links that were **literature-novel as of T=2016**, does a data-grounded ranker recover the ones that became
**literature-established after T** better than literature-rarity and single-axis data baselines? It measures
whether fixed experimental grounding *ranks future-established links higher within the novel set* — a proxy for
decision quality, **not** biological truth and **not** forecasting.

## The common comparison frame (F-001, F-002, F-004 — the core fix)
- **Frame = the novel-at-T set:** ALL (gene∈A, disease∈C) pairs with `ac_lit_asof(2016) ≤ 1`. Every method ranks
  the SAME frame. A×C = 3,935×12 = 47,220; the frame is the novel-at-T subset (enumerated exactly, not sampled).
- **Positives = post-T establishment WITHIN the frame:** `ac_lit_now ≥ 5` (primary). Because the frame is already
  novel-at-T, positives isolate *establishment*, not novelty — so lit-rarity cannot win on the novelty component.
- **Full enumeration is the prerequisite** (F-003, F-004): compute the sliced frame exactly, report its size, its
  overlap (Jaccard) with the current-literature frame, and the **exact** positive count **before** any ranking.
  The spike's ~1,469 is *preliminary* (pre-referee-stratification); the frozen protocol uses the enumerated count.
  Delete the "gate can only shrink" assertion — composition can shift; reconstruct and report it.

## The rankers (F-002, F-011 — exact total-orders over the frame)
All rank the identical novel-at-T frame; ties broken by a fixed rule (then stable pair-id order).
1. **Wayfinder** = primary sort by the **EXHAUSTIVE** referee verdict class (F-002; the 8 classes
   `referee_triple.py` line-refs 104–132), best→worst: `supported` > `supported_flagged` > `supported_weak` >
   `refuted_program` > `refuted_effect` > `refuted_for_c` > `untested_for_c` > `untested` — then by the §3.2
   score computed **as-of-T** (`ac_known` term = 0), then stable pair-id. (My v2 omitted `refuted_program` — now
   included; the intra-class order is pre-registered and only the `supported*` classes reach the top-k.) This is
   an **evaluation variant** of `propose.py`'s ordering (which pre-filters to survivors); we rank the *whole
   frame* and say so.
2. **B-disease-hop-only** (F-011, the sharpest baseline) — executable definition MIRRORING
   `referee_triple.py::_hop3_for_disease` (lines 51–75): for each (gene, C-disease, condition), filter
   `t3_exploded` to that triple, take rows with `p_adj_fdr < 0.05`; **supported iff ≥1 such row**; the score is
   the **min-FDR row** (`sig.sort_values("p_adj_fdr").iloc[0]`) — rank supported-first, then by that row's OR
   (desc), then −FDR. This collapses the multiple T3 cluster rows per pair exactly as the referee does, and
   isolates whether a Wayfinder win comes from the **exact-C disease hop** vs the QC/effect/program hops.
3. **B-lit-rarity** — ascending as-of-T `ac_lit` (classic "rare = interesting").
4. **B-effect** — downstream-DE count (time-invariant).
5. **B-enrichment-continuous** — same as (2) but the raw enrichment score without the referee's binary gate.
6. **B-random** — seeded shuffle.

## Frozen primary estimand + multiplicity (F-006, F-012 — pre-register before labels)
- **TWO CO-PRIMARY contrasts (F-014 — each with a frozen decision role), on the novel-at-T frame, T=2016,
  establish-k=5, novel=`asof≤1`, precision@20, gene-and-disease two-way-clustered paired bootstrap 95% CI (F-005):**
  - **C-broad:** `prec@20(Wayfinder) − prec@20(B-lit-rarity)` — tests the *broad fixed-substrate hypothesis*
    (does experimental grounding beat obscurity).
  - **C-mech:** `prec@20(Wayfinder) − prec@20(B-disease-hop-only)` — the *mechanistic decomposition* (do the
    QC/effect/program hops add value beyond the GWAS-derived disease enrichment).
  - **Pre-registered joint-outcome interpretation (no post-hoc spin):**
    | C-broad | C-mech | Conclusion (frozen) |
    |---|---|---|
    | +CI>0 | +CI>0 | Full claim: fixed-substrate grounding *and* the three referee hops add measured value |
    | +CI>0 | null/neg | Narrow claim: the win is carried by the disease-enrichment hop; QC/effect/program add **no measured** incremental value — report as such |
    | null/neg | — | Broad hypothesis fails; report the null straight |
- **Secondary (reported, not headline):** precision@{5,10,50}, MAP, recall@N; T∈{2018,2020}; k∈{3}, pure-disjoint
  (`asof==0`); popularity-stratified metrics (F-013).
- **Multiplicity:** one primary estimand fixed above; all else secondary/sensitivity. No metric/cutoff/T is
  promoted to headline after seeing results.
- **Blinded feasibility gate (F-012):** decide GO/adjust using **label counts only** (frame size, positive count)
  — never method performance. Fixed fallback order if positives < ~100 after enumeration: widen k-establish→3 →
  T→2014 → relax novel→`asof≤2`. Frame is LOCKED before any method's performance is inspected.

## Inference (F-005)
Paired method-difference intervals via bootstrap that **resamples genes and diseases** (two-way cluster), not
pairs i.i.d. **Remove** the "non-overlapping marginal CIs" acceptance rule — report the paired-difference CI and
its sign; a null (CI spans 0) is reported straight.

## Signal layer + query integrity (F-007, F-008, F-009)
- Add `cooccur_count_asof(a, b, T)` to `sources.py` (append `AND (FIRST_PDATE:[1900-01-01 TO {T}-12-31])`;
  VERIFIED 2026-07-12). Recompute `ab`, `bc`, `ac_lit` as-of-T. **`ac_known` DROPPED** → this is explicitly the
  **`ac_known`-ablated variant** (F-007); report a sensitivity note (current-OT is leaky-vs-conservative), do not
  claim method-identity with the headline pipeline.
- **Query-integrity tests (F-008):** golden-query fixtures, cutoff-boundary tests (T-1/T/T+1), gene/disease alias
  handling, and persisted **query receipts**.
- **Reproducibility contract (F-009):** freeze + hash every (query, result, retrieval-date) into a committed,
  non-sensitive **count manifest** sufficient to recompute all metrics WITHOUT live API drift. A gitignored cache
  is not a research receipt — the manifest is. (Fixes the audit's reproducibility-honesty flag too.)

## Where it runs
**Claude Science (native)** via `drive-claude-science` — CS authors + runs the enumeration, the as-of-T sweep,
and the metric harness, with provenance to `operon-cli.db` and an independent reviewer verifying every number
(a §4.5-consistent CS result). **CS-driver health-check PASSED 2026-07-12** (end-to-end on a fresh project:
sign-in → create → send → auto-approve code card → Python run → artifact, sha256 hash-verified vs local;
`operon-cli.db` captured it). **Build note:** CS runs on **port 8000**; the driver + skill default to 8765 —
override `--url http://localhost:8000/` + mint the nonce on `:8000`. **Fallback:** run locally and **state it ran
locally** — never claim CS if it ran here (F-009 + calibrated-language discipline).

## Acceptance gates
(a) exact enumerated frame + positive count reported, blinded feasibility gate passed (F-012);
(b) frozen primary estimand computed with the two-way-clustered paired CI (F-005/F-006);
(c) the F-011 incremental contrast (Wayfinder − disease-hop-only) reported;
(d) query manifest committed, metrics recomputable from it (F-009);
(e) a §4 paragraph + one figure (precision@k per method, paired CIs) — **null reported straight if it doesn't separate.**

## Honest scoping (verbatim → manuscript)
- Measures ranking-of-future-literature within a novel-at-T frame — a proxy for decision quality, not biological
  truth; "established" = ≥5 Europe PMC co-mentions is **popularity-confounded** (F-013) → report popularity-
  stratified metrics + a blinded manual spot-check of a stratified label sample.
- `ac_known`-ablated variant; sliced funnel differs from the headline funnel (report both).
- Substrate not time-sliced (one fixed 2025 dataset) — the design *is* "does fixed experimental grounding recover
  future-established links," the LBD thesis; state it. **Audit (F-010):** confirm T3's disease labels are
  GWAS-derived (not Europe-PMC-literature-derived) so the disease hop cannot leak the outcome signal.

## Debate trail
Round-1 findings + resolutions: `docs/reviews/codex-debate_heldout-eval-plan_2026-07-12/`. Accept/reject ledger:
`round_02_claude.md`.
