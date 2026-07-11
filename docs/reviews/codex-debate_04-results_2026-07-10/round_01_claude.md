# Round 1 — Claude's opening position (§4 Results)

**Framing question.** Is §4 Results maximally rigorous, honest, and defensible to a hostile FRMA/LBD
reviewer — every quantitative claim exactly supported by the repo artifacts, language calibrated (no
overclaim), and is the Control-2 "substrate-inherited stringency" reading the correct, honest interpretation
of the label-shuffle result?

**Position.** §4 reports six results, all from repo-verified numbers, in calibrated language (never
proven/definitive/validated/genuine/discovered).

1. **Funnel + ledger (4.1).** 3,935 A-genes → 22,039 eligible pairs → 43 disease-C-supported → 30 clean
   (class split 30/10/3/1; 21,995 refuted-for-C). Two honesty caveats stated in Methods *and* here: the
   program hop is a within-funnel tautology (`refuted_program ≡ 0`), and "43" is a joint gate×referee
   product (referee alone supports 395/47,220). The ledger (NAB2 supported / EGR2 supported / NUDT1
   supported-weak / IL2 untested / SLC1A5 refuted) is framed as a *demonstration* the referee discriminates,
   NOT an accuracy benchmark.

2. **Sensitivity panel (4.1b)** — computed by `docs/manuscript/analysis/sensitivity_panel.py` (cache-free,
   deterministic, seed 20260710), reproduced **byte-identical inside Claude Science (delta 0, identical
   sha256, Sonnet-5-Reviewer-verified)** per `analysis/cs-reproduction/COMPARE.md`:
   - **Control 1:** 2,430 failed-KD genes → all 2,430 `untested` (100%, 0 leaks).
   - **Control 2 (the honest one):** disease hop over all 47,220 A×C pairs supports only 406 (0.86%),
     refutes 99.14%. Label-shuffle null (2,000 perms) = 467.7 ± 10.9; observed is **5.6 SD BELOW** null.
     I claim ONLY: the stringency is **substrate-inherited** from the enrichment FDR family (even random
     labels pass ~1%), NOT the referee's own discrimination; the significant departure establishes only
     **label-dependence**. I explicitly do NOT claim "passes rarer than chance = selective."
   - **Control 3:** NAB2 rank 1–8 across a 27-point weight grid, median 4, top-5 in 24/27 (89%); default
     reproduces rank 4. Verdicts are weight-independent by construction.

3. **NAB2 hero (4.3)** — 4-hop receipts: KD 2/2 guides adj-p≈1e-16; effect −16.9, 301 DE; Ota z=7.71
   adj-p 1.96e-13; eczema clusters OR 3.90/FDR 0.0028 & OR 3.43/FDR 0.0224 (clusters 90&100). Calibrated to
   "consistent with a re-derived chain the literature has not made"; disease hop = genetic-association
   nomination, two receipt classes kept explicit.

4. **STAT6 cis-refutation (4.4)** — authors' genome-wide DE: STAT6 +0.087/adj-p 0.788 UNMOVED, NAB2 self
   −3.078/7.2e-60; 302 of 10,282 moved; STAT6 rank 5444/10282. Scoped: strengthens NAB2-specificity of the
   *perturbation* signal, does not prove the disease link.

5. **Native CS reproduction + self-audit (4.5)** — three liveness claims distinct (full-scale = cached
   replay under guard, delta 0; live authorship = 12-gene microsweep, NAB2 absent so no cherry-pick; cross-
   family = external); Sonnet critic flagged "validated"/"definitive" → removed; role/model/checkpoint
   independence, not cross-vendor.

6. **Cross-model replication (4.6)** — 5 agents (3 Opus + 2 Codex), unanimous PASS, caught cluster-ID
   74/90→90/100 and 8×→3× z, reframed distinctness argument.

**What I want stress-tested:** (a) does any number mismatch its source artifact? (b) is the Control-2
framing honest and not spun in either direction? (c) any residual overclaim / calibrated-language slip?
(d) consistency with §1–§3 (I already softened §1's negative-control preview to match Control 2).
