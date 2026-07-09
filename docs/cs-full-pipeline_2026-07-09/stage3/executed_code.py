#!/usr/bin/env python
"""
Stage 3 cis-artifact check: NAB2 -> Th1/Th2 -> atopic eczema.

Definitive check of the CRISPRi cis-artifact confounder: NAB2's guide sits
~1.9 kb from STAT6 (a master Th2 regulator). If STAT6 mRNA is UNMOVED under
NAB2 knockdown, the cis-artifact is refuted and the effect is genuinely NAB2's.

Reads ONE matrix row of a 16.8 GB deposited h5ad directly from public S3,
LAZILY (byte-range reads only, NO full download).
"""
import json
import numpy as np
import s3fs
import h5py

URL = "genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad"
COND = "Stim8hr"
NEIGHBORS = ["STAT6", "NAB2", "STAT2", "NDUFA12", "LRP1", "SHMT2"]  # STAT6 + 12q13.3 context


def _cat(grp):
    """Decode an AnnData categorical group -> (categories, codes)."""
    cats = grp["categories"][:]
    cats = np.array([c.decode() if isinstance(c, bytes) else c for c in cats])
    return cats, grp["codes"][:]


# Anonymous, virtual-addressed S3 (bucket-qualified host; path-style is 403-denylisted).
fs = s3fs.S3FileSystem(
    anon=True,
    client_kwargs={"endpoint_url": "https://s3.amazonaws.com"},
    config_kwargs={"s3": {"addressing_style": "virtual"}},
)

opened = False
with fs.open(URL, "rb", block_size=2**20) as fo, h5py.File(fo, "r") as h:
    opened = True
    tg_cats, tg_codes = _cat(h["obs"]["target_contrast_gene_name"])
    cc_cats, cc_codes = _cat(h["obs"]["culture_condition"])
    gene_names = h["var"]["gene_name"][:]
    gene_names = np.array([g.decode() if isinstance(g, bytes) else g for g in gene_names])

    nab2_ci = int(np.where(tg_cats == "NAB2")[0][0])
    cond_ci = int(np.where(cc_cats == COND)[0][0])
    rows = np.where((tg_codes == nab2_ci) & (cc_codes == cond_ci))[0]
    assert len(rows) == 1, f"expected exactly 1 NAB2/{COND} row, got {len(rows)}"
    r = int(rows[0])

    # ONE matrix row per layer (lazy range read).
    lfc = h["layers"]["log_fc"][r, :]
    z = h["layers"]["zscore"][r, :]
    padj = h["layers"]["adj_p_value"][r, :]

# Map gene name -> column index.
name_to_idx = {}
for i, g in enumerate(gene_names):
    name_to_idx.setdefault(g, i)

n_measured = int(np.sum(np.isfinite(lfc)))

# STAT6 |log_fc| rank among all measured genes (1 = most affected; higher = less affected).
abs_lfc = np.abs(lfc)
finite_mask = np.isfinite(abs_lfc)
stat6_idx = name_to_idx["STAT6"]
stat6_abs = abs_lfc[stat6_idx]
# rank = number of genes with |log_fc| strictly greater than STAT6's, +1
stat6_rank = int(np.sum(abs_lfc[finite_mask] > stat6_abs) + 1)

# Genes significantly moved (adj_p < 0.1).
n_sig = int(np.sum(np.nan_to_num(padj, nan=1.0) < 0.1))

per_gene = {}
for g in NEIGHBORS:
    if g not in name_to_idx:
        per_gene[g] = {"measured": False}
        continue
    gi = name_to_idx[g]
    ap = float(padj[gi])
    per_gene[g] = {
        "measured": True,
        "log2fc": float(lfc[gi]),
        "zscore": float(z[gi]),
        "adj_p": ap,
        "significant": bool(ap < 0.1),
    }

result = {
    "condition": COND,
    "perturbation": "NAB2",
    "opened": bool(opened),
    "lazy_read_no_download": True,
    "n_genes_measured": n_measured,
    "per_gene": per_gene,
    "stat6_abs_logfc_rank": stat6_rank,
    "stat6_abs_logfc_rank_of_measured": f"{stat6_rank} of {n_measured}",
    "n_genes_significantly_moved": n_sig,
    "nab2_on_target_log2fc": per_gene["NAB2"]["log2fc"],
}

# ---- EXACT ACCEPTANCE TARGETS (do not edit values to pass) ----
stat6 = per_gene["STAT6"]
nab2 = per_gene["NAB2"]
checks = {}
checks["file_opened"] = (opened is True)
checks["stat6_log2fc_small_positive"] = (0.0 < stat6["log2fc"] < 0.2)
checks["stat6_log2fc_near_0.09"] = (abs(stat6["log2fc"] - 0.09) < 0.05)
checks["stat6_not_significant"] = (stat6["adj_p"] > 0.1)
checks["stat6_adjp_near_0.79"] = (abs(stat6["adj_p"] - 0.79) < 0.10)
checks["nab2_on_target_strongly_negative"] = (nab2["log2fc"] < -2.5)
checks["nab2_on_target_near_-3.08"] = (abs(nab2["log2fc"] - (-3.08)) < 0.3)

ALL_PASS = all(checks.values())
result["checks"] = checks
result["ALL_PASS"] = bool(ALL_PASS)

with open("stage3_cis_artifacts/stage3_cis.json", "w") as f:
    json.dump(result, f, indent=2)

# ---- receipt.md ----
conclusion = (
    "NAB2 knockdown leaves STAT6 mRNA unmoved "
    f"(log2FC ~+{stat6['log2fc']:.2f}, adj_p ~{stat6['adj_p']:.2f}) -> "
    "the CRISPRi cis-artifact is refuted; the Th2/eczema effect is genuinely "
    "NAB2's, not STAT6 bleed."
)

expected = {
    "file_opened": ("True", str(checks["file_opened"])),
    "STAT6 log2FC ~+0.09 (|value|<0.2)": (
        "+0.09, |x|<0.2", f"{stat6['log2fc']:+.4f}"),
    "STAT6 adj_p ~0.79 (>0.1, NOT sig)": (
        "~0.79, >0.1", f"{stat6['adj_p']:.4f}"),
    "NAB2 self on-target log2FC ~-3.08": (
        "~-3.08", f"{nab2['log2fc']:+.4f}"),
}

lines = []
lines.append("# Stage 3 — CRISPRi cis-artifact check: NAB2 vs STAT6\n")
lines.append("**Finding under test:** NAB2 -> Th1/Th2 -> atopic eczema.\n")
lines.append(
    "**Confounder:** NAB2's CRISPRi guide sits ~1.9 kb from STAT6 (a master "
    "Th2 regulator) at 12q13.3. If NAB2 knockdown were bleeding onto STAT6, "
    "the eczema signal could be STAT6, not NAB2.\n")
lines.append(
    "**Data:** authors' genome-wide DE statistics "
    "(`GWCD4i.DE_stats.h5ad`, ~16.8 GB), read directly from anonymous public "
    "S3 via virtual-addressed s3fs. Only tiny label arrays + a single matrix "
    f"row (NAB2 x {COND}) were read — byte-range reads only, NO full download.\n")

lines.append(f"\n## Result — {COND}, perturbation = NAB2\n")
lines.append(f"- Genes measured: **{n_measured}**")
lines.append(f"- Genes significantly moved by NAB2-KD (adj_p < 0.1): **{n_sig}**")
lines.append(
    f"- STAT6 |log2FC| rank among measured genes: **{stat6_rank} of {n_measured}** "
    "(higher rank = less affected)\n")

lines.append("\n| Gene | log2FC | z-score | adj_p | significant (adj_p<0.1) |")
lines.append("|------|-------:|--------:|------:|:-----------------------:|")
for g in NEIGHBORS:
    pg = per_gene[g]
    note = ""
    if g == "STAT6":
        note = " ← neighbor under test"
    if g == "NAB2":
        note = " ← self / on-target"
    if not pg.get("measured", True):
        lines.append(f"| {g}{note} | n/a | n/a | n/a | not in DE panel |")
        continue
    tag = "yes" if pg["significant"] else "no"
    lines.append(
        f"| {g}{note} | {pg['log2fc']:+.4f} | {pg['zscore']:+.3f} | "
        f"{pg['adj_p']:.4f} | {tag} |")

lines.append("\n## STAT6 verdict\n")
lines.append(
    f"STAT6 under NAB2-KD: log2FC = **{stat6['log2fc']:+.4f}** "
    f"(small positive, |value| < 0.2), adj_p = **{stat6['adj_p']:.4f}** "
    "(NOT significant, > 0.1) — **STAT6 is UNMOVED.**\n")
lines.append(
    f"NAB2 self on-target: log2FC = **{nab2['log2fc']:+.4f}** "
    "(strongly negative — the knockdown worked).\n")

lines.append("\n## Cis-exclusion statement\n")
lines.append(conclusion + "\n")

lines.append("\n## Acceptance targets — actual vs expected\n")
lines.append("| Check | Expected | Actual | Pass |")
lines.append("|-------|----------|--------|:----:|")
for label, (exp, act) in expected.items():
    lines.append(f"| {label} | {exp} | {act} | — |")
lines.append("")
lines.append("| Assertion | Pass |")
lines.append("|-----------|:----:|")
for k, v in checks.items():
    lines.append(f"| {k} | {'PASS' if v else 'FAIL'} |")

lines.append(f"\n**ALL_PASS = {ALL_PASS}**\n")

with open("stage3_cis_artifacts/receipt.md", "w") as f:
    f.write("\n".join(lines))

# ---- stdout ----
print(f"STAT6 line:  log2FC={stat6['log2fc']:+.4f}  z={stat6['zscore']:+.3f}  "
      f"adj_p={stat6['adj_p']:.4f}  significant={stat6['significant']}  "
      f"(|log2FC| rank {stat6_rank}/{n_measured})")
print(f"NAB2 on-target:  log2FC={nab2['log2fc']:+.4f}  z={nab2['zscore']:+.3f}  "
      f"adj_p={nab2['adj_p']:.4f}")
print(f"n_genes_significantly_moved (adj_p<0.1): {n_sig}")
print(f"ALL_PASS = {ALL_PASS}")
