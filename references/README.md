# References — source dataset paper & analysis code

## Source paper (the dataset our finding is built on)
Genome-scale CD4+ T-cell Perturb-seq study (Dann, Pritchard, Marson, and colleagues).
- **bioRxiv preprint:** 2025.12.23.696273v1 — https://www.biorxiv.org/content/10.1101/2025.12.23.696273v1
- **DOI:** 10.1101/2025.12.23.696273
- Local copy (gitignored, not redistributed — bioRxiv preprint): `Zhu_etal_2025_CD4_Perturbseq_bioRxiv_2025.12.23.696273.pdf`
- Supplementary tables we use are in `data/` (fetch via `data/fetch_data.sh`; public).
- *(Confirm the exact author list / title from the PDF when citing formally — see the
  independent read at `docs/source_paper_read_eczema_2026-07-08.md`.)*

## Analysis code (authors' own scripts, durable pointer)
**https://github.com/emdann/GWT_perturbseq_analysis_2025** — the authors' analysis repository for
this dataset (Emma Dann et al.). Contains the scripts used to produce the supplementary tables we
consume (DE stats, guide KD efficiency, the Th1/Th2 polarization signature, and the
**cluster autoimmune-disease enrichment** — the last is directly relevant to our STAT6-confounder
question: it defines how genes were grouped into modules and how disease enrichment was computed,
which determines whether NAB2's atopic-eczema signal is expression/co-regulation-driven or
locus-driven). Consult this repo to confirm the enrichment method (GWAS-locus overlap vs
co-expression module) if the paper text is ambiguous.

## Why this matters to our finding
Our NAB2 → Th1/Th2 → atopic-eczema finding rests on these tables. The paper + code are the ground
truth for: (1) how the Th1/Th2 program signature was derived, (2) how the autoimmune-disease cluster
enrichment (our T3) was computed — the load-bearing input to the STAT6-adjacency confounder analysis
(`docs/nab2_knowledge_synthesis_2026-07-08.md` §1).

## Deposited processed data (public S3, no credentials)
Biohub Virtual Cells Platform: `s3://genome-scale-tcell-perturb-seq/marson2025_data/` (`aws s3 ls --no-sign-request ...`). Key file for us: **`GWCD4i.DE_stats.h5ad`** (16.8 GB) — the genome-wide per-perturbation x per-gene DE results (`.layers`: log_fc/zscore/adj_p). We read it **lazily** (h5py+s3fs, only the needed chunks — no full download) to run the **definitive STAT6 cis-artifact check** (`docs/nab2_stat6_definitive_check.py`): NAB2 knockdown leaves STAT6 unmoved → cis artifact refuted. Raw single-cell matrices (D*_*.assigned_guide.h5ad, ~140 GB each) are the off-limits large data; the DE results are the CPU-feasible slice.
