# NAB2 Direction GEO Mining (2026-07-09)

Scope executed: primary bulk/array voting arms A/T/B/C plus the STAT6 direct test. scRNA ARM-D and all backup datasets were deferred.

Ceiling: these data establish direction of association and perturbation consistency where available; tracks does not mean effector.

## Per-arm results

| Arm | Dataset | Contrast | NAB2 result | Interpreted direction | Detection-filtered type-2 rho | STAT6 | Arm call |
|---|---|---|---|---|---|---|---|
| A | GSE330551 | baseline Lesion vs Non-Lesion, patient fixed effect; sensitivity Lesion vs Control | NAB2 log2FC=-0.323, FDR=0.00178 | NAB2 lower in the high/type-2 or post-treatment contrast | rho=-0.343, p=3.56e-06, n=174 | log2FC=-0.142, FDR=0.0313 | DOWN |
| T | GSE32959 | CD4 Th2(IL-4) vs Th1(IL-12), 12-72h, adjusted for time and biological replicate | 212803_at log2FC=0.152, FDR=0.337; 216017_s_at log2FC=-0.051, FDR=0.896 | weak or sign-discordant | 212803_at rho=0.422; 216017_s_at rho=-0.009 | log2FC=-0.226, FDR=0.617 | AMBIGUOUS |
| B | GSE292848 | NativeSkin cytokine treatment vs paired control, donor fixed effect | ENSG00000166886 log2FC=-0.109, FDR=0.73 | did not pass gate | rho=-0.098, p=0.64, n=25 | log2FC=0.030, FDR=0.736 | NO-CALL |
| C | GSE130588 | Dupilumab Week16 reversal beyond placebo, adjusted for time, lesion, and subject | 212803_at log2FC=0.095, FDR=0.989; 216017_s_at log2FC=-0.000, FDR=1 | weak or sign-discordant | 212803_at rho=-0.111; 216017_s_at rho=0.023 | log2FC=0.016, FDR=1 | AMBIGUOUS |

Type-2 rho shown in the table is the detection-filtered pre-specified score. `per_arm.json` also records full-score and chemokine/receptor-only sensitivity rhos plus the genes retained/dropped for each arm.


## STAT6 direct test

- Control_Act+IL-4 vs Control_Act: NAB2 log2FC=-0.089, FDR=0.821, direction=NO-CALL
- STAT6_Act+IL-4 vs STAT6_Act: NAB2 log2FC=-0.020, FDR=0.968, direction=NO-CALL
- STAT6-siRNA interaction: log2FC=0.069, FDR=0.967; negative values mean IL-4 induction is reduced under STAT6 siRNA.

## Triangulated call

Final CALL: **NO-CALL**.
Voting arms: {'A': 'DOWN', 'T': 'AMBIGUOUS', 'B': 'NO-CALL', 'C': 'AMBIGUOUS'}.
ARM T vs skin agreement: not assessable because ARM T did not yield a usable post-gate direction.
Calibration: Expression tracks direction of association, not whether NAB2 is an effector or feedback brake.

## Caveats

- ARM B is ex vivo NativeSkin cytokine perturbation, not isolated CD4 T cells.
- ARM A is bulk skin RNA-seq; without ARM-D in this run, cell-compartment attribution remains deferred.
- Array arms report both plan-specified NAB2 probes; sign discordance would make an arm AMBIGUOUS.
- RNA-seq contrasts used log2 CPM normalization and fixed-effect linear models; this is limma-voom-style in spirit but not empirical-Bayes moderated limma.
- STAT6 adjustment/sensitivity is reported as context because STAT6 can be a mediator of IL-4/IL-13 signaling.

## Deferred

- scRNA ARM-D (GSE204762) deferred
- all backup datasets deferred
