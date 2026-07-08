"""Full LBD proposer sweep + referee cull (the orchestrator; fresh, new-work-only).

Efficient funnel (order matters for API cost):
  1. A universe (answer-free) for the condition; ab per gene (Europe PMC, cached).
  2. bc per disease + Open Targets known-map per disease.
  3. GATE eligible (gene, disease): ab>=ab_gate AND bc>=min_bc AND ac_known<=tau.
  4. referee_triple CULL the eligible pairs FIRST (local, free) -> keep referee-SUPPORTED.
     (The proposer never pre-filters genes by referee-supportability -- that would leak the
      answer, per F-011. The full answer-free A universe is generated; the referee culls after.)
  5. A-C literature (Europe PMC) ONLY for the supported survivors (few calls).
  6. Novelty score + rank -> lbd_questions.json (supported, ranked) + a full audit JSON.

Run:  PYTHONPATH=src python -m arbiter.lbd.propose --condition Stim8hr
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from . import sources as S
from .entity_maps import program_terms
from .entities import build_a_universe, load_c
from .referee_triple import referee_triple, load_referee_data

_REPO = Path(__file__).resolve().parents[3]
OUT_DIR = _REPO / "data" / "lbd_out"


def _z(vals):
    xs = [math.log1p(max(0.0, v)) for v in vals]
    m = sum(xs) / len(xs) if xs else 0.0
    sd = (sum((x - m) ** 2 for x in xs) / len(xs)) ** 0.5 if len(xs) > 1 else 0.0
    return m, sd


def _zof(v, m, sd):
    lv = math.log1p(max(0.0, v))
    return 0.0 if sd == 0 else (lv - m) / sd


def sweep(condition: str = "Stim8hr", min_bc: int = 3, tau: float = 0.1,
          ab_gate_pct: float = 0.50, beta: float = 1.0, w: float = 1.0, w2: float = 3.0,
          program_significant: bool = True, max_genes: int | None = None, log=print) -> dict:
    a = build_a_universe(condition=condition, program_significant=program_significant)
    if max_genes:  # smoke-test guard: limit gene count (still effect-ranked for a meaningful slice)
        a = a.sort_values("n_downstream", ascending=False).head(max_genes)
    genes = list(dict.fromkeys(a["symbol"].tolist()))
    effect = dict(zip(a["symbol"], a["n_downstream"]))
    diseases = load_c()
    log(f"[sweep] condition={condition} genes={len(genes)} diseases={len(diseases)}")

    # 2. bc + known maps
    bc = {d["disease"]: S.cooccur_count(program_terms("BC"), d["disease"]) for d in diseases}
    known = {d["disease"]: S.opentargets_disease_targets(d["id"]) for d in diseases}
    log("[sweep] bc + known maps done")

    # 1. ab per gene (the long part)
    ab = {}
    for i, g in enumerate(genes, 1):
        ab[g] = S.cooccur_count(g, program_terms("AB"))
        if i % 250 == 0:
            log(f"[sweep] ab {i}/{len(genes)}")
    ab_gate = sorted(ab.values())[int(round(ab_gate_pct * (len(ab) - 1)))] if ab else 0
    log(f"[sweep] ab done; ab_gate({ab_gate_pct})={ab_gate}")

    # 3. gate -> eligible pairs
    eligible = [(g, d) for g in genes for d in diseases
                if ab[g] >= ab_gate and bc[d["disease"]] >= min_bc
                and S.opentargets_known(g, known[d["disease"]]) <= tau]
    log(f"[sweep] eligible pairs (pre-referee): {len(eligible)}")

    # 4. referee cull FIRST (local) -> supported only
    data = load_referee_data()
    supported = []
    for g, d in eligible:
        r = referee_triple(g, d["disease"], condition, data)
        if r["answer"] == "supported":
            supported.append((g, d, r))
    log(f"[sweep] referee-supported survivors: {len(supported)}")

    # 5. A-C literature ONLY for supported survivors
    zab_m, zab_sd = _z(list(ab.values()))
    zbc_m, zbc_sd = _z(list(bc.values()))
    zef_m, zef_sd = _z([effect.get(g, 0) for g in genes])
    rows = []
    for g, d, r in supported:
        dn = d["disease"]
        ac_lit = S.cooccur_count(g, dn)
        ac_known = S.opentargets_known(g, known[dn])
        score = (min(_zof(ab[g], zab_m, zab_sd), _zof(bc[dn], zbc_m, zbc_sd))
                 + beta * _zof(effect.get(g, 0), zef_m, zef_sd)
                 - w * math.log1p(ac_lit) - w2 * ac_known)
        rows.append({"a_gene": g, "b_program": "Th1_Th2_polarization", "c_disease": dn,
                     "condition": condition, "ab": ab[g], "bc": bc[dn], "ac_lit": ac_lit,
                     "ac_known": round(ac_known, 4), "effect": int(effect.get(g, 0)),
                     "pure_disjoint": ac_lit == 0, "score": round(score, 3),
                     "referee_overall": r["overall"]})
    rows.sort(key=lambda x: x["score"], reverse=True)
    log(f"[sweep] scored {len(rows)} supported survivors")

    return {
        "condition": condition,
        "params": {"min_bc": min_bc, "tau": tau, "ab_gate_pct": ab_gate_pct,
                   "ab_gate_value": ab_gate, "beta": beta, "w": w, "w2": w2,
                   "program_significant": program_significant},
        "funnel": {"a_genes": len(genes), "eligible_pairs": len(eligible),
                   "referee_supported": len(supported),
                   "pure_disjoint_supported": sum(1 for r in rows if r["pure_disjoint"])},
        "ranked_supported": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", default="Stim8hr")
    ap.add_argument("--ab-gate-pct", type=float, default=0.50)
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    res = sweep(condition=args.condition, ab_gate_pct=args.ab_gate_pct)
    out = OUT_DIR / f"sweep_{args.condition}.json"
    out.write_text(json.dumps(res, indent=2), encoding="utf-8")
    # the ranked questions the referee SUPPORTED (the demo-facing artifact)
    q = OUT_DIR / f"lbd_questions_{args.condition}.json"
    q.write_text(json.dumps(res["ranked_supported"], indent=2), encoding="utf-8")
    f = res["funnel"]
    print(f"FUNNEL {args.condition}: a_genes {f['a_genes']} -> eligible {f['eligible_pairs']}"
          f" -> referee-supported {f['referee_supported']}"
          f" (pure-disjoint {f['pure_disjoint_supported']})")
    print("TOP 10 supported (ranked by novelty):")
    for r in res["ranked_supported"][:10]:
        print(f"  {r['a_gene']:8} x {r['c_disease']:26} s={r['score']:6} "
              f"ab={r['ab']:5} ac_lit={r['ac_lit']:4} ac_known={r['ac_known']:.3f} eff={r['effect']:5}")
    print(f"wrote {out.name} + {q.name}")


if __name__ == "__main__":
    main()
