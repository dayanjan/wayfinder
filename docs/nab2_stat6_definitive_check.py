"""DEFINITIVE STAT6 cis-artifact check — does NAB2 knockdown move STAT6 expression?

Reads the authors' deposited genome-wide DE results (GWCD4i.DE_stats.h5ad; per-perturbation x
per-gene log_fc/zscore/adj_p) DIRECTLY from the public S3 bucket, LAZILY (only the chunks needed —
no 16.8 GB download). Public data, no credentials (anon S3).

If NAB2-KD leaves STAT6 unchanged (log_fc ~ 0, non-significant), the CRISPRi cis-artifact is refuted
definitively: the Th2/eczema effect is genuinely NAB2's, not STAT6 bleed via the 1.9 kb neighbor.

Source: github.com/emdann/GWT_perturbseq_analysis_2025 ; Biohub Virtual Cells Platform
   s3://genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad
Run: python docs/nab2_stat6_definitive_check.py   (needs h5py, s3fs)
"""
import numpy as np
import s3fs
import h5py

URL = "genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad"
COND = "Stim8hr"
NEIGHBORS = ["STAT6", "NAB2", "STAT2", "NDUFA12", "LRP1", "SHMT2"]  # STAT6 + 12q13/12q13.3 context


def _cat(grp):
    cats = grp["categories"][:]
    cats = np.array([c.decode() if isinstance(c, bytes) else c for c in cats])
    return cats, grp["codes"][:]


fs = s3fs.S3FileSystem(anon=True)
with fs.open(URL, "rb", block_size=2 ** 20) as fo, h5py.File(fo, "r") as h:
    tg_cats, tg_codes = _cat(h["obs"]["target_contrast_gene_name"])
    cc_cats, cc_codes = _cat(h["obs"]["culture_condition"])
    gene_names = h["var"]["gene_name"][:]
    gene_names = np.array([g.decode() if isinstance(g, bytes) else g for g in gene_names])

    nab2_ci = int(np.where(tg_cats == "NAB2")[0][0])
    cond_ci = int(np.where(cc_cats == COND)[0][0])
    rows = np.where((tg_codes == nab2_ci) & (cc_codes == cond_ci))[0]
    assert len(rows) == 1, f"expected 1 NAB2@{COND} row, got {len(rows)}"
    r = int(rows[0])
    print(f"NAB2 @ {COND}: obs row {r}  (of {len(tg_codes)} perturbation-condition rows)")

    # read the full NAB2 row across all genes from each layer (one row = cheap)
    lfc = h["layers"]["log_fc"][r, :]
    z = h["layers"]["zscore"][r, :]
    padj = h["layers"]["adj_p_value"][r, :]

    print("\nDE of selected genes UNDER NAB2 knockdown (@Stim8hr):")
    print(f"{'gene':10} {'log2FC':>8} {'zscore':>8} {'adj_p':>10}  significant?")
    for g in NEIGHBORS:
        j = np.where(gene_names == g)[0]
        if len(j) == 0:
            print(f"{g:10}  (not measured)")
            continue
        j = int(j[0])
        sig = "YES" if (padj[j] == padj[j] and padj[j] < 0.1) else "no"
        print(f"{g:10} {lfc[j]:8.3f} {z[j]:8.2f} {padj[j]:10.2e}  {sig}")

    # rank STAT6's |log_fc| among all genes moved by NAB2
    js = np.where(gene_names == "STAT6")[0]
    if len(js):
        j = int(js[0])
        finite = np.isfinite(lfc)
        stronger = int(np.sum(np.abs(lfc[finite]) > abs(lfc[j])))
        print(f"\nSTAT6 is moved LESS than {stronger} other genes by NAB2-KD "
              f"(rank {stronger+1} of {int(finite.sum())} measured; higher rank = less affected).")
        n_sig = int(np.sum((padj < 0.1) & np.isfinite(padj)))
        print(f"NAB2-KD significantly moves {n_sig} genes total; is STAT6 among them? "
              f"{'YES' if (padj[j]==padj[j] and padj[j]<0.1) else 'NO'}.")
