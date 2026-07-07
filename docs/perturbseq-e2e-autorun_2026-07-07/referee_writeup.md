# A Calibrated Hypothesis Referee for CD4+ T-cell Immunology

*Built from the Marson/Pritchard genome-scale CRISPRi Perturb-seq supplementary tables.*
Deliverables: `referee.py` (module), `join_spec.json` (join contract), `qc_report.md` (QC),
`linkage_diagram.png` (topology), `demo_traces.json` (three worked cases).

---

## 1. What the referee does

`referee(gene, condition)` traces a single gene through a four-hop evidence chain and returns a
**calibrated verdict** — every hop carries the *exact* numbers from the source table (the "receipt"),
and the language is disciplined so that **absence of evidence is never reported as evidence of absence**.

```
HOP 0  knockdown-QC gate   guide_kd_efficiency            <-- QUERIED FIRST
HOP 1  on-target effect     DE_stats
HOP 2  Th1/Th2 program      Th2_Th1_polarization ...       (faceted by BOTH contrasts)
HOP 3  autoimmune disease   cluster_autoimmune_enrichment  (neg. controls excluded)
```

`condition ∈ {Rest, Stim8hr, Stim48hr}`. Genes may be passed as a symbol (`GATA3`) or an Ensembl ID
(`ENSG00000107485`); the DE table's strictly 1:1 ENSG↔symbol map is used to translate between them.

![Linkage diagram]({{artifact:b5321d50-019d-4ffe-8734-bac0e304796b}})

## 2. The central design decision: HOP 0 first, and UNTESTED ≠ no-effect

The knockdown-QC gate is evaluated **before** anything else. A guide is only informative about a gene's
function if it actually knocked the gene down. The QC table records this per guide as `signif_knockdown`.

- If **no** guide for that gene×condition has `signif_knockdown=True`, the perturbation was **never
  established**. Any downstream "no differentially-expressed genes" is then *uninterpretable* — it could
  mean the gene has no effect, or simply that we never silenced it. The referee returns **UNTESTED**.
- Only when the gate **passes** does a `ontarget_significant=False` in DE_stats become a genuine
  **REFUTED** (a real perturbation that produced no on-target transcriptional effect).

This single rule is what separates a referee from a lookup table: it refuses to launder a technical
failure into a biological claim.

### Calibrated status vocabulary (per hop)
| status | meaning |
|---|---|
| **supported** | the row affirmatively backs the hypothesis |
| **refuted** | the row affirmatively contradicts it — *only downstream of a passed gate* |
| **untested** | the deciding measurement does not exist, or the gate did not pass |
| **flagged** | a quality caveat applies (e.g. `offtarget_flag=True`) |

## 3. Join topology (contract in `join_spec.json`)

| Hop | Left → Right | Exact keys | Notes |
|---|---|---|---|
| 0 | input → **KD** | gene→`perturbed_gene_id` (ENSG) + `culture_condition` | aggregate over 1–3 guides; gate = `any(signif_knockdown)` |
| 1 | KD → **DE** | `perturbed_gene_id`==`target_contrast` (ENSG) + `culture_condition` | 1:1; DE is the ENSG↔symbol Rosetta stone; 11,422 shared genes |
| 2 | DE → **POL** | `target_contrast_gene_name`==`variable` (symbol) | no condition dim; **faceted by both contrasts** (Ota 2021, Hollbacker 2021) |
| 3 | symbol → **ENR** | symbol ∈ `ast.literal_eval(intersecting_genes)`; `condition`→`gene_set` | `downstream_{cond}` + `regulators`; **negative controls excluded** |

**QC caveats carried into the logic** (full detail in `qc_report.md`):
- 933 KD guides have a null `perturbed_gene_id` (no ENSG map) → dropped from the gate aggregate.
- DE reproducibility columns are ~86–91% null *by design* (populated only for hits) → reported as
  "not reported", never as a failure.
- ENR has 924 negative-control rows (excluded) and 995 null-OR rows (empty intersection, `'[]'`,
  Fisher not computable) — these contribute no gene memberships.
- POL contrast coverage differs (24,821 vs 12,467 rows) → a gene may exist in one contrast only.

## 4. Three worked demonstrations (`demo_traces.json`)

Genes were selected **programmatically from the data**, not hardcoded.

### (a) Receipt-backed YES — `GATA3`, Stim48hr
The Th2 master transcription factor. All four hops fire.
- **HOP 0 · supported** — 2/2 guides `signif_knockdown=True`; best guide `GATA3-1`
  drops expression from `ntc_mean_expr=0.902` to `guide_mean_expr=0.348` (t=−22.6, p=1.0e−78).
- **HOP 1 · supported** — `ontarget_significant=True`, `effect_size=−14.95`, **1,252 downstream DE genes**;
  reproducible (cross-donor r=0.721, cross-guide r=0.884).
- **HOP 2 · supported** — significant in **both** contrasts, Th2-associated (Ota `log_fc=+1.02`,
  adj_p=2.2e−131; Hollbacker `log_fc=+1.25`, adj_p=8.4e−07).
- **HOP 3 · supported** — member of significant autoimmune-disease enrichments (FDR<0.05) via Stim48hr gene sets.
- **VERDICT: YES** — knockdown verified, on-target effect, program membership, disease enrichment.

### (b) UNTESTED artifact-catch — `IL2`, Rest  *(the whole point of the gate)*
IL2 is barely transcribed in **resting** CD4+ T cells, so there is essentially nothing to knock down.
- **HOP 0 · untested** — 0/2 guides significant; `guide_mean_expr=0.0259` vs `ntc_mean_expr=0.0356` —
  the guide and control expression are the same near-zero baseline (t=−1.16, p=0.25).
- **HOP 1** — DE shows `ontarget_significant=False`, `n_downstream=0`. A naive reader would call this
  **"no effect."** The referee instead returns **untested**, because the gate did not pass.
- **HOP 2 · supported** — notably, IL2 *is* a significant Th2-program gene in both contrasts
  (Ota `log_fc=+3.43`, adj_p=1.1e−121). The biology is real; **we simply did not test it here.**
- **VERDICT: UNTESTED** — "The perturbation was NOT established, so any downstream 'no effect' is
  uninterpretable." This is the artifact the gate exists to catch.

### (c) REFUTED — `CTLA4`, Rest
A real, verified knockdown that produced no on-target transcriptional effect in resting cells.
- **HOP 0 · supported** — 2/2 guides `signif_knockdown=True`; `CTLA4-1` drops expression
  `0.0533 → 0.0044` (t=−11.2, p=4.4e−21). The perturbation is genuine.
- **HOP 1 · refuted** — despite the passing knockdown, `ontarget_significant=False`, `n_downstream=0`.
  Because the gate passed, this is a legitimate **refutation** of a transcriptional-effect hypothesis
  for CTLA4 in the resting state — *not* an artifact.
- **HOP 2 · supported** — CTLA4 is a significant Th1-associated program gene (Ota `log_fc=−1.54`).
- **VERDICT: REFUTED** — "the perturbation was real and the effect hypothesis is refuted."

**The IL2 vs CTLA4 contrast is the core lesson:** both show `ontarget_significant=False` with zero
downstream genes at HOP 1. The gate at HOP 0 is the *only* thing that tells them apart — IL2 is
UNTESTED (never silenced), CTLA4 is REFUTED (silenced, no effect).

## 5. Reproducibility / usage

```python
from referee import Referee
ref = Referee.from_dir("~/pyzobot-data")
v = ref.referee("GATA3", "Stim48hr")
print(v.render())        # full hop-by-hop trace with receipts
v.to_dict()              # machine-readable
```
Or from the shell: `python referee.py ~/pyzobot-data GATA3 Stim48hr`.

Every number in every verdict is copied verbatim from the source supplementary tables; the referee
asserts nothing that is not in the tables.
