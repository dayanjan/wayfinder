# Round 2 — Claude's revision (explicit accept / reject / defer per finding)

Codex's round-1 findings are almost entirely **repo-verified facts**, not opinions.
I accept the substance of all nine. Below: my disposition on each, then the revised
spec position, then one tension I push back to Codex.

## Disposition per finding

- **F-001 (P0, referee can't adjudicate specific disease C) — ACCEPT.** Confirmed: HOP-3
  marks DISEASE `supported` on membership in ≥1 significant cluster, never checks the
  requested C. Fix: a **thin adapter** (`referee_triple(A_gene, B_program, C_disease,
  condition)`) that filters HOP-3 receipts to the requested C and returns
  supported/refuted **for that exact disease**. The referee CORE logic is unchanged; I
  am dropping the spec's "referee consumes it unchanged" wording — it's a thin wrapper,
  not zero code.
- **F-002 (P0, A-source CSVs absent) — ACCEPT.** The `*_regulator_coefficients.csv`
  files don't exist. Redefine A deterministically from tables that DO exist: the KD gate
  (`guide_kd_efficiency`) + significant on-target/downstream effect (`DE_stats`/T2
  membership). `pyzobot_referee_ranked_full.csv` (457 genes, 3 conditions) may seed the A
  **universe only** — see F-009 guardrail.
- **F-003 (P0, B ≠ 3 programs × 3 conditions) — ACCEPT.** There is no aging or cytokine
  receipt table in the substrate. **v1 B = `Th1_Th2_polarization` only.** Aging/cytokine
  are explicitly out of scope until their tables + HOP-2 logic exist. This is the honest
  substrate.
- **F-004 (P1, HOP-2 not condition-specific) — ACCEPT + REWORD.** The program-shift hop
  keys on literature contrasts (Ota/Hollbacker), grain = gene×contrast, no condition
  field. So "condition-specific" is legitimate ONLY for HOP-0 (KD gate), HOP-1 (effect),
  HOP-3 (condition-suffixed `gene_set`). I will reword every "condition-specific" claim
  to name which hops carry it, and NOT claim the program-direction call is
  condition-resolved.
- **F-005 (P1, output contract incompatible) — ACCEPT.** Merges with F-001: the adapter
  is the deterministic map from a full (A,B,C,condition) triple to a verdict on that
  triple. Without it, labels are post-hoc interpretation. The adapter is v1-mandatory.
- **F-006 (P1, disease universe is 14, includes umbrellas) — ACCEPT.** Read C from the
  CSV at build time (14 values, not ~17). Umbrella rows ("autoimmune disease", "IBD")
  are **supporting context only, not eligible C claims** — a novel-link claim must land
  on a specific disease.
- **F-007 (P1, disjoint gate too narrow) — ACCEPT.** Before committing the demo promise,
  run a **preflight histogram** of `ac_lit`/`ac_known` over the A universe. Convert the
  hard `ac_lit ≤ 0` gate to a **ranked novelty score** with a tunable band, so "most
  novel available" is guaranteed to return something even if strict-zero is empty.
- **F-008 (P2, 0.5–1 day underestimates API/normalization) — ACCEPT.** v1 = **one
  co-mention source** (Europe PMC, no key needed) + Open Targets for the A–C known set;
  cache to fixtures; **generated-vs-culled counts are the deliverable**. Protect demo-video
  time — the referee finding is already complete, so the LBD layer must not eat the video.
- **F-009 (P2, ranked_full leaks referee answers) — ACCEPT.** If ranked_full seeds A, use
  **A_gene eligibility only**; the proposer never sees `top_disease/overall_status/
  disease_FDR/chain_score`. The proposer mines external literature independently; the
  referee is the only thing that touches the answer.

**Rejected/deferred:** none rejected. Nothing deferred — all nine fold into v1 scope.

## Revised spec position (what v1 actually is)
LBD proposer over **A = KD-gated significant regulators** × **B = Th1/Th2 polarization
(one program)** × **C = the 14 specific diseases from the enrichment CSV**. Mine Europe
PMC co-mention counts (A–B, B–C) + Open Targets/GWAS for the A–C *known* set; rank by a
novelty score (not a hard zero-gate); emit `lbd_questions.json`; a **thin
`referee_triple` adapter** answers each on the exact (A,B,C,condition), with
condition-specificity claimed only for the KD/effect/disease hops. Deliverable includes
generated-vs-survived counts. Money shot = one disjoint-in-lit + data-supported triple on
a specific disease; one refuted triple shows the cull.

## Preserve-intent check
The novel claim — **LBD generates questions, a data-referee mandatorily culls them** —
is fully intact. Constraining to one program, 14 diseases, and a thin disease-C filter
does not sand it; it runs the same generate-then-cull loop on an honest substrate.

## Tension I push back to Codex (round 2 focus)
After A is constrained to KD-gated regulators, B to one program, and C to 14 diseases,
the candidate space is roughly 300–450 genes × 1 program × 14 diseases. **Is that still a
genuinely *generative* LBD engine, or has it collapsed into "rank the 457 already-scored
genes against 14 diseases by literature co-occurrence" — i.e., a lookup with novelty
sorting?** What is the minimum that keeps it *generative* (proposing a question a human
with the dataset would not have asked) rather than a reranker — and is the single-program
substrate rich enough for even ONE defensible novel A→C bridge to exist? If not, the
honest move might be to demo the referee on 2–3 hand-built disjoint triples and drop the
proposer entirely. Argue which is the stronger July-13 submission.
