# NEXT_SESSION — async handoff (canonical; written/read by session-closer & session-start)

## 🧭 READ-FIRST (anti-amnesia — do not skip)
Before ANY claim audit, review, referee-response, revision, or new experiment, read
**`docs/CLAIMS_EVIDENCE_LEDGER.md`** — the single living index of claim → status → evidence → source → critique.
**Rule:** reconcile every claim against BOTH the literature AND the experiment corpus it indexes.

## 🚀 SUBMISSION FIRE-READY — still governs (unchanged)
The Wayfinder hackathon submission remains BUILT + staged. On operator **"scrub and flip"**: run
`SUBMIT_CHECKLIST.md` steps 1–5 → flip `dayanjan/wayfinder` public → hand back the URL. Facts: `docs/HACKATHON.md`.

---

## Next session priorities — written 2026-07-12 (full-close, autonomous G1 build)

**Current state**: **G1 (the held-out evaluation = the manuscript's publish gate) is BUILT, RUN, and
INTEGRATED.** The audit's central FATAL — "method demonstrated, never measured" — is **CLOSED**: the method is
now *measured*, and the honest result is a **NULL at the pre-registered primary metric**, reported straight in
new **§4.7 + Fig 5**. Manuscript compiles clean (**34 pp, 0 errors**). Full audit trail:
`docs/g1-build-log_2026-07-12.md`. Commits `8858d67`→`a3f3141`, all pushed; tree clean.

**G1 result (for context)**: frame 22,437 novel-at-2016 pairs, 5,570 positives (24.8%). C_broad (Wayfinder−lit-
rarity) +0.20 [−0.20,+0.65]; C_mech (Wayfinder−disease-hop-only) −0.15 [−0.35,+0.30]; joint `broad_null`, robust
across k=3/k=5/pure-disjoint. Wayfinder leads on secondary p@5 (0.80) + MAP (0.287) but not the primary; disease-
hop-only matches/beats it at p@20 — the measured face of §4.1b's substrate-inherited stringency.

**DONE 2026-07-13** (the 3 prior next-moves): (1) the 9 manuscript honesty fixes — 5 applied + 4 already
resolved, verified; (2) contribution reframe — abstract + §1 now state the method is *measured* (null reported
straight), "evaluated honestly rather than asserted"; (3) CS metric-verification ATTEMPTED but the headless
drive didn't converge (driver fragility) → **fell back to an independent local recompute** (fresh code path
confirms C_broad +0.20 / C_mech −0.15) + codex code-review + reproducibility + unit tests. Manuscript **35 pp,
0 errors**. Commits `a695c43`, `8f1cb3d`.

**ALSO DONE 2026-07-13:** **CS corroboration OBTAINED** (blind + headless; the driver fix = target an existing
frame URL, persisted to auto-memory `cs-driving-method` + the skill's known-limitations) — §4.7 carries it,
result at `data/eval_out/cs_verify_result.json`. **G3 DONE** — frozen EGR-distinctness receipt
`docs/manuscript/analysis/egr_distinctness_results.json` (`opposition_confirmed=true`); §4.3 leads with the
NAB1 paralog-opposition D3 fact; ledger R5 → SUPPORTED-BY-EXP. Manuscript 35 pp, 0 errors. Commits through `e09dfe2`.

**Next action** (pick one; ordered by value):
1. **Re-assess publishability** now that G1 is measured (the audit's "do not publish until measured" is
   satisfied) and R5 has a receipt: decide whether the paper is submission-ready as an evaluated-methods paper
   with an honest null, or whether to strengthen (external ground-truth panel / larger disease panel) first. **[CLAUDE]**
2. **Frontiers/FRMA submission formatting** — the current build uses the LightsOut LaTeX template; convert to the
   venue's format if submitting. **[CLAUDE]**
3. **G2 eQTL-existence spike** — does a NAB2 CD4⁺ cis-eQTL exist (gates whether B5/12q13 is resolvable)? **[CODEX-SPIKE then CLAUDE]**

**Prerequisites**: none blocking. Manuscript compiles via 4-pass `pdflatex; bibtex main; pdflatex; pdflatex`
(latexmk broken). CS up on :8000 if pursuing #3.

**Open questions**: does the null survive an external ground-truth panel + a larger (>12) disease panel (raises
power)? Given G1 is now measured, is the paper publishable as-is (audit's "do not publish until measured" is met)?

**Do not touch**: submission artifacts / demo video (fire-ready; "scrub and flip"). The committed G1 receipts
(`data/eval_out/count_manifest_full_T2016_k5.json`, `eval_results_T2016_k5.json`, `sensitivity.json`) and the
dated audit/reconciliation/debate records are IMMUTABLE — cite, don't edit; update `CLAIMS_EVIDENCE_LEDGER.md`.

**Context to preload** (≤10): `docs/g1-build-log_2026-07-12.md`; `docs/CLAIMS_EVIDENCE_LEDGER.md`;
`docs/manuscript/latex/sections/04_results.tex` (§4.7); `data/eval_out/SUMMARY.md`;
`docs/claims-vs-experiments_2026-07-12/NEW_EXPERIMENTS.md`; `docs/reviews/diff_g1-harness_2026-07-12.md`;
`src/arbiter/eval/`; `memory/NEXT_SESSION.md`.

**Estimated budget**: honesty fixes ≈ ½ session; contribution reframe ≈ ½ session; CS verify ≈ ½–1 session.

## Mirror of this handoff is appended to memory/sessions/2026-07-12.md by session-closer.
