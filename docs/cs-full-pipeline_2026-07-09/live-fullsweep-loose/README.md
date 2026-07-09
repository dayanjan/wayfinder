# Full 100%-live LBD sweep in Claude Science — loose genes, all 3 conditions (2026-07-09)

Option 4: the real `arbiter.lbd.propose.sweep(program_significant=False)` run **100% live** (cold cache →
9,557 live Europe PMC + Open Targets calls) natively in CS over the FULL loose gene universe (all KD-gated
genes, not just program-significant) at **Rest, Stim8hr, Stim48hr**. Resumable persistent cache at
`/home/dayanjan/pyzobot-cs-live/data/lbd_cache`. Driven headless; CS Reviewer passed (1 cosmetic caption fix).

## Result (the two things this answers)
1. **The program-significance filter was SAFE.** Loose Stim8hr reproduced the **identical 30 clean-supported**
   candidates as the original program-significant run; every extra loose gene was refuted at HOP-2 (program) —
   `refuted_program: 16` — so the filter cost zero Stim8hr candidates.
2. **Timepoint expansion generated NEW hypotheses** the Stim8hr-only original never saw: **Rest = 4** clean-
   supported, **Stim48hr = 11** clean-supported (see `sweep_Rest.json`, `sweep_Stim48hr.json`,
   `all_conditions_top.json`).

## NAB2 → atopic eczema — confirmed AND timepoint-resolved (the positive control)
The full-scale, 100%-live loose sweep **reproduced the headline finding exactly**: NAB2 → atopic eczema at
**Stim8hr, rank 4/43** with the **identical raw signals** (ab 66, bc 2184, ac_lit 6, ac_known 0.0376, effect
301, referee `supported`) — see the acceptance PASS table in `receipt.md`. Rank held at 4 despite the larger
loose scoring population; only the novelty score nudged (−1.25 vs the original −1.137), as expected. This is an
independent reproduction from fresh live API calls over every gene (no cache).
**New nuance (this run):** NAB2 → atopic eczema surfaces **ONLY at Stim8hr** — it does *not* complete a supported
chain at Rest or Stim48hr (`sweep_Rest.json` / `sweep_Stim48hr.json` contain no NAB2 supported row). Not a miss:
the referee is condition-matched, so this shows the NAB2→eczema chain is a **stimulation-dependent, timepoint-
specific** signal (acute 8 h window), not present at rest or at 48 h. The loose sweep therefore both *confirms*
and *sharpens* the finding.

Chain classes — Stim8hr: refuted_for_c 49261 / supported 30 / supported_weak 10 / refuted_program 16 /
supported_flagged 3 / refuted_effect 1. Rest: supported 4 / supported_weak 7. Stim48hr: supported 11 /
supported_weak 4 / refuted_effect 4. 100% live (cache 0→9,557).
