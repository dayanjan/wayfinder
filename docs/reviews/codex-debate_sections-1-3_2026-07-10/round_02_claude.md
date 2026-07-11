# Round 2 — Claude's revision (all 14 round-1 findings accepted + applied)

All 14 findings **accepted** and folded into the section files (prose v2). Disposition table is in
`round_01_codex.md`. The novel claims were preserved; each fix scoped a claim, none removed one. Highlights:

- **F-004 (verified in code):** `ac_known` reworded to Open Targets *overall* target–disease association
  score (a known-link/novelty prior), explicitly separated from the T3 disease labels (which the source
  study derives from genetic evidence). §3.1 + §3.2.
- **F-001:** §1 close + §2.1 now state plainly that the method closes the *triage* loop, not the
  experimental-follow-up loop; "true in fresh experimental data" → "supported by independent experimental
  data it has not seen."
- **F-003:** §1 NAB2 sentence + §3.3 hop-3 now keep the disease hop an association nomination, and the
  STAT6 falsification is scoped to a *cis-artifact explanation of the perturbation signal* — strengthening
  NAB2-specificity, not proving the disease link.
- **F-005:** §3.3 concedes that within the funnel hops 0–2 are pre-gated (dominant cull = disease-C), and
  points the broad four-hop discrimination to the out-of-funnel ledger (§4).
- **F-006:** "supported" defined as a bounded verdict label; the calibration claim scoped to
  manuscript-facing output with the legacy "validated" log acknowledged.
- **F-008:** the no-API driver now carries its guardrails (operator session, fixed workspace, logged
  approvals, confined network, guard-protected receipts); "honest substitute" dropped.
- Plus F-002/007/009/010/011/012/013/014 as tabled.

## Revised position (what I now defend)
The three novel claims stand, each now scoped so a hostile FRMA/LBD reviewer's first attacks are pre-empted
in the prose itself: (1) the agentic loop closes the *triage* loop (explicitly not experimental follow-up);
(2) the confident receipt-backed NO is demonstrated by demotions/exact-C refutations *and* the out-of-funnel
ledger, with "supported" a bounded label and the disease hop an association nomination; (3) the self-audit
is role/model/checkpoint independence over manuscript-facing output (legacy logs acknowledged), and the
no-API driver is reproducibility engineering with an inspectable consent trail, not a safety bypass.

## What I want round 2 to press
- **Verify against the FILE** that each fix landed and reads cleanly (doctrine: verify the file, not this
  prose). Flag any fix I claimed but did not land, or any that introduced a new inconsistency.
- **Over-correction check (preserve-intent both ways):** did any concession (esp. F-005's funnel/ledger
  split, F-008's guardrails, F-006's scoping) go so far it now *under*-sells a real strength or reads as
  defensive? The novel claims must stay sharp.
- **New gaps** exposed by the heavier honesty prose — especially whether §3.3 is now too long/hedged, and
  whether the §1 demonstration paragraph still flows after absorbing three fixes.
- Any remaining sentence where "approach" slips to "product", the disease hop reads experimental, or the
  self-audit reads cross-vendor.
