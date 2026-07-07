#!/usr/bin/env bash
# Fetch the public Perturb-seq supplementary tables (~25 MB). New-work-only compliant: public data.
set -euo pipefail
cd "$(dirname "$0")"
BASE="https://raw.githubusercontent.com/emdann/GWT_perturbseq_analysis_2025/master/metadata/suppl_tables"
for f in \
  DE_stats.suppl_table.csv \
  Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv \
  cluster_autoimmune_enrichment_results.suppl_table.csv \
  guide_kd_efficiency.suppl_table.csv ; do
  echo "fetching $f"
  curl -sSL -o "$f" "$BASE/$f"
done
echo "done: $(ls -1 *.csv | wc -l) tables"
