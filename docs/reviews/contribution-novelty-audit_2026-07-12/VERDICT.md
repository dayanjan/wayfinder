# VERDICT — Contribution & novelty audit, Wayfinder manuscript
**Date:** 2026-07-12 · **Question:** does this manuscript make a real, literature-verified contribution
that moves science forward — or should it not be published?

## How this was reached
13 independent agents, mixed Claude + Codex, every load-bearing finding cross-verified by a *different*
model re-running or re-adjudicating the live literature (Europe PMC + OpenAlex + Semantic Scholar):
- **3 claim extractors** (2 Claude + 1 Codex) → 16–23 claims each, converged → `MASTER_REGISTER.md` (M1–M10, B1–B7)
- **6 Claude literature-verifiers** (real `search_all`) → `verify_{gap,prim,audit,th2,eczema,dir}.md`
- **2 adversaries** (Claude hostile lit-backed + Codex) → `adversarial_{claude,codex}.md`
- **2 Phase-D cross-checkers** (Claude fresh independent searches + Codex re-adjudication) → `crosscheck_{claude,codex}.md`

The consensus below is **unanimous** on the bottom line; dissents are recorded where they exist.

---

## BOTTOM LINE
**Do NOT publish in the current form or framing.** As a *biological discovery* paper it should not be
published — the flagship is a thin, admittedly-undischargeable locus nomination. As an *evaluated methods*
paper it should not be published — the method is demonstrated, never measured. **It is not garbage:** there
is a real, small, honest kernel, and a concrete path (below) that would make it a legitimate, modestly-novel
**methods-and-norms note**. The decision is therefore: *don't publish* (defensible, honest) **or** *reframe +
do one evaluation* (≈1–2 sessions) to earn a modest publication. Not: publish as-is.

Both adversaries and the Codex cross-adjudicator independently reached "do-not-publish-as-discovery /
major-revision-as-methods-note." No agent dissented from that.

---

## WHAT SURVIVES EVERY ATTACK (the real kernel)
1. **Method novelty as an integration (M1) — REAL but NARROW.** No surfaced system does the full chain
   (LBD front-end → *deterministic non-LLM* referee → *held, pre-existing* Perturb-seq substrate → per-hop
   *experimental* receipt → QC-abstention → falsification). Every named neighbor genuinely does something
   else (Co-Scientist/Robin run *new* experiments; PaperQA2 cites literature; PerturbQA/rbio1 score
   *prediction*). Confirmed across 20+ queries by two independent Claude searches + Codex. The "we are not
   aware of" hedge holds. **The durable wedge = "deterministic referee over a held substrate."**
2. **NAB2 → Th1/Th2 *polarization* (B1) — genuinely novel-for-polarization.** No paper places NAB2 in the
   Th1/Th2 switch. Mechanistically *foreseeable* (one hop from the documented Egr-1/NAB2 T-cell axis,
   Collins 2008; EGR2/3 are established T-cell regulators, Singh 2017) — neither already-reported nor
   surprising. A real, modest nomination.
3. **STAT6 *cis*-test (B3) — competent and honest.** Both adversaries steelmanned it and could not break it.
   A reusable deposited-data cis-artifact-falsification template. Clears the *perturbation-signal* confound
   (not the disease-label one — correctly).
4. **The calibration / honesty apparatus** — exemplary; more disciplined than most 2025–26 "AI-scientist"
   papers. Teaching value even though selective-prediction theory is old.

## WHAT DOES NOT CLEAR THE BAR
1. **The method is DEMONSTRATED, NEVER EVALUATED (FATAL for a methods paper).** No precision, recall,
   baseline, or held-out benchmark; §5.3b concedes every one as *future* work. Sharpened by →
2. **Two evaluated near-neighbors are UNCITED.**
   - **Popper — arXiv 2502.09858 (2025):** an agentic *sequential-falsification* validator for the
     *identical* LLM-hypothesis-overproduction problem, with strict Type-I error control, **empirically
     evaluated across six domains vs human scientists** (abstract confirmed, two independent pulls).
   - **VERITAS — arXiv 2604.12144 (2026):** mechanically labels outcomes **Supported / Refuted /
     Underpowered / Invalid** with a "fully auditable evidence trail," motivating *Underpowered* with the
     exact "non-significant ≠ absent effect" logic that is this paper's hero feature.
   They do **not** collapse the deterministic-referee-over-held-substrate wedge, but they **reduce M1's
   novelty to an unevaluated *implementation* distinction**, and they make abstain/refute-as-outcomes +
   receipt-per-hop **prior art** (application-only, not conceptual firsts). Must be cited and compared.
3. **The biology flagship (NAB2 → atopic eczema, B2) cannot headline a discovery.** NAB2 is not a named
   12q13 AD candidate in any prioritization paper; STAT6 is the recognized (though not cleanly fine-mapped)
   locus driver; the disease label is an uncolocalized GWAS label. The link is a **serious, unresolved
   alternative** the substrate *cannot discharge* — the paper says exactly this, so it is **honestly scoped,
   not overstated**. But a thin, unresolvable nomination is not a discovery.
4. **Method primitives (M2/M4/M8/M9/M10) are all known** (selective prediction / reject-option; grounded
   tool-use; LBD ranking; leakage avoidance; permutation controls). The paper wisely does not claim to have
   invented them — so no overstatement — but they are not the contribution.
5. **The agentic-workbench tricks (M5/M6/M7)** — language-critic self-audit, headless reproduction,
   cross-model replication lab — are well-executed **engineering/QA**, each with an active prior-art field,
   not standalone novel science. Fine as method/vehicle; must not be promoted to "contributions."

## RECORDED DISSENT / CALIBRATION (keeps the "no" honest)
- **On B2 (Codex cross-adjudicator + Claude cross-checker):** the evidence supports "NAB2 *may* be an LD
  passenger; STAT6 is the *leading alternative*" — NOT "NAB2 is *likely* a passenger" or "STAT6 is the
  *proven* fine-mapped driver" (systematic triangulation, Sobczyk 2021, did **not** resolve 12q13 to one
  gene). Abstract-level search absence ≠ proven absence. The manuscript's hedge is accurate.
- **On B1:** "novel-for-NAB2" full-stop is loose — NAB2 has a documented T-cell role (Egr-1/NAB2 axis). The
  accurate, stronger claim is "absent from the Th1/Th2 *polarization* literature." Cite the EGR axis.
- **On B3 geometry:** "43 kb makes *cis*-spread unlikely" is *literature-plausible, not proven safe*
  (KRAB/KAP1 can repress long-range; Lensch 2022 shows spread crosses insulators). The paper leans on the
  empirical null, not geometry — correctly — so it is not overstated.
- All negatives are "not surfaced in N queries," not proofs of absence (abstracts read, not full
  supplementary locus tables).

---

## THE PATH FROM "NO" → "YES" (a modest but real publication)
If the goal is to publish honestly rather than not at all, the minimum that converts this into a legitimate
**methods-and-norms note** (in priority order):
1. **Do ONE §5.3b evaluation** — the single highest-value move. Either a *time-sliced held-out* eval
   (freeze literature at a cutoff; measure precision@k / recall on post-cutoff gene→program→disease links)
   or an *external known-true/known-false panel* scored for false-refutation and false-abstention rates on
   the *refuted*/*untested* classes. This converts "demonstrated" → "measured." ~1–2 sessions.
2. **Cite + compare Popper (2502.09858) and VERITAS (2604.12144);** reframe abstain/refute/receipts as
   *application/instantiation* of a known primitive; keep "deterministic referee over held substrate" as the
   wedge. (Add MOOSE-Chem3 2505.17873 for completeness.)
3. **Reframe from discovery → methods/norms note:** NAB2 becomes the illustrative worked example (with the
   EGR2/3 adjacency cited), not the headline; the headline is the triage method + honesty apparatus.
4. **Add the minor citations flagged:** selective-prediction/reject-option (for the abstention primitive);
   ML-leakage (for the answer-free construction); the long-range-KRAB paper (as the cis counter-consideration).
5. For the *biological* headline to stand as discovery would require the 12q13 variant-level colocalization
   **and** a prospective NAB2 perturbation — both named as future work, i.e. not achievable within this paper.

## Files
`PLAN.md` · `MASTER_REGISTER.md` · `extract_{claude_1,claude_2,codex}.md` ·
`verify_{gap,prim,audit,th2,eczema,dir}.md` · `adversarial_{claude,codex}.md` ·
`crosscheck_{claude,codex}.md` · this `VERDICT.md`.
