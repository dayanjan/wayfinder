# Timing Calibration Probe — Receipt

**Probe:** 74 live calls (50 ab + 12 bc Europe PMC, 12 Open Targets) · wall 95.4s · 0.34s politeness sleep between calls · no cache · CPU-only.

## Per-type network latency (seconds; request time only, excludes sleep)
| type | n | mean | median | p95 | max |
|------|---|------|--------|-----|-----|
| ab (gene×program) | 50 | 0.7033 | 0.6025 | 1.2905 | 1.8782 |
| bc (program×disease) | 12 | 1.1886 | 1.1443 | 1.6634 | 1.9037 |
| ot (Open Targets) | 12 | 1.729 | 1.9513 | 2.0579 | 2.0584 |
| **overall** | 74 | 0.9483 | 0.7048 | 2.0255 | 2.0584 |

**Effective per-call wall time** (net + 0.34s sleep + overhead) = **1.290s/call**

## Full-sweep extrapolation (~4020 calls: 3935 ab + 12 bc + 43 ac_lit + 30 OT)
- (a) wall-based  = 4020 × 1.290s = **86.4 min**
- (b) median_net + sleep = 4020 × (0.7048 + 0.34)s = **70.0 min**
- (b′) ab-median + sleep (ab-dominant) = 4020 × (0.6025 + 0.34)s = **63.1 min**

## Throttle check
- HTTP 429s: none · exceptions/timeouts: none · retries: 0
- p95 (2.026s) vs 3×median (2.115s): within — soft-throttle not flagged
- **VERDICT: THROTTLE_FREE** — safe to run the full sweep
