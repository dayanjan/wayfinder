# Round 1 — Claude's opening position

## Framing question
Is `docs/manuscript/OUTLINE.md` the strongest, most honest, most reviewer-proof plan for a
**methods + demonstration** paper for *Frontiers in Research Metrics and Analytics* (FRMA,
Text-mining/LBD section) — AND does every quantitative claim in its §7 claim-inventory actually
hold against this repo?

## The position I am defending
1. **Genre + venue fit.** The paper should inherit the Henry et al. 2021 (FRMA 6:644728) house style
   — "we built the instrument, here is the finding it produced," method fully described but the
   *result* is the argument — and submit to the same venue. Wayfinder is the operator's own LBD
   lineage; the R01-critique frame ("LBD overproduces, nothing gets validated") is a genuine,
   ownable narrative spine.

2. **The headline is the agentic loop, not just the finding.** The novel contribution is: Claude
   *generates* hypotheses, deterministic tools *adjudicate* each against a held Perturb-seq substrate
   with a receipt at every hop, and an independent critic model *enforces calibrated language on the
   platform's own output*. NAB2 is the worked example; the verdict **ledger** (supported / untested /
   refuted) is what proves the referee discriminates — the thing Henry structurally could not show.

3. **The falsification thesis is the moat and gets its own Results subsection** (§4.2): the confident,
   receipt-backed NO + the knockdown-QC gate (failed KD → *untested*, not *negative*).

4. **Honesty scoping is deliberate.** NAB2 stays a *nomination* (disease label is Open Targets
   GWAS-genetic, no colocalization); the perturbation-backed claim is only "NAB2 is a Th1/Th2
   regulator." The drug-direction thread (Th2-brake / restore-not-knockdown) is Discussion-as-next-
   experiment, not Results, because it is association-backed and needs perturbation proof.

5. **Every headline number is repo-verifiable and inventoried in §7** (C1–C25) so it can be checked
   before it ossifies into a submitted paper. One conflict is already flagged: the dataset DOI (C23).

## What I most want stress-tested (preserve-intent applies to the *novel claims*, not the numbers)
- The **novel claims** — "an agentic workbench closes the LBD loop," "the referee says a confident,
  receipt-backed NO," "the platform self-audits its own calibrated language" — must NOT be sanded
  toward a safe generic-LBD-tool paper. Push on them, but if they survive, keep them sharp.
- The **numbers** get no such protection: verify C1–C25 against the actual source files
  (`docs/lbd_finding_nab2_2026-07-08.md`, `docs/cs-full-pipeline_2026-07-09/README.md`,
  `docs/replication_report_2026-07-08.md`, `docs/nab2_stat6_definitive_check.py`,
  `docs/perturbseq-qc_2026-07-07/`, `references/`). Opening those files to confirm each value is the
  single highest-value thing this debate can do. If a number is wrong, say so with the file:line.
- The **reviewer-proofing**: attack §8's open questions as a hostile FRMA/LBD reviewer — especially
  whether the agentic headline over-reaches for a text-mining venue, and whether the ledger is
  strong enough as "the referee discriminates" evidence or whether a reviewer will demand a
  held-out precision/recall benchmark.
