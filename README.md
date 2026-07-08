# PyZoBot Arbiter

**A hypothesis referee for T-cell immunology.** Give it a mechanistic claim — *"gene G regulates T-cell program P implicated in autoimmune disease D"* — and Claude agents adjudicate it: gather the literature evidence, then **validate each hop against real experimental data**, and return a verdict with a **receipt for every hop** — *supported*, *refuted*, or *untested (knockdown failed)*.

> Built for *Built with Claude: Life Sciences* (Anthropic × Gladstone Institutes), July 2026. **Researcher track — a researcher who also builds:** the deliverable is a reproducible T-cell finding reached through Claude Science, and the referee / question-engine are the instruments built to *ask and answer* the research questions.

## Why this exists

Three NIH reviewers killed the R01 behind this line of work (**1R01LM015392-01**) with one recurring critique:

> *"This application has the same major problem that has plagued all LBD work: it generates an enormous number of hypotheses, almost none of which ever get followed up."*

They were right. Literature-based discovery tools overproduce hypotheses and validate almost none. **PyZoBot Arbiter is the opposite of a generator.** Its job is to *cull and ground* — to say a confident, receipt-backed **NO** to a plausible-sounding claim, and to distinguish "the gene has no effect" from "the knockdown just failed."

## What it validates — a 3-hop chain, each hop with an experimental receipt

Using the genome-scale CD4+ T-cell Perturb-seq resource (Marson/Pritchard):

1. **Gene -> effect** — did perturbing gene G produce a real, reproducible transcriptional effect? *(receipt: differential-expression stats + cross-donor/guide reproducibility)*
2. **Gene -> program** — do G's downstream effects shift a real T-cell program? *(receipt: Th1/Th2 polarization signature)*
3. **Program -> disease** — does G's downstream cluster enrich for an autoimmune disease? *(receipt: cluster->disease odds ratio + intersecting genes)*
4. **QC gate** — a null result is only "no effect" if the knockdown actually worked. *(receipt: guide knockdown-efficiency)*

Every causal edge shown traces to a data receipt (odds ratio / p-value / effect size). Claude *interprets* receipts; it does not assert biology.

## Status
Under active development during the hackathon (July 7-13, 2026). See `docs/plan.md` for the full build plan.

## Quickstart
```bash
# fetch the public validation data (~25 MB of supplementary tables)
bash data/fetch_data.sh
# (build instructions to follow as the app lands)
```

## Data
Public supplementary tables from the genome-scale CD4+ T-cell Perturb-seq study (MIT-licensed). Fetched via `data/fetch_data.sh`; provenance in `data/README.md`. This repo commits no raw data.

## Language / calibration
This tool reports **calibrated** verdicts — "consistent with," "re-derived," "flagged for follow-up," "refuted by," "untested." It does not claim "discovery" or "proof."

## License
MIT — see `LICENSE`.
