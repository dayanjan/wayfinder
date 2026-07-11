"""Gate-threshold sensitivity grid for manuscript Section 4.1c (C10; new work 2026-07-11).

Extends sensitivity_panel.py (Controls 1-3) with a threshold-ROBUSTNESS diagnostic: how do
the pipeline's outputs move as the three GATE thresholds vary around the manuscript defaults?

  ab_gate_pct : literature co-mention percentile floor      (default 0.50)
  min_bc      : program-disease co-mention floor            (default 3)
  tau         : Open Targets known-association ceiling       (default 0.10; the novelty gate)

Per grid cell we report: the clean full-chain survivor COUNT, the NAB2 x atopic-eczema RANK,
and the JACCARD overlap of the clean-survivor SET against the default cell.

Framing guardrail (roadmap C10): this is a threshold-robustness DIAGNOSTIC of the machinery's
behaviour, never a validation. Referee VERDICTS are weight- and gate-independent by
construction (a pair's supported/refuted/untested class does not read the gate); the gate only
sets ELIGIBILITY (which pairs are scored) and thus which survivors appear and how NAB2 ranks
among them. This complements Control 3 (rank stability under objective *weights*).

Offline + deterministic:
  * build_a_universe + all z-normalization params are GATE-INDEPENDENT (the universe A and the
    z-scale are computed over the fixed data, not the gate), so a pair's SCORE is identical in
    every cell -- each surviving pair is scored once and re-ranked per cell.
  * ab / bc / known maps are served from data/lbd_cache/ (populated by the main sweep); the
    referee is local. The only literature lookup is ac_lit for clean survivors, cached-first.
  * The harness records cache growth; a pure-replay run adds ZERO cache files.

Run:  PYTHONPATH=src python docs/manuscript/analysis/gate_grid.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "src"))

from arbiter.lbd import sources as S                                   # noqa: E402
from arbiter.lbd.entity_maps import program_terms                     # noqa: E402
from arbiter.lbd.entities import build_a_universe, load_c             # noqa: E402
from arbiter.lbd.referee_triple import load_referee_data, referee_triple  # noqa: E402

CONDITION = "Stim8hr"
BETA, W, W2 = 1.0, 1.0, 3.0                     # manuscript default objective weights
DEFAULT = (0.50, 3, 0.10)                       # (ab_gate_pct, min_bc, tau) -- the paper's setting
GRID_PCT = [0.25, 0.50, 0.75]
GRID_MINBC = [2, 3, 5]
GRID_TAU = [0.05, 0.10, 0.20]
FLAGSHIP = ("NAB2", "atopic eczema")
KEEP = {"supported", "supported_flagged", "supported_weak"}
_CACHE = _REPO / "data" / "lbd_cache"


def _z_params(vals):
    xs = [math.log1p(max(0.0, v)) for v in vals]
    m = sum(xs) / len(xs) if xs else 0.0
    sd = (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5 if len(xs) > 1 else 0.0
    return m, sd


def _zof(v, m, sd):
    lv = math.log1p(max(0.0, v))
    return 0.0 if sd == 0 else (lv - m) / sd


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return round(len(a & b) / len(a | b), 4)


def main(log=print):
    n_cache_start = len(list(_CACHE.glob("*.json")))

    # --- universe + cached signals (gate-independent) ---
    a = build_a_universe(condition=CONDITION, program_significant=True)
    genes = list(dict.fromkeys(a["symbol"].tolist()))
    effect = dict(zip(a["symbol"], a["n_downstream"]))
    diseases = load_c()
    dnames = [d["disease"] for d in diseases]
    log(f"[grid] A universe: {len(genes)} genes x {len(diseases)} diseases "
        f"= {len(genes) * len(diseases)} pairs")

    bc = {d["disease"]: S.cooccur_count(program_terms("BC"), d["disease"]) for d in diseases}
    known = {d["disease"]: S.opentargets_disease_targets(d["id"]) for d in diseases}
    ab = {g: S.cooccur_count(g, program_terms("AB")) for g in genes}
    log("[grid] ab/bc/known cached maps loaded")

    zab = _z_params(list(ab.values()))
    zbc = _z_params(list(bc.values()))
    zef = _z_params([effect.get(g, 0) for g in genes])

    # --- referee verdict for EVERY (gene, disease) pair, ONCE (gate-independent) ---
    data = load_referee_data()
    verdict: dict[tuple[str, str], str] = {}
    for i, g in enumerate(genes, 1):
        for d in dnames:
            verdict[(g, d)] = referee_triple(g, d, CONDITION, data)["answer"]
        if i % 500 == 0:
            log(f"[grid] referee {i}/{len(genes)} genes")
    log(f"[grid] referee verdicts computed for {len(verdict)} pairs")

    # --- ac_known lookup (offline) + the per-pair score is gate-independent ---
    def ac_known_of(g, dn):
        return S.opentargets_known(g, known[dn])

    def ab_gate_value(pct):
        vals = sorted(ab.values())
        return vals[int(round(pct * (len(vals) - 1)))] if vals else 0

    def eligible_pairs(pct, min_bc, tau):
        gate = ab_gate_value(pct)
        return [(g, dn) for g in genes for dn in dnames
                if ab[g] >= gate and bc[dn] >= min_bc and ac_known_of(g, dn) <= tau]

    # --- per cell: eligible -> KEEP survivors -> clean survivors ---
    def cell_survivors(pct, min_bc, tau):
        elig = eligible_pairs(pct, min_bc, tau)
        keep = [(g, dn) for (g, dn) in elig if verdict[(g, dn)] in KEEP]
        clean = [(g, dn) for (g, dn) in elig if verdict[(g, dn)] == "supported"]
        return elig, keep, clean

    _, _, default_clean = cell_survivors(*DEFAULT)
    default_clean_set = set(default_clean)

    # --- ac_lit only for the union of clean survivors (cached-first) ---
    union_clean = set()
    grid_cells = [(p, m, t) for p in GRID_PCT for m in GRID_MINBC for t in GRID_TAU]
    for (p, m, t) in grid_cells:
        union_clean |= set(cell_survivors(p, m, t)[2])
    ac_lit = {(g, dn): S.cooccur_count(g, dn) for (g, dn) in union_clean}
    log(f"[grid] ac_lit for {len(union_clean)} distinct clean survivors (union across cells)")

    def score_of(g, dn):
        return (min(_zof(ab[g], *zab), _zof(bc[dn], *zbc))
                + BETA * _zof(effect.get(g, 0), *zef)
                - W * math.log1p(ac_lit[(g, dn)]) - W2 * ac_known_of(g, dn))

    def flagship_rank(clean):
        ranked = sorted(clean, key=lambda p: score_of(*p), reverse=True)
        return ranked.index(FLAGSHIP) + 1 if FLAGSHIP in ranked else None

    # --- assemble the grid ---
    cells = []
    for (p, m, t) in grid_cells:
        elig, keep, clean = cell_survivors(p, m, t)
        clean_set = set(clean)
        cells.append({
            "ab_gate_pct": p, "min_bc": m, "tau": t,
            "ab_gate_value": ab_gate_value(p),
            "eligible_pairs": len(elig),
            "disease_c_supported_total": len(keep),
            "clean_supported": len(clean),
            "nab2_eczema_rank": flagship_rank(clean),
            "nab2_eczema_survives": FLAGSHIP in clean_set,
            "jaccard_vs_default": _jaccard(clean_set, default_clean_set),
            "is_default": (p, m, t) == DEFAULT,
        })

    n_cache_end = len(list(_CACHE.glob("*.json")))
    ranks = [c["nab2_eczema_rank"] for c in cells if c["nab2_eczema_rank"] is not None]
    out = {
        "condition": CONDITION,
        "default_cell": {"ab_gate_pct": DEFAULT[0], "min_bc": DEFAULT[1], "tau": DEFAULT[2]},
        "grid_size": len(cells),
        "default_clean_supported": len(default_clean),
        "default_nab2_eczema_rank": flagship_rank(default_clean),
        "nab2_eczema_rank_min": min(ranks) if ranks else None,
        "nab2_eczema_rank_max": max(ranks) if ranks else None,
        "nab2_eczema_survives_n": sum(1 for c in cells if c["nab2_eczema_survives"]),
        "clean_supported_min": min(c["clean_supported"] for c in cells),
        "clean_supported_max": max(c["clean_supported"] for c in cells),
        "jaccard_vs_default_min": min(c["jaccard_vs_default"] for c in cells),
        "jaccard_vs_default_median": sorted(c["jaccard_vs_default"] for c in cells)[len(cells) // 2],
        "cache_files_added": n_cache_end - n_cache_start,
        "cells": cells,
    }
    dest = Path(__file__).resolve().parent / "gate_grid_results.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")

    dflt = next(c for c in cells if c["is_default"])
    log("\n=== C10 gate-threshold grid (Stim8hr) ===")
    log(f"  default cell (pct={DEFAULT[0]}, min_bc={DEFAULT[1]}, tau={DEFAULT[2]}): "
        f"clean={dflt['clean_supported']}  NAB2xeczema rank={dflt['nab2_eczema_rank']}  "
        f"(anchor: 30 / rank 4)")
    log(f"  grid {out['grid_size']} cells:")
    log(f"    clean-survivor count : [{out['clean_supported_min']} .. {out['clean_supported_max']}]")
    log(f"    NAB2xeczema rank     : [{out['nab2_eczema_rank_min']} .. {out['nab2_eczema_rank_max']}]"
        f"  (survives in {out['nab2_eczema_survives_n']}/{out['grid_size']} cells)")
    log(f"    Jaccard vs default   : min {out['jaccard_vs_default_min']}, "
        f"median {out['jaccard_vs_default_median']}")
    log(f"  cache files added (0 = pure replay): {out['cache_files_added']}")
    log(f"\nwrote {dest}")
    return out


if __name__ == "__main__":
    main()
