# LBD loose full-sweep — LIVE run receipt

**Pipeline:** `arbiter.lbd.propose.sweep(condition, program_significant=False)` — run UNCHANGED.
**Mode:** 100% live literature/DB calls (Europe PMC, Open Targets, MyGene), CPU-only, resumed from an on-disk cache of prior live responses.
**Only change vs the standard sweep:** `program_significant=False` — the FULL KD-gated + effect gene universe (loose), not the program-significant subset.
**Conditions (run order):** Stim8hr → Rest → Stim48hr.
**Total wall time:** 3h04m (11099s).

> Framing: every row below is a **generated candidate** A→B→C triple that the referee then evaluated — these are questions the dataset can resolve, *reproduced* from the live pipeline, NOT discoveries or proven associations. NAB2 is a known reproduction anchor; all other rows are candidates to referee, not findings.

---

## Liveness

- Cached live responses at start (reused / resume): **n_start = 632**
- Cached live responses at end: **n_end = 9557**
- New live responses fetched this run: **8925**
- `n_start -> n_end`: **632 -> 9557**

The cache is content-hash keyed; the 632 prior responses were reused and only un-fetched calls went live.

---

## Per-condition funnel

| Condition | a_genes | eligible_pairs | disease_C_supported_total | clean_supported | ab_gate_value | wall |
|-----------|--------:|---------------:|--------------------------:|----------------:|--------------:|------|
| Stim8hr   | 8560 | 49321 | 43 | 30 | 18 | 2h26m (8801s) |
| Rest      | 8238 | 47196 | 11 | 4 | 18 | 0h19m (1190s) |
| Stim48hr  | 8551 | 49504 | 17 | 11 | 18 | 0h18m (1107s) |

Chain-class breakdown (referee cull, pre-A-C-lit):
- **Stim8hr:** {"refuted_for_c": 49261, "supported": 30, "supported_weak": 10, "refuted_program": 16, "supported_flagged": 3, "refuted_effect": 1}
- **Rest:** {"refuted_for_c": 47185, "supported": 4, "supported_weak": 7}
- **Stim48hr:** {"refuted_for_c": 49477, "supported": 11, "supported_weak": 4, "refuted_effect": 4, "supported_flagged": 2, "refuted_program": 6}

### Loose vs. program-significant (known Stim8hr baseline)

The loose funnel is **new territory** — no pre-known counts, so nothing is asserted against a fixed expectation. For reference, the known **program-significant** Stim8hr baseline was **3935 genes / ab_gate 26 / 30 clean**. Dropping the program-significance filter gives, at Stim8hr, **8560 genes / ab_gate 18 / 30 clean**. The larger, lower-signal loose population pulls the 50th-percentile ab_gate down (26 → 18) while the clean-supported count lands at 30. That difference IS the result of dropping the filter; it is reported, not asserted.

---

## ACCEPTANCE — NAB2 @ Stim8hr raw-signal check

NAB2 × "atopic eczema" **found** in `results["Stim8hr"]["ranked_supported"]`.

| signal | expected | got | match |
|--------|---------:|----:|:-----:|
| ab | 66 | 66 | PASS |
| bc | 2184 | 2184 | PASS |
| ac_lit | 6 | 6 | PASS |
| ac_known | 0.0376 | 0.0376 | PASS |
| effect | 301 | 301 | PASS |
| referee_answer | supported | supported | PASS |

**RAW-SIGNAL CHECK: PASS** — all 6 identical values reproduced live, referee `supported`.

**Loose rank/score (reported, NOT asserted):** in the loose run NAB2 ranks **#4 / 43** in `ranked_supported` and **#4 / 30** in `ranked_clean_supported`, score **-1.25**. Rank and score differ from the program-significant run because the z-scores and ab_gate are computed over the larger loose population — this is expected and correct.

---

## Merged cross-condition top 15 (union of all clean_supported, score desc)

| # | a_gene | c_disease \| condition | score | ab | bc | ac_lit | ac_known | effect |
|---|--------|------------------------|------:|---:|---:|-------:|---------:|-------:|
| 1 | UFM1 | multiple sclerosis | Stim8hr | -0.74 | 29 | 34423 | 43 | 0.0620 | 2278 |
| 2 | BHLHE40 | ankylosing spondylitis | Stim8hr | -1.08 | 507 | 4773 | 26 | 0.0713 | 1996 |
| 3 | NUDT1 | type 1 diabetes mellitus | Stim8hr | -1.155 | 26 | 3725 | 0 | 0.0678 | 4 |
| 4 | NAB2 | atopic eczema | Stim8hr | -1.25 | 66 | 2184 | 6 | 0.0376 | 301 |
| 5 | TUFM | Crohn's disease | Stim8hr | -1.343 | 38 | 8319 | 31 | 0.0501 | 651 |
| 6 | NAB2 | asthma | Stim8hr | -1.861 | 66 | 66242 | 76 | 0.0516 | 301 |
| 7 | EGR2 | ankylosing spondylitis | Stim8hr | -2.249 | 662 | 4773 | 50 | 0.0986 | 854 |
| 8 | EGR2 | celiac disease | Stim8hr | -2.323 | 662 | 5165 | 67 | 0.0480 | 854 |
| 9 | ATP5MG | rheumatoid arthritis | Rest | -2.359 | 18 | 46621 | 13 | 0.0941 | 21 |
| 10 | EGR2 | type 1 diabetes mellitus | Stim8hr | -2.388 | 662 | 3725 | 55 | 0.0486 | 854 |
| 11 | MYB | asthma | Stim48hr | -2.453 | 1040 | 66242 | 850 | 0.0241 | 1221 |
| 12 | NUDT1 | Crohn's disease | Stim8hr | -2.58 | 26 | 8319 | 7 | 0.0610 | 4 |
| 13 | MYB | asthma | Stim8hr | -2.669 | 1040 | 66242 | 850 | 0.0241 | 1024 |
| 14 | ZMAT3 | ankylosing spondylitis | Stim48hr | -2.697 | 27 | 4773 | 3 | 0.0256 | 1 |
| 15 | ZMAT3 | ankylosing spondylitis | Stim8hr | -2.707 | 27 | 4773 | 3 | 0.0256 | 1 |

Full pooled clean rows: 45 (all 45 saved to `all_conditions_top.json`; capacity was top-50 but only 45 pooled clean rows exist).

---

## Artifacts written to `live_fullsweep_loose/`

- `sweep_Stim8hr.json`, `sweep_Rest.json`, `sweep_Stim48hr.json` — full per-condition results (funnel + ranked_supported + ranked_clean_supported)
- `lbd_questions_<cond>.json` — clean full-chain supported candidates per condition (checkpoints)
- `all_conditions_top.json` — merged clean_supported across conditions (all 45 rows; sorted score desc, capped at 50)
- `run_summary.json` — funnels + params + liveness + wall time
- `executed_code.py` — the faithful code that was executed (unmodified)
- `run.log` — full streamed pipeline progress
