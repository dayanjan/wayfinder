# Live LBD micro-sweep — generated candidate questions

**These are GENERATED CANDIDATE QUESTIONS to be refereed next — NOT findings.**
Each is of the form: *"Does gene A regulate the Th1/Th2 program (B) and thereby
link to autoimmune disease C?"* surfaced by the Swanson ABC "disconnected but
bridgeable" heuristic. All signals below come from LIVE HTTP calls made this run
(Europe PMC + Open Targets); nothing is cached.

## Top ranked candidate questions (eligible pairs)
| rank | A gene | C disease | ab | bc | ac_lit | ac_known | effect | score |
|---|---|---|---|---|---|---|---|---|
| 1 | CD3E | atopic eczema | 3521 | 1095 | 21 | 0.0022 | 5710 | -2.8233 |
| 2 | VAV1 | atopic eczema | 855 | 1095 | 8 | 0.0 | 4897 | -3.7882 |
| 3 | CD3D | atopic eczema | 1629 | 1095 | 12 | 0.0 | 4983 | -3.9445 |
| 4 | LAT | atopic eczema | 1785 | 1095 | 53 | 0.0 | 5535 | -4.0927 |
| 5 | CD3G | atopic eczema | 749 | 1095 | 14 | 0.0037 | 4965 | -4.1426 |
| 6 | ZAP70 | atopic eczema | 1832 | 1095 | 19 | 0.0028 | 5021 | -4.2913 |
| 7 | CD3E | asthma | 3521 | 30473 | 1069 | 0.0211 | 5710 | -4.4977 |
| 8 | CD3G | type 1 diabetes mellitus | 749 | 1716 | 29 | 0.0169 | 4965 | -4.5694 |
| 9 | VAV1 | type 1 diabetes mellitus | 855 | 1716 | 35 | 0.0 | 4897 | -4.8685 |
| 10 | CD3D | type 1 diabetes mellitus | 1629 | 1716 | 46 | 0.0175 | 4983 | -4.9763 |

_ab_ = gene×program co-mentions; _bc_ = program×disease co-mentions;
_ac_lit_ = direct gene×disease co-mentions (low = under-explored);
_ac_known_ = Open Targets curated association score (0 = no curated link);
_effect_ = n_downstream from perturbation data.

## Liveness proof (exact query strings + returned counts this run)
- **first ab query**: `("TADA2B") AND ("Th2 cells" OR "T helper 2" OR "type 2 immunity" OR "Th2 differentiation" OR "Th1 cells" OR "T helper 1" OR "type 1 immunity" OR "Th1 differentiation" OR "Th1/Th2 polarization" OR "CD4 T cell polarization" OR "T helper cell differentiation")` → hitCount = **7**
- **first bc query**: `("Th2 cells" OR "T helper 2" OR "type 2 immunity" OR "Th2 differentiation" OR "Th1 cells" OR "T helper 1" OR "type 1 immunity" OR "Th1 differentiation" OR "Th1/Th2 polarization" OR "CD4 T cell polarization" OR "T helper cell differentiation") AND ("asthma")` → hitCount = **30473**
- **first ac_lit query**: `("TADA2B") AND ("asthma")` → hitCount = **82**
- **Open Targets disease**: `MONDO_0004979` → rows returned = **3000**

## Method (as executed)
- A = top 12 KD-gated (signif_knockdown @Stim8hr) regulators by n_downstream effect.
- Gate (eligible): ab ≥ median(ab over 12 genes) AND bc ≥ 3 AND ac_known ≤ 0.1.
- Score = min(z(ab), z(bc)) + z(effect) − log1p(ac_lit) − 3·ac_known.
- z(x) = (log1p(x) − mean(log1p)) / std(log1p), guarded to 0 when std==0.
- n_eligible = 22 of 48 gene×disease pairs.

**Calibrated summary:** 22 under-explored A→(Th1/Th2)→disease pairs were *generated* as candidate questions (strong data effect + literature-bridged, no curated direct link); they are candidates for referee review, not discoveries.
