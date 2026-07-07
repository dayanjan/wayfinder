# PyzoBot Hypothesis-Referee (the Validator) — results

`referee(gene, condition)` traces one CD4+ T-cell gene (SYMBOL or ENSG; condition in
{Rest, Stim8hr, Stim48hr}) through the 4-table Perturb-seq evidence chain defined in
`pyzobot_join_spec.json`, returning a structured verdict where **every status carries the
exact table value that justifies it**. Calibrated vocabulary only —
*supported / refuted / untested / flagged* — never "proven" or "discovered".

## Chain & the hero feature
- **HOP 0 GATE (T4)** runs FIRST. Guides are aggregated to gene x condition; the gate passes
  only if >=1 guide has `signif_knockdown=True`. **If the gate fails, the whole verdict is
  `untested` and the referee stops** — a null downstream result is declared uninterpretable,
  never "no effect". This is the artifact catch.
- **HOP 1 EFFECT (T1)** on-target KD status + `n_downstream` DE genes, with cross-donor /
  cross-guide reproducibility surfaced only where those columns are populated; `offtarget_flag`
  downgrades the hop to `flagged`.
- **HOP 2 PROGRAM (T2)** Th1/Th2 shift, **faceted by both contrasts** (Ota 2021 & Hollbacker
  2021) — never silently collapsed to one.
- **HOP 3 DISEASE (T3)** membership in autoimmune-disease-enriched clusters; `intersecting_genes`
  is `ast.literal_eval`-exploded, `negative_control_disease` rows excluded, and the `gene_set`
  suffix aligned to the queried condition. `supported` requires FDR<0.05.

## Demonstration — three genes, three verdicts

### 1. EGR2 @ Stim8hr — receipt-backed YES (chain re-derived)
- **GATE supported**: 2/2 guides significant, best adj-p 1e-16 (guide expr 0.25 vs NTC 0.88).
- **EFFECT supported**: on-target KD, effect size -11.06, **854 downstream DE genes**; cross-donor r=0.61, cross-guide r=0.79 (reproducible).
- **PROGRAM supported**: Th1-associated in Hollbacker 2021 (log_fc 2.44, adj-p 0.049); not significant in Ota 2021 (adj-p 0.59) — **both contrasts reported**.
- **DISEASE supported**: member of **34 significant disease clusters** across 13 autoimmune diseases; top hit asthma OR 20.4, FDR 5e-5.
- **Overall:** *consistent with a validated gene -> program -> disease chain re-derived from the tables.*

### 2. IL2 @ Rest — the artifact catch (UNTESTED, not "no effect")
- **GATE untested**: 0/2 guides significant (best adj-p 0.32). Guide mean expr 0.031 vs NTC 0.036 — **the target is barely expressed at Rest, so there is nothing to knock down.**
- Referee **halts at HOP 0**. IL2 is a canonical, biologically important gene that appears in both the Th program and disease gene-sets — a naive pipeline reading the empty downstream result would wrongly call it "no effect". The referee returns *untested — knockdown failed QC gate*, which is the correct, honest verdict.

### 3. SLC1A5 @ Stim8hr — a plausible disease link REFUTED
- **GATE supported**: 1/2 guides significant (best adj-p 0.009).
- **EFFECT refuted**: pooled `ontarget_significant=False`, only 1 downstream DE gene (a valid receipt-level disagreement with the single-guide gate, surfaced not hidden).
- **PROGRAM supported**: Th1-associated in Ota 2021 (adj-p 0.001).
- **DISEASE refuted**: SLC1A5 appears in **9** disease cluster gene-sets but **none reach FDR<0.05** (best FDR 0.054, T1D, OR 2.73). The plausible-looking metabolic-gene -> autoimmunity link is **not supported by the enrichment data**.
- **Overall:** *gene->disease link refuted: gene in cluster gene-sets but enrichment not significant.*

## Reproducibility
- Module: `pyzobot_referee.py` — `RefereeData` loads/indexes the four tables once; `referee()` /
  `referee_json()` return the verdict. Join contract read from `pyzobot_join_spec.json`.
- Thresholds centralized (`SIG_ALPHA=0.05`); all statuses trace to a printed receipt value.
- `python pyzobot_referee.py` reproduces the three verdicts above.
