You are a senior computational-biology + software reviewer giving an INDEPENDENT second
opinion to a peer (Claude) mid-build. Read-only inside the repo. Open the files referenced
below and verify claims against the actual code + data — a repo-grounded opinion is worth far
more than a speculative one. Be direct; disagree where warranted. This is a real consult, not
a rubber stamp.

# Context (a hackathon: "Built with Claude: Life Sciences", Researcher track, deadline July 13)
The project (PyZoBot Arbiter) is a hypothesis referee over a CD4+ T-cell Perturb-seq dataset.
The strategic reframe: use literature-based discovery (Swanson ABC) as a QUESTION-GENERATION
engine — mine literature for the highest-value UNTESTED gene(A)→program(B)→disease(C) triples
the dataset can resolve, then hand each to an already-built data-referee that answers it
(supported / refuted-for-C / untested). The novel-yet-data-supported disjoint triple is the
"money shot"; the referee's ability to REFUTE is the cull.

A 3-round repo-read codex-debate already hardened the spec v1→v2 (record:
`docs/reviews/codex-debate_lbd-proposer-spec_2026-07-07.md`). Then Claude authored a fresh tool
layer and ran a SAMPLE preflight. We now want your independent read before the next build.

# Read these
- `docs/lbd-build-log.md` — the running process doc: tool inventory, the disease→MONDO id
  verification, the A-universe sizing decision, the PREFLIGHT RESULT + caveats, and the next move.
- `docs/lbd-proposer-spec.md` — the hardened v2 spec.
- `src/arbiter/lbd/entities.py` — A universe (KD gate ∩ effect; answer-free; `program_significant` flag).
- `src/arbiter/lbd/cooccur.py` — the co-occurrence + novelty scoring + `preflight_sample`.
- `src/arbiter/lbd/sources.py` — Europe PMC / Open Targets / MyGene clients.
- `src/arbiter/lbd/entity_maps.py` — pinned MONDO disease ids + Th1/Th2 keyword arms.
- `.claude/scratch/lbd-debate/preflight_sample.json` — the raw sample result (18 genes × 12
  diseases; 10 disjoint survivors, all obscure alphabetical genes ABCD2/AAMDC/AAK1/ABC-transporters).

# The questions I actually want your opinion on
1. **Is the "disjoint survivors are obscure/understudied genes" outcome a FUNDAMENTAL flaw in
   the LBD-as-question-generator approach, or a sampling artifact** fixable by ranking over the
   full program-significant universe (4,373) + referee-culling? An understudied gene trivially
   has ac_lit=0 — does the novelty score (`zscore(ab)+zscore(bc) − w·ac_lit − w2·ac_known`)
   actually surface INTERESTING novelty, or will it systematically reward obscurity? If the
   latter, what scoring change fixes it? (Read `cooccur.py::novelty_score`.)
2. **Method bugs / validity risks in the code.** Especially: short gene symbols (AAK1, ABCD2)
   producing false-positive Europe PMC matches; the A–B query using bare symbols; the Open
   Targets pagination/score-floor logic; whether the A universe is truly answer-free.
3. **Is the next-move plan right?** (build `referee_triple` adapter → `propose.py` rank+cull →
   `emit.py` → full background sweep, validated against GATA3/EGR2 without seeding A from them).
   What is mis-ordered, missing, or a trap?
4. **Strategic, given the deadline + demo weighting:** is the LBD proposer still worth building,
   or is the stronger July-13 submission to demo the referee on a few hand-built disjoint triples?
   Take a position.

# Output
Plain prose (not JSON). Lead with a one-line bottom-line verdict, then your answers to 1–4 with
file:line evidence where you verified something, then a "biggest thing Claude is missing" line.
Keep it tight — findings over throat-clearing.
