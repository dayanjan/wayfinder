# Codex-debate synthesis — G1 held-out-eval implementation plan (2026-07-12)
Repo-read, read-only, `--preserve-intent`, 3 rounds. Artifact:
`docs/plans/heldout-eval-implementation-plan_2026-07-12.md` (now v3). Per-round trail:
`docs/reviews/codex-debate_heldout-eval-plan_2026-07-12/round_0{1,2,3}_{claude,codex}.{md,json}`.

## Framing question
Is the time-sliced held-out-eval plan a valid, buildable, **decision-quality** spec — in particular, (Q1) is
"Wayfinder = referee-supported-first" a circular leak that trivially beats literature-rarity, and (Q2) does
dropping `ac_known` bias the comparison?

## Outcome: CONVERGED at round 3, repo-verified, novel claim preserved (no sanding).
- **Q1 answered:** the design is **NOT circular** — Codex confirmed (F-010, both rounds) that the fixed-2025
  Perturb-seq signal and the post-2016 Europe PMC outcome labels are genuinely distinct; the referee never sees
  the outcome label.
- **Q2 answered:** dropping `ac_known` is the conservative (leak-avoiding) choice; now handled as an explicitly
  named **`ac_known`-ablated variant** with a sensitivity note (F-007), not claimed identical to the headline pipeline.

## Trajectory
- **R1** — Claude proposed the eval. Codex: 13 findings — "not circular, but the spec is materially
  underspecified" (ranking population, Wayfinder comparator, gate reconstruction, inference, reproducibility).
- **R2** — Claude accepted 12/13 → plan v2. Codex **dropped 11** (fixed), **escalated 2** repo-verified
  (F-002 verdict order omitted `refuted_program`; F-011 disease-hop baseline not executable — multiple T3 rows
  per pair), **surfaced F-014** (the incremental contrast needs a frozen decision role).
- **R3** — Claude applied all 3 → plan v3. Codex **converged**: verdict enum + disease-hop collapse now match
  `referee_triple.py`; co-primary rule closes F-014. No new findings, no escalations.

## Convergent findings (what the debate added — all repo-checked)
1. **Rank within the novel-at-T frame** (F-001) — else lit-rarity wins on the novelty component. Core validity fix.
2. **One exhaustive Wayfinder total-order** over the whole frame (F-002) — 8 verdict classes incl. `refuted_program`.
3. **No "gate only shrinks" assumption** (F-003) — full enumeration + report the sliced frame/overlap/positive count.
4. **B-disease-hop-only baseline** mirroring `_hop3_for_disease` (F-011) — isolates what the QC/effect/program
   hops add beyond the GWAS disease enrichment (the sharpest scientific catch).
5. **Two co-primary contrasts with a frozen joint-outcome interpretation** (F-014) — a disease-hop-carried win
   cannot be spun as a three-hop success.
6. **Gene+disease two-way-clustered paired-difference CIs**, one pre-registered primary estimand, blinded
   feasibility gate (F-005/F-006/F-012); **query-integrity tests + a committed count manifest** for real
   reproducibility (F-008/F-009); **popularity-stratified labels** (F-013); estimand reworded to *retrospective
   literature time-slicing against a contemporary fixed substrate* + a T3-label-provenance leakage audit (F-010).

## Persistent disagreements
**None.** Clean convergence.

## Preserve-intent / novelty-preservation check
The novel claim — *a fixed experimental substrate recovers currently-novel gene→program→disease links that
become literature-established later, better than literature-rarity, with an honest-null commitment* — is
**intact and unsanded**. Codex set no `convergence_sanding_warning`, explicitly kept it "an open empirical
question," and the co-primary rule + straight-null commitment *strengthen* rather than dilute it. Convergence
here is genuine (repo-verified fixes), not sycophantic.

## Recommended next move
Build G1 to v3. Order: (1) CS-driver health-check; (2) enumerate the novel-at-T frame + count manifest + blinded
feasibility gate; (3) implement the 6 rankers (Wayfinder 8-class order + B-disease-hop-only collapse) + the two
co-primary contrasts with clustered paired CIs; (4) run in Claude Science (native) with reviewer verification, or
locally-and-say-so; (5) §4 paragraph + figure, null reported straight. Delegation: build = [CODEX-RESCUE] against
v3 (a debate-hardened spec should land near one-shot); integration + manuscript = [CLAUDE].
