# Recon — CONFOUNDER cluster (STAT6-cis, cluster-membership, EGR mechanism)
**Claims: B3, B4, B5, R5.** Read-only reconciliation of the CS/in-data experiments against the
manuscript claims AND the contribution-novelty panel (adversarial_claude H2/H3, crosscheck_claude
X2/X3/X5, VERDICT). Step 2 of the claims↔experiments audit. 2026-07-12.

---

## THE CRUX — split the "STAT6 LD-passenger" attack into its three separable channels

The panel's headline attack (adversarial_claude **H2, MAJOR/FATAL**) frames the whole NAB2→eczema
flagship as "**likely a STAT6 LD-passenger**" and rates it undischargeable. That verdict is correct
*only for one of three distinct confounder channels*. The experiments in this cluster discharge the
other two at the levels they can be tested. The panel's own H3 + VERDICT concede this — but the FATAL
H2 headline visually swallows the B3/B4 wins, treating "passenger" as monolithic. **This is exactly
the over-generalization the recon must correct.**

| Channel | Sub-question | Claim | Experiment | Status |
|---|---|---|---|---|
| **(1) Expression-level cis-artifact** | Does NAB2-KD repress STAT6 *mRNA*, so the Th2 readout is really STAT6's? | **B3** | stage3_cis.json (genome-wide DE) | **RULED OUT — ANSWERED** |
| **(2) Cluster-membership / 12q13-locus artifact** | Are NAB2's eczema modules just a 12q13 genomic block? | **B4** | nab2_stat6_confounder_check.py + cis_artifact_check.py | **REJECTED — ANSWERED** |
| **(3) GWAS disease-LABEL LD-inheritance** | Is the atopic-eczema *label itself* an LD shadow of STAT6 at the variant level? | **B5** | none possible in-data | **NO-EXPERIMENT — genuine open GAP (correctly conceded)** |

The precise correction to the panel: H2 is right that channel (3) is undischargeable, but wrong to
let that sink channels (1) and (2). The manuscript already scopes exactly channel (3) as open
(§4.4b/§5.3) and refuses to let the cis-test rescue the disease claim — so it is **honestly scoped,
not overstated** (VERDICT "WHAT DOES NOT CLEAR THE BAR" #3 agrees).

---

## B3 — STAT6 cis-effect ruled out at the expression level → **SUPPORTS (definitively)**

**What was tested.** `docs/nab2_stat6_definitive_check.py` reads the study authors' own deposited
genome-wide DE matrix (`GWCD4i.DE_stats.h5ad`, Biohub Virtual Cells S3, lazy anon read — no download)
and pulls the full NAB2-knockdown row across all genes @Stim8hr. Output = `stage3_cis.json`.

**Key numbers (stage3_cis.json):**
- STAT6 under NAB2-KD: **log2FC +0.087, z 1.20, adj_p 0.788 → NOT significant.**
- NAB2 on-target: **log2FC −3.08, z −16.9, adj_p 7.2e-60** (knockdown genuinely worked — this is not a
  failed-KD "untested").
- STAT6 |log2FC| **rank 5444 of 10282** measured genes (moved *less* than half the genome).
- NAB2-KD significantly moves **302 genes; STAT6 is not among them.**
- Neighbours STAT2 (+0.30, n.s.), NDUFA12 (−0.01, n.s.), SHMT2 (−0.12, n.s.) — no 12q13 cis-spread.
- `ALL_PASS: true` on all 7 asserted checks.

**Classification: SUPPORTS.** The expression-level CRISPRi cis-artifact (a guide targeting NAB2 also
repressing STAT6 and reading out STAT6's Th2 biology) is refuted against the authors' own data.

**vs PANEL: the under-credited win.** adversarial_claude **H3** steelmans this exact test and concedes
"**I cannot honestly attack this as wrong**"; VERDICT lists it under "WHAT SURVIVES EVERY ATTACK"
(#3, "competent and honest … a reusable deposited-data cis-artifact-falsification template"). The
panel *did* credit B3 in H3 — but rated the flagship FATAL in H2 anyway, because H2 attacks channel
(3), not (1). So B3 is answered; the audit correction is to stop the FATAL-H2 headline from being read
as if it also defeated B3.

---

## B4 — eczema modules are genome-wide functional modules, not a 12q13 artifact → **SUPPORTS**

**What was tested.** `docs/nab2_stat6_confounder_check.py` — Check A maps NAB2's *significant*
atopic-eczema clusters' member genes to cytobands (MyGene) and asks whether they concentrate on
12q13; Check B compares NAB2 vs STAT6 Th1/Th2 program vectors + referee disease profiles.
`docs/nab2_cis_artifact_check.py` adds the co-clustering proxy + reproducibility R.

**Key evidence.**
- **Corrected significant clusters = 90 & 100** (FDR<0.05), *derived* not hardcoded — genome-wide
  spread, STAT6 absent from the member lists (the design intent stated in-script).
- **Cis-artifact proxy (co-clustering):** NAB2 and STAT6 do **not** share a perturbation-effect cluster
  (empty intersection) → NAB2-KD does not phenocopy STAT6-KD.
- **Reproducibility (paper's own bar):** NAB2 cross-guide/cross-donor R reported alongside STAT6; NAB2
  is the more reproducible nomination.

**Classification: SUPPORTS** — the cluster-membership / locus-block artifact is rejected. Scope is
exactly right: B4 rejects the *cluster-membership* artifact **only** (it does not touch channel 3).

**vs PANEL.** crosscheck_claude **X2** rates "NAB2 = passenger" as well-supported but "STAT6 is the
*proven fine-mapped* driver" as *mildly OVERSTATED* (Sobczyk 2021 triangulation did not resolve 12q13
to one gene) — i.e. the panel itself softens the passenger claim. B4's genome-wide-module evidence is
consistent with that softening.

---

## B5 — 12q13 LD-inherited disease label cannot be discharged → **NO-EXPERIMENT (genuine gap, correctly foregrounded)**

**Is it testable by any experiment in this cluster? No.** Channel (3) is a *variant-level*
colocalization question (does the atopic-eczema GWAS signal share a causal variant with NAB2
regulation, with materially weaker evidence for STAT6?). None of stage3_cis.json / confounder_check /
cis_artifact_check can answer it — they operate on perturbation-effect and expression data, not
variant-level genetics. It requires external data: a NAB2 CD4⁺ cis-eQTL + colocalization vs the 12q13
AD GWAS (adversarial_claude H2 "what would rebut me"; adversarial_codex finding 2).

**Classification: NO-EXPERIMENT (GAP).** This is **not a defect** — the manuscript explicitly
foregrounds it as undischargeable (§4.4b(iii): the LD-inherited label "we cannot settle," needs
variant-level coloc that itself presupposes a detectable NAB2 cis-eQTL). adversarial_claude concedes
"the manuscript itself lists [it] as *future* work (§5.3b)." → Step 3 `NEW_EXPERIMENTS.md` candidate
(external genetics; CS-native only if an eQTL/coloc source can be wired in).

---

## R5 — NAB2 is a distinct regulator, not a swappable EGR corepressor → **PARTIAL (supports, but evidence-thin: no captured output)**

**What was tested.** `docs/nab2_egr_mechanism_check.py` (+ raw-working-trail twin) compares NAB2 vs
NAB1, EGR1, EGR2, EGR3 across effect size, downstream count, off-target flag, Th1/Th2 program shift
(both contrasts), and referee disease profiles — the logic being that if NAB2-KD acted purely by
de-repressing EGR, its phenotype would mirror the EGR/NAB module. Distinct program/disease profiles
argue NAB2 is its own regulator (NAB1 paralog opposition per the Collins-2008 Egr-1/NAB2 vs
Egr-2/Egr-3 axis).

**Classification: PARTIAL.** The script exercises the distinctness test, and crosscheck_claude **X3**
supplies the corroborating literature — EGR2/EGR3 are established T-cell regulators, and the 2008
"**Opposing** regulation of T-cell function by **Egr-1/NAB2 and Egr-2/Egr-3**" paper directly names the
paralog-opposition R5 leans on. BUT: **there is no captured output artifact/JSON** for the EGR check
(unlike stage3_cis.json for B3), and no numeric receipt for R5 in the ledger — so R5 is materially
thinner than B3/B4. It is a print-only script whose result is not frozen. **Flag for Step 3:** capture
an `egr_mechanism.json` so R5 has a receipt, or downgrade R5's language to match the evidence actually
frozen.

**vs PANEL.** adversarial_claude notes "NAB2 as a Th2 regulator is a short step along the already-known
EGR2/NAB2 axis — family-adjacency stacked on locus-adjacency," and crosscheck_claude X3 REFINEs
"novel-for-NAB2" to the defensible "absent from the Th1/Th2 *polarization* literature." R5's "distinct,
not swappable" framing is compatible with (and sharpened by) that refine — but the panel is right that
the EGR-adjacency lowers the surprise, so R5 should be stated as *distinctness within a known family*,
not de-novo novelty.

---

## HONESTY FLAGS

1. **The hardcoded-[74,90] wrong-cluster QC bug is REAL — and was self-caught (net positive).**
   `docs/provenance/raw-working-trail/stat6_confounder_checks.py` line 34 hardcodes `for cl in [74, 90]`
   — but cluster **74 is NON-significant** for atopic eczema; the actually-significant clusters are
   **90 & 100**. Running the locus test on a non-significant cluster is a genuine defect. **It was
   caught and fixed by the cross-model replication** (the "74/90 → 90/100" catch, adversarial_claude
   H3 + VERDICT): the corrected `docs/nab2_stat6_confounder_check.py` (lines 32-37) now *derives*
   `SIG_CLUSTERS` from `p_adj_fdr < 0.05` and carries an in-code comment documenting the prior bug.
   **B4 rests on the corrected 90/100, not the buggy 74.** So this is a defect that the honesty
   apparatus surfaced rather than buried — it supports M5/M7, but the manuscript/ledger must never cite
   the raw-working-trail script as the B4 evidence (only the corrected one).

2. **"1.9 kb" vs corrected "~43 kb" — stale distance in the provenance headers.** The NAB2↔STAT6
   distance is stated as **"1.9 kb"** in the *header comments* of `nab2_stat6_definitive_check.py`
   (line 8), `nab2_cis_artifact_check.py` (lines 5-6), and throughout `source_paper_read_eczema`
   (p78/p97, dated 2026-07-08). The panel and the corrected manuscript use **"~43 kb"**
   (adversarial_claude H2/H3, adversarial_codex finding 10). The 1.9 kb figure is wrong/stale.
   **Mitigating scope:** the distance lives only in motivational *comments* and feeds only the
   *geometry* argument ("CRISPRi spread over N kb is unlikely"). The load-bearing B3 result
   (stage3_cis.json) contains **no distance number** — it is the empirical DE null (STAT6 +0.087,
   p0.79), which is unaffected. VERDICT confirms "the paper leans on the empirical null, not geometry —
   correctly." So the stale 1.9 kb weakens only a secondary argument; still worth a cleanup pass so the
   provenance headers match the manuscript's ~43 kb.

3. **crosscheck X5 caveat on the geometry argument.** Even at 43 kb, KRAB/KAP1 can repress long-range
   (Lensch 2022 shows spread crossing insulators); "43 kb is safe" would be OVERSTATED. The manuscript's
   reliance on the empirical null rather than the geometry is the correct posture — do not let any
   redraft promote "43 kb → safe."

---

## NET FOR THE RECONCILIATION LEDGER
- **B3 SUPPORTS**, **B4 SUPPORTS** — two answered confounder channels the FATAL-H2 headline
  under-credits. Surface both as panel-answering wins (audit priority (a)).
- **B5 NO-EXPERIMENT** — genuine, honestly-conceded gap → Step 3 external-genetics experiment.
- **R5 PARTIAL** — distinctness tested + lit-corroborated, but no frozen receipt; capture output or
  soften language.
- **Two honesty flags:** the self-caught wrong-cluster QC (cite only the corrected script) and the
  stale 1.9 kb → ~43 kb header drift (cosmetic to B3's result, real for provenance cleanliness).
