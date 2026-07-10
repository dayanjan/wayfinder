# Data — genome-scale CD4+ T-cell Perturb-seq (public supplementary tables)

Source: Zhu, Dann, et al. (Marson & Pritchard labs), *Genome-scale perturb-seq in
primary human CD4+ T cells* (bioRxiv 2025; doi:10.64898/2025.12.23.696273). Public
supplementary tables, used under the hackathon's public-dataset provision; the
analysis-reference repository (github.com/emdann/GWT_perturbseq_analysis_2025) is
MIT-licensed. This repo commits no raw data; run `fetch_data.sh` to reproduce.

Files fetched (~25 MB total):
- `DE_stats.suppl_table.csv` — per perturbation x condition: up/down genes, on-target effect, cross-donor/guide reproducibility. (Hop 1: gene -> effect.)
- `Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv` — per-gene log_fc/zscore/p in the Th1/Th2 contrast. (Hop 2: gene -> program.)
- `cluster_autoimmune_enrichment_results.suppl_table.csv` — cluster -> disease odds ratios + intersecting genes. (Hop 3: program -> disease.)
- `guide_kd_efficiency.suppl_table.csv` — guide knockdown efficiency + significance. (QC gate.)

Full raw dataset (22M cells, h5ad) is available via the CZI Virtual Cells platform / vcp-cli
and S3, but is NOT needed: the aggregated tables above are the validation substrate.
