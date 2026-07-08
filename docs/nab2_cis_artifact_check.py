"""Cis-artifact + reproducibility check for the NAB2 finding.

Prompted by the source-paper read (docs/source_paper_read_eczema_2026-07-08.md): the disease labels
are Open Targets GWAS-genetic evidence (LD-susceptible), and NAB2 sits 1.9 kb from STAT6 — so the
sharpest confounder is a CRISPRi CIS artifact (a guide targeting NAB2 also repressing STAT6, reading
out STAT6's Th2/eczema biology). Two in-data tests:

1. CIS-ARTIFACT PROXY: clusters are built from perturbation-effect correlations (HDBSCAN). If NAB2-KD
   really phenocopied STAT6-KD (because it repressed STAT6), they would co-cluster. Do they?
2. REPRODUCIBILITY (the paper's own bar for novel nominations): cross-guide & cross-donor correlation.

Definitive test NOT possible from our 4 tables (needs the deposited per-perturbation x per-gene DE
matrix — authors' repo github.com/emdann/GWT_perturbseq_analysis_2025): does NAB2-KD lower STAT6 mRNA?
"""
import sys
sys.path.insert(0, "src")
from arbiter.lbd.referee_triple import load_referee_data

d = load_referee_data()
t1, te, gs = d.t1, d.t3_exploded, "downstream_Stim8hr"

print("REPRODUCIBILITY (paper bar: cross-guide + cross-donor R):")
for g in ["NAB2", "STAT6"]:
    r = t1[(t1.target_contrast_gene_name == g) & (t1.culture_condition == "Stim8hr")]
    if len(r):
        r = r.iloc[0]
        print(f"  {g:6}: eff={r.ontarget_effect_size:+.2f} n_down={int(r.n_downstream)} "
              f"cross-guide R={r.crossguide_correlation:.2f} cross-donor R={r.crossdonor_correlation_mean:.2f} "
              f"offtarget={r.offtarget_flag}")

nab2 = {int(c) for c in te[(te.gene == "NAB2") & (te.gene_set == gs)].cluster.unique()}
stat6 = {int(c) for c in te[(te.gene == "STAT6") & (te.gene_set == gs)].cluster.unique()}
print("\nCIS-ARTIFACT PROXY (do NAB2 & STAT6 co-cluster on perturbation effect?):")
print(f"  NAB2 clusters:  {sorted(nab2)}")
print(f"  STAT6 clusters: {sorted(stat6)}")
print(f"  shared: {sorted(nab2 & stat6)}  -> empty means NAB2-KD does NOT phenocopy STAT6-KD")
print("\nInterpretation: non-overlap + NAB2 more reproducible than STAT6 argue AGAINST the cis "
      "artifact. Definitive check (NAB2-KD -> STAT6 mRNA) requires the deposited DE matrix.")
