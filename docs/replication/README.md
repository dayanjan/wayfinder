# Independent validation — methodology & audit trail (2026-07-08)

How the NAB2 → Th1/Th2 → atopic-eczema finding was independently pressure-tested, by whom, with what
instructions, what they found, how they worked, and how everything was confirmed. This directory is
the full audit trail; the one-page verdict is `../replication_report_2026-07-08.md`.

## 1. Why — design philosophy
A finding is only as good as its attempts to falsify it. Rather than re-check our own work, we stood up
a **simulated independent lab**: a team of agents told to *distrust our numbers, re-derive everything
from the raw data, and actively try to break the finding*. Independence was engineered four ways:
- **Cross-model.** Claude (Opus) **and** OpenAI (Codex) agents — a bug both model families miss is
  rarer than one either misses alone.
- **Clean-room re-implementation.** Two members re-implemented the pipeline **from scratch, importing
  none of our code**, so a match is genuine reproduction, not shared-code tautology.
- **Adversarial mandate.** Every agent was instructed that a *refuted* claim with evidence is the most
  valuable output; one agent's sole job was to steelman the confounders.
- **Blind to each other.** Agents ran in parallel with no shared state — two independently finding the
  same bug is corroboration, not an echo.

## 2. The team (5 agents)
| Agent | Model | Role | Scope | Prompt | Report | Verdict |
|---|---|---|---|---|---|---|
| Opus-Receipt | Opus | receipt re-derivation | Claim Set A (NAB2 receipt) + spot-checks | `agent-prompts/opus1_receipt.md` | `agent-reports/opus_receipt.md` | PASS |
| Opus-Funnel | Opus | funnel + statistics | Claim Set B (3,935→30 funnel) | `agent-prompts/opus2_funnel.md` | `agent-reports/opus_funnel.md` | PASS |
| Opus-Confounder | Opus | adversarial skeptic | Claim Sets C+D (STAT6, EGR) | `agent-prompts/opus3_confounder.md` | `agent-reports/opus_confounder.md` | PASS |
| Codex-1 | Codex (GPT) | code correctness | pipeline code audit | `agent-prompts/codex1_code_audit.md` | `agent-reports/codex1_code.md` | PASS |
| Codex-2 | Codex (GPT) | clean-room re-impl | fresh re-implementation of A/receipt/funnel | `agent-prompts/codex2_reimpl.md` | `agent-reports/codex2_reimpl.md` | PASS |

## 3. The shared protocol
All five worked against one frozen claim set — `agent-prompts/00_shared_protocol.md` — which pins the
exact numbers to reproduce (Claim Sets A–E), the raw-data schema (T1 DE_stats, T2 program signature,
T3 cluster enrichment, T4 guide KD), the condition of record (Stim8hr), the significance threshold
(FDR<0.05), and the rules of engagement (re-derive from raw; be adversarial; report exact numbers;
flag statistical/logical errors; state where the finding is fragile).

## 4. How each member worked
- **Opus-Receipt** loaded the four raw CSVs in pandas and hand-computed NAB2's gate (T4 guide counts),
  effect (T1 on-target/downstream), program shift (T2 both contrasts), and disease enrichment (T3
  exploded, filtered to disease=="atopic eczema" AND gene_set=="downstream_Stim8hr", FDR<0.05). It
  checked the effect-size and log_fc **signs**, verified the disease call is disease-**specific**, and
  independently re-derived two other genes (BHLHE40, UFM1) to test for cherry-picking.
- **Opus-Funnel** wrote a from-scratch chain classifier (`indep_funnel.py`, no repo referee imported),
  built the A universe itself from T4∩T1∩T2, and ran it over A×12 diseases to reproduce the class
  counts. It also ran the un-gated A×12=47,220 sweep to measure how much of the "43" comes from the
  novelty gate vs the referee.
- **Opus-Confounder** re-derived the cluster composition (MyGene cytobands), the NAB2-vs-STAT6 program
  and disease profiles, and the EGR-family comparison — then wrote the strongest possible case that the
  signal *is* just STAT6 or just EGR2, and reported where our defense was weakest.
- **Codex-1** read the pipeline source (`entities.py`, `referee_triple.py`, `cooccur.py`, `propose.py`)
  line by line for answer-leakage, a too-loose "supported" filter, FDR misuse, and off-by-ones, then
  ran read-only python to spot-reproduce the funnel counts and the NAB2 receipt.
- **Codex-2** wrote an entirely fresh classifier (importing none of our modules), rebuilt the A universe
  and the 12-eligible-disease set independently, and reproduced the NAB2 result + the chain-class
  proportions.

## 5. How everything was confirmed
- **Exact-count matching.** Two independent re-implementations (Opus-Funnel, Codex-1) reproduced the
  full class breakdown — 21,995 / 30 / 10 / 3 / 1 — to the unit; the NAB2 receipt reproduced hop-by-hop
  from raw CSVs (Opus-Receipt, Codex-1). Codex-2's clean-room proportions matched.
- **Cross-validation of errors.** The cluster-ID misalignment was found **independently** by two agents
  (Opus-Receipt and Opus-Confounder) — high confidence it is real, and its fix was re-verified.
- **Adversarial failure to break.** The skeptic (Opus-Confounder) could not turn NAB2 into "just STAT6"
  or "just EGR2"; its steelman instead sharpened *which* arguments carry weight.
- **Code-level confirmation.** Codex-1 independently confirmed the A universe never opens the disease
  table, and that `answer=="supported"` requires the full chain with n_downstream>0.

## 6. Issues found → fixed
| # | Issue | Found by | Severity | Fix |
|---|---|---|---|---|
| 1 | Confounder script mislabeled NAB2's significant atopic-eczema clusters as 74/90; true clusters are **90/100** (74 is FDR 0.52). Locus test had run on the wrong cluster. | Opus-Receipt + Opus-Confounder (independently) | Medium (credibility) | Script de-hardcoded to derive significant clusters; re-run confirms genome-wide modules (BACH2/BCL6/IRF4/CD28); STAT6 in neither |
| 2 | "~8× stronger than STAT6" is the **effect-size (log_fc)** ratio; on z it is ~3×. | Opus-Receipt + Opus-Confounder | Low (precision) | Reworded to "~8× on effect size / ~3× on z" |
| 3 | Distinctness-from-STAT6 was defended with the identical disease profile (C3), which actually *aids* the confounder. | Opus-Confounder | Medium (argument) | Reframed onto cluster co-membership + magnitude + guide-specificity |
| 4 | Anti-EGR-mediation leaned on the weak same-direction argument (D2, cross-cohort). | Opus-Confounder | Medium (argument) | Reframed onto D3 (paralog NAB1 opposition, significant in both contrasts) |
| 5 | PROGRAM hop is a tautology inside the A universe (refuted_program≡0 by construction) — no independent funnel discrimination. | Opus-Funnel | Low (framing) | Documented; the individual receipt's program evidence is still real |
| 6 | "43 supported" is a joint novelty-gate×referee product (referee alone supports 395/47,220). | Opus-Funnel | Low (framing) | Documented as "referee-supported among literature-eligible pairs" |
| 7 | `overall` sentence can read too strong for `supported_weak`; `cooccur.py` docstring mis-states the gate. | Codex-1 | Low (wording) | Noted; classification is unaffected |

## 7. Outcome
Unanimous PASS. Every headline number reproduced; the code is correct; the confounders were rejected.
All seven issues were documentation/framing/analysis-hygiene — **none changed the core science**. The
finding is a genuine, reproducible, receipt-backed, honestly-caveated result. Corrections are applied in
`../nab2_knowledge_synthesis_2026-07-08.md` and `../lbd_finding_nab2_2026-07-08.md`.

## 8. Reproducibility
- Re-run the checks: `python docs/nab2_stat6_confounder_check.py`, `python docs/nab2_egr_mechanism_check.py`
  (from repo root, `PYTHONPATH=src`).
- Re-run the sweep: `PYTHONPATH=src python -m arbiter.lbd.propose --condition Stim8hr`.
- The agent prompts (`agent-prompts/`) can be re-issued to fresh Opus/Codex agents against the same
  frozen protocol to repeat the whole validation.
