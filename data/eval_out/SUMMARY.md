# G1 held-out eval — SUMMARY (T=2016, k=5, novel<= 1)

- Frame size: **22437**  · positives: **5570** (base rate 24.8%)
- Primary metric: precision@20
- Retrieval date: 2026-07-12  · manifest sha256 rows: cce1bb3ccc650fe2…

## Per-method precision (higher = better)
| method | p@5 | p@10 | p@20 | p@50 | MAP |
|---|---|---|---|---|---|
| wayfinder | 0.8 | 0.5 | 0.35 | 0.4 | 0.2869 |
| disease_hop_only | 0.4 | 0.4 | 0.5 | 0.38 | 0.2575 |
| lit_rarity | 0.4 | 0.2 | 0.15 | 0.1 | 0.1801 |
| effect | 0.0 | 0.0 | 0.15 | 0.26 | 0.2658 |
| enrichment_continuous | 0.4 | 0.6 | 0.45 | 0.38 | 0.2576 |
| random | 0.4 | 0.4 | 0.25 | 0.24 | 0.2465 |

## Co-primary contrasts (paired prec@20 diff, two-way-clustered bootstrap 95% CI)
- **C_broad** (Wayfinder − lit-rarity): +0.200 [-0.200, +0.650]  → NULL
- **C_mech** (Wayfinder − disease-hop-only): -0.150 [-0.350, +0.300]  → NULL

### Pre-registered joint outcome: **broad_null**

_A CI spanning 0 is reported straight; no metric/cutoff was promoted post-hoc._