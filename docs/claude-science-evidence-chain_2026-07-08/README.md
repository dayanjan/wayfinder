# Claude Science evidence chain — the reasoning-provenance layer

The executable notebook (`notebooks/pyzobot_arbiter_evidence_chain.ipynb`) *runs* the evidence chain
deterministically. This folder is its companion **reasoning layer**: an **independent adjudication of
the same claim by Claude Science** — Anthropic's local scientific workbench — driven headlessly.

## What was done
A **fresh** Claude Science project (`proj_6fe6d8a34e19`, 2026-07-08) was given **only** the four public
Perturb-seq tables and the question — *does NAB2 → Th1/Th2 → atopic eczema hold?* — with instructions to
act as a skeptical data-referee, compute a real receipt at every hop, stress-test the STAT6 *cis*-artifact
confounder, and **refute if the data did not support it**. It was *not* told the answer. Claude Science
loaded the tables, wrote and ran its own pandas/matplotlib code, and reasoned to its own verdict.

*(Driven via the user-level `drive-claude-science` skill; task prompt archived at
`.claude/scratch/cs-drive/prompt.txt`. Data staged at `~/pyzobot-data/` in WSL — the same four public
`*.suppl_table.csv` the notebook uses.)*

## The result — independent corroboration
Claude Science reached the **identical receipt-backed verdict**, every headline number matching the
notebook and the 5-agent replication (`docs/replication_report_2026-07-08.md`):

| Hop | Claude Science receipt | Verdict |
|---|---|---|
| 0 · GATE | 2/2 NAB2 guides signif_knockdown, adj-p 1e-16, expr 0.033/0.079 vs NTC 0.567 (~90% KD) | passed |
| 1 · EFFECT | on-target, effect −16.88, 301 downstream, no off-target, R 0.74 | supported |
| 2 · PROGRAM | Ota z 7.71 (p 2e-13, Th1-assoc); Höllbacher same direction, n.s. | supported (1 of 2, stated honestly) |
| 3 · DISEASE | 2 of 4 atopic-eczema clusters FDR<0.05: c100 OR 3.90, c90 OR 3.43 | supported |
| confounder | STAT6 absent from NAB2's clusters (genome-wide members); **zero** shared perturbation clusters ({74,90,98,100} vs {30,61,85}); NAB2 ≥ STAT6 reproducibility | cis-artifact **weakened by all three checks** |

It also independently reproduced the **discrimination**, without which the referee is a rubber stamp:
- **SATB1 → asthma = UNTESTED** (the hero catch): 0/2 guides knocked down (guide 2.39/2.40 vs NTC 2.35).
  Note it flagged that T2 *does* show a Th2 hit for SATB1 — *"but the knockdown never took, so this
  readout is uninterpretable → UNTESTED, not a negative."* Exactly the thesis, stated by an independent agent.
- **SLC1A5 → asthma = REFUTED** at the disease hop (zero asthma-cluster membership).

And it converged on the same calibrated framing — *nomination, not proven causation* — with an explicit
**"what we do NOT claim"** section.

## Files
- `claude_science_evidence_chain.md` — Claude Science's full hop-by-hop reasoning narrative + verdict.
- `claude_science_verdict.json` — the structured verdict (hops, confounder checks, contrast cases, overall).
- `nab2_evidence_chain.png` — Claude Science's own 6-panel figure (receipt chain; NAB2-vs-STAT6 program
  shift; disease-enrichment odds ratios; reproducibility; perturbation-cluster Venn; locus composition).
  Note panel **c** honestly shows STAT6 *is* in its own significant atopic cluster (c85) — a **different**
  module than NAB2's, and one they don't share on perturbation effect, which is the independence argument.

## Why this matters for the submission
Two independent instruments — a deterministic Python referee (the notebook) and an Anthropic scientific
agent reasoning from scratch (this) — plus a 5-agent replication lab, all land on the same receipt-backed
verdict *and* the same confident refusals. The agreement is the point.

## Provenance / compliance
New work authored during the event (2026-07-08). Claude Science ran on public data only, needed a single
approval, and its outputs are the ground truth here (copied verbatim from the workspace, unedited).
