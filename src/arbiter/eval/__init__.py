"""`arbiter.eval` — the G1 time-sliced held-out evaluation harness (fresh, new-work-only).

Measures whether the LBD+referee method (Wayfinder) ranks *future-established*
gene -> Th1/Th2 -> disease links above baselines, within a literature-novel-as-of-T frame.
This is the manuscript's publish gate: it converts the method from *demonstrated* to *measured*.

Spec of record: docs/plans/heldout-eval-implementation-plan_2026-07-12.md (v3, codex-debate-converged).
Modules:
  fetch           - bounded-concurrent, cached, resumable Europe PMC count fetcher.
  enumerate_frame - build the full A x C frame, label positives, write the count manifest.
  rankers         - the 6 frozen total-orders over the frame (Wayfinder + 5 baselines).
  metrics         - precision@k / MAP / recall + the two co-primary contrasts + clustered bootstrap CIs.
  run_eval        - orchestrator CLI.
"""
