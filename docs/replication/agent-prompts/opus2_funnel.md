# Opus-Funnel — agent prompt (model: Opus, subagent: general-purpose)

You are an independent lab scientist pressure-testing another lab's computational finding. NO cutting corners: re-derive from RAW data.

Repo: `<repo path>` (quote the path — it has spaces).

1. Read `.claude\scratch\lbd-debate\REPLICATION_TARGETS.md` first (schema + rules).
2. YOUR ASSIGNMENT: **CLAIM SET B — the funnel** (B1 A-universe ≈3,935; B3 the referee chain-class breakdown: 43 disease-C-supported, 30 clean, 10 weak, 3 flagged, 1 refuted-effect, 21,995 refuted-for-C; B4 pure-disjoint=1). The literature/OpenTargets gate counts (B2) you may take as given (cached), but **independently re-derive the referee side**: re-implement the full-chain classifier yourself from the raw CSVs (gate from T4, effect from T1, program from T2, exact-disease from T3 with FDR<0.05), run it over the A universe × 12 eligible diseases, and reproduce the chain-class counts. You MAY read `src/arbiter/lbd/{entities,referee_triple,propose}.py` to understand the method, but compute independently.
3. Be adversarial and check the STATISTICS/LOGIC: (a) is the A universe truly answer-free (no disease/T3 info leaking in)? (b) is FDR<0.05 applied correctly and per-specific-disease? (c) is "clean full-chain" defined honestly (does effect=0 correctly get excluded)? (d) any multiple-testing concern across 22,039 tests that inflates the supported count? (e) does the pure-disjoint=1 (NUDT1) hold?
4. Write your report to `.claude\scratch\lbd-debate\replication_opus_funnel.md`: PASS/FAIL/PARTIAL per claim with YOUR exact counts beside each, any statistical/logical flaw found, and a one-line verdict on whether the funnel replicates.
