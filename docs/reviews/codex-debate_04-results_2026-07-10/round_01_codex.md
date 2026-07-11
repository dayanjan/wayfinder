# Round 1 — Codex critique

**Convergence:** round 1 — no prior position to converge with

**Position:** Claude's position is broadly repo-grounded on the headline counts, but §4 is not yet maximally defensible. The worst problems are not gross numeric mismatches; they are interpretive overreach around Control 2, a calibrated-language breach inside the very section claiming no such breach, and a few scope/traceability slips that a hostile FRMA/LBD reviewer can exploit.

## F-001 [P1] sev4/lik4/blast4 nov=True correctness
**Control-2 mechanism exceeds what the shuffle proves**

- EVIDENCE: MISMATCH/OVERINTERPRETATION: §4 says real disease associations 'concentrate on fewer diseases per gene' and that this explains why observed < null (docs/manuscript/sections/04_results.md:91,99). The code only counts distinct (gene,disease) pairs after permuting the disease column across enrichment rows (docs/manuscript/analysis/sensitivity_panel.py:95-108); it does not compute per-gene disease cardinality, disease marginal concentration, cluster-size effects, or any decomposition proving that causal explanation. The numeric basis HOLDS: observed=406, null=467.727±10.935 in docs/manuscript/analysis/sensitivity_results.json:14-18.
- CONCERN: A reviewer accepts the 5.6 SD direction but rejects the explanatory sentence as a just-so story. The result supports label-dependence of this counting statistic; it does not identify the biological/statistical mechanism of fewer diseases per gene without an added decomposition.
- ACTION: Replace the causal explanation with a scoped inference or add a decomposition showing per-gene disease-cardinality compression under true labels.

## F-002 [P1] sev4/lik4/blast3 nov=True correctness
**Control-2 significance conflicts with stored empirical_p**

- EVIDENCE: MISMATCH/RISK: §4 calls the departure 'significant' and says label-independent formality is excluded (docs/manuscript/sections/04_results.md:88-99). The artifact stores only `empirical_p: 1.0` because the code computes the upper-tail count `null_counts >= observed` (docs/manuscript/analysis/sensitivity_panel.py:109,118; docs/manuscript/analysis/sensitivity_results.json:21). The z-score direction HOLDS mathematically: (406-467.727)/10.935 ≈ -5.65, but the reported artifact's empirical p-value is the wrong tail for the prose claim.
- CONCERN: A hostile reviewer sees `empirical_p=1.0` in the ground-truth JSON and can accuse the manuscript of calling a non-significant empirical result significant, even though the z-score is compelling.
- ACTION: Add lower-tail/two-sided permutation p-values to the artifact or avoid 'significant' and report only the signed z-distance.

## F-003 [P1] sev3/lik4/blast4 nov=True novelty
**Control-2 heading still credits discrimination to the hop**

- EVIDENCE: MISMATCH/TENSION: §4's body correctly says stringency is substrate-inherited and 'not a demonstration of the referee's own discriminating power' (docs/manuscript/sections/04_results.md:94-102), which HOLDS against the null pass rate 0.99% in docs/manuscript/analysis/sensitivity_results.json:20. But the subsection title says 'stringent and label-dependent, not a rubber stamp' (docs/manuscript/sections/04_results.md:82), and the opening summary says the controls probe 'how much of that discrimination is a property of the data versus an artifact' (docs/manuscript/sections/04_results.md:19-22).
- CONCERN: Even with the honest paragraph, reviewers quote the heading as a residual spin: the observed count is below a sparse null, so 'not a rubber stamp' is defensible only as label-dependence, not as referee selectivity.
- ACTION: Retitle Control 2 around substrate-inherited sparsity plus label-dependence, avoiding 'rubber stamp' rhetoric.

## F-004 [P1] sev4/lik5/blast3 nov=False correctness
**Calibrated-language breach: 'validated' appears in §4 claim text**

- EVIDENCE: MISMATCH: The §4 preamble promises calibrated language and says never 'validated' (docs/manuscript/sections/04_results.md:4-5), and the self-audit says the reviewer flagged 'validated'/'definitive' and they were removed (docs/manuscript/sections/04_results.md:208-210; source HOLDS in docs/cs-full-pipeline_2026-07-09/README.md:82-84). But §4.3 still says 'polarity marker-validated' (docs/manuscript/sections/04_results.md:149).
- CONCERN: This is an own-goal: the manuscript makes calibrated language a methodological result, then violates the exact banned token in the Results section.
- ACTION: Replace 'polarity marker-validated' with a neutral phrase such as 'polarity marker-checked' or cite the actual marker check without the word validated.

## F-005 [P1] sev4/lik3/blast4 nov=True correctness
**STAT6/locus-artifact language can overrun the disease-label caveat**

- EVIDENCE: PARTIAL MISMATCH: The perturbation cis result HOLDS: STAT6 log2FC +0.087, adj_p 0.788, rank 5444/10282; NAB2 self -3.078, adj_p 7.16e-60; 302 genes moved (docs/cs-full-pipeline_2026-07-09/stage3/stage3_cis.json:8-18,47-50). The disease-label caveat also HOLDS: no colocalization/LD control and the label is GWAS/Open Targets genetic-association nomination (docs/lbd_finding_nab2_2026-07-08.md:75-78; docs/manuscript/sections/04_results.md:158-159). But §4.6 says corrected modules 'reject the locus-artifact reading' (docs/manuscript/sections/04_results.md:231-232), which can sound broader than the evidence: it rejects the cluster-ID/locus-membership artifact, not LD inheritance of the disease label.
- CONCERN: A reviewer can argue the manuscript quietly upgrades 'STAT6 mRNA not cis-repressed' and 'STAT6 absent from clusters 90/100' into a broad rejection of locus artifact, while the GWAS label remains vulnerable to LD/near-gene provenance.
- ACTION: Scope 'locus-artifact' to the module-membership/cluster-ID error and explicitly preserve the unresolved GWAS-label/LD caveat in the same sentence.

## F-006 [P2] sev3/lik3/blast3 nov=False correctness
**'Every headline number reproduced' overstates agent-level replication**

- EVIDENCE: PARTIAL MISMATCH: §4.6 says every headline number reproduced to the unit from independent raw-CSV computation (docs/manuscript/sections/04_results.md:221-225). The replication summary supports many exact reproductions, including NAB2 receipt and funnel counts (docs/replication_report_2026-07-08.md:22-27), but it also says Codex-2 reproduced A=3,935 and clean/weak/flagged proportions, not every full headline number (docs/replication_report_2026-07-08.md:18-19,26-27).
- CONCERN: The lab-level replication is strong, but the current wording implies all members independently reproduced all headline numbers to unit precision, which the replication report does not say.
- ACTION: Change to 'across the replication lab, the headline numbers reproduced...' and avoid implying every agent checked every number.

## F-007 [P2] sev2/lik5/blast2 nov=False correctness
**'We report five results' miscounts the Results architecture**

- EVIDENCE: MISMATCH: §4 says 'We report five results' (docs/manuscript/sections/04_results.md:19), then enumerates funnel/ledger §4.1, sensitivity §4.1b, confident no/QC §4.2, NAB2 §4.3, STAT6 §4.4, native reproduction/self-audit §4.5, and cross-model replication §4.6 (docs/manuscript/sections/04_results.md:19-26). Claude's opening position itself calls these six results, counting 4.1 and 4.1b together but still listing six numbered claims.
- CONCERN: This is editorial, but hostile reviewers use small arithmetic inconsistencies to question control of the manuscript.
- ACTION: Either say 'six results' or combine the funnel and sensitivity panel explicitly as one result in the roadmap.

## F-008 [P2] sev3/lik5/blast3 nov=True correctness
**Earlier-section calibration drift: Introduction says 'proves'**

- EVIDENCE: MISMATCH WITH LOCKED FRAMING: §4 avoids 'proves' except in negated form (docs/manuscript/sections/04_results.md:159,186), but §1 says the disease hop's stringency 'proves largely inherited' (docs/manuscript/sections/01_introduction.md:69-71). This conflicts with the manuscript's own calibration rule in docs/manuscript/sections/01_introduction.md:4-5 and with OUTLINE guidance to avoid 'proven/definitive/validated/genuine' (docs/manuscript/OUTLINE.md:173-174).
- CONCERN: Even if §4 is fixed, reviewers read the paper as a whole; an overclaimed preview can contaminate the Control-2 interpretation before Results.
- ACTION: Replace 'proves largely inherited' with 'is largely consistent with substrate-inherited stringency' or equivalent calibrated language.

## F-009 [P2] sev3/lik3/blast3 nov=False correctness
**'§4.1b supplies the rate' is underspecified and can be misread as accuracy**

- EVIDENCE: PARTIAL MISMATCH: §4.1 says the ledger examples are not sampled to estimate a rate and that §4.1b supplies the rate (docs/manuscript/sections/04_results.md:69). The actual §4.1b rate is disease-hop support over all 47,220 A×C combinations, observed 406/47,220 = 0.86% (docs/manuscript/analysis/sensitivity_results.json:11-15), not a ledger rate, not a full-chain survivor rate, and not precision/recall.
- CONCERN: A reviewer can read 'the rate' as a measured accuracy or verdict-distribution rate for the showcased ledger, which the authors explicitly disclaim elsewhere.
- ACTION: Specify '§4.1b supplies a disease-hop support-rate control over A×C, not a ledger accuracy rate.'

## F-010 [P2] sev2/lik4/blast2 nov=False correctness
**Primary-source traceability is uneven for §4.4 corroborations**

- EVIDENCE: HOLDS BUT TRACEABILITY WEAK: §4.4's primary STAT6/NAB2 numbers are directly in stage3_cis.json (docs/cs-full-pipeline_2026-07-09/stage3/stage3_cis.json:8-18,47-50). However, the corroborating claims 'zero perturbation-effect clusters,' 'cross-guide/donor R 0.74,' and off-target flag False are sourced in the narrative finding doc (docs/lbd_finding_nab2_2026-07-08.md:85-88), not in the provided stage3 JSON; §4 cites them as if they sit in the same direct genome-wide DE check (docs/manuscript/sections/04_results.md:180-183).
- CONCERN: FRMA/LBD reviewers may accept the main cis check but ask for the exact table/script receipts for the three corroborations, because they are not visible in the stage3 artifact §4 otherwise leans on.
- ACTION: Add explicit citations/receipts for the cluster-overlap, reproducibility R, and off-target-flag fields or demote them to secondary corroboration.

**Next question:** Address Control-2 first: will Claude add a lower-tail/two-sided permutation p-value and soften the per-gene concentration mechanism, while preserving the honest substrate-inherited stringency thesis rather than spinning it into referee selectivity?
