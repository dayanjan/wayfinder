from __future__ import annotations

import gzip
import json
import math
import os
import re
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


OUT = Path("docs/nab2-direction-geo_2026-07-09")
DL = OUT / "downloads"
DL.mkdir(parents=True, exist_ok=True)

URLS = {
    "GSE32959_matrix.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE32nnn/GSE32959/matrix/GSE32959_series_matrix.txt.gz",
    "GSE17851_matrix.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17851/matrix/GSE17851_series_matrix.txt.gz",
    "GSE130588_matrix.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE130nnn/GSE130588/matrix/GSE130588_series_matrix.txt.gz",
    "GSE330551_matrix.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE330nnn/GSE330551/matrix/GSE330551_series_matrix.txt.gz",
    "GSE330551_counts.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE330nnn/GSE330551/suppl/GSE330551_counts.txt.gz",
    "GSE292848-GPL24676_matrix.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE292nnn/GSE292848/matrix/GSE292848-GPL24676_series_matrix.txt.gz",
    "GSE292848-GPL34284_matrix.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE292nnn/GSE292848/matrix/GSE292848-GPL34284_series_matrix.txt.gz",
    "GSE292848_raw_exon_counts_all.txt.gz": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE292nnn/GSE292848/suppl/GSE292848_raw_exon_counts_all.txt.gz",
    "GPL570.annot.gz": "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPLnnn/GPL570/annot/GPL570.annot.gz",
    "GPL6102.annot.gz": "https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL6nnn/GPL6102/annot/GPL6102.annot.gz",
}

NAB2_SYMBOL = "NAB2"
STAT6_SYMBOL = "STAT6"
NAB2_ENSEMBL = "ENSG00000166886"
STAT6_ENSEMBL = "ENSG00000166888"
GPL570_NAB2_PROBES = ["212803_at", "216017_s_at"]
GPL6102_NAB2_PROBES = ["ILMN_1663554"]
TYPE2_SYMBOLS = ["IL13", "IL4", "IL5", "IL31", "CCL17", "CCL22", "CCL26", "TSLP", "IL4R"]
TYPE2_CHEM_RECEPTOR = ["CCL17", "CCL22", "CCL26", "TSLP", "IL4R", "IL31"]
ENSEMBL_BY_SYMBOL = {
    "NAB2": "ENSG00000166886",
    "STAT6": "ENSG00000166888",
    "IL13": "ENSG00000169194",
    "IL4": "ENSG00000113520",
    "IL5": "ENSG00000113525",
    "IL31": "ENSG00000112293",
    "CCL17": "ENSG00000102970",
    "CCL22": "ENSG00000102962",
    "CCL26": "ENSG00000234177",
    "TSLP": "ENSG00000145777",
    "IL4R": "ENSG00000077238",
}


def download_all() -> None:
    opener = urllib.request.build_opener()
    api_key = os.environ.get("NCBI_API_KEY")
    if api_key is None:
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("NCBI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break
    # GEO FTP downloads do not require the key; this only records that the allowed key was available.
    key_state = "env" if os.environ.get("NCBI_API_KEY") else ("dotenv" if api_key else "not_used")
    (OUT / "download_note.json").write_text(json.dumps({"ncbi_api_key_source": key_state}, indent=2), encoding="utf-8")
    for name, url in URLS.items():
        path = DL / name
        if not path.exists() or path.stat().st_size == 0:
            print(f"download {name}")
            urllib.request.urlretrieve(url, path)


def clean(x):
    if isinstance(x, str):
        return x.strip().strip('"')
    return x


def parse_geo_matrix(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    meta_lines = []
    begin = end = None
    with gzip.open(path, "rt", errors="replace") as f:
        for i, line in enumerate(f):
            if line.startswith("!series_matrix_table_begin"):
                begin = i
            elif line.startswith("!series_matrix_table_end"):
                end = i
                break
            elif line.startswith("!Sample_"):
                meta_lines.append(line.rstrip("\n"))
    if begin is None or end is None:
        expr = pd.DataFrame()
    else:
        expr = pd.read_csv(path, sep="\t", compression="gzip", skiprows=begin + 1, nrows=end - begin - 1)
        expr.columns = [clean(c) for c in expr.columns]
        if "ID_REF" in expr.columns:
            expr = expr.rename(columns={"ID_REF": "ID"})
        expr["ID"] = expr["ID"].map(clean)
        expr = expr.set_index("ID")
        expr = expr.apply(pd.to_numeric, errors="coerce")

    fields: dict[str, list[list[str]]] = {}
    for line in meta_lines:
        vals = [clean(v) for v in line.split("\t")]
        fields.setdefault(vals[0], []).append(vals[1:])
    accessions = fields.get("!Sample_geo_accession", [[]])[0]
    md = pd.DataFrame(index=accessions)
    for key, rows in fields.items():
        base = key.replace("!Sample_", "").replace("_ch1", "")
        for j, vals in enumerate(rows):
            col = base if len(rows) == 1 else f"{base}_{j}"
            if len(vals) == len(md):
                md[col] = vals
            if "characteristics" in base or "description" in base:
                for k, v in enumerate(vals):
                    if ":" in str(v):
                        kk, vv = str(v).split(":", 1)
                        md.loc[accessions[k], kk.strip().lower().replace(" ", "_")] = vv.strip()
    return expr, md


def read_annot(path: Path) -> pd.DataFrame:
    header = None
    rows = []
    with gzip.open(path, "rt", errors="replace") as f:
        for line in f:
            if line.startswith("#") or line.startswith("!") or line.startswith("^"):
                continue
            if line.startswith("ID\t"):
                header = line.rstrip("\n").split("\t")
            elif header is not None:
                rows.append(line.rstrip("\n").split("\t"))
    df = pd.DataFrame(rows, columns=header)
    df["ID"] = df["ID"].map(clean)
    return df.set_index("ID")


def bh(pvals: np.ndarray) -> np.ndarray:
    p = np.asarray(pvals, dtype=float)
    out = np.full(p.shape, np.nan)
    ok = np.isfinite(p)
    pv = p[ok]
    if pv.size == 0:
        return out
    order = np.argsort(pv)
    ranked = pv[order]
    m = len(ranked)
    q = ranked * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    tmp = np.empty_like(q)
    tmp[order] = np.minimum(q, 1.0)
    out[ok] = tmp
    return out


def design_matrix(md: pd.DataFrame, terms: list[str], intercept=True) -> tuple[np.ndarray, list[str]]:
    cols = []
    names = []
    if intercept:
        cols.append(np.ones(len(md)))
        names.append("intercept")
    for term in terms:
        s = md[term]
        if pd.api.types.is_numeric_dtype(s) or set(pd.Series(s).dropna().unique()).issubset({0, 1, 0.0, 1.0}):
            cols.append(pd.to_numeric(s).to_numpy(dtype=float))
            names.append(term)
        else:
            d = pd.get_dummies(s.astype(str), prefix=term, drop_first=True, dtype=float)
            for c in d.columns:
                cols.append(d[c].to_numpy(dtype=float))
                names.append(c)
    X = np.column_stack(cols)
    keep = []
    keep_names = []
    rank = 0
    for i in range(X.shape[1]):
        trial = X[:, keep + [i]]
        r = np.linalg.matrix_rank(trial)
        if r > rank:
            keep.append(i)
            keep_names.append(names[i])
            rank = r
    return X[:, keep], keep_names


def lm_contrast(expr: pd.DataFrame, md: pd.DataFrame, terms: list[str], contrast_name: str) -> pd.DataFrame:
    X, names = design_matrix(md, terms)
    if contrast_name not in names:
        raise ValueError(f"contrast {contrast_name} not estimable; columns={names}")
    c = np.zeros(len(names))
    c[names.index(contrast_name)] = 1.0
    Y = expr.loc[:, md.index].T.to_numpy(dtype=float)
    ok_genes = np.isfinite(Y).all(axis=0)
    Y2 = Y[:, ok_genes]
    pinv = np.linalg.pinv(X)
    beta = pinv @ Y2
    fitted = X @ beta
    resid = Y2 - fitted
    df = X.shape[0] - np.linalg.matrix_rank(X)
    rss = np.sum(resid * resid, axis=0)
    sigma2 = rss / max(df, 1)
    xtx_inv = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.maximum(sigma2 * float(c @ xtx_inv @ c), 0))
    effect = c @ beta
    t = effect / se
    p = 2 * stats.t.sf(np.abs(t), df=max(df, 1))
    full_effect = np.full(expr.shape[0], np.nan)
    full_p = np.full(expr.shape[0], np.nan)
    full_effect[ok_genes] = effect
    full_p[ok_genes] = p
    res = pd.DataFrame({"log2fc": full_effect, "p": full_p}, index=expr.index)
    res["fdr"] = bh(res["p"].to_numpy())
    return res


def logcpm(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0)
    return np.log2((counts + 0.5).div(lib + 1.0, axis=1) * 1_000_000)


def zscore_rows(df: pd.DataFrame) -> pd.DataFrame:
    mu = df.mean(axis=1)
    sd = df.std(axis=1).replace(0, np.nan)
    return df.sub(mu, axis=0).div(sd, axis=0)


def pick_symbol_rows(expr: pd.DataFrame, annot: pd.DataFrame, symbols: list[str]) -> tuple[pd.DataFrame, dict]:
    picked = []
    evidence = {}
    for sym in symbols:
        mask = annot["Gene symbol"].fillna("").str.split(" /// ").apply(lambda xs: sym in [x.strip() for x in xs])
        ids = [x for x in annot.index[mask] if x in expr.index]
        evidence[sym] = ids
        if ids:
            means = expr.loc[ids].mean(axis=1)
            picked_id = means.idxmax()
            picked.append((sym, picked_id, expr.loc[picked_id]))
    if not picked:
        return pd.DataFrame(index=symbols, columns=expr.columns), evidence
    return pd.DataFrame({sym: vals for sym, _pid, vals in picked}).T, evidence


def selected_symbol_probe(expr: pd.DataFrame, annot: pd.DataFrame, symbol: str) -> str | None:
    mask = annot["Gene symbol"].fillna("").str.split(" /// ").apply(lambda xs: symbol in [x.strip() for x in xs])
    ids = [x for x in annot.index[mask] if x in expr.index]
    if not ids:
        return None
    return expr.loc[ids].mean(axis=1).idxmax()


def type2_score(expr_by_gene: pd.DataFrame, samples: list[str]) -> tuple[pd.Series, dict]:
    scores, meta = type2_score_variants(expr_by_gene, samples)
    score = scores.get("detection_filtered") if "detection_filtered" in scores else next(iter(scores.values()))
    return score, meta


def type2_score_variants(expr_by_gene: pd.DataFrame, samples: list[str]) -> tuple[dict[str, pd.Series], dict]:
    present_full = [g for g in TYPE2_SYMBOLS if g in expr_by_gene.index]
    detected = []
    for g in present_full:
        vals = expr_by_gene.loc[g, samples]
        thresh = np.nanpercentile(expr_by_gene.loc[:, samples].to_numpy(), 25)
        if float((vals > thresh).mean()) >= 0.20:
            detected.append(g)
    chem = [g for g in TYPE2_CHEM_RECEPTOR if g in expr_by_gene.index]
    scores = {}
    if present_full:
        scores["full"] = zscore_rows(expr_by_gene.loc[present_full, samples]).mean(axis=0)
    if detected:
        scores["detection_filtered"] = zscore_rows(expr_by_gene.loc[detected, samples]).mean(axis=0)
    if chem:
        scores["chemokine_receptor"] = zscore_rows(expr_by_gene.loc[chem, samples]).mean(axis=0)
    return scores, {
        "full_genes_present": present_full,
        "detection_filtered_genes": detected,
        "chemokine_receptor_genes_present": chem,
        "dropped_full": [g for g in TYPE2_SYMBOLS if g not in present_full],
    }


def spearman_pair(x: pd.Series, y: pd.Series) -> dict:
    both = pd.concat([x, y], axis=1).dropna()
    if len(both) < 3:
        return {"rho": None, "p": None, "n": len(both)}
    rho, p = stats.spearmanr(both.iloc[:, 0], both.iloc[:, 1])
    return {"rho": float(rho), "p": float(p), "fdr": float(p), "n": int(len(both))}


def type2_rhos(nab2: pd.Series, scores: dict[str, pd.Series]) -> dict[str, dict]:
    return {name: spearman_pair(nab2, score) for name, score in scores.items()}


def gate_direction(effect: float | None, fdr: float | None, threshold=0.3) -> str:
    if effect is None or fdr is None or not np.isfinite(effect) or not np.isfinite(fdr):
        return "NO-CALL"
    if abs(effect) >= threshold and fdr < 0.05:
        return "UP" if effect > 0 else "DOWN"
    return "NO-CALL"


def probe_call(rows: list[dict]) -> tuple[str, str]:
    passed = [r for r in rows if r.get("direction") in {"UP", "DOWN"}]
    signs = {r["direction"] for r in rows if r.get("direction") in {"UP", "DOWN"}}
    all_nonzero_signs = {("UP if positive" if r.get("log2fc", 0) > 0 else "DOWN if negative") for r in rows if r.get("log2fc") is not None}
    raw_signs = {np.sign(r.get("log2fc")) for r in rows if r.get("log2fc") is not None and np.isfinite(r.get("log2fc")) and r.get("log2fc") != 0}
    if len(raw_signs) > 1:
        return "AMBIGUOUS", "array probes are sign-discordant"
    if not passed:
        return "NO-CALL", "no NAB2 probe passed the per-arm gate"
    if len(signs) == 1:
        return signs.pop(), f"{len(passed)}/{len(rows)} NAB2 probes passed; raw signs={sorted(all_nonzero_signs)}"
    return "AMBIGUOUS", "passing NAB2 probes are sign-discordant"


def prepare_gse330551(md: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = pd.read_csv(DL / "GSE330551_counts.txt.gz", sep="\t", compression="gzip", skiprows=1)
    raw = raw.rename(columns={"Geneid": "gene"})
    count_cols = list(raw.columns[6:])
    libnames = md["library_name"].str.replace("Library name: ", "", regex=False) if "library_name" in md else md["description_0"].str.replace("Library name: ", "", regex=False)
    libnames = libnames.map(lambda x: str(x).strip())
    summed = {}
    for acc, lib in libnames.items():
        cols = [c for c in count_cols if c.startswith(lib + "_")]
        if cols:
            summed[acc] = raw[cols].sum(axis=1)
    counts = pd.DataFrame(summed)
    counts.index = raw["gene"].astype(str)
    counts = counts.groupby(level=0).sum()
    md2 = md.loc[[c for c in counts.columns if c in md.index]].copy()
    return counts.loc[:, md2.index], md2


def prepare_gse292848(md1: pd.DataFrame, md2: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    first = gzip.open(DL / "GSE292848_raw_exon_counts_all.txt.gz", "rt", errors="replace").readline().rstrip("\n").split("\t")
    sample_cols = [clean(x) for x in first]
    df = pd.read_csv(DL / "GSE292848_raw_exon_counts_all.txt.gz", sep="\t", compression="gzip", header=None, skiprows=1)
    df.columns = ["gene"] + sample_cols
    df["gene"] = df["gene"].map(clean)
    counts = df.set_index("gene").apply(pd.to_numeric, errors="coerce")
    md = pd.concat([md1, md2], axis=0)
    colmap = {}
    for acc, row in md.iterrows():
        vals = [str(v) for v in row.values]
        col = None
        for v in vals:
            if "Column name in raw_exon_counts_all.txt.gz:" in v:
                col = v.split(":", 1)[1].strip()
        if col in counts.columns:
            colmap[col] = acc
    counts = counts.loc[:, list(colmap.keys())].rename(columns=colmap)
    md = md.loc[list(colmap.values())].copy()
    return counts, md


def gene_rows_from_rna(log_expr: pd.DataFrame, symbol_to_id: dict[str, str]) -> pd.DataFrame:
    rows = {}
    for sym, ens in symbol_to_id.items():
        if sym in log_expr.index:
            rows[sym] = log_expr.loc[sym]
        elif ens in log_expr.index:
            rows[sym] = log_expr.loc[ens]
    return pd.DataFrame(rows).T


def main() -> dict:
    download_all()
    gpl570 = read_annot(DL / "GPL570.annot.gz")
    gpl6102 = read_annot(DL / "GPL6102.annot.gz")
    results = {"arms": {}, "deferred": ["scRNA ARM-D (GSE204762) deferred", "all backup datasets deferred"]}

    # ARM A: GSE330551 baseline lesional vs non-lesional, with lesion/control sensitivity and type-2 rho.
    _expr_a, md_a0 = parse_geo_matrix(DL / "GSE330551_matrix.txt.gz")
    counts_a, md_a = prepare_gse330551(md_a0)
    log_a = logcpm(counts_a)
    md_a["lesion"] = md_a["tissue_type"].str.lower().str.contains("lesion") & ~md_a["tissue_type"].str.lower().str.contains("non")
    md_a["nonlesion"] = md_a["tissue_type"].str.lower().str.contains("non lesion")
    md_a["control"] = md_a["tissue_type"].str.lower().eq("control")
    md_a["baseline"] = md_a["time"].astype(str).str.contains("Visit 3/BL", regex=False) | md_a["control"]
    base_pair = md_a[md_a["baseline"] & (md_a["lesion"] | md_a["nonlesion"])].copy()
    base_pair["is_lesion"] = base_pair["lesion"].astype(int)
    res_a = lm_contrast(log_a, base_pair, ["is_lesion", "patient"], "is_lesion")
    lesion_control = md_a[(md_a["baseline"]) & (md_a["lesion"] | md_a["control"])].copy()
    lesion_control["is_lesion"] = lesion_control["lesion"].astype(int)
    res_a_ctrl = lm_contrast(log_a, lesion_control, ["is_lesion"], "is_lesion")
    gene_a = gene_rows_from_rna(log_a, {**ENSEMBL_BY_SYMBOL, "NAB2": "NAB2", "STAT6": "STAT6"})
    scores_a, score_meta_a = type2_score_variants(gene_a, list(md_a.index))
    score_a = scores_a.get("detection_filtered", next(iter(scores_a.values())))
    rho_three_a = type2_rhos(gene_a.loc["NAB2"], scores_a)
    rho_a = rho_three_a.get("detection_filtered", next(iter(rho_three_a.values())))
    stat6_a = res_a.loc["STAT6"].to_dict() if "STAT6" in res_a.index else {}
    arm_a_dir = gate_direction(float(res_a.loc["NAB2", "log2fc"]), float(res_a.loc["NAB2", "fdr"]))
    rho_dir = None
    if rho_a["rho"] is not None and abs(rho_a["rho"]) >= 0.3 and rho_a["p"] < 0.05:
        rho_dir = "UP" if rho_a["rho"] > 0 else "DOWN"
    if arm_a_dir in {"UP", "DOWN"} and rho_dir and rho_dir != arm_a_dir:
        arm_a_call, arm_a_reason = "AMBIGUOUS", "primary lesional FC and type-2 rho disagree in sign"
    else:
        arm_a_call, arm_a_reason = arm_a_dir, "primary baseline lesional-vs-nonlesional paired model"
    results["arms"]["A"] = {
        "dataset": "GSE330551",
        "contrast": "baseline Lesion vs Non-Lesion, patient fixed effect; sensitivity Lesion vs Control",
        "preflight": {"n_samples": int(len(md_a)), "n_primary_samples": int(len(base_pair)), "NAB2_resolved": "NAB2 row", "STAT6_resolved": "STAT6 row"},
        "primary": {"gene": "NAB2", **{k: float(v) for k, v in res_a.loc["NAB2"].to_dict().items()}, "direction": arm_a_dir},
        "lesion_vs_control_sensitivity": {k: float(v) for k, v in res_a_ctrl.loc["NAB2"].to_dict().items()},
        "type2_rho": rho_a,
        "type2_rho_three_scores": rho_three_a,
        "type2_score": score_meta_a,
        "STAT6": {k: float(v) for k, v in stat6_a.items()},
        "arm_call": arm_a_call,
        "reason": arm_a_reason,
    }

    # ARM T: GSE32959 Th2 vs Th1 primary, both NAB2 probes.
    expr_t, md_t = parse_geo_matrix(DL / "GSE32959_matrix.txt.gz")
    title_t = md_t["title"]
    md_t["condition_raw"] = title_t.str.extract(r"CD4\+_(Act(?:\+IL-12|\+IL-4)?|0h)_", expand=False)
    md_t["condition"] = md_t["condition_raw"].replace({"Act+IL-12": "Th1", "Act+IL-4": "Th2", "Act": "Act"})
    md_t["time"] = title_t.str.extract(r"_(\d+h)_rep", expand=False)
    md_t["rep"] = title_t.str.extract(r"_rep(\d+)", expand=False)
    tt = md_t[md_t["condition"].isin(["Th1", "Th2"]) & md_t["time"].isin(["12h", "24h", "48h", "72h"])].copy()
    tt["is_th2"] = (tt["condition"] == "Th2").astype(int)
    res_t = lm_contrast(expr_t, tt, ["is_th2", "time", "rep"], "is_th2")
    array_gene_t, ann_ev_t = pick_symbol_rows(expr_t, gpl570, TYPE2_SYMBOLS + [STAT6_SYMBOL])
    scores_t, score_meta_t = type2_score_variants(array_gene_t, list(tt.index))
    score_t = scores_t.get("detection_filtered", next(iter(scores_t.values())))
    probe_rows_t = []
    for probe in GPL570_NAB2_PROBES:
        row = res_t.loc[probe]
        d = gate_direction(float(row["log2fc"]), float(row["fdr"]))
        probe_rows_t.append({"probe": probe, "log2fc": float(row["log2fc"]), "p": float(row["p"]), "fdr": float(row["fdr"]), "direction": d, "type2_rho": spearman_pair(expr_t.loc[probe, tt.index], score_t), "type2_rho_three_scores": type2_rhos(expr_t.loc[probe, tt.index], scores_t)})
    arm_t_call, arm_t_reason = probe_call(probe_rows_t)
    stat6_probe_t = selected_symbol_probe(expr_t, gpl570, STAT6_SYMBOL)
    results["arms"]["T"] = {
        "dataset": "GSE32959",
        "contrast": "CD4 Th2(IL-4) vs Th1(IL-12), 12-72h, adjusted for time and biological replicate",
        "preflight": {"n_samples": int(len(tt)), "NAB2_resolved": GPL570_NAB2_PROBES, "platform_mapping": {p: gpl570.loc[p, ["Gene symbol", "Gene ID"]].to_dict() for p in GPL570_NAB2_PROBES}},
        "primary_probes": probe_rows_t,
        "type2_score": score_meta_t,
        "STAT6": {"selected_probe": stat6_probe_t, **({k: float(v) for k, v in res_t.loc[stat6_probe_t].to_dict().items()} if stat6_probe_t in res_t.index else {})},
        "arm_call": arm_t_call,
        "reason": arm_t_reason,
        "source_polarity_crosscheck": "source finding T2 signature polarity is +log_fc = Th2; this arm uses +log2FC = Th2 over Th1",
    }

    # ARM B: GSE292848 cytokines vs paired NativeSkin controls.
    _e1, md_b1 = parse_geo_matrix(DL / "GSE292848-GPL24676_matrix.txt.gz")
    _e2, md_b2 = parse_geo_matrix(DL / "GSE292848-GPL34284_matrix.txt.gz")
    counts_b, md_b = prepare_gse292848(md_b1, md_b2)
    log_b = logcpm(counts_b)
    md_b["donor"] = md_b["donor"].astype(str)
    md_b["treatment_clean"] = md_b["treatment"].str.replace(" \\(100 ng/mL\\)", "", regex=True).str.replace("PBS with 0.1% BSA", "Control", regex=False).str.replace("IL-4 + IL-13", "IL4_IL13", regex=False).str.replace("IL-4", "IL4", regex=False).str.replace("IL-13", "IL13", regex=False).str.replace("IL-22", "IL22", regex=False)
    gene_b = gene_rows_from_rna(log_b, ENSEMBL_BY_SYMBOL)
    scores_b, score_meta_b = type2_score_variants(gene_b, list(md_b.index))
    score_b = scores_b.get("detection_filtered", next(iter(scores_b.values())))
    rho_three_b = type2_rhos(gene_b.loc["NAB2"], scores_b)
    b_contrasts = []
    for treatment in ["IL4", "IL13", "IL4_IL13", "IL22"]:
        sub = md_b[md_b["treatment_clean"].isin(["Control", treatment])].copy()
        sub["is_treat"] = (sub["treatment_clean"] == treatment).astype(int)
        res = lm_contrast(log_b, sub, ["is_treat", "donor"], "is_treat")
        stat6 = res.loc[STAT6_ENSEMBL].to_dict() if STAT6_ENSEMBL in res.index else {}
        b_contrasts.append({
            "contrast": f"{treatment} vs Control",
            "gene": NAB2_ENSEMBL,
            **{k: float(v) for k, v in res.loc[NAB2_ENSEMBL].to_dict().items()},
            "direction": gate_direction(float(res.loc[NAB2_ENSEMBL, "log2fc"]), float(res.loc[NAB2_ENSEMBL, "fdr"])),
            "STAT6": {k: float(v) for k, v in stat6.items()},
            "type2_rho": rho_three_b.get("detection_filtered", next(iter(rho_three_b.values()))),
            "type2_rho_three_scores": rho_three_b,
        })
    primary_b = next(x for x in b_contrasts if x["contrast"].startswith("IL4_IL13"))
    dirs_b = {x["direction"] for x in b_contrasts if x["contrast"].split()[0] in {"IL4", "IL13", "IL4_IL13"} and x["direction"] in {"UP", "DOWN"}}
    if len(dirs_b) > 1:
        arm_b_call, arm_b_reason = "AMBIGUOUS", "IL-4/IL-13 cytokine contrasts disagree"
    else:
        arm_b_call = primary_b["direction"]
        arm_b_reason = "primary endpoint is IL4_IL13 vs Control; single-cytokine contrasts are co-reported"
    results["arms"]["B"] = {
        "dataset": "GSE292848",
        "contrast": "NativeSkin cytokine treatment vs paired control, donor fixed effect",
        "preflight": {"n_samples": int(len(md_b)), "NAB2_resolved": NAB2_ENSEMBL, "STAT6_resolved": STAT6_ENSEMBL},
        "primary": primary_b,
        "all_cytokine_contrasts": b_contrasts,
        "type2_score": score_meta_b,
        "arm_call": arm_b_call,
        "reason": arm_b_reason,
    }

    # ARM C: GSE130588 dupilumab reversal using treatment/time/lesion/subject fixed model.
    expr_c, md_c = parse_geo_matrix(DL / "GSE130588_matrix.txt.gz")
    ad = md_c[md_c["treatment"].isin(["Dupilumab", "Placebo"]) & md_c["time"].isin(["Week0", "Week16"]) & md_c["tissue"].isin(["LS", "NL"])].copy()
    ad["week16"] = (ad["time"] == "Week16").astype(int)
    ad["ls"] = (ad["tissue"] == "LS").astype(int)
    ad["dup_week16"] = ((ad["treatment"] == "Dupilumab") & (ad["time"] == "Week16")).astype(int)
    res_c = lm_contrast(expr_c, ad, ["week16", "dup_week16", "ls", "subject_id"], "dup_week16")
    array_gene_c, ann_ev_c = pick_symbol_rows(expr_c, gpl570, TYPE2_SYMBOLS + [STAT6_SYMBOL])
    scores_c, score_meta_c = type2_score_variants(array_gene_c, list(ad.index))
    score_c = scores_c.get("detection_filtered", next(iter(scores_c.values())))
    probe_rows_c = []
    for probe in GPL570_NAB2_PROBES:
        row = res_c.loc[probe]
        d = gate_direction(float(row["log2fc"]), float(row["fdr"]))
        probe_rows_c.append({"probe": probe, "log2fc": float(row["log2fc"]), "p": float(row["p"]), "fdr": float(row["fdr"]), "direction": d, "type2_rho": spearman_pair(expr_c.loc[probe, ad.index], score_c), "type2_rho_three_scores": type2_rhos(expr_c.loc[probe, ad.index], scores_c)})
    arm_c_call, arm_c_reason = probe_call(probe_rows_c)
    stat6_probe_c = selected_symbol_probe(expr_c, gpl570, STAT6_SYMBOL)
    results["arms"]["C"] = {
        "dataset": "GSE130588",
        "contrast": "Dupilumab Week16 reversal beyond placebo, adjusted for time, lesion, and subject",
        "preflight": {"n_samples": int(len(ad)), "NAB2_resolved": GPL570_NAB2_PROBES, "platform_mapping": {p: gpl570.loc[p, ["Gene symbol", "Gene ID"]].to_dict() for p in GPL570_NAB2_PROBES}},
        "primary_probes": probe_rows_c,
        "type2_score": score_meta_c,
        "STAT6": {"selected_probe": stat6_probe_c, **({k: float(v) for k, v in res_c.loc[stat6_probe_c].to_dict().items()} if stat6_probe_c in res_c.index else {})},
        "arm_call": arm_c_call,
        "reason": arm_c_reason,
    }

    # STAT6 direct test: GSE17851.
    expr_s, md_s = parse_geo_matrix(DL / "GSE17851_matrix.txt.gz")
    md_s["sirna"] = md_s["genome/variation"].str.replace(" siRNA", "", regex=False).str.replace("Control", "Control", regex=False).str.replace("STAT6", "STAT6", regex=False)
    md_s["condition"] = md_s["description"].str.extract(r"_(Act(?:\+IL-4)?)_", expand=False)
    md_s["time"] = md_s["description"].str.extract(r"_(\d+h)_", expand=False)
    md_s["rep"] = md_s["description"].str.extract(r"_rep(\d+)", expand=False)
    md_s2 = md_s[md_s["condition"].isin(["Act", "Act+IL-4"]) & md_s["time"].isin(["12h", "24h", "48h", "72h"])].copy()
    md_s2["il4"] = (md_s2["condition"] == "Act+IL-4").astype(int)
    md_s2["stat6sirna"] = (md_s2["sirna"] == "STAT6").astype(int)
    md_s2["il4_x_stat6sirna"] = md_s2["il4"] * md_s2["stat6sirna"]
    res_s_inter = lm_contrast(expr_s, md_s2, ["il4", "stat6sirna", "il4_x_stat6sirna", "time", "rep"], "il4_x_stat6sirna")
    stat6_tests = {}
    for sirna, label in [("Control", "Control_Act+IL-4 vs Control_Act"), ("STAT6", "STAT6_Act+IL-4 vs STAT6_Act")]:
        sub = md_s2[md_s2["sirna"] == sirna].copy()
        sub["il4"] = (sub["condition"] == "Act+IL-4").astype(int)
        res = lm_contrast(expr_s, sub, ["il4", "time", "rep"], "il4")
        stat6_tests[label] = {k: float(v) for k, v in res.loc[GPL6102_NAB2_PROBES[0]].to_dict().items()} | {"direction": gate_direction(float(res.loc[GPL6102_NAB2_PROBES[0], "log2fc"]), float(res.loc[GPL6102_NAB2_PROBES[0], "fdr"]))}
    results["stat6_direct_test"] = {
        "dataset": "GSE17851",
        "contrast": "NAB2 IL-4 induction under control siRNA and STAT6 siRNA; interaction tests loss under STAT6 siRNA",
        "preflight": {"n_samples": int(len(md_s2)), "NAB2_resolved": GPL6102_NAB2_PROBES, "platform_mapping": {p: gpl6102.loc[p, ["Gene symbol", "Gene ID"]].to_dict() for p in GPL6102_NAB2_PROBES}},
        "NAB2_by_siRNA": stat6_tests,
        "STAT6_dependency_interaction": {k: float(v) for k, v in res_s_inter.loc[GPL6102_NAB2_PROBES[0]].to_dict().items()},
    }

    voting = {k: v["arm_call"] for k, v in results["arms"].items()}
    usable = [v for v in voting.values() if v in {"UP", "DOWN"}]
    up = usable.count("UP")
    down = usable.count("DOWN")
    if up >= 2 and up > down:
        call = "DOWN-hyp"
        rationale = "NAB2 tracks type-2/high-disease arms upward; association-backed hypothesis is to down-modulate NAB2."
    elif down >= 2 and down > up:
        call = "UP-hyp"
        rationale = "NAB2 tracks type-2/high-disease arms downward; association-backed hypothesis is to up-modulate NAB2."
    elif len(usable) < 2:
        call = "NO-CALL"
        rationale = "fewer than two voting arms passed post-gate/post-conflict direction"
    else:
        call = "AMBIGUOUS"
        rationale = "usable voting arms are not concordant"
    if call in {"DOWN-hyp", "UP-hyp"} and voting.get("B") not in {"UP", "DOWN"}:
        call = call + " association-backed, not perturbation-backed"
    elif call == "DOWN-hyp" and voting.get("B") == "UP":
        call = "DOWN-hyp perturbation-consistent"
    elif call == "UP-hyp" and voting.get("B") == "DOWN":
        call = "UP-hyp perturbation-consistent"
    skin_dirs = [voting.get(x) for x in ["A", "B", "C"] if voting.get(x) in {"UP", "DOWN"}]
    t_agree = None
    if voting.get("T") in {"UP", "DOWN"} and skin_dirs:
        t_agree = all(voting["T"] == d for d in skin_dirs)
    results["decision"] = {
        "voting_arm_calls": voting,
        "triangulated_call": call,
        "rationale": rationale,
        "arm_T_vs_skin_agreement": t_agree,
        "ceiling": "Expression tracks direction of association, not whether NAB2 is an effector or feedback brake.",
    }
    return results


def write_report(results: dict) -> None:
    lines = []
    lines.append("# NAB2 Direction GEO Mining (2026-07-09)\n")
    lines.append("Scope executed: primary bulk/array voting arms A/T/B/C plus the STAT6 direct test. scRNA ARM-D and all backup datasets were deferred.\n")
    lines.append("Ceiling: these data establish direction of association and perturbation consistency where available; tracks does not mean effector.\n")
    lines.append("## Per-arm results\n")
    lines.append("| Arm | Dataset | Contrast | NAB2 result | Interpreted direction | Detection-filtered type-2 rho | STAT6 | Arm call |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for arm, r in results["arms"].items():
        if "primary_probes" in r:
            nab2 = "; ".join([f"{x['probe']} log2FC={x['log2fc']:.3f}, FDR={x['fdr']:.3g}" for x in r["primary_probes"]])
            rho = "; ".join([f"{x['probe']} rho={x['type2_rho']['rho']:.3f}" if x["type2_rho"]["rho"] is not None else f"{x['probe']} rho=NA" for x in r["primary_probes"]])
        else:
            p = r["primary"]
            nab2 = f"{p.get('gene','NAB2')} log2FC={p['log2fc']:.3f}, FDR={p['fdr']:.3g}"
            tr = r.get("type2_rho") or p.get("type2_rho", {})
            rho = "NA" if tr.get("rho") is None else f"rho={tr['rho']:.3f}, p={tr['p']:.3g}, n={tr['n']}"
        stat6 = r.get("STAT6", {})
        if not stat6 and "primary" in r and "STAT6" in r["primary"]:
            stat6 = r["primary"]["STAT6"]
        stat6_txt = "NA"
        if stat6:
            if "log2fc" in stat6:
                stat6_txt = f"log2FC={stat6['log2fc']:.3f}, FDR={stat6['fdr']:.3g}"
            elif "selected_probe" in stat6:
                stat6_txt = f"{stat6.get('selected_probe')} log2FC={stat6.get('log2fc', float('nan')):.3f}, FDR={stat6.get('fdr', float('nan')):.3g}"
        if r["arm_call"] == "UP":
            interp = "NAB2 higher in the high/type-2 or post-treatment contrast"
        elif r["arm_call"] == "DOWN":
            interp = "NAB2 lower in the high/type-2 or post-treatment contrast"
        elif r["arm_call"] == "AMBIGUOUS":
            interp = "weak or sign-discordant"
        else:
            interp = "did not pass gate"
        lines.append(f"| {arm} | {r['dataset']} | {r['contrast']} | {nab2} | {interp} | {rho} | {stat6_txt} | {r['arm_call']} |")
    lines.append("\nType-2 rho shown in the table is the detection-filtered pre-specified score. `per_arm.json` also records full-score and chemokine/receptor-only sensitivity rhos plus the genes retained/dropped for each arm.\n")
    lines.append("\n## STAT6 direct test\n")
    s = results["stat6_direct_test"]
    for label, row in s["NAB2_by_siRNA"].items():
        lines.append(f"- {label}: NAB2 log2FC={row['log2fc']:.3f}, FDR={row['fdr']:.3g}, direction={row['direction']}")
    inter = s["STAT6_dependency_interaction"]
    lines.append(f"- STAT6-siRNA interaction: log2FC={inter['log2fc']:.3f}, FDR={inter['fdr']:.3g}; negative values mean IL-4 induction is reduced under STAT6 siRNA.\n")
    lines.append("## Triangulated call\n")
    d = results["decision"]
    lines.append(f"Final CALL: **{d['triangulated_call']}**.")
    lines.append(f"Voting arms: {d['voting_arm_calls']}.")
    if d["arm_T_vs_skin_agreement"] is None:
        agree_text = "not assessable because ARM T did not yield a usable post-gate direction"
    else:
        agree_text = str(d["arm_T_vs_skin_agreement"])
    lines.append(f"ARM T vs skin agreement: {agree_text}.")
    lines.append(f"Calibration: {d['ceiling']}\n")
    lines.append("## Caveats\n")
    lines.append("- ARM B is ex vivo NativeSkin cytokine perturbation, not isolated CD4 T cells.")
    lines.append("- ARM A is bulk skin RNA-seq; without ARM-D in this run, cell-compartment attribution remains deferred.")
    lines.append("- Array arms report both plan-specified NAB2 probes; sign discordance would make an arm AMBIGUOUS.")
    lines.append("- RNA-seq contrasts used log2 CPM normalization and fixed-effect linear models; this is limma-voom-style in spirit but not empirical-Bayes moderated limma.")
    lines.append("- STAT6 adjustment/sensitivity is reported as context because STAT6 can be a mediator of IL-4/IL-13 signaling.\n")
    lines.append("## Deferred\n")
    for x in results["deferred"]:
        lines.append(f"- {x}")
    (OUT / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    res = main()
    (OUT / "per_arm.json").write_text(json.dumps(res, indent=2, sort_keys=True), encoding="utf-8")
    write_report(res)
    print("NAB2 GEO direction mining summary")
    print("Scope: primary arms A/T/B/C plus STAT6 direct test; scRNA ARM-D and backups deferred.")
    for arm, r in res["arms"].items():
        if "primary_probes" in r:
            vals = "; ".join(f"{x['probe']} {x['log2fc']:+.3f} FDR={x['fdr']:.3g}" for x in r["primary_probes"])
        else:
            vals = f"{r['primary'].get('gene','NAB2')} {r['primary']['log2fc']:+.3f} FDR={r['primary']['fdr']:.3g}"
        print(f"ARM {arm} {r['dataset']}: {r['arm_call']} ({vals})")
    s = res["stat6_direct_test"]["NAB2_by_siRNA"]
    for label, row in s.items():
        print(f"STAT6 direct {label}: NAB2 {row['log2fc']:+.3f} FDR={row['fdr']:.3g} {row['direction']}")
    inter = res["stat6_direct_test"]["STAT6_dependency_interaction"]
    print(f"STAT6 direct interaction: {inter['log2fc']:+.3f} FDR={inter['fdr']:.3g}")
    print(f"FINAL CALL: {res['decision']['triangulated_call']}")
    print(f"ARM T vs skin agreement: {res['decision']['arm_T_vs_skin_agreement']}")
