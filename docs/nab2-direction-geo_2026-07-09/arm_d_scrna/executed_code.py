"""
ARM D scRNA execution for GSE204762.

Question: does ARM-A bulk NAB2-down in AD lesional skin reflect within-cell-type
NAB2 regulation in Th2-relevant compartments, or a cell-composition shift?

This script is intentionally deterministic: no LLM calls, no biology assertions
without tabulated receipts. It downloads GEO supplementary sample files, processes
one h5ad at a time, and writes report.md plus arm_d.json.
"""

from __future__ import annotations

import gzip
import io
import json
import math
import os
import re
import shutil
import tarfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import typing_extensions

if not hasattr(typing_extensions, "sentinel") and hasattr(typing_extensions, "Sentinel"):
    typing_extensions.sentinel = typing_extensions.Sentinel

import anndata as ad
import numpy as np
import pandas as pd
from scipy import sparse, stats


ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "docs" / "nab2-direction-geo_2026-07-09" / "downloads" / "GSE204762"
RAW_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE204nnn/GSE204762/suppl/GSE204762_RAW.tar"
FILELIST_URL = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE204nnn/GSE204762/suppl/filelist.txt"
GEO_EUTILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

TARGET_GENES = ["NAB2", "STAT6", "IL13", "CCL17", "GATA3"]
TYPE2_GENES_FULL = ["IL13", "IL4", "IL5", "IL31", "CCL17", "CCL22", "CCL26", "TSLP", "IL4R"]
TYPE2_GENES_SENS = ["CCL17", "CCL22", "CCL26", "TSLP", "IL4R", "IL31"]

MARKERS = {
    "keratinocyte": ["KRT14", "KRT5", "KRT1"],
    "fibroblast": ["COL1A1", "LUM", "PDGFRA"],
    "endothelial": ["PECAM1", "VWF"],
    "myeloid": ["LYZ", "CD68", "AIF1"],
    "T/NK": ["CD3D", "CD3E", "TRAC", "NKG7"],
    "melanocyte": ["MLANA"],
}


@dataclass
class SampleInfo:
    gsm: str
    filename: str
    sample_name: str
    patient: str
    condition: str
    replicate: str | None
    size_bytes: int


def log(msg: str) -> None:
    print(time.strftime("[%H:%M:%S]"), msg, flush=True)


def read_ncbi_key() -> str | None:
    key = os.environ.get("NCBI_API_KEY")
    if key:
        return key
    env_path = ROOT / ".env"
    if not env_path.exists():
        return None
    with env_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("NCBI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def fetch_filelist() -> list[SampleInfo]:
    text = urlopen(FILELIST_URL, timeout=60).read().decode("utf-8")
    rows: list[SampleInfo] = []
    for line in text.splitlines():
        if not line.startswith("File\t"):
            continue
        parts = line.split("\t")
        filename = parts[1]
        if "Scleroderma" in filename or "mouse" in filename:
            continue
        m = re.match(r"(GSM\d+)_(.+)\.h5ad\.gz$", filename)
        if not m:
            continue
        gsm, sample_name = m.groups()
        if sample_name.startswith("Healthy"):
            patient = sample_name.split("-")[0]
            condition = "healthy"
            replicate = sample_name.split("-", 1)[1] if "-" in sample_name else None
        else:
            patient, suffix = sample_name.split("-", 1)
            condition = "AD non-lesional" if suffix.startswith("NL") else "AD lesional"
            replicate = suffix
        rows.append(
            SampleInfo(
                gsm=gsm,
                filename=filename,
                sample_name=sample_name,
                patient=patient,
                condition=condition,
                replicate=replicate,
                size_bytes=int(parts[3]),
            )
        )
    return rows


def touch_metadata_api() -> dict[str, Any]:
    """Record that NCBI key handling works, without printing or storing the key."""
    key = read_ncbi_key()
    url = f"{GEO_EUTILS_URL}?db=gds&term=GSE204762[Accession]&retmode=json"
    if key:
        url += "&api_key=" + key
    try:
        raw = urlopen(Request(url, headers={"User-Agent": "PyZoBot-Arbiter/ARM-D"}), timeout=30).read()
        payload = json.loads(raw.decode("utf-8"))
        ids = payload.get("esearchresult", {}).get("idlist", [])
        return {"queried_ncbi_eutils": True, "api_key_source": "env_or_single_env_line" if key else "none", "gds_ids": ids}
    except Exception as exc:
        return {"queried_ncbi_eutils": False, "api_key_source": "env_or_single_env_line" if key else "none", "error": repr(exc)}


def ensure_sample_files(samples: list[SampleInfo]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    missing = [s.filename for s in samples if not (CACHE_DIR / s.filename).exists()]
    if not missing:
        log("All selected .h5ad.gz sample files are already cached.")
        return
    log(f"Streaming GEO RAW tar; extracting {len(missing)} missing human AD/healthy members.")
    missing_set = set(missing)
    with urlopen(RAW_URL, timeout=120) as response:
        with tarfile.open(fileobj=response, mode="r|") as tar:
            for member in tar:
                name = Path(member.name).name
                if name not in missing_set:
                    continue
                out_path = CACHE_DIR / name
                log(f"Extracting {name} ({member.size / 1e6:.1f} MB compressed)")
                extracted = tar.extractfile(member)
                if extracted is None:
                    raise RuntimeError(f"Could not extract {name}")
                tmp_path = out_path.with_suffix(out_path.suffix + ".part")
                with tmp_path.open("wb") as out:
                    shutil.copyfileobj(extracted, out, length=1024 * 1024)
                tmp_path.replace(out_path)
                missing_set.remove(name)
                if not missing_set:
                    break
    if missing_set:
        raise RuntimeError(f"RAW tar ended before extracting: {sorted(missing_set)}")


def gunzip_to_work(gz_path: Path, work_path: Path) -> None:
    if work_path.exists():
        work_path.unlink()
    with gzip.open(gz_path, "rb") as src, work_path.open("wb") as dst:
        shutil.copyfileobj(src, dst, length=1024 * 1024)


def normalize_gene_names(var: pd.DataFrame) -> dict[str, int]:
    candidates = []
    for col in ["gene_symbols", "gene_symbol", "symbol", "features", "gene_ids", "gene_name", "names"]:
        if col in var.columns:
            candidates.append(var[col].astype(str))
    candidates.append(pd.Series(var.index.astype(str), index=var.index))
    mapping: dict[str, int] = {}
    for i, vals in enumerate(zip(*[c.to_numpy() for c in candidates])):
        for val in vals:
            for token in re.split(r"[;,\s|]+", str(val)):
                token = token.strip().upper()
                if token and token not in mapping:
                    mapping[token] = i
    return mapping


def get_existing_celltype_col(obs: pd.DataFrame) -> str | None:
    preferred = [
        "cell_type", "celltype", "cell type", "annotation", "annotations",
        "cell_ontology_class", "cluster_celltype", "celltype_major", "major_cell_type",
        "predicted_cell_type",
    ]
    cols_by_lower = {c.lower(): c for c in obs.columns}
    for key in preferred:
        if key in cols_by_lower:
            col = cols_by_lower[key]
            if obs[col].nunique(dropna=True) > 1:
                return col
    for col in obs.columns:
        low = col.lower()
        if ("cell" in low and "type" in low) or "annot" in low:
            if obs[col].nunique(dropna=True) > 1 and obs[col].nunique(dropna=True) < max(200, len(obs) // 20):
                return col
    return None


def as_1d(x: Any) -> np.ndarray:
    if sparse.issparse(x):
        return np.asarray(x.toarray()).ravel()
    return np.asarray(x).ravel()


def matrix_columns(adata: ad.AnnData, indices: list[int]) -> np.ndarray:
    cols = adata.X[:, indices]
    if sparse.issparse(cols):
        return cols.toarray()
    return np.asarray(cols)


def infer_cell_types(adata: ad.AnnData, gene_to_idx: dict[str, int]) -> tuple[pd.Series, str]:
    obs = adata.obs
    col = get_existing_celltype_col(obs)
    if col:
        return obs[col].astype(str).reset_index(drop=True), f"obs:{col}"

    score_arrays = []
    names = []
    for cell_type, genes in MARKERS.items():
        idx = [gene_to_idx[g] for g in genes if g in gene_to_idx]
        names.append(cell_type)
        if idx:
            score_arrays.append(matrix_columns(adata, idx).mean(axis=1))
        else:
            score_arrays.append(np.zeros(adata.n_obs))
    scores = np.vstack([np.asarray(s).ravel() for s in score_arrays]).T
    best = scores.argmax(axis=1)
    max_score = scores.max(axis=1)
    labels = np.array(names, dtype=object)[best]
    labels[max_score <= 0] = "unassigned"
    return pd.Series(labels), "canonical_marker_argmax"


def canonicalize_cell_type(label: str) -> str:
    s = str(label).strip().lower()
    if any(x in s for x in ["keratin", "krt", "basal", "spinous", "granular"]):
        return "keratinocyte"
    if any(x in s for x in ["fibro", "col1", "stromal"]):
        return "fibroblast"
    if any(x in s for x in ["endo", "vascular", "pecam"]):
        return "endothelial"
    if any(x in s for x in ["myeloid", "macroph", "mono", "dendritic", "dc", "langer", "mast", "neut"]):
        return "myeloid"
    if any(x in s for x in ["t cell", "t-cell", " t", "cd4", "cd8", "nk", "nkt", "lymph"]):
        return "T/NK"
    if any(x in s for x in ["melano", "mlana"]):
        return "melanocyte"
    return str(label).strip() or "unassigned"


def gene_vector(adata: ad.AnnData, gene_to_idx: dict[str, int], gene: str) -> np.ndarray | None:
    idx = gene_to_idx.get(gene.upper())
    if idx is None:
        return None
    return as_1d(adata.X[:, idx])


def mean_for_mask(vec: np.ndarray | None, mask: np.ndarray) -> float | None:
    if vec is None or mask.sum() == 0:
        return None
    return float(np.mean(vec[mask]))


def pct_for_mask(vec: np.ndarray | None, mask: np.ndarray) -> float | None:
    if vec is None or mask.sum() == 0:
        return None
    return float(np.mean(vec[mask] > 0) * 100.0)


def process_sample(sample: SampleInfo) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    gz_path = CACHE_DIR / sample.filename
    work_path = CACHE_DIR / sample.filename.replace(".gz", "")
    log(f"Processing {sample.filename}")
    gunzip_to_work(gz_path, work_path)
    try:
        adata = ad.read_h5ad(work_path, backed="r")
        gene_to_idx = normalize_gene_names(adata.var)
        cell_types_raw, method = infer_cell_types(adata, gene_to_idx)
        cell_types = cell_types_raw.map(canonicalize_cell_type).to_numpy()
        gene_vecs = {g: gene_vector(adata, gene_to_idx, g) for g in sorted(set(TARGET_GENES + TYPE2_GENES_FULL))}
        rows = []
        prop_rows = []
        for cell_type in sorted(pd.Series(cell_types).dropna().unique()):
            mask = cell_types == cell_type
            n_cells = int(mask.sum())
            if n_cells == 0:
                continue
            row = {
                "gsm": sample.gsm,
                "sample_name": sample.sample_name,
                "patient": sample.patient,
                "condition": sample.condition,
                "replicate": sample.replicate,
                "cell_type": cell_type,
                "cell_label_method": method,
                "n_cells": n_cells,
                "total_cells_sample": int(adata.n_obs),
            }
            for gene in TARGET_GENES:
                vec = gene_vecs.get(gene)
                row[f"{gene}_mean"] = mean_for_mask(vec, mask)
                row[f"{gene}_pct_expr"] = pct_for_mask(vec, mask)
            detected_full = []
            for gene in TYPE2_GENES_FULL:
                vec = gene_vecs.get(gene)
                if vec is not None and int(np.sum(vec[mask] > 0)) >= 20:
                    detected_full.append(gene)
            for score_name, genes in [("type2_full", TYPE2_GENES_FULL), ("type2_detected", detected_full), ("type2_sensitivity", TYPE2_GENES_SENS)]:
                vals = [gene_vecs[g] for g in genes if gene_vecs.get(g) is not None]
                row[f"{score_name}_genes"] = ",".join([g for g in genes if gene_vecs.get(g) is not None])
                row[f"{score_name}_mean"] = float(np.mean([np.mean(v[mask]) for v in vals])) if vals else None
            rows.append(row)
            prop_rows.append({
                "gsm": sample.gsm,
                "sample_name": sample.sample_name,
                "patient": sample.patient,
                "condition": sample.condition,
                "replicate": sample.replicate,
                "cell_type": cell_type,
                "n_cells": n_cells,
                "total_cells_sample": int(adata.n_obs),
                "proportion": n_cells / float(adata.n_obs),
                "cell_label_method": method,
            })
        meta = {
            "sample": asdict(sample),
            "n_obs": int(adata.n_obs),
            "n_vars": int(adata.n_vars),
            "var_columns": list(map(str, adata.var.columns)),
            "obs_columns": list(map(str, adata.obs.columns)),
            "cell_label_method": method,
            "target_gene_present": {g: gene_to_idx.get(g) is not None for g in sorted(set(TARGET_GENES + TYPE2_GENES_FULL))},
        }
        adata.file.close()
        return rows, prop_rows, meta
    finally:
        if work_path.exists():
            work_path.unlink()


def log2fc(a: float, b: float, eps: float = 1e-6) -> float:
    return math.log2((a + eps) / (b + eps))


def mannwhitney(x: list[float], y: list[float]) -> float | None:
    x = [v for v in x if pd.notna(v)]
    y = [v for v in y if pd.notna(v)]
    if len(x) < 2 or len(y) < 2:
        return None
    try:
        return float(stats.mannwhitneyu(x, y, alternative="two-sided").pvalue)
    except Exception:
        return None


def paired_test(wide: pd.DataFrame, a: str, b: str) -> dict[str, Any]:
    usable = wide[[a, b]].dropna()
    if len(usable) < 2:
        return {"paired_n": int(len(usable)), "paired_mean_delta": None, "paired_p": None}
    delta = usable[a] - usable[b]
    p = float(stats.wilcoxon(usable[a], usable[b]).pvalue) if len(usable) >= 3 and not np.allclose(delta, 0) else None
    return {"paired_n": int(len(usable)), "paired_mean_delta": float(delta.mean()), "paired_p": p}


def summarize(pseudo: pd.DataFrame, props: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    # Collapse technical/site replicates to patient-condition-cell_type first.
    agg_cols = [c for c in pseudo.columns if c.endswith("_mean") or c.endswith("_pct_expr")]
    per_patient = pseudo.groupby(["patient", "condition", "cell_type"], as_index=False).agg(
        {**{c: "mean" for c in agg_cols}, "n_cells": "sum", "gsm": "nunique"}
    ).rename(columns={"gsm": "n_samples"})
    prop_patient = props.groupby(["patient", "condition", "cell_type"], as_index=False).agg(
        proportion=("proportion", "mean"), n_cells=("n_cells", "sum"), gsm=("gsm", "nunique")
    ).rename(columns={"gsm": "n_samples"})

    comp_rows = []
    for cell_type, sub in per_patient.groupby("cell_type"):
        by_cond = {cond: g for cond, g in sub.groupby("condition")}
        row = {"cell_type": cell_type}
        for cond, g in by_cond.items():
            row[f"{cond}_patients"] = int(g["patient"].nunique())
            row[f"{cond}_samples"] = int(g["n_samples"].sum())
            row[f"{cond}_cells"] = int(g["n_cells"].sum())
            row[f"{cond}_NAB2_mean"] = float(g["NAB2_mean"].mean()) if "NAB2_mean" in g else None
            row[f"{cond}_NAB2_pct_expr"] = float(g["NAB2_pct_expr"].mean()) if "NAB2_pct_expr" in g else None
        if "AD lesional" in by_cond and "AD non-lesional" in by_cond:
            les = by_cond["AD lesional"].set_index("patient")["NAB2_mean"]
            non = by_cond["AD non-lesional"].set_index("patient")["NAB2_mean"]
            wide = pd.concat([les.rename("AD lesional"), non.rename("AD non-lesional")], axis=1)
            row["lesional_vs_nonlesional_log2FC"] = log2fc(row.get("AD lesional_NAB2_mean") or 0, row.get("AD non-lesional_NAB2_mean") or 0)
            row.update({f"lesional_vs_nonlesional_{k}": v for k, v in paired_test(wide, "AD lesional", "AD non-lesional").items()})
        if "AD lesional" in by_cond and "healthy" in by_cond:
            row["lesional_vs_healthy_log2FC"] = log2fc(row.get("AD lesional_NAB2_mean") or 0, row.get("healthy_NAB2_mean") or 0)
            row["lesional_vs_healthy_p"] = mannwhitney(by_cond["AD lesional"]["NAB2_mean"].tolist(), by_cond["healthy"]["NAB2_mean"].tolist())
        comp_rows.append(row)

    prop_rows = []
    for cell_type, sub in prop_patient.groupby("cell_type"):
        by_cond = {cond: g for cond, g in sub.groupby("condition")}
        row = {"cell_type": cell_type}
        for cond, g in by_cond.items():
            row[f"{cond}_mean_proportion"] = float(g["proportion"].mean())
            row[f"{cond}_patients"] = int(g["patient"].nunique())
        if "AD lesional" in by_cond and "AD non-lesional" in by_cond:
            les = by_cond["AD lesional"].set_index("patient")["proportion"]
            non = by_cond["AD non-lesional"].set_index("patient")["proportion"]
            wide = pd.concat([les.rename("AD lesional"), non.rename("AD non-lesional")], axis=1)
            row["lesional_minus_nonlesional_prop"] = row["AD lesional_mean_proportion"] - row["AD non-lesional_mean_proportion"]
            row.update({f"lesional_vs_nonlesional_{k}": v for k, v in paired_test(wide, "AD lesional", "AD non-lesional").items()})
        prop_rows.append(row)

    focus = {}
    for cell_type in ["T/NK", "keratinocyte"]:
        recs = [r for r in comp_rows if r["cell_type"] == cell_type]
        focus[cell_type] = recs[0] if recs else None
    return pd.DataFrame(comp_rows), pd.DataFrame(prop_rows), focus


def direction_word(value: Any) -> str:
    if value is None or pd.isna(value):
        return "not estimated"
    if value < -0.05:
        return "down"
    if value > 0.05:
        return "up"
    return "flat"


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [json_safe(v) for v in value]
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if pd.isna(value) else float(value)
    if value is pd.NA:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def make_verdict(cell_summary: pd.DataFrame, prop_summary: pd.DataFrame) -> dict[str, Any]:
    focus = cell_summary[cell_summary["cell_type"].isin(["T/NK", "keratinocyte"])].copy()
    focus_dirs = {
        r["cell_type"]: direction_word(r.get("lesional_vs_nonlesional_log2FC"))
        for _, r in focus.iterrows()
    }
    props = prop_summary.set_index("cell_type") if not prop_summary.empty else pd.DataFrame()
    immune_up = False
    keratin_down_prop = False
    if "T/NK" in props.index and pd.notna(props.loc["T/NK"].get("lesional_minus_nonlesional_prop")):
        immune_up = props.loc["T/NK", "lesional_minus_nonlesional_prop"] > 0.01
    if "myeloid" in props.index and pd.notna(props.loc["myeloid"].get("lesional_minus_nonlesional_prop")):
        immune_up = immune_up or props.loc["myeloid", "lesional_minus_nonlesional_prop"] > 0.01
    if "keratinocyte" in props.index and pd.notna(props.loc["keratinocyte"].get("lesional_minus_nonlesional_prop")):
        keratin_down_prop = props.loc["keratinocyte", "lesional_minus_nonlesional_prop"] < -0.01

    confirmed = any(v == "down" for v in focus_dirs.values())
    flat_or_up_focus = all(v in {"flat", "up", "not estimated"} for v in focus_dirs.values()) and bool(focus_dirs)
    if confirmed:
        call = "CONFIRMED_PER_CELL_PARTIAL"
        text = "Bulk NAB2-down is consistent with at least one Th2-relevant compartment showing within-cell-type NAB2 down."
    elif flat_or_up_focus and (immune_up or keratin_down_prop):
        call = "EXPLAINED_BY_COMPOSITION"
        text = "Bulk NAB2-down is more consistent with cell-composition shift than within-cell-type NAB2 down in the focus compartments."
    else:
        call = "INCONCLUSIVE"
        text = "The processed scRNA evidence does not cleanly separate within-cell-type regulation from composition."
    return {
        "call": call,
        "text": text,
        "focus_directions": focus_dirs,
        "composition_flags": {"immune_proportion_up": immune_up, "keratinocyte_proportion_down": keratin_down_prop},
    }


def write_outputs(samples: list[SampleInfo], metadata_api: dict[str, Any], sample_meta: list[dict[str, Any]], pseudo: pd.DataFrame, props: pd.DataFrame, cell_summary: pd.DataFrame, prop_summary: pd.DataFrame, verdict: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pseudo.to_csv(OUT_DIR / "pseudobulk_by_sample_celltype.csv", index=False)
    props.to_csv(OUT_DIR / "celltype_proportions_by_sample.csv", index=False)
    cell_summary.to_csv(OUT_DIR / "nab2_by_celltype_condition.csv", index=False)
    prop_summary.to_csv(OUT_DIR / "proportion_shifts.csv", index=False)

    result = {
        "arm": "D",
        "dataset": "GSE204762",
        "question": "Within-cell-type NAB2 direction vs composition artifact for ARM-A bulk NAB2-down.",
        "samples": [asdict(s) for s in samples],
        "metadata_api": metadata_api,
        "processing": {
            "per_sample": True,
            "raw_url": RAW_URL,
            "filelist_url": FILELIST_URL,
            "excluded": ["scleroderma samples", "mouse samples"],
            "cell_label_policy": "Use existing obs cell-type/annotation column if present; otherwise canonical marker argmax.",
            "target_genes": TARGET_GENES,
            "type2_genes_full": TYPE2_GENES_FULL,
            "type2_genes_sensitivity": TYPE2_GENES_SENS,
        },
        "sample_metadata": sample_meta,
        "nab2_celltype_condition": cell_summary.replace({np.nan: None}).to_dict(orient="records"),
        "proportion_shifts": prop_summary.replace({np.nan: None}).to_dict(orient="records"),
        "verdict": verdict,
    }
    (OUT_DIR / "arm_d.json").write_text(json.dumps(json_safe(result), indent=2), encoding="utf-8")

    focus_cols = [
        "cell_type", "AD lesional_patients", "AD non-lesional_patients", "healthy_patients",
        "AD lesional_cells", "AD non-lesional_cells", "healthy_cells",
        "AD lesional_NAB2_mean", "AD non-lesional_NAB2_mean", "healthy_NAB2_mean",
        "lesional_vs_nonlesional_log2FC", "lesional_vs_nonlesional_paired_n",
        "lesional_vs_nonlesional_paired_p", "lesional_vs_healthy_log2FC", "lesional_vs_healthy_p",
    ]
    prop_cols = [
        "cell_type", "AD lesional_mean_proportion", "AD non-lesional_mean_proportion", "healthy_mean_proportion",
        "lesional_minus_nonlesional_prop", "lesional_vs_nonlesional_paired_n", "lesional_vs_nonlesional_paired_p",
    ]
    focus_table = cell_summary[[c for c in focus_cols if c in cell_summary.columns]].sort_values("cell_type")
    prop_table = prop_summary[[c for c in prop_cols if c in prop_summary.columns]].sort_values("cell_type")

    report = []
    report.append("# ARM D scRNA: GSE204762 NAB2 Direction and Cell Composition\n")
    report.append("## Scope\n")
    report.append("Tested whether ARM-A bulk NAB2-down in lesional AD skin is present within Th2-relevant cell types, especially T/NK and keratinocytes, or better explained by cell-composition shifts. Language is association-calibrated; scRNA pseudobulk does not prove therapeutic direction.\n")
    report.append("## Data and Processing\n")
    report.append(f"- Dataset: GSE204762 human skin scRNA, GEO supplementary RAW tar.\n")
    report.append(f"- Included samples: {len(samples)} human AD lesional/non-lesional/healthy `.h5ad.gz` files. Excluded mouse and scleroderma files.\n")
    report.append("- Processing: one sample at a time; decompressed working `.h5ad` deleted after each sample; per-sample/cell-type pseudobulk mean log-normalized expression and percent expressing NAB2.\n")
    methods = sorted(set(m.get("cell_label_method", "") for m in sample_meta))
    report.append(f"- Cell labels: {', '.join(methods)}.\n")
    report.append("- Type-2 score genes followed the plan: full `{IL13,IL4,IL5,IL31,CCL17,CCL22,CCL26,TSLP,IL4R}` plus detection-filtered and chemokine/receptor sensitivity scores in the CSV/JSON receipts.\n")
    report.append("\n## NAB2 Within Cell Type\n")
    report.append(focus_table.to_markdown(index=False, floatfmt=".4g"))
    report.append("\n\n## Cell-Type Proportion Shifts\n")
    report.append(prop_table.to_markdown(index=False, floatfmt=".4g"))
    report.append("\n\n## Verdict\n")
    report.append(f"**{verdict['call']}**: {verdict['text']}\n")
    for cell_type, direction in verdict["focus_directions"].items():
        report.append(f"- {cell_type}: NAB2 lesional vs non-lesional within-cell-type direction = {direction}.\n")
    flags = verdict["composition_flags"]
    report.append(f"- Composition flags: immune proportion up = {flags['immune_proportion_up']}; keratinocyte proportion down = {flags['keratinocyte_proportion_down']}.\n")
    report.append("\n## Caveats\n")
    report.append("- Pseudobulk values are mean values from the supplied h5ad matrix; interpretation assumes the h5ad expression layer is log-normalized as distributed.\n")
    report.append("- Tests are simple paired Wilcoxon by patient where both lesional and non-lesional are present, and Mann-Whitney for lesional vs healthy. They are context receipts, not full mixed models.\n")
    report.append("- Tracks does not imply effector; bulk does not imply per-cell; skin compartments do not by themselves establish topical therapeutic direction.\n")
    (OUT_DIR / "report.md").write_text("".join(report), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    samples = fetch_filelist()
    metadata_api = touch_metadata_api()
    log(f"Selected {len(samples)} human AD/healthy samples from GEO filelist.")
    ensure_sample_files(samples)
    pseudo_rows: list[dict[str, Any]] = []
    prop_rows: list[dict[str, Any]] = []
    sample_meta: list[dict[str, Any]] = []
    for sample in samples:
        rows, props, meta = process_sample(sample)
        pseudo_rows.extend(rows)
        prop_rows.extend(props)
        sample_meta.append(meta)
        pd.DataFrame(pseudo_rows).to_csv(OUT_DIR / "pseudobulk_by_sample_celltype.partial.csv", index=False)
        pd.DataFrame(prop_rows).to_csv(OUT_DIR / "celltype_proportions_by_sample.partial.csv", index=False)
    pseudo = pd.DataFrame(pseudo_rows)
    props = pd.DataFrame(prop_rows)
    cell_summary, prop_summary, _ = summarize(pseudo, props)
    verdict = make_verdict(cell_summary, prop_summary)
    write_outputs(samples, metadata_api, sample_meta, pseudo, props, cell_summary, prop_summary, verdict)
    log("Done.")
    focus = cell_summary[cell_summary["cell_type"].isin(["T/NK", "keratinocyte"])]
    print("\n~15-line summary")
    print("ARM D GSE204762 scRNA completed.")
    print(f"Samples processed: {len(samples)} human AD/healthy h5ad.gz files.")
    print(f"Cell-label methods: {', '.join(sorted(set(m.get('cell_label_method', '') for m in sample_meta)))}")
    for _, row in focus.iterrows():
        print(f"{row['cell_type']}: L vs NL NAB2 log2FC={row.get('lesional_vs_nonlesional_log2FC'):.4g}, paired_n={row.get('lesional_vs_nonlesional_paired_n')}, p={row.get('lesional_vs_nonlesional_paired_p')}")
        print(f"{row['cell_type']}: L vs healthy NAB2 log2FC={row.get('lesional_vs_healthy_log2FC'):.4g}, p={row.get('lesional_vs_healthy_p')}")
    for ct in ["T/NK", "myeloid", "keratinocyte"]:
        sub = prop_summary[prop_summary["cell_type"] == ct]
        if not sub.empty:
            r = sub.iloc[0]
            print(f"{ct} proportion L-NL={r.get('lesional_minus_nonlesional_prop'):.4g}, paired_n={r.get('lesional_vs_nonlesional_paired_n')}, p={r.get('lesional_vs_nonlesional_paired_p')}")
    print(f"Verdict: {verdict['call']} - {verdict['text']}")
    print(f"Report: {OUT_DIR / 'report.md'}")
    print(f"JSON: {OUT_DIR / 'arm_d.json'}")


if __name__ == "__main__":
    main()
