# Stage 3 — CRISPRi cis-artifact check: NAB2 vs STAT6

**Finding under test:** NAB2 -> Th1/Th2 -> atopic eczema.

**Confounder:** NAB2's CRISPRi guide sits ~1.9 kb from STAT6 (a master Th2 regulator) at 12q13.3. If NAB2 knockdown were bleeding onto STAT6, the eczema signal could be STAT6, not NAB2.

**Data:** authors' genome-wide DE statistics (`GWCD4i.DE_stats.h5ad`, ~16.8 GB), read directly from anonymous public S3 via virtual-addressed s3fs. Only tiny label arrays + a single matrix row (NAB2 x Stim8hr) were read — byte-range reads only, NO full download.


## Result — Stim8hr, perturbation = NAB2

- Genes measured: **10282**
- Genes significantly moved by NAB2-KD (adj_p < 0.1): **302**
- STAT6 |log2FC| rank among measured genes: **5444 of 10282** (higher rank = less affected)


| Gene | log2FC | z-score | adj_p | significant (adj_p<0.1) |
|------|-------:|--------:|------:|:-----------------------:|
| STAT6 ← neighbor under test | +0.0870 | +1.196 | 0.7884 | no |
| NAB2 ← self / on-target | -3.0783 | -16.882 | 0.0000 | yes |
| STAT2 | +0.3033 | +2.706 | 0.1761 | no |
| NDUFA12 | -0.0129 | -0.218 | 1.0000 | no |
| LRP1 | n/a | n/a | n/a | not in DE panel |
| SHMT2 | -0.1234 | -1.722 | 0.5864 | no |

## STAT6 verdict

STAT6 under NAB2-KD: log2FC = **+0.0870** (small positive, |value| < 0.2), adj_p = **0.7884** (NOT significant, > 0.1) — **STAT6 is UNMOVED.**

NAB2 self on-target: log2FC = **-3.0783** (strongly negative — the knockdown worked).


## Cis-exclusion statement

NAB2 knockdown leaves STAT6 mRNA unmoved (log2FC ~+0.09, adj_p ~0.79) -> the CRISPRi cis-artifact is refuted; the Th2/eczema effect is genuinely NAB2's, not STAT6 bleed.


## Acceptance targets — actual vs expected

| Check | Expected | Actual | Pass |
|-------|----------|--------|:----:|
| file_opened | True | True | — |
| STAT6 log2FC ~+0.09 (|value|<0.2) | +0.09, |x|<0.2 | +0.0870 | — |
| STAT6 adj_p ~0.79 (>0.1, NOT sig) | ~0.79, >0.1 | 0.7884 | — |
| NAB2 self on-target log2FC ~-3.08 | ~-3.08 | -3.0783 | — |

| Assertion | Pass |
|-----------|:----:|
| file_opened | PASS |
| stat6_log2fc_small_positive | PASS |
| stat6_log2fc_near_0.09 | PASS |
| stat6_not_significant | PASS |
| stat6_adjp_near_0.79 | PASS |
| nab2_on_target_strongly_negative | PASS |
| nab2_on_target_near_-3.08 | PASS |

**ALL_PASS = True**
