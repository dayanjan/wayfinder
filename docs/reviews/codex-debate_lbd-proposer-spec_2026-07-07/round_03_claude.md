# Round 3 — Claude's final position (the artifact is now rewritten)

The round-2 P0 was correct and decisive: my accept/reject was prose; the **artifact**
still encoded the rejected v1 design. I have now **rewritten `docs/lbd-proposer-spec.md`
to v2**, landing every accepted finding into the spec a builder actually follows. This
round is the acceptance gate: verify the *revised* artifact against the repo.

## Disposition on round-2 findings
- **F-010 (P0, fixes didn't land in the artifact) — RESOLVED.** The spec is rewritten.
  A now derives from `guide_kd_efficiency` + `DE_stats` (+ optional T2), not the absent
  `*_regulator_coefficients.csv`; B = Th1/Th2 only; C = 14 CSV-read diseases with the two
  umbrella terms excluded; the disjoint hard-gate is now a ranked novelty score with a
  mandatory preflight histogram; "referee unchanged" is replaced by the mandatory
  `referee_triple` adapter; effort revised to ~1–1.5 days. See the v2 banner + §1–§6.
- **F-011 (P1, ranked_full is answer-conditioned at the row level) — ACCEPT, HARDENED.**
  You're right that all 602 rows are `disease_status=supported`, so even reading only
  `gene`/`condition` biases A. v2 **bans `ranked_full` from seeding entirely** (§1, bold)
  and builds A only from raw KD/DE/T2 tables that contain no disease answer. The
  "generative not lookup" rationale is now written into §3.
- **F-012 (P1, adapter needs exact verdict semantics) — ACCEPT.** §3 now specifies
  `referee_triple` as a first-class contract: HOP-3 filters `t3_exploded` on
  `disease==C_disease AND gene_set==downstream_<condition>`; supported iff that exact row
  FDR<0.05; "gene in other diseases but not C" → **refuted-for-C**; the triple `overall`
  is synthesized **after** exact-C HOP-3, so it can never say supported while C is refuted.
- **F-004 / F-006 (dropped in round 2) — stay resolved** in the rewrite (condition
  wording names only KD/effect/disease hops; 14 diseases read from CSV, umbrellas excluded).

## Position on the round-2 generative-vs-lookup tension
The constrained pipeline **remains a generative LBD engine**, and v2 §3 states why:
(1) A is built from raw KD/DE tables with no disease answer in them; (2) the A–C novelty
signal comes from *external* literature (Europe PMC / Open Targets), independent of the
referee; (3) the referee runs *after* generation and can refute. The generated-vs-survived
counts are the falsifiable proof of independence. The single-program substrate is a real
limit, so v2 documents the honest fallback (§6): if the preflight histogram shows no
disjoint survivor, widen the band or demo `referee_triple` on 2–3 hand-built triples — the
pipeline stays the method. I do NOT think the honest move is to drop the proposer: the
generate-then-cull loop with reported counts is the thesis, and it survives the constraints.

## Preserve-intent check (final)
The novel claim — **LBD generates questions, a data-referee mandatorily culls them** — is
intact and now *more* defensible, because the answer-leak path (ranked_full seeding) that
would have quietly turned it into a re-ranker is explicitly closed.

## What round 3 should verify
Read the **rewritten** `docs/lbd-proposer-spec.md` against the repo and confirm: (a) A is
now derivable from the named existing tables (check `guide_kd_efficiency` /`DE_stats`
headers carry the needed gate/significance columns); (b) the `referee_triple` HOP-3
override is faithfully specified against `pyzobot_referee.py:70-74` / `:251-266`; (c) no
residual v1 claim survived the rewrite. Flag anything still inconsistent, or confirm the
spec is build-ready.
