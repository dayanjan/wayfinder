"""
PyzoBot Hypothesis-Referee — BATCH mode
=======================================

Runs `referee(gene, condition)` over a candidate gene set and produces a ranked
verdict table, so the strongest *and least obvious* gene -> program -> disease
chains surface at the top.

Candidate set (condition-matched):
    genes that PASS the HOP-0 knockdown-QC gate AND appear in a T3
    autoimmune-disease-enriched cluster at FDR<0.05 for the SAME condition
    (negative-control disease rows already excluded upstream).

chain_score combines the four hops on comparable log/normalized scales:
    kd_term       weight the whole chain by gate pass (0/1; candidates are all 1)
    effect_term   |HOP-1 ontarget_effect_size|            -> log1p, capped
    program_term  best HOP-2 -log10(adj_p) across BOTH contrasts (Ota, Hollbacker)
    disease_term  best HOP-3 combination of log2(odds_ratio) and -log10(FDR)
    novelty_term  small bonus for LESS obvious chains (fewer disease clusters,
                  program significant in only one contrast) so blockbuster hubs
                  don't crowd out subtle-but-solid candidates

    chain_score = kd_ok * (effect_term + program_term + disease_term) * (1 + novelty_term)

All terms trace to printed receipts; scoring weights are module constants so the
ranking is transparent and reproducible.
"""
from __future__ import annotations
import os, json, math, argparse
import numpy as np
import pandas as pd

import pyzobot_referee as R   # reuse RefereeData + referee()

# ------------------------------------------------------------------ scoring config
EFFECT_CAP   = 12.0    # |effect_size| beyond this saturates (EGR2 ~ -11)
PROGRAM_CAP  = 20.0    # -log10(adj_p) cap to keep p==0 rows finite
DISEASE_OR_CAP = 25.0
NOVELTY_MAX  = 0.30    # max multiplicative novelty bonus


def _safe_neglog10(p):
    if p is None or (isinstance(p, float) and (math.isnan(p) or p <= 0)):
        return PROGRAM_CAP if (p == 0) else 0.0
    return min(-math.log10(p), PROGRAM_CAP)


def _effect_term(effect_size):
    if effect_size is None:
        return 0.0
    return min(math.log1p(abs(effect_size)), math.log1p(EFFECT_CAP))


def _disease_term(odds_ratio, fdr):
    if odds_ratio is None or odds_ratio <= 0:
        return 0.0
    or_part = math.log2(min(odds_ratio, DISEASE_OR_CAP))
    fdr_part = min(_safe_neglog10(fdr), PROGRAM_CAP)
    return or_part + 0.5 * fdr_part


def _extract(hops, name):
    for h in hops:
        if h.name == name:
            return h
    return None


def score_verdict(v) -> dict:
    """Turn a Verdict into a flat scored row with receipts."""
    gate = _extract(v.hops, "GATE")
    eff  = _extract(v.hops, "EFFECT")
    prog = _extract(v.hops, "PROGRAM")
    dis  = _extract(v.hops, "DISEASE")

    kd_ok = int(v.gate_pass)

    # HOP-1 effect size
    effect_size = eff.receipt.get("ontarget_effect_size") if eff else None
    ontarget_sig = eff.receipt.get("ontarget_significant") if eff else None
    n_downstream = eff.receipt.get("n_downstream_DE_genes") if eff else None

    # HOP-2 best program adj_p + which contrast
    program_adj_p = None; program_contrast = None; n_prog_sig = 0
    if prog and prog.receipt:
        for contrast, d in prog.receipt.items():
            if isinstance(d, dict) and "adj_p_value" in d:
                p = d["adj_p_value"]
                if d.get("significant"):
                    n_prog_sig += 1
                if p is not None and (program_adj_p is None or p < program_adj_p):
                    program_adj_p = p; program_contrast = contrast

    # HOP-3 best disease OR/FDR + top disease
    disease_OR = None; disease_FDR = None; top_disease = None; n_dis_clusters = 0
    if dis and dis.receipt and "top_hits" in dis.receipt:
        n_dis_clusters = dis.receipt.get("n_significant_disease_clusters", 0)
        best = None
        for hit in dis.receipt["top_hits"]:
            if best is None or hit["p_adj_fdr"] < best["p_adj_fdr"]:
                best = hit
        if best:
            disease_OR = best["odds_ratio"]; disease_FDR = best["p_adj_fdr"]
            top_disease = best["disease"]

    # terms
    e_term = _effect_term(effect_size)
    p_term = _safe_neglog10(program_adj_p)
    d_term = _disease_term(disease_OR, disease_FDR)

    # novelty: reward fewer disease clusters (less obvious) + single-contrast program
    novelty = 0.0
    if n_dis_clusters:
        novelty += NOVELTY_MAX * (1.0 / n_dis_clusters)          # 1 cluster -> full, many -> ~0
    if n_prog_sig == 1:
        novelty += 0.10
    novelty = min(novelty, NOVELTY_MAX)

    chain_score = kd_ok * (e_term + p_term + d_term) * (1.0 + novelty)

    return {
        "gene": v.gene_symbol, "ensg": v.gene_ensg, "condition": v.condition,
        "top_disease": top_disease, "overall_status": v.overall,
        "kd_ok": kd_ok,
        "ontarget_significant": ontarget_sig, "effect_size": effect_size,
        "n_downstream": n_downstream,
        "program_contrast": program_contrast, "program_adj_p": program_adj_p,
        "n_program_contrasts_sig": n_prog_sig,
        "disease_OR": disease_OR, "disease_FDR": disease_FDR,
        "n_disease_clusters": n_dis_clusters,
        "effect_term": round(e_term, 4), "program_term": round(p_term, 4),
        "disease_term": round(d_term, 4), "novelty_bonus": round(novelty, 4),
        "chain_score": round(chain_score, 4),
        "effect_status": eff.status if eff else None,
        "program_status": prog.status if prog else None,
        "disease_status": dis.status if dis else None,
    }


# ------------------------------------------------------------------ candidate enumeration
def build_candidates(data: R.RefereeData) -> pd.DataFrame:
    """(gene, condition) pairs: gate passes AND >=1 sig disease cluster same condition."""
    sig = data.t3_exploded[data.t3_exploded.p_adj_fdr < R.SIG_ALPHA].copy()
    sig["condition"] = sig.gene_set.str.replace("downstream_", "", regex=False)
    sig = sig[sig.condition.isin(R.CONDITIONS)]
    pairs = sig[["gene", "condition"]].drop_duplicates()

    # keep only gate-passing pairs (join on ENSG + condition)
    pass_gate = data.gate[data.gate.gate_pass]
    pass_set = set(zip(pass_gate.perturbed_gene_id, pass_gate.culture_condition))
    keep = [(r.gene, r.condition) for _, r in pairs.iterrows()
            if (data.sym2ens.get(r.gene), r.condition) in pass_set]
    return pd.DataFrame(keep, columns=["gene", "condition"]).drop_duplicates()


def run_batch(data: R.RefereeData, candidates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in candidates.iterrows():
        v = R.referee(r.gene, r.condition, data)
        rows.append(score_verdict(v))
    df = pd.DataFrame(rows)
    return df.sort_values("chain_score", ascending=False).reset_index(drop=True)


CSV_COLS = ["gene", "condition", "top_disease", "overall_status", "kd_ok",
            "effect_size", "program_adj_p", "disease_OR", "disease_FDR", "chain_score"]


def main(data_dir=R.DEFAULT_DATA_DIR, spec=R.DEFAULT_SPEC,
         out_csv="pyzobot_referee_ranked.csv"):
    data = R.RefereeData(data_dir, spec)
    cands = build_candidates(data)
    ranked = run_batch(data, cands)
    ranked.to_csv(out_csv.replace(".csv", "_full.csv"), index=False)   # all columns
    ranked[CSV_COLS].to_csv(out_csv, index=False)                      # requested schema
    return ranked


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", default=R.DEFAULT_DATA_DIR)
    ap.add_argument("--spec", default=R.DEFAULT_SPEC)
    ap.add_argument("--out", default="pyzobot_referee_ranked.csv")
    a = ap.parse_args()
    ranked = main(a.data_dir, a.spec, a.out)
    print(f"candidates scored: {len(ranked)}")
    print(ranked[CSV_COLS].head(15).to_string(index=False))
