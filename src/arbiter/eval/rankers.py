"""The 6 frozen total-orders over the novel-at-T frame (plan v3). Offline: no network.

Every ranker returns a list of pair-ids (`"gene||disease"`) best -> worst, covering ALL frame pairs;
ties broken by a fixed rule then stable pair-id. Definitions are FROZEN by plan v3:

  1. wayfinder             - exhaustive 8-class referee verdict, then as-of-T ac_known-ablated score.
  2. disease_hop_only      - mirrors referee_triple._hop3_for_disease (min-FDR collapse); the sharpest baseline.
  3. lit_rarity           - ascending ac_lit_asof (rare = interesting).
  4. effect               - descending downstream-DE count (time-invariant).
  5. enrichment_continuous- raw min-FDR enrichment magnitude, no binary gate.
  6. random               - seeded shuffle.

Inputs come from the enumerate_frame manifest (ac_lit_asof/now, ab_asof, bc_asof, effect) + the local
referee tables (load_referee_data) -- so the whole module is offline-reproducible from committed data.
"""
from __future__ import annotations

import math
import random

from ..lbd.referee_triple import SIG_ALPHA, load_referee_data, referee_triple

# Exhaustive verdict order, best -> worst (referee_triple.py:103-132). untested_for_c is included for
# completeness though the current _hop3_for_disease never emits it.
WAYFINDER_ORDER = ["supported", "supported_flagged", "supported_weak", "refuted_program",
                   "refuted_effect", "refuted_for_c", "untested_for_c", "untested"]
_CLASS_RANK = {c: i for i, c in enumerate(WAYFINDER_ORDER)}
_WORST = len(WAYFINDER_ORDER) + 1


def pid(gene: str, disease: str) -> str:
    return f"{gene}||{disease}"


def _zstats(vals):
    xs = [math.log1p(max(0.0, float(v))) for v in vals]
    m = sum(xs) / len(xs) if xs else 0.0
    sd = (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5 if len(xs) > 1 else 0.0
    return m, sd


def _zof(v, m, sd):
    lv = math.log1p(max(0.0, float(v)))
    return 0.0 if sd == 0 else (lv - m) / sd


def _t3_min_fdr_row(data, gene, condition, disease):
    """The min-FDR T3 row for (gene, downstream_{condition}, disease), mirroring _hop3_for_disease.
    Returns (odds_ratio, p_adj_fdr) or None if the gene is absent from that disease's cluster set."""
    gs = f"downstream_{condition}"
    sub = data.t3_exploded[(data.t3_exploded.gene == gene)
                           & (data.t3_exploded.gene_set == gs)
                           & (data.t3_exploded.disease == disease)]
    if len(sub) == 0:
        return None
    top = sub.sort_values("p_adj_fdr").iloc[0]
    return float(top.odds_ratio), float(top.p_adj_fdr)


def build_orders(manifest: dict, condition: str = "Stim8hr", seed: int = 20260712,
                 beta: float = 1.0, w: float = 1.0, data=None) -> dict:
    """Compute all 6 total-orders. `manifest` is the enumerate_frame output dict."""
    rows = [r for r in manifest["rows"] if r["in_frame"]]
    ab_asof = manifest["ab_asof"]
    bc_asof = manifest["bc_asof"]
    effect = manifest["effect"]
    if data is None:
        data = load_referee_data()

    genes = sorted({r["gene"] for r in rows})
    diseases = sorted({r["disease"] for r in rows})
    zab_m, zab_sd = _zstats([ab_asof.get(g) or 0 for g in genes])
    zbc_m, zbc_sd = _zstats([bc_asof.get(d) or 0 for d in diseases])
    zef_m, zef_sd = _zstats([effect.get(g) or 0 for g in genes])

    pids = [pid(r["gene"], r["disease"]) for r in rows]

    # --- 1. Wayfinder: verdict class, then as-of-T ac_known-ablated score ---
    way = []
    for r in rows:
        g, d = r["gene"], r["disease"]
        ans = referee_triple(g, d, condition, data)["answer"]
        crank = _CLASS_RANK.get(ans, _WORST)
        ab, bc = ab_asof.get(g), bc_asof.get(d)
        if ab is None or bc is None:
            score = float("-inf")  # failed fetch -> sink within class
        else:
            score = (min(_zof(ab, zab_m, zab_sd), _zof(bc, zbc_m, zbc_sd))
                     + beta * _zof(effect.get(g, 0), zef_m, zef_sd)
                     - w * math.log1p(max(0, r["ac_lit_asof"] or 0)))
        way.append((crank, -score, pid(g, d)))
    way.sort()
    wayfinder = [p for _, _, p in way]

    # --- 2. B-disease-hop-only: min-FDR collapse mirroring _hop3_for_disease ---
    dh = []
    for r in rows:
        g, d = r["gene"], r["disease"]
        mf = _t3_min_fdr_row(data, g, condition, d)
        if mf is None:
            dh.append((1, 0.0, 1.0, pid(g, d)))            # no row -> last, fdr=1
        else:
            orr, fdr = mf
            supported = 0 if fdr < SIG_ALPHA else 1         # 0 sorts first (supported-first)
            dh.append((supported, -orr, fdr, pid(g, d)))
    dh.sort()
    disease_hop_only = [p for *_, p in dh]

    # --- 3. B-lit-rarity: ascending ac_lit_asof ---
    lr = sorted(rows, key=lambda r: (r["ac_lit_asof"] if r["ac_lit_asof"] is not None else 10**9,
                                     pid(r["gene"], r["disease"])))
    lit_rarity = [pid(r["gene"], r["disease"]) for r in lr]

    # --- 4. B-effect: descending downstream count ---
    ef = sorted(rows, key=lambda r: (-(effect.get(r["gene"], 0)), pid(r["gene"], r["disease"])))
    effect_order = [pid(r["gene"], r["disease"]) for r in ef]

    # --- 5. B-enrichment-continuous: raw min-FDR magnitude, no gate ---
    ec = []
    for r in rows:
        g, d = r["gene"], r["disease"]
        mf = _t3_min_fdr_row(data, g, condition, d)
        mag = -math.log10(mf[1]) if (mf and mf[1] > 0) else float("-inf")
        ec.append((-mag, pid(g, d)))
    ec.sort()
    enrichment_continuous = [p for _, p in ec]

    # --- 6. B-random: seeded shuffle ---
    rnd = list(pids)
    random.Random(seed).shuffle(rnd)

    return {"wayfinder": wayfinder, "disease_hop_only": disease_hop_only,
            "lit_rarity": lit_rarity, "effect": effect_order,
            "enrichment_continuous": enrichment_continuous, "random": rnd}
