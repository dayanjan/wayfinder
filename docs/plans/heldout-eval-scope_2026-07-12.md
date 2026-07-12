# Scope — time-sliced held-out evaluation (the audit's #1 "no → yes" move)

**Why:** the 2026-07-12 contribution audit's central FATAL: the method is *demonstrated, never
evaluated* — no precision/recall/baseline. This eval converts "the machinery runs" → "the machinery
is right," and directly answers the adversaries' "no baseline comparison" attack. It is §5.3b step (1),
and the paper already promises it. Reference: `docs/reviews/contribution-novelty-audit_2026-07-12/VERDICT.md`.

## The question the eval answers
*Given the literature frozen at a cutoff T, does Wayfinder's data-grounded ranking recover the
gene→Th1/Th2→disease links that became literature-established only AFTER T — better than literature-rarity
and simpler data baselines?* (i.e., does the Perturb-seq referee add predictive signal beyond obscurity?)

## Design (yetisgen2009 time-slice, adapted to this pipeline)
1. **Freeze literature at T.** Recompute the generation signals `ab`, `bc`, `ac_lit` **as-of-T** by adding a
   publication-date ceiling to every Europe PMC co-mention query.
2. **Generate as-of-T.** Run the funnel over the same 3,935-gene universe; candidates that are *novel as of T*
   = near-zero as-of-T direct co-mention (`ac_lit_asof ≈ 0`).
3. **Ground truth (positive class).** A (gene, Th1/Th2, disease) candidate is a POSITIVE if its direct
   co-mention was ≈0 as-of-T but is ≥ k **now** (the link got written down after T). Everything else is a
   negative (stayed obscure).
4. **Score & rank** every as-of-T-eligible candidate by each method (below), then measure recovery of the
   post-T positives.

## Methods compared (this is what answers "no baseline comparison")
- **Wayfinder** = referee-gated (QC/effect/program/disease hops hold) + full ranking score.
- **Baseline A** — literature-rarity alone (classic LBD: rank by inverse as-of-T co-mention).
- **Baseline B** — effect-size alone (downstream-DE count).
- **Baseline C** — disease-enrichment alone (OR/FDR at the disease hop).
- **Baseline D** — random.
**Metrics:** precision@k (k = 5,10,20,50), recall, mean average precision; report separately whether the
**referee gate** (not just the score) improves precision over the ungated literature baseline — that is the
load-bearing "the data test adds value" result.

## Feasibility — CONFIRMED and CONSTRAINTS (from recon of `src/arbiter/lbd/sources.py`)
- **as-of-T co-mention is feasible.** `europepmc_count(query)` → `hitCount`; `cooccur_count` just builds
  `(A) AND (B)`. Add a date ceiling clause — Europe PMC supports `FIRST_PDATE:[1000-01-01 TO {T}]` (verify
  exact field/format in the spike). New fn `cooccur_count_asof(a, b, cutoff)`; no pipeline redesign.
- **CONSTRAINT — Open Targets `ac_known` is current-only** (no as-of-T API). It must be **dropped** from the
  time-sliced variant (its current value would exclude exactly the links that later became known — the
  positives). Novelty as-of-T is defined by **as-of-T literature** only. State this scoping in the paper.
- **CONSTRAINT — the experimental substrate is not time-sliced** (there is one Zhu 2025 dataset). Honest
  framing: "literature-time-sliced eval against a fixed contemporary experimental substrate" — it measures
  whether *data-grounding predicts future literature*, which is precisely the LBD thesis. Flag explicitly.

## Two load-bearing unknowns → DE-RISK WITH A SPIKE FIRST (do not build blind)
1. **Does Europe PMC date-windowing behave?** Run `cooccur_count` for a few known pairs with vs without the
   `FIRST_PDATE` ceiling; confirm counts drop monotonically as T recedes and the syntax is honored.
2. **Is the post-T positive class big enough to measure?** For candidate cutoffs T ∈ {2016, 2018, 2020}, count
   how many gene→program→disease links go from `ac_lit_asof ≈ 0` to `≥ k` now. If only a handful survive,
   precision/recall are too noisy → **pivot to §5.3b step (2), an external known-true/known-false panel**
   (curated immunology + Open Targets) instead of time-slicing. The spike decides which design is viable.

Spike must run with **live network** (Europe PMC) → it is a Claude/main-thread task, **not** codex-sandbox
(no network). ~1 short session. Output: `docs/spikes/heldout-eval-feasibility_<date>.md` with the positive
counts per T and the go/pivot recommendation.

## Build plan (after the spike says "go")
1. `cooccur_count_asof` + an `ab/bc/ac_lit` as-of-T path in the sweep (small, mechanical). **[HYBRID → CODEX-RESCUE]**
2. Positive-class labeler (as-of-T ≈0 → now ≥k) + the 4 baselines + metric harness. **[CODEX-RESCUE]** (clear spec, cheap to verify)
3. Run at the spike-chosen T; write `docs/manuscript/analysis/heldout_eval.py` + a results JSON; add a §4 results
   subsection + one figure panel. **[CLAUDE]** (synthesis + manuscript prose)
4. Re-run the full pipeline gate; the eval must be deterministic/cache-backed like the other analyses (doctrine §19).

## Honest caveats to carry into the manuscript
- Time-sliced literature recovery measures *prediction of future literature*, a proxy for *biological
  correctness* — not the same thing (a real link may never get written down; a written link may be wrong).
  Report it as decision-quality-vs-literature, not ground-truth-biology.
- `ac_known` dropped as-of-T → the time-sliced funnel differs slightly from the headline funnel; report both.
- Small positive class → wide CIs; report bootstrap CIs, not point estimates alone.

## Delegation summary
- **Spike (de-risk):** live Europe PMC feasibility + positive-class sizing — **Claude/main-thread** (needs network). Do this FIRST.
- **Build:** windowed-count + baselines + metrics — **CODEX-RESCUE** (mechanical, clear spec, cheap to verify).
- **Manuscript integration + figure + reframe:** **CLAUDE**.
Estimated: spike ≈ ½ session; build ≈ 1 session; integration ≈ ½–1 session.
