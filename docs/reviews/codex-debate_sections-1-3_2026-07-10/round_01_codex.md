# Round 1 — Codex findings (prose debate, sections 1-3, repo-read)

**Position summary:** directionally right but too generous — several sentences let the method inherit more
experimental / follow-up / independence weight than the evidence supports, especially in compressed
references and opening rhetoric. 14 findings; all accepted → prose v2.

| ID | Pri | Title | Fix applied |
|----|-----|-------|-------------|
| F-001 | P0 | "follow-up" not closed by retrospective adjudication | §1 close + §2.1: explicitly close the *triage* loop, not the follow-up loop; killed "true in fresh experimental data" |
| F-003 | P0 | two-receipt distinction blurs in compressed refs | §1 NAB2 sentence + §3.3 hop-3: STAT6 falsifies a cis-artifact of the *perturbation* signal, not the disease link; hop-3 marked association receipt |
| F-004 | P0 | Open Targets `ac_known` is *overall* score, not "genetic" (verified in `sources.py`) | §3.1 + §3.2: "overall target–disease association score", separated from the T3 genetic disease labels |
| F-006 | P0/P1 | "supported" too strong; artifact still says "validated" | §3.3: "supported" = bounded verdict label; §3.4: calibration claim scoped to manuscript-facing output, legacy log acknowledged |
| F-002 | P1 | discovery language at the opening | §1: "testable connections"; "candidate connection — novel in the literature, not yet biology" |
| F-005 | P1 | confident-NO overstated (funnel pre-gates hops 0–2) | §3.3: funnel cull is disease-C-dominated; broad discrimination shown by the out-of-funnel ledger (§4) |
| F-007 | P1 | "platform checked its own work" slogan | §1: replaced with bounded role/model/checkpoint statement |
| F-008 | P1 | no-API driver reads as security-bypass | §3.4: added guardrails (operator session, fixed workspace, logged approvals, confined network, guard-protected receipts); dropped "honest substitute" |
| F-009 | P1 | grant number still in §2 | removed from §2.1 |
| F-010 | P2 | under-motivates the substrate choice | §2.2: "bounded, independent adjudication surface, not a universal oracle" |
| F-011 | P2 | "answer-free" overclaims | §3.2: "disease-answer-free, not evidence-free" |
| F-012 | P2 | objective not justified for a metrics audience | §3.2: fixed-before-run, not tuned to survivor, rank≠verdict, sensitivity → §4 |
| F-013 | P2 | novelty criterion (NAB2 has nonzero co-mentions) | §1: operational criterion (low direct-lit + low curated, not strict A–C absence) |
| F-014 | P2 | negative-control panel too compressed | §1: named the controls (failed-KD→untested; label-shuffled→chance) |

**Preserve-intent:** `null` — all three novel claims + the no-API element intact; every fix scoped, none removed.
