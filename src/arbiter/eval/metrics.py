"""Metrics + inference for G1 (plan v3, F-005/F-006/F-014). Offline; deterministic.

Frozen primary estimand: TWO CO-PRIMARY paired contrasts on precision@20 over the novel-at-T frame:
  C_broad = prec@20(Wayfinder) - prec@20(B-lit-rarity)         [fixed-substrate-vs-obscurity]
  C_mech  = prec@20(Wayfinder) - prec@20(B-disease-hop-only)   [do QC/effect/program hops add value]
Inference: gene-AND-disease two-way-clustered paired bootstrap 95% CI (resample genes and diseases with
replacement; a pair's multiplicity = count(gene) x count(disease)). A CI spanning 0 is a NULL, reported straight.
Pre-registered joint-outcome table maps (C_broad, C_mech) signs -> {full, narrow_disease_hop_carried, broad_null}.
"""
from __future__ import annotations

import random
from collections import Counter

PRIMARY_K = 20


def precision_at_k(order, positives, k):
    top = order[:k]
    return sum(1 for p in top if p in positives) / k if k else 0.0


def average_precision(order, positives):
    hits = 0
    s = 0.0
    for i, p in enumerate(order, 1):
        if p in positives:
            hits += 1
            s += hits / i
    n = len([p for p in order if p in positives])
    return s / n if n else 0.0


def recall_at_n(order, positives, n):
    top = order[:n]
    npos = len(positives)
    return sum(1 for p in top if p in positives) / npos if npos else 0.0


def _prec_resampled(order, positives, pair_meta, gcount, dcount, k):
    """precision@k on a two-way cluster resample: a pair fills count(gene)*count(disease) slots."""
    filled = hits = 0
    for p in order:
        g, d = pair_meta[p]
        m = gcount.get(g, 0) * dcount.get(d, 0)
        if m == 0:
            continue
        ispos = p in positives
        take = min(m, k - filled)
        filled += take
        if ispos:
            hits += take
        if filled >= k:
            break
    return hits / k if k else 0.0


def clustered_bootstrap_diff(order_a, order_b, positives, pair_meta, frame_genes, frame_diseases,
                             k=PRIMARY_K, n_boot=2000, seed=20260712):
    """Paired prec@k difference (A-B) with a gene-and-disease two-way-clustered bootstrap 95% CI."""
    rng = random.Random(seed)
    ng, nd = len(frame_genes), len(frame_diseases)
    diffs = []
    for _ in range(n_boot):
        gc = Counter(rng.choices(frame_genes, k=ng))
        dc = Counter(rng.choices(frame_diseases, k=nd))
        pa = _prec_resampled(order_a, positives, pair_meta, gc, dc, k)
        pb = _prec_resampled(order_b, positives, pair_meta, gc, dc, k)
        diffs.append(pa - pb)
    diffs.sort()
    lo = diffs[int(0.025 * n_boot)]
    hi = diffs[min(n_boot - 1, int(0.975 * n_boot))]
    point = precision_at_k(order_a, positives, k) - precision_at_k(order_b, positives, k)
    return {"point": round(point, 4), "ci_lo": round(lo, 4), "ci_hi": round(hi, 4),
            "n_boot": n_boot, "significant": bool(lo > 0 or hi < 0), "positive": bool(lo > 0)}


def joint_outcome(c_broad: dict, c_mech: dict) -> str:
    """Pre-registered joint interpretation (no post-hoc spin)."""
    if c_broad["ci_lo"] > 0 and c_mech["ci_lo"] > 0:
        return "full"  # fixed-substrate grounding AND the three referee hops add measured value
    if c_broad["ci_lo"] > 0:
        return "narrow_disease_hop_carried"  # win carried by the disease-enrichment hop
    return "broad_null"  # broad hypothesis fails; report the null straight


def all_metrics(orders: dict, positives, pair_meta, frame_genes, frame_diseases,
                n_boot=2000, seed=20260712) -> dict:
    """Full metric bundle: per-method precision@k / MAP / recall + the two co-primary contrasts."""
    pos = set(positives)
    ks = [5, 10, 20, 50]
    n_frame = len(pair_meta)
    per_method = {}
    for name, order in orders.items():
        per_method[name] = {
            **{f"prec@{k}": round(precision_at_k(order, pos, k), 4) for k in ks},
            "MAP": round(average_precision(order, pos), 4),
            "recall@50": round(recall_at_n(order, pos, 50), 4),
            "recall@100": round(recall_at_n(order, pos, 100), 4),
        }
    c_broad = clustered_bootstrap_diff(orders["wayfinder"], orders["lit_rarity"], pos, pair_meta,
                                       frame_genes, frame_diseases, n_boot=n_boot, seed=seed)
    c_mech = clustered_bootstrap_diff(orders["wayfinder"], orders["disease_hop_only"], pos, pair_meta,
                                      frame_genes, frame_diseases, n_boot=n_boot, seed=seed)
    return {
        "frame_size": n_frame, "positive_count": len(pos),
        "base_rate": round(len(pos) / n_frame, 4) if n_frame else 0.0,
        "primary_k": PRIMARY_K,
        "per_method": per_method,
        "C_broad_wayfinder_vs_lit_rarity": c_broad,
        "C_mech_wayfinder_vs_disease_hop_only": c_mech,
        "joint_outcome": joint_outcome(c_broad, c_mech),
    }
