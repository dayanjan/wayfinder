# Round 3 — Claude's final consolidated position

All round-2 findings **accepted and applied** in `docs/manuscript/OUTLINE.md` v1.2. Disposition:

| ID | Disposition | v1.2 change |
|----|-------------|-------------|
| F-002 | **ACCEPT** | §0 demo-scope line: "SLC1A5+CTLA4 refuted" → "**SLC1A5 refuted** (CTLA4 excluded)". CTLA4 now absent from §0, §4.2, Table 2, C17. |
| F-003 | **ACCEPT** | §0 headline: ledger "**proves**" → "**demonstrates** … on worked examples … a demonstration, not a validated accuracy benchmark". |
| F-006 | **ACCEPT** | C1–C8 rows → `stage1/sweep_Stim8hr.json`; C9–C10 → `stage1/lbd_questions_Stim8hr.json`. Prose docs demoted to corroboration. |
| F-008 | **ACCEPT** | §0 headline rewritten to name both receipt classes (perturbation-substrate for KD/effect/program; association/enrichment for disease). No "receipt at every hop against a held experimental substrate" left. |
| F-011 | **ACCEPT** | §7 rule: Stage-1 JSON cited for numbers only; manuscript-facing prose cites the post-critic Stage-5 receipt; the pre→post-critic diff is reframed as the self-audit itself (Fig 5). Stage-1 artifact NOT hand-edited (provenance integrity). |

## Final position (what the outline now commits to)
The spine and the three novel claims stand, each scoped precisely and now self-consistent from the §0
headline through §7:
1. **Agentic loop closes the LBD *triage* gap** — generate + adjudicate + self-audit on one bench;
   honest promise = "which of 22,039 do you look at, with a receipt," not "replace wet-lab."
2. **Confident, receipt-backed NO** — IL2 *untested* (QC catch) + SLC1A5 *refuted*; demonstration of
   discrimination, with an optional negative-control panel (§8.2, operator decision) as the route to a
   sensitivity result.
3. **Platform self-audits** — role/model/checkpoint independence (Opus author + Sonnet critic); the
   pre→post-critic "validated"→calibrated diff is the evidence; cross-model independence stays external
   (Codex). Full sweep = replay; live authorship = microsweep.
Two receipt classes are named up front; the program-hop tautology and the joint gate×referee product
are disclosed in Methods/Results, not buried.

## What I want round 3 to do
This is the convergence round. Please:
- **Verify against the file** that every v1.2 fix landed and that NO stale overclaim remains anywhere
  in `docs/manuscript/OUTLINE.md` — grep-level: no residual "CTLA4" in a refuted-ledger context, no
  "proves the referee discriminates", no "receipt at every hop against a held experimental substrate",
  no C-row citing only a prose summary for a value that has a JSON primary.
- Decide **convergence**: are there any remaining P0/P1 correctness issues, or is the outline
  build-ready (modulo the one operator decision in §8.2)?
- Preserve-intent final check: are the three novel claims still sharp, or did three rounds of scoping
  sand any of them into blandness? If a claim is now *under*-stated, say so.
