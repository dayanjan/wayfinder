# Wayfinder

**A hypothesis referee that says a confident *no*.** Every scientist is caught between two floods — over a
million papers a year and omics runs returning millions of measurements per sample. Wayfinder helps you
navigate the gap: it surfaces the data's implicit hypotheses with literature-based discovery, then **tests
each one against real experimental data and returns a verdict with a receipt for every hop** — *supported*,
*refuted*, or *untested (the knockdown failed)*. The library and the lab, on one bench.

> **▶ 3-minute demo video:** https://youtu.be/MbgojaAFfz0
>
> Built for **Built with Claude: Life Sciences** (Anthropic × Gladstone Institutes), July 2026 —
> **Researcher track ("a researcher who also builds").** The whole pipeline was reproduced natively inside
> **Claude Science**, Anthropic's scientific workbench.

## Why this exists

Three NIH reviewers killed the R01 behind this line of work (**1R01LM015392-01**) with one recurring critique:

> *"This application has the same major problem that has plagued all LBD work: it generates an enormous
> number of hypotheses, almost none of which ever get followed up."*

They were right. Literature-based discovery overproduces hypotheses and tests almost none. **Wayfinder is the
answer to that critique** — it puts hypothesis *generation* and *testing* on one bench, culls aggressively,
and is willing to say a confident, receipt-backed **NO**. Falsification, not confirmation, is the moat.

## The finding (a receipt-backed nomination)

On the genome-scale CD4+ T-cell Perturb-seq resource (Marson lab), Wayfinder posed **22,039** gene→program→
disease hypotheses; a deterministic referee culled them to **30 clean, receipt-backed survivors.** The
standout: **NAB2 → Th1/Th2 polarization → atopic eczema** — a connection the literature had never drawn,
re-derived here with a receipt at every hop.

- **The confident NO (the moat).** A failed knockdown returns **untested**, never "no effect": IL2's
  knockdown-QC gate failed (0/2 guides reached significance) → *untested*, an artifact caught rather than a
  false negative. NAB2's gate passed (2/2 guides, adj_p 1e−16), so NAB2 can be judged.
- **A confounder refuted against the authors' own data.** NAB2 sits ~1.9 kb from *STAT6* (a master Th2/atopy
  regulator), so a CRISPRi cis-artifact was the obvious worry. Reading the authors' own deposited genome-wide
  DE matrix, **STAT6 is unmoved by NAB2 knockdown** (log2FC +0.09, adj_p 0.79) while NAB2's own transcript
  drops (−3.08 log2FC, z≈−17) → the cis-artifact is **refuted**.
- **Calibrated, not overclaimed.** The eczema link is an Open Targets GWAS-genetic *nomination* (no
  colocalization); the perturbation-backed claim is NAB2 as a **Th1/Th2 regulator**. NAB2 stays a nomination —
  never "proven" or "discovered."

## How it works — a 4-hop chain, each hop with an experimental receipt

1. **QC gate** — a null result counts only if the knockdown actually worked *(receipt: guide knockdown-efficiency)*.
2. **Gene → effect** — did perturbing the gene produce a real, reproducible transcriptional effect? *(receipt: DE stats + cross-donor/guide reproducibility)*
3. **Gene → program** — do the downstream effects shift a real T-cell program? *(receipt: Th1/Th2 polarization signature)*
4. **Program → disease** — does the downstream cluster enrich for an autoimmune disease? *(receipt: cluster→disease odds ratio + intersecting genes)*

Every causal edge traces to a data receipt (odds ratio / p-value / effect size). Claude *interprets* receipts;
it does not assert biology. Deterministic data lookups are tools, not "agents" — visible agency is reserved
for judgment.

## Built inside Claude Science

The generation → referee → provenance pipeline ran natively in **Claude Science** (Anthropic's scientific
workbench), which authored and ran the literature-based-discovery generator live and executed a multi-model
**actor–critic**: an **Opus 4.8** author with an independent **Sonnet 5 reviewer** that verified every number
*and enforced calibrated language* — it flagged the words "validated" and "definitive" as overclaims, and they
were cut. The platform checked its own work.

## Reproduce

```bash
bash data/fetch_data.sh                     # public supplementary tables (~25 MB); no raw data committed
# then, from a Python env with the repo installed:
#   open notebooks/ — the evidence-chain notebook recomputes every headline number live from the tables
#   or call the referee directly:  from arbiter.lbd import referee_triple
```

Full method + build plan: `docs/plan.md`. Independent 5-agent replication: `docs/replication_report_2026-07-08.md`.
Native Claude Science pipeline + provenance: `docs/cs-full-pipeline_2026-07-09/`.

## Data

Public supplementary tables from the genome-scale CD4+ T-cell Perturb-seq study — Zhu, Dann, … Marson
(Gladstone/UCSF), bioRxiv 2025, **doi:10.64898/2025.12.23.696273** — used under the hackathon's public-dataset
provision; all analysis performed during the event. Provenance in `data/README.md`; analysis reference:
`github.com/emdann/GWT_perturbseq_analysis_2025`. This repo commits no raw data.

## About the builder

Built by **Dayanjan Shanaka Wijesinghe, Ph.D. ("Shanaka")** — tenured Associate Professor at **Virginia
Commonwealth University School of Pharmacy** and former Deputy Director of VCU's Lipidomics/Metabolomics Core
Facility. Having spent years handing researchers data matrices of thousands of features and fielding the same
question — *"what does it all mean?"* — he now builds AI instruments for precision medicine and drug discovery.
[linkedin.com/in/dayanjanwijesinghe](https://www.linkedin.com/in/dayanjanwijesinghe/)

## License

Code: **MIT** — see `LICENSE`. All files authored during the event (started 2026-07-07); the git history is the
new-work compliance proof.
