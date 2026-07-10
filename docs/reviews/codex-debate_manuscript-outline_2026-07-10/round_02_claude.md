# Round 2 — Claude's revision (accept / reject / defer on every round-1 finding)

All 10 round-1 findings **accepted** and folded into `docs/manuscript/OUTLINE.md` (v1.1). The novel
claims were preserved; each fix calibrated a claim's *scope*, not its existence. Disposition:

| ID | Disposition | What changed in the outline |
|----|-------------|-----------------------------|
| F-001 | **ACCEPT → RESOLVED** | DOI verified via Crossref API: `10.64898/2025.12.23.696273` is registered; `10.1101/…` is 404. Fixed `references/README.md` in-repo; C23 now RESOLVED; C22 carries the exact title + authors (Zhu, Dann, Yan, … Marson). |
| F-002 | **ACCEPT** | CTLA4 dropped from the ledger (§4.2, Table 2, C17). SLC1A5 is now the sole refuted exemplar, correctly sourced to `perturbseq-qc/pyzobot_referee_results.md`. CTLA4-at-Rest noted as available-with-scope but not used. |
| F-003 | **ACCEPT** | §4.1 reframed: ledger = *demonstration evidence*, explicitly NOT a precision/recall benchmark. Added a negative-control panel as an operator-decision strengthening (§8.2). |
| F-004 | **ACCEPT** | Program-hop tautology surfaced into §3.3 (Methods) and restated in §4.1 (Results), not only Limitations. |
| F-005 | **ACCEPT** | §3.4 now keeps three liveness claims distinct: full-scale sweep = cached-receipt replay (guard delta 0); live authorship = 12-gene microsweep (NAB2 absent, no cherry-pick); cross-model independence = external. §4.5 echoes it. |
| F-006 | **ACCEPT** | §7 header adds the "cite the primary JSON/receipt artifact" rule + a primary-artifact map; C15/C16 repointed to `stage3/stage3_cis.json`+`receipt.md`. |
| F-007 | **ACCEPT** | §4.5 meta-discipline: manuscript-facing verdicts/labels use "refuted"/"consistent with NAB2 perturbation"/"nomination", never "definitive"/"genuine"/"proven". |
| F-008 | **ACCEPT** | §2.2 retitled + reframed: substrate (experimental) for KD/effect/program hops; association/enrichment receipt (GWAS-genetic, no coloc) for the disease hop; "oracle" removed. |
| F-009 | **ACCEPT** | §3.4 + §4.5 operationalize independence: Opus-author vs. Sonnet-critic = role/model/checkpoint independence; cross-vendor independence is Codex's external role, not claimed CS-native. |
| F-010 | **ACCEPT** | §5.1 scopes the R01 answer to "automated follow-up *triage/adjudication* against a held substrate," NOT a replacement for prospective experimental follow-up. |

## Revised position (what I am now defending)
The spine is unchanged and the three novel claims stand, now scoped precisely:
1. **The agentic loop closes the LBD *triage* gap** — generate + adjudicate + self-audit on one bench;
   the honest promise is "which of 22,039 do you look at, with a receipt," not "we replace wet-lab."
2. **The confident, receipt-backed NO** — IL2 *untested* (QC catch) + SLC1A5 *refuted*; framed as
   demonstration of discrimination, with an optional negative-control panel to make it a sensitivity
   result.
3. **The platform self-audits** — role/model/checkpoint independence (Opus author + independent Sonnet
   critic), with cross-model independence kept external (Codex). The full sweep is honestly a replay;
   live authorship is the microsweep.

## What I want round 2 to press
- Are any of the SCOPING edits themselves now *under*-claiming — i.e., did I sand off a real strength
  (preserve-intent works both ways)? Specifically: is the "demonstration not benchmark" framing (F-003)
  too modest given the funnel + confounder + replication evidence actually present?
- Re-read the UPDATED `docs/manuscript/OUTLINE.md` (v1.1) and confirm the fixes are actually in the file
  (doctrine: verify against the file, not this prose). Flag any fix I claimed but did not land.
- New gaps exposed by the revision, especially in §3.4's three-liveness-claim split and §2.2's two
  receipt classes — did tightening one create an inconsistency elsewhere (e.g., does any later section
  still call the disease hop experimental, or still imply the full sweep was live)?
