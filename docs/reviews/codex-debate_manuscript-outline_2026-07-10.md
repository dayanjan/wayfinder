# Codex debate — Wayfinder manuscript outline (3 rounds, repo-read, --preserve-intent)

**Date:** 2026-07-10 · **Artifact:** `docs/manuscript/OUTLINE.md` (now v1.2, build-ready) ·
**Mode:** repo-read (Codex opened source files to verify claims against reality, doctrine §22) ·
**Rounds:** 3 · **Result:** CONVERGED, zero sanding of novel claims.

## Framing question
Is the outline the strongest, most honest, most reviewer-proof, internally self-consistent plan for a
methods+demonstration paper for *Frontiers in Research Metrics and Analytics* — and does every
quantitative claim (§7, C1–C25) hold against the repo?

## Trajectory
| Round | Codex findings | Disposition |
|-------|----------------|-------------|
| 1 | 10 (2×P0, 3×P1, 5×P2) | all accepted → v1.1 |
| 2 | 5 open (4 escalated stale-headline + 1 new F-011), 5 dropped | all accepted → v1.2 |
| 3 | 1 (F-012, P2 trivial title-version) | fixed; **converged** |

Finding-count trajectory 10 → 5 → 1; no pushbacks (every finding was repo-verified and cheap to
accept — the §22 specification-completion pattern). Codex **verified C1–C21 hold** against primary
JSON/receipt artifacts.

## The two paper-blocking corrections (round 1, P0)
1. **Dataset DOI conflict → resolved.** Crossref API confirms `10.64898/2025.12.23.696273` is the
   registered bioRxiv/openRxiv DOI; the `10.1101/…` form our `references/README.md` carried is a 404.
   Fixed the repo file + outline; captured the exact source-paper title (Zhu, Dann, Yan, … Marson).
2. **CTLA4 ledger mis-source → fixed.** In the *cited* `perturbseq-qc` source CTLA4 is **supported**,
   not refuted (its refutation lives in a different Rest-condition artifact). CTLA4 dropped from the
   headline ledger; **SLC1A5** is the sole, correctly-sourced refuted exemplar.

## The substantive honesty-scoping wins (rounds 1–2)
- Disease hop = **association/enrichment receipt** (GWAS-genetic nomination), NOT part of the "held
  experimental substrate" — corrected in both §2.2 and the §0 headline.
- **CS liveness** split into three never-blurred claims: full sweep = *cached-receipt replay*; live
  authorship = *12-gene microsweep* (NAB2 absent → no cherry-pick); cross-model independence = *external*.
- **Program-hop tautology** (A-universe preselects program-significant genes) surfaced into
  Methods/Results, not buried in Limitations.
- **Self-audit independence** operationalized: Opus-author vs. Sonnet-critic = role/model/checkpoint
  independence; cross-vendor independence is Codex's external role.
- **Ledger** reframed from "proves discrimination" to "*demonstrates* on worked examples, not a
  validated accuracy benchmark."
- **F-011 (pre/post-critic language):** the Stage-1 receipt JSON still says "validated" (the exact word
  the critic later removed). Rule: cite Stage-1 JSON for *numbers only*, post-critic Stage-5 receipt for
  *prose* — the pre→post-critic diff **is** the self-audit evidence (Fig 5). A liability made a strength.
- **R01 answer** scoped to "automated follow-up *triage/adjudication* against a held substrate," not a
  replacement for prospective wet-lab.

## Preserve-intent (both directions)
The three novel claims — (1) agentic workbench closes the LBD *triage* loop; (2) confident, receipt-backed
NO; (3) role/model/checkpoint self-audit — **survived all three rounds sharp**, `convergence_sanding_
warning: null` every round. Every fix calibrated a claim's *scope*, none removed a claim, and round 3's
both-ways check found no claim now *under*-stated.

## Persistent disagreements
None. Full convergence with no residual P0/P1.

## One open operator decision (not a debate finding — a strengthening)
**§8.2 — add a small negative-control / discrimination panel?** (failed-KD genes → all *untested*;
label-shuffled disease → refutation rate.) Upgrades the ledger from *demonstration* to a modest
*sensitivity result* and directly blunts F-003's "the ledger isn't a benchmark." Bounded new CS
analysis. Recommendation: light **yes**.

## Recommended next move
The outline is build-ready. Next: (a) operator decides §8.2; (b) drop the citation-resolver task card
`[CODEX-RESCUE]`; (c) begin drafting §1 (Introduction) on the main thread → CS actor-critic review; OR
(d) de-risk the CS figure path early by generating the first Fig-4 data figure in the CS kernel.
A **second codex-debate on the full draft** is planned before submission (checks prose overclaim,
figure-label calibration per F-007, citation completeness — things this outline debate structurally cannot).

Per-round artifacts: `docs/reviews/codex-debate_manuscript-outline_2026-07-10/round_0{1,2,3}_{claude,codex}.{md,json}`.
