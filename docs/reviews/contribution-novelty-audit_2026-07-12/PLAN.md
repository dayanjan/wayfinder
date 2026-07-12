# Contribution & novelty audit — Wayfinder manuscript (2026-07-12)

**Operator ask:** an independent, honest, mixed-model, adversarial, literature-backed
verdict on whether this manuscript makes a real contribution that moves science forward.
"If it is none, that is fine too and we won't publish. There is enough garbage out there."

**Method:** map every claim presented as novel/a contribution → run REAL literature searches
per claim (repo `src.arbiter.lit.search.search_all`, live Europe PMC / OpenAlex / Semantic
Scholar via .env) → adversarial attack → cross-model verify (every finding re-checked by a
different model re-running the literature).

## Deliverable to read
`docs/manuscript/latex/main.pdf` (32pp). Sections: abstract + `sections/0{1..5}_*.tex`.

## The two claim families under test
1. **Method novelty** — "deterministic, non-LLM referee scoring each hypothesis against a
   HELD, pre-existing experimental substrate, per-hop EXPERIMENTAL receipt for every edge,
   QC-gated ABSTENTION (failed knockdown = untested, not negative), FALSIFICATION as a
   first-class verdict." Claimed distinct from: Google AI co-scientist (gottweis2025),
   FutureHouse Robin/PaperQA2 (robin2025, paperqa2024), SciAgents (sciagents2025),
   Coscientist/Boiko (boiko2023), The AI Scientist (aiscientist2024), PerturbQA
   (perturbqa2025), "Plausibility is not prediction" (plausibility2026).
2. **Biology novelty** — NAB2 → Th1/Th2 → atopic eczema is literature-novel; STAT6 *cis*-effect
   ruled out at expression level; 12q13 LD confounder foregrounded-not-discharged; NAB2 direction
   (Th2 brake) exploratory.

## Phases & status
- [ ] A — claim extraction: 2 Claude + 1 Codex, independent → master register (MAIN merges)
- [ ] B — literature-backed novelty verification, per claim (Claude agents run search_all)
- [ ] C — adversarial: codex-adversarial + Claude hostile reviewer (lit-backed attacks)
- [ ] D — cross-verification: each B/C finding re-checked by a DIFFERENT model
- [ ] E — MAIN synthesis: honest publish / don't-publish verdict

## Constraint
Codex sandbox = no live network. Live searching → Claude agents. Codex = cross-model
extraction + adversarial reasoning + re-adjudication of the ACTUAL retrieved papers, and
names missed queries for a Claude agent to run.

## Outputs land here
`docs/reviews/contribution-novelty-audit_2026-07-12/`
- `extract_claude_1.md`, `extract_claude_2.md`, `extract_codex.md`
- `MASTER_REGISTER.md` (MAIN)
- `verify_<claim-id>.md` (Phase B)
- `adversarial_codex.md`, `adversarial_claude.md` (Phase C)
- `crosscheck_<finding-id>.md` (Phase D)
- `VERDICT.md` (Phase E, MAIN)
