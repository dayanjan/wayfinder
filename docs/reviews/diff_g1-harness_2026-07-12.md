# Codex review — G1 held-out-eval harness (2026-07-12)

Read-only `codex review --commit HEAD` on commit `8858d67` (the direct-written harness). Codex's WRITE
sandbox was broken (see build log T4), but the READ-ONLY review path works — reclaiming the cross-model
check the blocked codex-rescue would have given. Raw log: `.claude/scratch/g1/codex-review.log` (trimmed here).

## Findings (all ACCEPTED + FIXED in commit following 8858d67)

- **[P1] Bootstrap must resample UNIQUE clusters** — `run_eval.py:23` + `metrics.clustered_bootstrap_diff`.
  I passed one gene/disease entry *per pair* (duplicated ~12x / ~thousands x) into the two-way cluster
  bootstrap, so `rng.choices` weighted clusters by pair-count and drew `len(frame_rows)` times → **spuriously
  narrow, incorrectly-weighted CIs** on the load-bearing co-primary inference. **Fix:** dedupe to unique
  gene/disease clusters inside `clustered_bootstrap_diff` (defensive) AND pass unique lists from `run_eval`
  (each cluster drawn n_clusters times; a pair's multiplicity = count(gene)*count(disease)). Regression test
  added (`test_bootstrap_dedups_perpair_lists_and_shows_separation`).

- **[P1] Failed `now`-fetch silently classed as negative** — `enumerate_frame.py`. A fetch failure is
  *unknown*, not a negative; labelling it negative biases the positive set. **Fix:** drop now-failed pairs
  from the labelled frame, record `excluded_now_fetch_fail` in the manifest header. (No-op at fail=0, but
  correct + honest.)

- **[P2] Membership sets rebuilt per row** — `enumerate_frame.py` built `set(frame)`/`set(positives)` inside
  the 47,220-row comprehension (O(n²)). **Fix:** build `frame_set`/`pos_set` once before the loop.

## Verdict
No correctness bug in the ranker definitions, the as-of-T query construction, or the metric formulae; the one
load-bearing statistical bug (P1 bootstrap) was caught and fixed before any result was computed. Tests: 11/11
green after fixes.
