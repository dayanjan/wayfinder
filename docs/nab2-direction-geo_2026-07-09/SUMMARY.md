# NAB2 skin-direction — orthogonal GEO mining: RESULT = NO-CALL (2026-07-09)

Executed the SHIP-approved plan (`docs/plans/nab2-direction-geo-mining-plan_2026-07-09.md`, v3; hardened by a
3-round codex-debate with live GEO verification, `docs/reviews/codex-debate_nab2-direction_2026-07-09/`). Scope
this run: the 4 voting arms' PRIMARY bulk/array datasets + the STAT6 direct test. scRNA ARM-D + backups deferred
(ARM-D now being run next to resolve the composition confound below). Full per-arm numbers: `report.md` +
`per_arm.json`; faithful analysis code: `executed_code.py`. Raw GEO downloads under `downloads/` are provenance,
NOT committed.

## The call: **NO-CALL**
| Arm | Dataset | NAB2 | Arm call |
|---|---|---|---|
| A — skin association | GSE330551 | **DOWN in lesional** (log2FC −0.32, FDR 0.002); anti-correlates with Th2 (ρ −0.34, p 3.6e-6) | DOWN |
| T — CD4 T-cell (on-point) | GSE32959 | 2 probes weak + **sign-discordant** (+0.15 ns / −0.05 ns) | AMBIGUOUS |
| B — cytokine causation | GSE292848 | IL-4/13 do **not** induce NAB2 (−0.11, FDR 0.73) | NO-CALL |
| C — dupilumab reversal | GSE130588 | probes weak/discordant, both ns | AMBIGUOUS |
| STAT6 test | GSE17851 | NAB2's IL-4 response is **not** STAT6-dependent | — |

Decision rule (≥2 concordant voting arms, cytokine-arm privileged) is not met → **NO-CALL**.

## Interpretation (calibrated)
1. **The topical NAB2-KNOCKDOWN hypothesis is not supported — and may be backwards.** The one significant arm
   (A) shows NAB2 **lower** in lesional skin and **anti-correlated** with Th2 activity, and the cytokine arm (B)
   shows IL-4/13 do not induce it. That pattern is more consistent with NAB2 being a **Th2 brake** (induced
   negative feedback) than a Th2 driver — i.e. you might want *more* NAB2, not less. Soft (single significant arm).
2. **Does NOT refute the original finding.** The finding = "NAB2 *knockdown reshapes* the Th1/Th2 program in CD4
   T cells" (a real perturbation effect). GEO answers the *different* question of therapeutic direction in skin,
   and returns NO-CALL. The two are not in conflict.
3. **The on-point T-cell arm (T) is ambiguous** — an independent CD4 T-cell Th2/Th1 dataset neither confirms nor
   cleanly denies the Perturb-seq's Th2-association. Genuinely unresolved.
4. **Ceiling (stated up front):** expression tracks direction of association, not effector-vs-brake. Only
   perturbation (the original Perturb-seq, or a purpose-built assay) separates them.

## The load-bearing caveat → why ARM-D is being run next
ARM A is **bulk** skin: NAB2-down-in-lesional could be **cell composition** (immune infiltrate diluting
keratinocytes) rather than per-cell regulation. **scRNA ARM-D (GSE204762)** pseudobulks NAB2 by cell type
(T cells, keratinocytes, …) in lesional vs non-lesional vs healthy — the one analysis that can turn NO-CALL into
a real call by telling us whether the bulk signal is a genuine per-cell direction or an artifact of mixing.

## Verification status
Codex's ARM-A grouping/sign logic was reviewed (correct: baseline lesional-vs-non-lesional, NAB2 by symbol,
log2-CPM); ARM A's two endpoints (lesional log2FC and Th2 ρ) are mutually concordant (both negative), which
corroborates the DOWN direction internally. The forthcoming reproducibility notebook re-runs the pipeline for a
reader. A full byte-level independent recompute of the per-BAM RNA-seq file was not performed (low value given
the robust NO-CALL); it can be added if the direction question is revisited.
