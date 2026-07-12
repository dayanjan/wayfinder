# Recon — CROSS-MODEL REPLICATION cluster (M7, B1, B3, B4, R5)

**Step 2 recon (2026-07-12).** What the independent/adversarial replication agents *actually did and
found*, classified against the manuscript CLAIM (SUPPORTS / REFUTES / COMPLICATES / PARTIAL) and against
the panel critique (`docs/reviews/contribution-novelty-audit_2026-07-12/`). This cluster is where the
sharpest self-corrections live — the manuscript MUST reflect the honesty flags below.

## Primary artifacts read
- `docs/replication_report_2026-07-08.md` (consolidated verdict)
- `docs/replication/README.md` (method + issue-log §6)
- `docs/replication/agent-reports/opus_receipt.md` (Claim A — NAB2 receipt, A1–A4 + spot-checks)
- `docs/replication/agent-reports/opus_funnel.md` (Claim B — funnel classifier, from scratch)
- `docs/replication/agent-reports/opus_confounder.md` (Claim C STAT6 + D EGR, adversarial) — verbatim copy at `docs/provenance/raw-working-trail/replication_opus_confounder.md`
- `docs/replication/agent-reports/codex1_code.md` (pipeline-code correctness audit)
- `docs/replication/agent-reports/codex2_reimpl.md` (clean-room re-implementation)
- `docs/replication/agent-prompts/opus3_confounder.md` (adversarial mandate for the skeptic)
- Panel: `verify_th2.md` (B1), `verify_eczema.md` (B2–B5, incl. B3 cis + B4), `VERDICT.md` (M7 rating)

## The team (what M7 actually is)
5-member simulated independent lab, **cross-vendor** (3 Opus + 2 Codex), engineered-independent 4 ways
(cross-model / clean-room re-impl importing zero pipeline code / adversarial mandate / blind-to-each-other
parallel). Two clean-room re-impls (Opus-Funnel `indep_funnel.py`, Codex-2). One pure adversarial skeptic
(Opus-Confounder, told a *refuted* claim with evidence is the most valuable output).

---

## M7 — "Cross-family adversarial clean-room replication lab reproduced every headline number and caught real errors"

**What the agents did + key results.** Unanimous 5/5 PASS. Reproduced *to the unit* from independent raw-CSV
re-derivation: NAB2 receipt (2/2 KD guides, effect −16.88, n_down 301, Ota z +7.71/adj-p 1.95e-13, Höllbacher
n.s., eczema OR 3.90/3.43); the full funnel 3,935 → 22,039 → 43 (30 clean / 10 weak / 3 flagged / 1
refuted-effect / 21,995 refuted-for-C); pure-disjoint = 1 (NUDT1×T1D). Two independent re-impls (Opus-Funnel,
Codex-1) hit the class counts exactly; Codex-2's clean-room reproduced A=3,935 + the clean/weak/flagged
*proportions* (0.76/0.21/0.03). Two non-NAB2 spot-checks (BHLHE40, UFM1) also held → not cherry-picked.
Codex-1 confirmed at the code level: A universe never opens the T3 disease table (answer-free), and
`answer=="supported"` requires the full chain with `n_downstream>0`.

**Classification vs CLAIM: SUPPORTS — with two precision caveats the manuscript must carry.**
1. **"Reproduced EVERY headline number" is slightly self-contradictory with "caught real errors."** Two
   published headline items were **CORRECTED, not reproduced**: the eczema cluster IDs (74→90/100) and the
   "~8×" magnitude (→ ~3× on z). Accurate phrasing: *"reproduced every headline number to the unit **except
   two it corrected.**"*
2. **Codex-2 reproduced proportions, not the gated absolute total** (it ran A×diseases *un-gated*, so its
   absolute counts — supported 411, clean 312 — are larger than the gated 43/30; the match is A-universe size
   + NAB2 result + chain-class proportions).

**Classification vs PANEL: M7 answers the "just a code artifact" critique but is not a scientific contribution.**
The panel (VERDICT §"WHAT DOES NOT CLEAR THE BAR" #5) rates M5/M6/**M7** as *"well-executed engineering/QA,
each with an active prior-art field, not standalone novel science… must NOT be promoted to 'contributions.'"*
So M7's role is *evidence of computational robustness* (which it delivers convincingly) — not a novelty claim.
The manuscript's own scope ("computational robustness, not biological validity") is exactly right and must stay.

**HONESTY FLAG (M7):** the lab's real value is the *self-correction*, not the green checkmark — the "every
number reproduced" framing under-sells the errors caught. Foreground the catches; they are the credibility.

---

## B1 — "NAB2 is a Th1/Th2 (Th2) regulator" (re-derived regulatory role)

**What the agents did + key results.** Opus-Receipt re-derived the receipt hop-by-hop from raw CSVs: A1 gate
2/2, A2 effect −16.88 / n_down 301 / offtarget False, A3 program Ota z +7.71 (adj-p 1.95e-13, sig; Höllbacher
n.s.), A4 eczema clusters OR 3.90/3.43 — all **exact**. Condition-of-record choice (Stim8hr) justified: Rest
and Stim48hr are weaker (n_down 1 and 6). The Th1/Th2-regulator receipt is fully reproducible.

**Classification vs CLAIM: SUPPORTS (exact reproduction).** The regulatory receipt for NAB2 replicates cleanly.

**Classification vs PANEL: SUPPORTS + adjacency caveat (panel `verify_th2.md`, VERDICT §"kernel" #2).** Panel
independently confirms NAB2→Th1/Th2 *polarization* is **genuinely absent from the surfaced literature** (15
queries, 0 hits) — NOVEL-for-NAB2. BUT panel flags it is **plausible-by-adjacency, not bolt-from-the-blue**:
NAB2 corepresses EGR2/3, and Singh 2017 (10.4049/jimmunol.1602010) shows EGR2/3 directly gate Th1 vs Th2/Th17
by blocking T-bet. Panel recommendation the manuscript must absorb: state "absent from the Th1/Th2
**polarization** literature" (not "novel-for-NAB2" full-stop, since NAB2 has a documented T-cell role), and
**cite the EGR2/3 axis** — this hardens honesty *and* strengthens plausibility.

**HONESTY FLAG (B1):** the A3 direction wording is a live trap. Referee labels NAB2 "Th1-associated" because
it reports the *KD-program* direction, but the gene's own Th2_vs_Th1 log_fc is **positive (+0.63) → NAB2 is
Th2-biased**. Say "KD shifts the program toward Th1" explicitly (Opus-Receipt caveat 3, Opus-Funnel direction note).

---

## B3 — "STAT6 cis-effect is ruled out at the expression level" (STAT6 unmoved under NAB2-KD, log2FC +0.087, p 0.79)

**What the agents did — IMPORTANT SCOPE NOTE.** The replication lab did **NOT re-run the cis-expression null
itself** (the +0.087 / p 0.79 STAT6-expression check lives in `stage3_cis.json` /
`nab2_stat6_definitive_check.py` — not re-derived here). Opus-Confounder attacked the STAT6 confounder at the
**cluster + program layer** (C1/C2/C3), not the cis-expression layer. So the replication is **adjacent
corroboration of the broader "not just STAT6" conclusion, not a re-derivation of B3's specific number.**

**What it found on the STAT6 confounder (C1/C2/C3):** confounder **rejected**, but the authors were leaning on
the *wrong* evidence. Reproduced exactly: C2 NAB2 z +7.71 vs STAT6 z +2.66 (both Ota-only); C3 NAB2 and STAT6
have **identical** referee disease profiles {asthma, atopic eczema}, Jaccard 1.00. The confounder is broken by
(i) **guide-level KD specificity** (2/2 on-target, offtarget False, n_down 301 — molecularly NAB2, not STAT6);
(ii) **STAT6's own independent, weaker KD** (z +2.66 < NAB2's +7.71 — a proxy can't out-perform its source);
(iii) **STAT6 absent from NAB2's clusters**, modules genome-wide (16–20 chromosome arms). The disease-profile
identity (C3) **actively AIDS the confounder** — do not use it as evidence of distinctness.

**Classification vs CLAIM: PARTIAL / COMPLICATES.** The *conclusion* B3 asserts (STAT6 is not driving the
signal) is **corroborated** by the replication via a different route (guide specificity + STAT6's weaker own KD
+ non-co-membership). But the specific cis-expression receipt B3 cites (+0.087, p 0.79) was **not re-run**, and
the replication surfaces that the STAT6-distinctness *argument* was built on its weakest leg (C3).

**Classification vs PANEL: CORROBORATES the panel's "cis-test survives."** Panel `verify_eczema.md` B3 + VERDICT
§kernel #3 rate the cis-test **"competent and honest — both adversaries steelmanned it and could not break it…
a reusable deposited-data cis-artifact-falsification template."** The replication's independent failure to turn
NAB2 into "just STAT6" corroborates that survival. Panel caveat to keep: the geometric "43 kb → cis-spread
unlikely" argument is *literature-plausible, not proven safe* (Lensch 2022 shows KRAB spread crosses
insulators); the paper correctly leans on the **empirical null**, not geometry — so it is not overstated. Panel
is careful that B3 clears only the *perturbation-signal* confound, **not** the disease-label one (B5, left open).

**HONESTY FLAG (B3):** distinctness-from-STAT6 must **NOT** be defended by the identical disease profile (C3)
— that is backwards, it's the confounder's best evidence. Rest the argument on cluster co-membership (C1,
corrected) + magnitude (C2) + guide specificity.

---

## B4 — "clusters 90/100 are genome-wide functional immune modules (STAT6 absent), not a 12q13 artifact"

**What the agents did + the flagship correction.** This is the **cluster-74→90/100 catch** — the sharpest
self-correction in the whole cluster, found **independently by two agents** (Opus-Receipt AND Opus-Confounder →
high confidence). The published confounder script **hardcoded `for cl in [74, 90]`**
(`docs/nab2_stat6_confounder_check.py:34`) and therefore ran its locus test on **cluster 74, which is
NON-significant (FDR 0.52)**, and **never tested cluster 100** (the actual OR 3.90 / FDR 0.0028 receipt).
Corrected significant eczema clusters: **90 (OR 3.43, FDR 0.0224) and 100 (OR 3.90, FDR 0.0028).** Re-run on the
correct clusters (MyGene cytobands): cl90 has 37 members over 16 arms, on-12q13 = {NAB2, TESPA1}; cl100 has 38
members over 20 arms, on-12q13 = {NAB2}; **STAT6 absent from both** (STAT6's own eczema clusters are 30/61/85).
Genome-wide functional module members: BACH2, BCL6, IRF4, CD28, CD200, CD226. Conclusion survives — but on the
*right* clusters.

**Classification vs CLAIM: SUPPORTS-AFTER-CORRECTION.** B4 as it now stands (90/100) is true and survives the
locus-artifact attack; but it stands only **because the replication fixed the cluster IDs**. The pre-correction
receipt pointed at the wrong object.

**Classification vs PANEL: ANSWERS the "just a 12q13 locus artifact" critique; panel calls B4
UNVERIFIABLE-BY-LIT and defers to exactly this replication.** Panel `verify_eczema.md` B4: *"Reassurance is
internal: the adversarial replication lab (§4.6) caught the 74/90→90/100 cluster-ID mislabel and re-ran the
locus test, which strengthens confidence… Verify computationally, not by literature."* The replication is the
sole verifier of B4, and it does answer the critique — STAT6 is not a co-member, modules are genome-wide.

**HONESTY FLAG (B4) — the highest-stakes one:** *"a QC that mislabels its own supporting clusters is exactly the
kind of thing a confounder hides behind"* (Opus-Confounder). For a project whose thesis is "a receipt for every
hop," a receipt that tested a non-significant cluster is a real credibility hole. The manuscript must (a) cite
90/100 everywhere (purge any residual 74), and (b) confirm the hardcoded `[74, 90]` is de-hardcoded to derive
significant clusters (README §6 says fixed; verify in the shipped script).

---

## R5 — "EGR mechanism: NAB2 is a *distinct* regulator, not a swappable EGR corepressor (NAB1 paralog opposition)"

**What the agents did + key results.** Opus-Confounder re-derived the EGR-family comparison (D1/D2/D3) and
steelmanned "NAB2 is just EGR2's de-repressor." Reproduced exactly: D1 supported-disease breadth (eligible-12)
EGR2 = 11, NAB2 = 2, NAB1/EGR1/EGR3 = 0. **D3 is the strongest single anti-EGR fact in the whole assignment:**
NAB1 — NAB2's paralog *in the same corepressor family* — goes the **opposite** direction (Th2; z −3.52 Ota /
−3.34 Höllbacher, **significant in BOTH contrasts**, 0 diseases). If NAB1 and NAB2 were both generic EGR
corepressors their KDs should look alike; instead they are cleanly opposite → NAB2 is a distinct regulator, not
a swappable EGR brake. NAB2 is also Th1-positive in *both* contrasts, so it never behaves like an EGR-derepressor.

**Classification vs CLAIM: SUPPORTS — but only after a load-bearing reframe.** The claim survives, yet the agent
shows the authors were leaning on the **weakest leg**: D2 ("same-direction as EGR2 refutes de-repression") is a
**cross-cohort comparison** — NAB2 is significant only in Ota (z 7.71), EGR2 only in Höllbacher (z 3.06,
**adj-p = 0.049, barely under threshold**); each is n.s. in the other's contrast → PARTIAL, not a clean
refutation. And D1's breadth contrast (EGR2 broad / NAB2 narrow) is **compatible** with EGR-mediation (NAB2's
{asthma, eczema} is a strict *subset* of EGR2's 11) — it cannot distinguish "independent regulator" from "narrow
EGR2-downstream effector." So R5 must rest on **D3 (paralog opposition, both-contrast-significant)**, not D2/D1.

**Classification vs PANEL: complements panel's B1 adjacency finding.** Panel `verify_th2.md` establishes EGR2/3
*do* gate Th1/Th2 (adjacency is real), which is precisely why the "is NAB2 just EGR2?" attack has teeth — and
D3 is what defeats it mechanistically. Panel does not separately adjudicate R5, but the EGR-axis adjacency it
surfaces makes D3 the mechanism-level answer to that adjacency.

**HONESTY FLAG (R5):** downgrade D2 (cross-cohort, EGR2 borderline p=0.049); promote **D3** as the sole
load-bearing anti-EGR-mediation evidence. State D1 does not discriminate the two models.

---

## Consolidated honesty-flag ledger (corrections the manuscript MUST reflect)

| # | Correction | Claim | Found by | Severity | Status per README §6 |
|---|-----------|-------|----------|----------|----------------------|
| 1 | Eczema clusters **74/90 → 90/100**; published script hardcoded `[74,90]`, tested non-sig cl74 (FDR 0.52), never tested cl100 | B4 | Opus-Receipt + Opus-Confounder (indep.) | Medium (credibility) | Fixed: de-hardcoded; re-run confirms |
| 2 | "~8× stronger than STAT6" = **log_fc ratio; ~3× (2.9×) on z** | B1/B-biology framing | Opus-Receipt + Opus-Confounder | Low (precision) | Reworded "~8× on effect size / ~3× on z" |
| 3 | Distinctness-from-STAT6 defended with identical disease profile (C3) — which **AIDS** the confounder | B3 | Opus-Confounder | Medium (argument) | Reframed onto co-membership + magnitude + guide-specificity |
| 4 | Anti-EGR leaned on weak D2 (cross-cohort, EGR2 borderline p=0.049) | R5 | Opus-Confounder | Medium (argument) | Reframed onto D3 (NAB1 paralog opposition, both contrasts sig) |
| 5 | PROGRAM hop is a tautology inside the A universe (`refuted_program`≡0 by construction) — no independent funnel discrimination | (funnel/R-claims) | Opus-Funnel | Low (framing) | Documented; individual receipt still real |
| 6 | "43 supported" is a joint **gate×referee** product — referee alone supports 395/47,220; the novelty gate culls 395→43 | (funnel) | Opus-Funnel | Low (framing) | Documented "referee-supported among literature-eligible pairs" |
| 7 | A3 "Th1-associated" = KD-program direction; the gene itself is Th2-biased (log_fc +0.63) | B1 | Opus-Receipt + Opus-Funnel | Low (wording) | Say "KD shifts program toward Th1" |
| 8 | M7 "reproduced EVERY headline number" is in tension with "caught real errors" — two numbers were corrected, not reproduced; Codex-2 reproduced proportions not gated absolutes | M7 | (this recon) | Low (framing) | Not yet reflected — recommend "reproduced to the unit except two it corrected" |

## Bottom line for reconciliation
- **M7 SUPPORTS** (robust replication) but is engineering/QA, not a scientific contribution (panel) — keep it scoped to "computational robustness."
- **B1 SUPPORTS** (exact) — add the EGR2/3 adjacency + polarization-scoped wording (panel).
- **B3 PARTIAL/COMPLICATES at the replication layer** (cis number not re-run; STAT6-distinctness argument rebuilt off C3) but **CORROBORATES the panel's "cis-test survives"** conclusion via guide specificity + STAT6's weaker own KD.
- **B4 SUPPORTS-AFTER-CORRECTION** — the 74→90/100 fix is the flagship self-correction and the *only* verifier of B4; a receipt-per-hop project cannot ship the old cluster ID.
- **R5 SUPPORTS-with-reframe** — NAB1 paralog opposition (D3) is the strongest anti-EGR fact; D2 must be downgraded, D1 does not discriminate.

The through-line: the replication does **not overturn** any claim, but it **materially re-argues** B3/B4/R5 and
imposes numeric corrections (clusters, 8×) the manuscript must carry. Its edge is the self-correction, not the PASS.
