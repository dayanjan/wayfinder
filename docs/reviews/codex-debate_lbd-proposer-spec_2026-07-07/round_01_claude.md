# Round 1 — Claude's opening position

## Framing question
Is `docs/lbd-proposer-spec.md` the shortest *correct* path to a receipt-backed,
condition-specific **novel** finding by July 13 — and do its load-bearing claims
(entity-A source tables, "referee consumes it unchanged", the disjoint-set gate)
hold up against the actual referee code + CSVs already in this repo?

## The position the spec takes
1. **The reframe is the moat.** LBD (Swanson ABC) is used as a *question-generation*
   engine, not a discovery engine: it mines literature for the highest-value
   **untested** A(gene)→B(program×condition)→C(disease) triples the CD4+ T-cell
   Perturb-seq dataset is uniquely positioned to resolve. Each survivor is handed to
   the **already-built referee** (`docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`),
   which answers it against the four tables. This fills the Researcher-track cold-start
   gap ("rich dataset, no question") that Claude Science structurally cannot fill
   itself, and answers the dead-R01 critique one level up: LBD proposes, the data
   referee culls.
2. **Thin + bounded.** Entities are bounded by the dataset (A≈200–500 regulators,
   B = 3 programs × 3 conditions, C ≈ 17 diseases read from
   `cluster_autoimmune_enrichment_results.suppl_table.csv`), so the whole matrix is
   pandas-computable. Pipeline is 3 stages: gather co-mention counts via APIs
   (PubTator3 / Europe PMC / OpenAlex + Open Targets / GWAS Catalog for the known
   A–C set) → compute disjoint novel candidates → emit `lbd_questions.json`.
3. **Referee unchanged for v1.** The spec claims no referee code changes are needed;
   the referee's existing gene+condition verdict is sufficient to answer each LBD
   question.
4. **The money shot** is one *disjoint-in-literature + data-supported + condition-
   specific* triple; one *refuted* triple proves the cull is real.

## Load-bearing assumptions I want stress-tested (verify against the repo)
- **A-source mismatch.** The spec restricts A to genes significant in
  `polarization_prediction...regulator_coefficients.csv` /
  `aging_prediction...regulator_coefficients.csv`. Those files are **not** in `data/`
  (which has `DE_stats`, `guide_kd_efficiency`, `Th2_Th1_polarization_signature_DE`,
  and the cluster enrichment table). Does the entity-A definition rest on data that
  doesn't exist here?
- **Referee disease-specificity gap.** The LBD question targets ONE disease C, but the
  referee's HOP-3 returns membership across ALL enriched clusters (EGR2 → 13 diseases;
  SLC1A5 → 9). Read `pyzobot_referee.py` HOP-3: does the returned verdict let you
  assert "gene → *asthma* specifically", or only "gene → some autoimmune diseases"?
  If the latter, "referee unchanged" is false for a disease-specific claim.
- **Disjoint gate too tight?** Candidate iff `ab≥3 AND bc≥3 AND ac_lit≤0 AND NOT
  ac_known`. Requiring zero A–C co-mentions AND passing KD AND significant program
  shift AND significant *specific*-disease enrichment is a narrow needle — is landing
  even one survivor realistic, or does the demo hinge on tuning `max_ac` up?
- **Condition first-classness.** B is program×condition; does the referee's
  condition handling actually thread through to a condition-specific verdict, or does
  condition get averaged somewhere?

## Preserve-intent (do NOT sand this off)
The novel claim is **"LBD as a question-GENERATION engine (not discovery), whose
output is mandatorily culled by a data-referee."** Critique its execution, but do not
converge it back into a generic "just run LBD" or "just run the referee" — the
generation-then-cull loop is the thesis.
