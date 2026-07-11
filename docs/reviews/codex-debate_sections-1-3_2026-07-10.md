# Codex debate — Wayfinder manuscript sections 1-3 (prose, 3 rounds, repo-read, --preserve-intent)

**Date:** 2026-07-10 · **Artifact:** `docs/manuscript/sections/0{1,2,3}_*.md` (now prose v2.1, build-ready) ·
**Mode:** repo-read (Codex opened the section files + repo artifacts + code, doctrine §22) ·
**Rounds:** 3 · **Result:** CONVERGED (14 → 4 → 0), zero sanding of novel claims.

## Framing question
Are the drafted sections 1-3 the strongest, most honest, most reviewer-proof PROSE for an FRMA
methods+demonstration paper — sound argument, consistent framing (approach-not-product; two receipt
classes), calibrated language, surviving a hostile LBD-community reviewer?

## Trajectory
| Round | Findings | Disposition |
|-------|----------|-------------|
| 1 | 14 (P0: F-001, F-003, F-004, F-006; P1: F-002/005/007/008/009; P2: F-010/011/012/013/014) | all accepted → v2 |
| 2 | dropped 12, escalated F-003/F-014, new F-015/F-016 | all accepted → v2.1 |
| 3 | 0 findings — **converged** | — |

This was distinct from the outline debate and the CS number-check: the CS pass verified *numbers*; this
debate attacked *argument, framing, and prose overclaim*. It caught what a number-check structurally cannot.

## The load-bearing catches
- **F-004 (P0, code-verified):** Codex opened `src/arbiter/lbd/sources.py` and found `ac_known` uses the
  Open Targets **overall** target–disease association score, not a genetics-only subset — so "genetic-
  association score" was factually wrong. Corrected in §3.1/§3.2, and separated from the T3 genetic disease
  labels (which come from the source study). A real error the manuscript would have shipped.
- **F-001 (P0):** the R01 critique is about hypotheses *not being followed up*; the prose sometimes sounded
  like retrospective lookup *is* follow-up. Now closes the **triage** loop explicitly, not the follow-up loop.
- **F-003 (P0):** the STAT6 falsification is now scoped to *a cis-artifact of the perturbation signal* —
  strengthening NAB2-specificity, not proving the disease link; the disease hop reads as an association
  nomination everywhere.
- **F-005 (P1):** conceded that within the funnel hops 0–2 are pre-gated (dominant cull = disease-C), with
  broad four-hop discrimination shown by the out-of-funnel ledger (§4) — the honest confident-NO.
- **F-006 (P0/P1):** "supported" is now a bounded verdict label; the self-audit's calibrated-language claim
  is scoped to manuscript-facing output, with the legacy "validated" generation log acknowledged.
- **F-008 (P1):** the no-API driver now reads as reproducibility engineering with an inspectable consent
  trail (operator session, fixed workspace, logged approvals, guard-protected receipts), not a safety bypass.

## Preserve-intent (both directions)
`convergence_sanding_warning: null` every round. Two rounds of substantial honesty/scoping edits did not
sand the three novel claims (agentic triage loop; confident receipt-backed NO; role/model/checkpoint
self-audit) or the no-API-driver element — round 3's both-ways check confirmed they stayed sharp.

## Persistent disagreements
None. Full convergence, 0 residual findings.

## Notes carried forward
- The label-shuffle null (§1) is now a non-quantified preview; **§4 must define the actual null
  distribution** when the negative-control panel is built (§4.1b).
- **§3.2 promises "rank stability under alternative weights in Section 4"** — §4 must deliver that
  sensitivity check (or the promise must be softened).
- The outline (`OUTLINE.md` §4.1b / §8.2) still says the panel's label-shuffle "rises to ~chance"; align it
  with the §1 "null pass rate" wording when building §4.

## Recommended next move
Sections 1-3 are build-ready. Draft **§4 (Results)** and **§5 (Discussion)** in the validated voice, honor
the two §4 promises above, then run the planned **full-draft debate** + figures + citation resolver.

Per-round artifacts: `docs/reviews/codex-debate_sections-1-3_2026-07-10/round_0{1,2,3}_{claude,codex}.{md,json}`.
