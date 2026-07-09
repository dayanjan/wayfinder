# Round 3 Codex Final — NAB2 Direction Plan v3

## Convergence Confirmations

1. **ARM T resolved.** v3 now adds an explicit CD4 T-cell association arm with GSE32959 primary, GSE60678 backup,
   and GSE17851 as the STAT6-dependence test. This closes the Round-2 concern that skin/epithelial evidence could
   be over-transferred to the T-cell mechanistic claim.

2. **Intra-arm conflict rule resolved.** v3 §1.2 now defines primary vs secondary endpoints, requires the primary
   endpoint to pass, marks sign-discordant primary/secondary or array probes as **AMBIGUOUS**, and treats backup
   absence as sensitivity-only rather than primary failure. This is executable and conservative.

3. **STAT6 test resolved.** v3 §3.6 makes the direct GSE17851 test primary: compare NAB2's IL-4 response under
   control siRNA vs STAT6 siRNA. The STAT6-adjusted regression is correctly demoted to sensitivity context with
   the mediator/over-control caveat.

## Live GEO Re-Verification, 2026-07-09

**GSE17851 — PASS for STAT6-dependence test.** Live series matrix from GEO:
`https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17851/matrix/GSE17851_series_matrix.txt.gz`.
Header confirms: "Genome-wide analysis of STAT6 target genes in IL-4 treated human cord blood CD4+ cells"; RNAi
STAT6 knockdown; 54 samples; 3 biological replicates; control siRNA and STAT6 siRNA; activated anti-CD3/anti-CD28
with and without IL-4 at 12/24/48/72h. Sample titles/descriptions explicitly enumerate
`STAT6_Act`, `STAT6_Act+IL-4`, `Control_Act`, `Control_Act+IL-4` for reps 1-3. This is the needed factorial.
Streaming GPL6102 SOFT scan:
`https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL6nnn/GPL6102/soft/GPL6102_family.soft.gz` confirms
`ILMN_1663554 = NAB2`, Entrez `4665`, RefSeq `NM_005967.3`.

**GSE60678 — PASS for adult donor-paired Th1/Th2 backup.** Live GEO page and series matrix confirm GPL14550,
48 samples, naive CD4+ T cells from four healthy buffy-coat donors, polarized Th1 with IL-12/IL-2/anti-IL-4 and
Th2 with IL-4/IL-2/anti-IL-12/anti-IFN-g, with S1-S4 donor-coded titles across 6h/24h/3d/6d/8d. This is usable
as a donor-paired mixed/fixed-effect backup; model donor and time, and do not treat timepoints as independent.
Streaming GPL14550 SOFT scan:
`https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL14nnn/GPL14550/soft/GPL14550_family.soft.gz` confirms
`A_33_P3248794 = NAB2`, Entrez `4665`, RefSeq `NM_005967`, Ensembl `ENST00000357680`, cytoband `12q13.3`.

Note: local PowerShell/curl TLS failed; live verification was completed through Node fetch/web GEO. NCBI API key
was not needed and `.env` was not read.

## Blocking Gaps

No remaining P0/P1 blockers. A competent analyst can execute v3 end-to-end without re-deriving the study design,
dataset roles, row/probe resolution rules, conflict handling, type-2 detection gates, cell-composition guard, or
STAT6 sensitivity logic.

Cosmetic only: v3 could optionally name the exact ARM T primary contrast/time model in one sentence, but the current
text is sufficient because §1 and §3 already define the endpoints, covariates, and pairing requirement.

## Verdict

**SHIP.** Execute v3 as-is.
