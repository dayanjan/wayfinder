"""Co-occurrence + novelty scoring for the LBD proposer (fresh, new-work-only).

For each (A gene, B program, C disease) triple:
  ab       = Europe PMC co-mentions, gene x program terms          (A-B bridge; per gene)
  bc       = Europe PMC co-mentions, program terms x disease        (B-C bridge; per disease)
  ac_lit   = Europe PMC co-mentions, gene x disease                 (A-C literature)
  ac_known = Open Targets association score (gene, disease)         (A-C known; disease map)
  effect   = dataset effect strength (n_downstream DE genes)        (per gene; the "not obscure
                                                                      IN THE DATA" prior)

Scoring is a GATED/BALANCED objective, not a linear reward (Codex consult 2026-07-08):
  GATE (eligibility): ab >= ab_gate  AND  bc >= min_bc  AND  ac_known <= tau  AND  ac_lit <= max_ac
  RANK score        : min(z(log1p ab), z(log1p bc))  +  beta*z(log1p effect)
                      -  w*log1p(ac_lit)  -  w2*ac_known
`min(z_ab, z_bc)` stops one axis rescuing a weak other; `ab_gate` (a universe percentile)
excludes genes that are "novel" only because they are understudied; the effect prior rewards
"understudied in literature BUT strong in the data" -- the compelling novelty, not obscurity.
"""
from __future__ import annotations

import math
from statistics import mean, pstdev

from . import sources as S
from .entity_maps import program_terms
from .entities import build_a_universe, load_c


def _zmap(values: dict) -> dict:
    """z-score of log1p(value) across a dict {key: raw}. Returns {key: z}."""
    logs = {k: math.log1p(max(0.0, v)) for k, v in values.items()}
    m, sd = mean(logs.values()), pstdev(logs.values()) if len(logs) > 1 else 0.0
    return {k: (0.0 if sd == 0 else (lv - m) / sd) for k, lv in logs.items()}


def _percentile(sorted_vals, q):
    if not sorted_vals:
        return 0
    i = min(len(sorted_vals) - 1, max(0, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[i]


def preflight_sample(n_genes: int = 20, condition: str = "Stim8hr",
                     min_bc: int = 3, max_ac: int = 0, tau: float = 0.1,
                     ab_gate_pct: float = 0.50, beta: float = 1.0, w: float = 1.0,
                     w2: float = 3.0, program_significant: bool = True,
                     rank_genes_by_effect: bool = True, extra_genes=None) -> dict:
    """Run the pipeline over a bounded gene sample; return histograms + ranked survivors.

    Genes are chosen by dataset effect strength (rank_genes_by_effect) rather than
    alphabetically, so the sample probes the biologically-strong corner, not the obscure one.
    API cost: n_genes A-B + 12 B-C + 12 disease maps + n_genes*12 A-C-lit (all cached).
    """
    a = build_a_universe(condition=condition, program_significant=program_significant)
    if rank_genes_by_effect:
        a = a.sort_values("n_downstream", ascending=False)
    genes = list(dict.fromkeys(a["symbol"].tolist()))[:n_genes]
    effect = dict(zip(a["symbol"], a["n_downstream"]))
    for g in (extra_genes or []):
        if g not in genes:
            genes.append(g)
            effect.setdefault(g, 0)
    diseases = load_c()

    bc = {d["disease"]: S.cooccur_count(program_terms("BC"), d["disease"]) for d in diseases}
    known = {d["disease"]: S.opentargets_disease_targets(d["id"]) for d in diseases}
    ab = {g: S.cooccur_count(g, program_terms("AB")) for g in genes}

    ab_gate = _percentile(sorted(ab.values()), ab_gate_pct)
    z_ab = _zmap(ab)
    z_bc = _zmap(bc)
    z_eff = _zmap({g: effect.get(g, 0) for g in genes})

    triples = []
    for g in genes:
        for d in diseases:
            dn = d["disease"]
            ac_lit = S.cooccur_count(g, dn)
            ac_known = S.opentargets_known(g, known[dn])
            # GATE = real program bridge + disease footprint + NOT a curated known association.
            # ac_lit is NOT in the gate (F-007): raw literature co-mention is noisy, so it only
            # PENALIZES the rank -- otherwise well-studied strong regulators (which usually have
            # some disease literature) are all excluded and nothing survives.
            eligible = (ab[g] >= ab_gate and bc[dn] >= min_bc and ac_known <= tau)
            score = (min(z_ab[g], z_bc[dn]) + beta * z_eff[g]
                     - w * math.log1p(ac_lit) - w2 * ac_known)
            triples.append({"gene": g, "disease": dn, "ab": ab[g], "bc": bc[dn],
                            "ac_lit": ac_lit, "ac_known": round(ac_known, 4),
                            "effect": int(effect.get(g, 0)),
                            "pure_disjoint": bool(ac_lit <= max_ac),
                            "score": round(score, 3), "eligible": bool(eligible)})

    survivors = sorted([t for t in triples if t["eligible"]],
                       key=lambda t: t["score"], reverse=True)
    return {
        "n_genes": len(genes), "condition": condition, "n_triples": len(triples),
        "gene_selection": "effect-ranked" if rank_genes_by_effect else "alphabetical",
        "params": {"min_bc": min_bc, "max_ac": max_ac, "tau": tau,
                   "ab_gate_pct": ab_gate_pct, "ab_gate_value": ab_gate,
                   "beta": beta, "w": w, "w2": w2},
        "ac_lit_zero_frac": round(sum(1 for t in triples if t["ac_lit"] == 0) / len(triples), 3),
        "ac_known_below_tau_frac": round(sum(1 for t in triples if t["ac_known"] <= tau) / len(triples), 3),
        "n_eligible_survivors": len(survivors),
        "n_pure_disjoint_survivors": sum(1 for t in survivors if t["pure_disjoint"]),
        "top_survivors": survivors[:12],
        "genes": genes,
    }
