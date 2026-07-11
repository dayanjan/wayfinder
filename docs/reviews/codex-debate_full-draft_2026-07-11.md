# Full-draft codex-debate — Abstract + §1–§5 — 2026-07-11 (repo-read, --preserve-intent)

**Framing question.** Is the full manuscript internally consistent, calibrated, and defensible to a hostile
FRMA/LBD reviewer end-to-end — no cross-section contradiction, no overclaim, every quantitative claim
traceable, with the novel claims neither sanded nor overstated?

## Outcome (honest): 1 real fix, and a method-reliability finding

This debate hit a reliability wall on a 9,173-word multi-section artifact, and the honest record matters more
than a manufactured convergence. What the debate **reliably** produced: one verbatim-verified Abstract fix.
What it also produced: two Codex passes that confabulated and were rejected on verification.

### Trajectory
| Pass | Result | Disposition |
|---|---|---|
| Inline full-draft R1 (all 9.2k words inlined) | 14 findings, "3 P0" | **REJECTED — all hallucinated.** Every quoted phrase was absent from the actual files (grep: 0 hits): a grant number that isn't there, "genetic-association" where §3 says "overall", "new discoveries" where §1 says "testable connections". Codex critiqued a generic-LBD prior, not the draft. (`round_01_REJECTED_note.md`.) |
| Grounded R1 (Abstract + §5 inlined; verbatim-quote-or-drop; cross-section via repo-read) | **1 finding (F-001, P1)** | **ACCEPTED + FIXED.** Real, verbatim-verified. |
| Grounded R2 | 0 findings, but reasoning **confabulated a different domain** ("deploy runbook / entitlement / managed-endpoint", DROPPED F-002…F-017 that never existed) | 0-findings taken at face value (nothing false to fix); the "converged" *reasoning* is not trustworthy. |

### The one real finding — F-001 (P1, fixed)
The Abstract applied "reproduced **byte-for-byte**" to the entire loop, but byte-identity/delta-0 is scoped to
the **sensitivity panel** (`cs-reproduction/COMPARE.md`); the full pipeline reproduced the exact funnel and
NAB2 rank (digit-for-digit output, `04_results.md`). Codex quoted all four strings verbatim and they check
out. **Fix:** the Abstract now reads "…its analyses reproduced exactly when the workbench was driven
programmatically — the pipeline's funnel and ranking digit-for-digit, and the sensitivity panel byte-for-byte."

## What the debate confirms
§1–§4 were already hardened by two prior *converged* debates
(`codex-debate_sections-1-3_2026-07-10`, `codex-debate_04-results_2026-07-10`). Even the hallucinating inline
pass could not surface a single **real** issue in them (all 14 were fabricated or already-addressed), and the
grounded pass found nothing in §1–§4 — corroborating that the earlier per-section debates did their job. The
only surviving whole-paper issue was the Abstract over-scope, now fixed. Preserve-intent: no protected claim
was sanded (no sanding warning fired on the grounded pass).

## Method-reliability lesson (for the project's lessons log)
**Codex-debate degrades on large multi-section manuscripts inlined whole** — it pattern-matches a generic
prior and fabricates quotes. The reliable pattern is the one that worked for §4 and the grounded pass here:
(1) inline **one artifact at a time** (a single section), (2) require **verbatim-quote-or-drop**, (3) force
repo-read verification, and (4) **verify every quoted string yourself** before acting (grep the file). Never
apply a Codex manuscript finding without confirming the quote exists.

## Recommended real final gate (supersedes further hand-rolled rounds)
Use the **`manuscript-integrity`** skill from `2026-03-05-LightsOut-R01` — a Claude×Codex two-round
pre-submission sweep that verifies every number/method/figure against source data + code and checks
cross-section numeric consistency deterministically. It is purpose-built for this stage and does not depend
on the model reading a giant inline blob correctly. Precede it with `check-consistency` and
`verify-citations live` once the citation stack is ported and figures exist.
