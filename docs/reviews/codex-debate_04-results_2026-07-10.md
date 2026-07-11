# Codex debate — §4 Results (3 rounds, repo-read, --preserve-intent) — 2026-07-10

**Framing question.** Is §4 Results maximally rigorous, honest, and defensible to a hostile FRMA/LBD
reviewer — every quantitative claim traceable to a primary artifact, language calibrated, and the Control-2
"substrate-inherited stringency" reading correct on *both* tails?

**Method.** 3-round Claude ↔ Codex debate, Codex running `-s read-only` **from the repo** and instructed to
verify every claim against the actual artifacts (doctrine §22). `--preserve-intent` protected three claims:
the falsification thesis, the honest Control-2 reading, and role/model/checkpoint self-audit. Per-round
artifacts in `codex-debate_04-results_2026-07-10/round_0{1,2,3}_{claude,codex}.*`.

## Trajectory: 10 → 1 → 1 (converged)

| Round | Codex findings | Disposition |
|---|---|---|
| 1 | **10** (2×P1 correctness, 3×P1, 5×P2), all repo-verified | Claude accepted all 10 |
| 2 | dropped all 10 (verified fixed in files); **1 new** (F-011) | Claude accepted F-011 |
| 3 | dropped all 10; escalated F-011 → **1 new** (F-012, a code-comment nit) | Claude accepted F-012 |

No `convergence_sanding_warning` fired in any round. The debate converged on substance by round 2; rounds
2–3 only chased the Control-2 mechanism claim down to a code comment.

## What the debate changed (all fixes verified in the files)

**The load-bearing catch (F-001 + F-002 + F-011 + F-012 — the Control-2 chain).** Round 1's draft claimed
the label-shuffle showed the disease hop "concentrates on fewer diseases per gene" and called the departure
"significant" while the stored `empirical_p` was **1.0**. Codex caught both: the mechanism was an unproven
just-so story, and the stored p was the *upper* tail (the wrong one for the prose). Response was a **data
fix**, not a hedge: `sensitivity_panel.py` was extended to emit `signed_z = −5.645`,
`empirical_p_lower = 0.0005`, `empirical_p_two_sided = 0.001`, and a per-gene disease-cardinality
decomposition — which **disproved the strong mechanism claim** (2.39 true vs. 2.44 null: the concentration
effect is real but small). §4 now asserts only what the artifact measures: substrate-inherited stringency
(null pass rate 0.99%) + label-dependence (lower-tail p ≈ 5×10⁻⁴), with the cardinality figure reported but
not interpreted. The enhanced panel re-reproduced **delta-0 in Claude Science** (sha `49797eae`).

**Calibrated-language own-goals.** F-004: "polarity marker-**validated**" in §4.3 — the banned word, inside
the section that makes calibrated language a result — → "marker-checked". F-008: §1 said the stringency
"**proves** largely inherited" (introduced by an earlier softening edit) → "is largely inherited".

**Scope tightening.** F-005: the STAT6 cis-refutation now rejects only the *cluster-membership* locus
artifact, explicitly leaving the GWAS-label LD question open. F-006: replication scoped to lab-level, not
per-agent-per-number. F-009/F-010: "the rate" and the §4.4 corroborations given precise provenance. F-007:
"five results" → "six".

## Persistent disagreements
None. Every finding was accepted and fixed; the last was a P2 code comment.

## Preserve-intent check (novelty preservation)
All three protected claims survived intact and were **sharpened, not sanded**: the falsification thesis is
unchanged; the Control-2 honesty moved from an overclaimed "rarer-than-chance selectivity" toward a
strictly-defensible "substrate-inherited stringency + label-dependence"; the self-audit remains
role/model/checkpoint (not cross-vendor). The debate made §4 *more* conservative, not more consensual.

## Recommended next move
§4 is submission-ready on the axes tested. The remaining manuscript work is orthogonal: figures (Fig 4 hero
chain + a §4.1b sensitivity panel from the CS kernel), the citation resolver, and a full-draft debate across
§1–§5 before submission (which will also re-check §4-in-context). No spike needed.
