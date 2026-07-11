"""Sensitivity panel for manuscript Section 4.1b (new work, 2026-07-10).

Three deterministic controls over the local Perturb-seq tables, cache-free:

  Control 1 -- QC gate does its job: every failed-knockdown gene returns `untested`.
  Control 2 -- disease hop is not rubber-stamping: label-shuffle null for the disease
               hop over the referee's native A x C (=3935 x 12 = 47,220) pair space.
  Control 3 -- rank stability of NAB2 under alternative objective weights (beta, w, w2).

All numbers trace to `data/*.suppl_table.csv` + `data/lbd_out/lbd_questions_Stim8hr.json`.
No network, no literature cache. Run:  PYTHONPATH=src python docs/manuscript/analysis/sensitivity_panel.py

Designed to run identically inside the Claude Science kernel (the manuscript's dogfood gate):
the local ground-truth numbers and the CS reproduction must match.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "src"))

from arbiter.lbd.entities import build_a_universe, load_c            # noqa: E402
from arbiter.lbd.referee_triple import load_referee_data, referee_triple  # noqa: E402

CONDITION = "Stim8hr"
GENE_SET = f"downstream_{CONDITION}"
SIG_ALPHA = 0.05
N_PERM = 2000
SEED = 20260710
FAILED_KD_SAMPLE = None  # None = run ALL failed-KD genes; int = random sample of that size


# ------------------------------------------------------------------ helpers
def _z_params(vals):
    xs = [math.log1p(max(0.0, v)) for v in vals]
    m = sum(xs) / len(xs) if xs else 0.0
    sd = (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5 if len(xs) > 1 else 0.0
    return m, sd


def _zof(v, m, sd):
    lv = math.log1p(max(0.0, v))
    return 0.0 if sd == 0 else (lv - m) / sd


# ------------------------------------------------------------------ control 1
def control1_failed_kd_untested(data) -> dict:
    """Every gene that FAILS the knockdown-QC gate at Stim8hr must return `untested`."""
    t4 = pd.read_csv(_REPO / "data" / "guide_kd_efficiency.suppl_table.csv",
                     usecols=["perturbed_gene_id", "culture_condition", "signif_knockdown"])
    t4 = t4[t4["culture_condition"] == CONDITION].dropna(subset=["perturbed_gene_id"])
    t4["sig"] = t4["signif_knockdown"].astype(str).str.strip().str.lower().eq("true")
    gate = t4.groupby("perturbed_gene_id")["sig"].any()
    failed = sorted(gate[~gate].index.tolist())          # ENSG ids that fail the gate
    tested = failed
    if FAILED_KD_SAMPLE and len(failed) > FAILED_KD_SAMPLE:
        rng = np.random.default_rng(SEED)
        tested = sorted(rng.choice(failed, size=FAILED_KD_SAMPLE, replace=False).tolist())
    n_untested = 0
    leaks = []
    for ensg in tested:
        ans = referee_triple(ensg, "atopic eczema", CONDITION, data)["answer"]
        if ans == "untested":
            n_untested += 1
        else:
            leaks.append((ensg, ans))
    return {"n_failed_kd_genes": len(failed), "n_tested": len(tested),
            "n_untested": n_untested,
            "fraction_untested": round(n_untested / len(tested), 6) if tested else None,
            "leaks": leaks[:20]}


# ------------------------------------------------------------------ control 2
def control2_label_shuffle_null(data, a_symbols: set[str], c_diseases: list[str]) -> dict:
    """Label-shuffle null for the disease hop over A x C (47,220) pairs.

    Observed: # distinct (gene in A, disease in C) pairs with a significant
    (gene, downstream_Stim8hr, disease) enrichment row (FDR<0.05).
    Null: permute the `disease` column across the downstream_Stim8hr rows (FDR travels
    with the row), recompute the count; repeat N_PERM times.
    """
    t3 = data.t3_exploded
    sub = t3[t3["gene_set"] == GENE_SET].copy()
    sub = sub[sub["gene"].isin(a_symbols)]                       # genes in A only
    cset = set(c_diseases)
    n_pairs = len(a_symbols) * len(c_diseases)

    def _count_supported(disease_col: pd.Series) -> tuple[int, float]:
        """Return (n distinct sig (gene,disease in C) pairs, mean distinct C-diseases per passing gene).

        The second value is a descriptive per-passing-gene cardinality summary, NOT a full mechanism
        decomposition of the observed-vs-null gap: it is only one component of that gap and is small in
        practice (~2.39 true vs ~2.44 null), so it is reported but not interpreted as the cause of the
        observed-below-null direction.
        """
        sig = sub["p_adj_fdr"] < SIG_ALPHA
        mask = sig & disease_col.isin(cset)
        genes = sub.loc[mask, "gene"].to_numpy()
        dis = disease_col.loc[mask].to_numpy()
        pairs = set(zip(genes, dis))
        # mean distinct diseases per gene, over genes with >=1 passing pair
        per_gene: dict = {}
        for g, d in pairs:
            per_gene.setdefault(g, set()).add(d)
        card = [len(v) for v in per_gene.values()]
        mean_card = float(np.mean(card)) if card else 0.0
        return len(pairs), mean_card

    observed, observed_card = _count_supported(sub["disease"])
    rng = np.random.default_rng(SEED)
    disease_vals = sub["disease"].to_numpy()
    null_counts = np.empty(N_PERM, dtype=int)
    null_cards = np.empty(N_PERM, dtype=float)
    for i in range(N_PERM):
        perm = rng.permutation(disease_vals)                    # RNG call sequence unchanged (numbers stable)
        c, mc = _count_supported(pd.Series(perm, index=sub.index))
        null_counts[i] = c
        null_cards[i] = mc
    mean = float(null_counts.mean()); sd = float(null_counts.std(ddof=1))
    n_ge = int((null_counts >= observed).sum())
    n_le = int((null_counts <= observed).sum())
    p_upper = (n_ge + 1) / (N_PERM + 1)                          # P(null >= observed)  [rarer-than-chance test]
    p_lower = (n_le + 1) / (N_PERM + 1)                          # P(null <= observed)  [observed is at low tail]
    p_two = min(1.0, 2 * min(p_upper, p_lower))
    return {"pair_space_AxC": n_pairs, "n_A_genes": len(a_symbols), "n_C_diseases": len(c_diseases),
            "observed_disease_hop_supported": observed,
            "observed_rate": round(observed / n_pairs, 6),
            "n_perm": N_PERM,
            "null_mean": round(mean, 3),
            "null_sd": round(sd, 3),
            "null_max": int(null_counts.max()),
            "null_rate_mean": round(mean / n_pairs, 6),
            "signed_z": round((observed - mean) / sd, 3) if sd > 0 else None,
            "empirical_p": round(p_upper, 6),                    # retained: upper-tail (back-compatible)
            "empirical_p_upper": round(p_upper, 6),
            "empirical_p_lower": round(p_lower, 6),
            "empirical_p_two_sided": round(p_two, 6),
            "fold_over_null": round(observed / mean, 2) if mean > 0 else None,
            "mean_distinct_C_diseases_per_gene_observed": round(observed_card, 3),
            "mean_distinct_C_diseases_per_gene_null": round(float(null_cards.mean()), 3)}


# ------------------------------------------------------------------ control 3
def control3_rank_stability() -> dict:
    """NAB2 rank across a (beta, w, w2) weight grid, re-ranking the 30 clean survivors.

    score_i(beta,w,w2) = M_i + beta*zef_i - w*log1p(ac_lit_i) - w2*ac_known_i,
    where M_i = min(z_ab, z_bc) is weight-independent and recovered from the stored
    default-weight score (beta=1,w=1,w2=3): M_i = score_i - zef_i + log1p(ac_lit_i) + 3*ac_known_i.
    zef_i uses z-params over the full A-universe effect column (local, cache-free).
    """
    rows = json.loads((_REPO / "data" / "lbd_out" / "lbd_questions_Stim8hr.json").read_text())
    a = build_a_universe(condition=CONDITION, program_significant=True)
    zef_m, zef_sd = _z_params(a["n_downstream"].tolist())
    for r in rows:
        zef = _zof(r["effect"], zef_m, zef_sd)
        L = math.log1p(r["ac_lit"]); K = r["ac_known"]
        r["_zef"] = zef; r["_L"] = L; r["_K"] = K
        r["_M"] = r["score"] - (1.0 * zef - 1.0 * L - 3.0 * K)   # recover weight-indep part

    def _rank_of(gene, beta, w, w2):
        scored = sorted(rows, key=lambda r: r["_M"] + beta * r["_zef"] - w * r["_L"] - w2 * r["_K"],
                        reverse=True)
        order = [r["a_gene"] for r in scored]
        return order.index(gene) + 1 if gene in order else None

    # sanity: default weights must reproduce the stored ranking (NAB2 = rank 4)
    default_rank = _rank_of("NAB2", 1.0, 1.0, 3.0)

    betas = [0.5, 1.0, 2.0]; ws = [0.5, 1.0, 2.0]; w2s = [1.0, 3.0, 5.0]
    ranks = []
    grid = []
    for b in betas:
        for w in ws:
            for w2 in w2s:
                rk = _rank_of("NAB2", b, w, w2)
                ranks.append(rk)
                grid.append({"beta": b, "w": w, "w2": w2, "nab2_rank": rk})
    ranks = [r for r in ranks if r is not None]
    top5 = sum(1 for r in ranks if r <= 5)
    return {"n_survivors": len(rows), "default_rank_check": default_rank,
            "grid_size": len(grid),
            "grid_beta": betas, "grid_w": ws, "grid_w2": w2s,
            "nab2_rank_min": min(ranks), "nab2_rank_max": max(ranks),
            "nab2_rank_median": int(np.median(ranks)),
            "nab2_top5_fraction": round(top5 / len(ranks), 3),
            "grid": grid}


# ------------------------------------------------------------------ main
def main():
    data = load_referee_data()
    a = build_a_universe(condition=CONDITION, program_significant=True)
    a_symbols = set(a["symbol"].dropna().unique())
    c_diseases = [d["disease"] for d in load_c()]

    out = {
        "condition": CONDITION,
        "control1_failed_kd_untested": control1_failed_kd_untested(data),
        "control2_label_shuffle_null": control2_label_shuffle_null(data, a_symbols, c_diseases),
        "control3_rank_stability": control3_rank_stability(),
    }
    dest = Path(__file__).resolve().parent / "sensitivity_results.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")

    c1 = out["control1_failed_kd_untested"]
    c2 = out["control2_label_shuffle_null"]
    c3 = out["control3_rank_stability"]
    print("=== Control 1 (QC gate) ===")
    print(f"  failed-KD genes: {c1['n_failed_kd_genes']}  tested: {c1['n_tested']}  "
          f"-> untested: {c1['n_untested']}  ({c1['fraction_untested']:.4%})  leaks: {len(c1['leaks'])}")
    print("=== Control 2 (label-shuffle null, disease hop over A x C) ===")
    print(f"  pair space A x C: {c2['pair_space_AxC']}  observed supported: "
          f"{c2['observed_disease_hop_supported']}  ({c2['observed_rate']:.4%})")
    print(f"  null mean+/-sd: {c2['null_mean']} +/- {c2['null_sd']}  (max {c2['null_max']})  "
          f"n_perm {c2['n_perm']}")
    print(f"  signed z: {c2['signed_z']}  p_upper: {c2['empirical_p_upper']}  "
          f"p_lower: {c2['empirical_p_lower']}  p_two: {c2['empirical_p_two_sided']}")
    print(f"  mean distinct C-diseases/gene  observed: {c2['mean_distinct_C_diseases_per_gene_observed']}  "
          f"null: {c2['mean_distinct_C_diseases_per_gene_null']}")
    print("=== Control 3 (rank stability) ===")
    print(f"  default-rank check (must be 4): {c3['default_rank_check']}")
    print(f"  grid {c3['grid_size']} settings -> NAB2 rank "
          f"[{c3['nab2_rank_min']}..{c3['nab2_rank_max']}], median {c3['nab2_rank_median']}, "
          f"top5 {c3['nab2_top5_fraction']:.0%}")
    print(f"\nwrote {dest}")


if __name__ == "__main__":
    main()
