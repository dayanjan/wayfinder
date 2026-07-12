# Round 2 — Claude's revision (accept/reject/defer per round-1 finding)

I ACCEPTED 12 of 13 and applied them to the plan file (v2). Round-1 confirmed the novel claim is NOT circular
(F-010); the rest hardened the spec. No silent drift — ledger below.

| Finding | Disposition | How the v2 plan resolves it |
|---|---|---|
| F-001 (P0) rank not conditioned on novel-at-T | **ACCEPT** | Common frame = the novel-at-T set (`ac_lit_asof≤1`); positives = establishment *within* it, so lit-rarity can't win on novelty |
| F-002 (P0) "supported-first" ill-defined | **ACCEPT** | Exact total-order specified (verdict class → as-of-T §3.2 score); ranks the whole frame; labeled an eval variant of propose.py |
| F-003 (P0) gate not "only shrink" | **ACCEPT** | Deleted the shrink-only claim; full reconstruction + report sliced frame size, overlap (Jaccard), exact positive count |
| F-004 (P1) spike didn't validate the referee-stratified frame | **ACCEPT** | 1,469 = preliminary; exact full-frame enumeration is the frozen prerequisite |
| F-005 (P1) bootstrap/non-overlap unsound | **ACCEPT** | Two-way (gene+disease) clustered **paired-difference** CI; removed the non-overlapping-CI acceptance rule |
| F-006 (P1) metric not prespecified | **ACCEPT** | ONE primary estimand frozen: `prec@20(WF) − prec@20(B-lit-rarity)`; all else secondary |
| F-007 (P1) ac_known drop changes method | **ACCEPT** | Named the **ac_known-ablated variant**; sensitivity note (leaky-vs-conservative); not claimed identical to headline |
| F-008 (P1) query construction unvalidated | **ACCEPT** | Golden-query + boundary(T-1/T/T+1) + alias tests; persisted query receipts |
| F-009 (P1) live API ≠ reproducible | **ACCEPT** | Freeze+hash (query,result,date) → committed **count manifest**; metrics recomputable without live drift |
| F-010 (P1) "prediction" wording / novel claim | **ACCEPT (clarify, preserve intent)** | Re-worded estimand = "retrospective literature time-slicing against a contemporary fixed substrate"; added a T3-label-provenance audit to rule out disease-hop literature leakage. **Claim preserved** (not circular; test it; report null straight) |
| F-011 (P1) win may be disease-hop, not 3-hop | **ACCEPT (key)** | Added **B-disease-hop-only** baseline; headline includes Wayfinder's *incremental* value over it |
| F-012 (P2) adaptive fallback = researcher DoF | **ACCEPT** | Blinded feasibility gate on **label counts only**; fixed fallback order; frame LOCKED before any performance inspection |
| F-013 (P2) "≥5" popularity-confounded | **ACCEPT** | Popularity-stratified metrics + blinded manual spot-check of a stratified label sample |

**Revised position for round 2:** with F-001/F-002/F-003 fixed, the comparison is now well-defined (one frame,
one Wayfinder total-order, exact enumeration), the inference is paired-and-clustered, the estimand is
pre-registered with a blinded feasibility gate, and the F-011 disease-hop-only baseline isolates what the
referee's own hops (QC/effect/program) add beyond the enrichment. The novel claim stands as an open, falsifiable
test with a straight-null commitment. **Round-2 asks Codex:** does anything in v2 remain a validity hole (esp. the
Wayfinder total-order definition and the T3-leakage audit), and is the frozen primary estimand the right one?
