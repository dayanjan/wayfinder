You are a senior computational-biology reviewer giving an INDEPENDENT judgment call to a peer
(Claude), read-only in the repo. Verify claims against the actual sweep output + referee code;
a repo-grounded opinion is worth far more than a speculative one. Be direct; disagree if warranted.

# Situation
The LBD proposer full sweep ran (condition Stim8hr). Honest funnel:
**a_genes 3,935 -> eligible pairs 22,039 -> referee-supported 44 -> pure-disjoint(ac_lit=0) 1.**
The proposer is answer-free (A from KD/DE tables, novelty from external Europe PMC/Open Targets);
the referee (`referee_triple`) culls on the EXACT disease. Full results:
`data/lbd_out/lbd_questions_Stim8hr.json` (44 supported, ranked). Process: `docs/lbd-build-log.md`
(read the "FULL SWEEP result" section). Referee: `docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`.

# Candidates (verify these in the JSON + by reading the referee receipts)
- **NAB2 x atopic eczema** (proposed HEADLINE money-shot): ac_lit=6, ac_known=0.038, effect=301.
  Receipt: GATE 2/2 guides adj-p 1e-16; EFFECT on-target -16.9, 301 downstream, NO off-target flag;
  PROGRAM Th1-assoc Ota zscore 7.71 adj-p 1.96e-13 (Hollbacker n.s.); DISEASE atopic-eczema cluster
  OR 3.90 FDR 0.0028. Mechanistic note: NAB2 is the EGR2 corepressor; EGR2 is the project's
  validated hero gene.
- **DNAJB9 x type 1 diabetes**: supported but EFFECT FLAGGED (off-target True). effect=117, ac_lit=12.
- **NUDT1 x type 1 diabetes**: the ONLY pure-disjoint (ac_lit=0) but effect=4 (trivial), program
  shift borderline (Ota adj-p 0.038).

# The judgment I want
1. **Is NAB2 x atopic eczema the right HEADLINE money-shot?** Verify its receipt in the referee.
   Is the chain solid, or is there a weakness I'm glossing (e.g. only 1 of 2 program contrasts
   significant; only 2 disease clusters; the -16.9 effect size sign)? 
2. **Is the honest framing right** — lead with the 22,039->44 funnel + NAB2 as a *near-novel*
   (not zero-literature) receipt-backed hypothesis, explicitly flag that the ONE pure-disjoint
   (NUDT1) is weak (why we rank not hard-gate), and show DNAJB9's off-target flag + refuted
   examples as the cull? Anything dishonest or overclaimed? Is the EGR2-NAB2 mechanistic note a
   legitimate hypothesis-strengthener or a reach I should drop?
3. **Red flags in the 44** — scan `lbd_questions_Stim8hr.json`: any candidate that looks like a
   query/scoring artifact rather than biology? Is ac_lit=6 for NAB2 plausibly real or a
   symbol-ambiguity artifact ("NAB2" matching unrelated text)?
4. **Worth running the other 2 conditions (Rest, Stim48hr)** for more/better candidates, or is
   Stim8hr sufficient for the demo? Take a position given the July-13 deadline.

# Output
Plain prose. Lead with a one-line verdict on the NAB2 headline (keep / replace / keep-with-caveat),
then answers to 1-4 with file/line or JSON evidence, then "biggest risk in featuring NAB2".
Tight; findings over throat-clearing.
