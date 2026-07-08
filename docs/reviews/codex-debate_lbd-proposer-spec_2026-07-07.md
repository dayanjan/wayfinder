# Codex-debate synthesis — LBD question-proposer spec (v1 → v2)

**Artifact:** `docs/lbd-proposer-spec.md` · **Rounds:** 3 (repo-read, `-s read-only`) ·
**Date:** 2026-07-07 · **Preserve-intent:** ON (held — no sanding) ·
**Per-round artifacts:** `docs/reviews/codex-debate_lbd-proposer-spec_2026-07-07/round_*`

## Framing question
Is the LBD proposer spec the shortest *correct* path to a receipt-backed, condition-specific
**novel** finding by July 13 — and do its load-bearing claims hold up against the actual referee
code + CSVs in this repo? Plus (round 2+): after constraining A/B/C, is it still a *generative*
LBD engine or a lookup?

## Outcome: CONVERGED, build-ready. Finding trajectory 9 → 3 → 0.
Codex accepted the rewritten v2 spec as build-ready; all 12 findings dropped-as-addressed by the
final round; zero escalated, zero new, no convergence-sanding. The novel claim — **LBD generates
questions, a data-referee mandatorily culls them** — is intact and *more* defensible than in v1.

## What the debate changed (every finding was repo-verified, not speculative)

| # | Finding (round raised) | Verdict in v2 |
|---|---|---|
| F-002 | Entity-A source CSVs (`*_regulator_coefficients.csv`) **don't exist** in `data/` | A now derived from `guide_kd_efficiency` + `DE_stats` (+ optional T2) |
| F-003 | Substrate has **only the Th1/Th2 program** — no aging/cytokine receipt table | v1 B = Th1/Th2 **only**; aging/cytokine out of scope |
| F-001/F-005/F-012 | Referee returns "gene in *some* disease cluster" — **cannot answer a specific C**; output contract has no B/C params | Mandatory thin **`referee_triple(A,B,C,condition)`** adapter overriding HOP-3 with exact-C filter; `overall` synthesized *after* exact-C so it can't pass while C is refuted |
| F-004 | HOP-2 program shift is **contrast-based, not condition-resolved** | "condition-specific" claimed **only** for KD/effect/disease hops |
| F-006 | Disease universe is **14 rows, 2 are umbrellas** ("autoimmune disease", "IBD"), not ~17 | Read the 12 eligible specific diseases from the CSV; umbrellas = context only |
| F-007 | `ac_lit ≤ 0` hard gate likely yields **no money-shot survivor** | Converted to a **ranked novelty score** + mandatory preflight `ac_lit`/`ac_known` histogram |
| F-009/F-011 | `ranked_full.csv` is **answer-conditioned at the row level** (all 602 rows `disease_status=supported`) — seeding A from it turns the proposer into a re-ranker | **Banned** from seeding entirely; A built only from answer-free KD/DE tables |
| F-008 | 0.5–1 day **underestimates** API/normalization/adapter work | Revised to ~1–1.5 days; v1 = one co-mention source (Europe PMC) + Open Targets, cached fixtures; protect demo-video time |
| F-010 | (round 2 P0) Accepted fixes **hadn't landed in the artifact** — a builder follows the spec, not the debate prose | Spec fully **rewritten to v2** |

## The generative-vs-lookup question (resolved)
Both models ended agreeing (genuine, not sanded, per the preserve-intent check): the constrained
pipeline **remains generative** because (1) A is built from raw KD/DE tables with no disease answer
in them; (2) the A–C novelty signal is *external* literature (Europe PMC / Open Targets), not the
referee's own outputs; (3) the referee runs *after* generation and can refute. Generated-vs-survived
counts are the falsifiable proof of independence. Documented fallback if the preflight shows no
disjoint survivor: widen the novelty band, or demo `referee_triple` on 2–3 hand-built triples — the
pipeline stays the method.

## Persistent disagreements
None. Clean convergence on repo-verified facts — the ideal outcome for a plan debate (the debate
functioned as specification-completion, not argument).

## Recommended next move (Codex's final + my agreement)
Before building: **(1)** pin the 12 disease→EFO map + the Th1/Th2 keyword map by hand (the one
non-mechanical step), **(2)** run the mandatory novelty preflight histogram over the A universe to
confirm a disjoint survivor exists, **then** delegate the mechanical client/adapter build to Codex
`[HYBRID]`. The referee finding is already a complete submission — keep the LBD layer thin.
