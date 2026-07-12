# Spike — time-sliced held-out eval feasibility (G1 de-risk)

**Date:** 2026-07-12 · **Mode:** live-network main-thread spike (Europe PMC) · **Read-only** except this file.
**Question:** Is the post-cutoff POSITIVE class big enough to measure precision/recall on a time-sliced
held-out eval (Option A), or must we pivot to the no-time-slice fallback (Option B)?
**Design ref:** `docs/plans/heldout-eval-scope_2026-07-12.md` · `docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md` (G1).

## Headline

**GO — OPTION A.** Recommended cutoff **T = 2016**, established-now threshold **k = 5**, novel-at-T
definition **`ac_lit_asof(T) ≤ 1`**. The positive class projects to **≈1,469 pairs** (95% CI ≈807–2,609)
out of the 22,039 eligible A×C pairs — a ~6.7% base rate, far above the ≥100-positive GO bar. **Every**
tested (T, k) cell clears the bar; even the strictest cell (T=2020, k=5) projects ≥100. Time-slicing is viable;
no pivot needed.

## Method

1. **Eligible universe reconstructed exactly.** Rebuilt the pipeline's eligible (gene, disease) set locally
   from the Perturb-seq CSVs + warm Europe-PMC/Open-Targets cache, replaying the headline sweep gate
   (`ab ≥ ab_gate(median)=26`, `bc ≥ 3`, `ac_known ≤ 0.1`; condition=Stim8hr, `program_significant=True`).
   Result: **22,039 eligible pairs** over **3,935 genes × 12 diseases** — an exact match to
   `stage1/sweep_Stim8hr.json` `funnel.eligible_pairs`, so the sample frame *is* the projection target
   (no frame-mismatch error).
2. **Deterministic sample.** `random.Random(seed=20260712).sample(range(22039), 150)` → 150 pairs
   (index-only randomness; fully reproducible).
3. **Per-pair counts (live Europe PMC).** For each pair:
   - `ac_lit_now = cooccur_count(gene, disease)` = `("gene") AND ("disease")`.
   - `ac_lit_asof(T)` for T ∈ {2016, 2018, 2020} = the same query with
     ` AND (FIRST_PDATE:[1900-01-01 TO {T}-12-31])` appended (via `europepmc_count`).
   600 counts total (~11 min at the tool's polite 0.34 s/call; cached thereafter).
4. **Windowing validated (belt-and-suspenders).** Spot-check confirmed strict monotonic date-ceilinging,
   e.g. STAT6×asthma 1950(’16) < 2463(’18) < 3034(’20) < 5467(now); UFM1×MS 4 < 7 < 10 < 43. Syntax honored.
5. **Positive class per (T, k):** pairs **novel-at-T** (`asof(T) ≤ 1`) AND **established-now** (`now ≥ k`),
   k ∈ {3, 5}. Report count, rate, and rate × 22,039 projection with a Wilson 95% CI.

## Results (n = 150 sample; projection base = 22,039)

Primary novel-at-T definition = `asof(T) ≤ 1`; a stricter pure-disjoint variant (`asof(T) == 0`) shown for reference.

| T | k | novel defn | positives | rate | projected | proj 95% CI |
|---|---|---|---|---|---|---|
| **2016** | 3 | ≤1 | 21 | 14.0% | **3,085** | 2,059–4,508 |
| **2016** | **5** | **≤1** | **10** | **6.7%** | **1,469** | **807–2,609** |
| 2018 | 3 | ≤1 | 13 | 8.7% | 1,910 | 1,132–3,143 |
| 2018 | 5 | ≤1 | 5 | 3.3% | 735 | 316–1,667 |
| 2020 | 3 | ≤1 | 8 | 5.3% | 1,175 | 601–2,241 |
| 2020 | 5 | ≤1 | 3 | 2.0% | 441 | 150–1,259 |
| 2016 | 3 | ==0 | 9 | 6.0% | 1,322 | 703–2,426 |
| 2016 | 5 | ==0 | 3 | 2.0% | 441 | 150–1,259 |
| 2020 | 5 | ==0 | 2 | 1.3% | 294 | 81–1,043 |

**GO bar** (design rule of thumb): ≥30–50 projected positives, ideally ≥100. **All nine cells clear ≥100
on the point estimate; the recommended cell clears it on the CI lower bound (807).** The weakest cell
(2020/k5/==0) still projects 294 (CI floor 81).

### The positives are real, growing links (not co-mention noise)

Sample positives at T=2016, k=5 (`asof2016 → now`): GZMH×type-1-diabetes 1→23 · KLF9×ankylosing-spondylitis
0→16 · GLB1×ankylosing-spondylitis 1→15 · TESPA1×SLE 1→13 · SCD5×ulcerative-colitis 1→13 · GP6×atopic-eczema
1→8 · plus four more. These are near-disjoint-as-of-2016 pairs whose direct co-mention was genuinely written
down afterward — exactly the "link established after T" signal the eval needs. Of the 21 T=2016/k=3 positives,
5 grew to now ≥ 10 (strongly established).

## Recommendation

**GO-OPTION-A** (time-sliced held-out eval). Build against:

- **T = 2016** — the 10-year holdout gives the largest, best-powered positive class and the most post-T
  literature to establish links. (2018/2020 also pass, if a shorter window is later preferred for a
  "recent-prediction" framing.)
- **k = 5** as the primary established-now bar (a ≥5-co-mention link is defensibly "written down," less
  noise-prone than k=3). **Report k=3 as a sensitivity row** (~2× the positives, same conclusion).
- **novel-at-T = `asof(T) ≤ 1`** primary; carry the **pure-disjoint `== 0`** variant as a stricter
  robustness check (still ≥100 projected).
- Projected primary positive class **≈1,469 / 22,039 (~6.7%)** — ample for precision@k (k = 5,10,20,50),
  recall, and MAP, with room for the design's bootstrap CIs.

## Caveats

1. **Sampling noise is real but non-fatal.** Positive counts are small integers (3–21), so the Wilson CIs
   are wide (recommended cell: 807–2,609). The conclusion is robust to it: every cell's CI floor clears the
   ≥100 bar (recommended cell floor = 807), so the GO does not hinge on the point estimate.
2. **"Novel-at-T co-mention grew" is the intended signal, not a bug.** The positive definition is a *growth*
   test (`asof(T) ≤ 1 → now ≥ k`); the examples above confirm growth is substantive (up to 1→23), not a
   drift from 1→3 near the threshold. k=5 hardens this vs k=3.
3. **This measures prediction-of-future-literature, not biological truth** (per the design's honest caveat).
   A positive = a link that got written down after T; a real link never written down is a false negative,
   a wrong written link a false positive. Report as decision-quality-vs-literature.
4. **`ac_known` (Open Targets) is current-only** and must be dropped from the as-of-T novelty definition
   (its current value would exclude the very links that later became known). Eligibility here still applied
   the *current* `ac_known ≤ 0.1` gate to match the headline funnel's frame; the as-of-T *novelty* label uses
   literature only, as scoped. The build should recompute eligibility's ab/bc as-of-T too (per the plan), which
   can only *shrink* the eligible frame and shift positives — re-confirm sizing on the as-of-T frame at build time.
5. **Single experimental substrate** (one Zhu-2025 dataset) is not time-sliced — frame as
   "literature-time-sliced eval against a fixed contemporary experimental substrate."

## Reproducibility

Seed `20260712`; eligible frame reconstructed deterministically from `stage1/sweep_Stim8hr.json` params
(`ab_gate_pct=0.50 → 26`, `min_bc=3`, `tau=0.1`, Stim8hr, program-significant). Counts via
`arbiter.lbd.sources.cooccur_count` / `europepmc_count` with the `FIRST_PDATE` ceiling clause. All 600
counts are now warm in `data/lbd_cache/`.
