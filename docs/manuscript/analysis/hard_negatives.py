"""Out-of-funnel referee discrimination + frozen-nomination hard negatives.

Manuscript Section 4.2b (roadmap C2 / R2 F-012; new work 2026-07-11). Answers reviewer B1
("the referee's own no is thin") by QUANTIFYING the discrimination the referee supplies at its
OWN hops -- knockdown-QC (hop 0) and effect (hop 1) -- which are its own deterministic
computations, distinct from the disease-hop stringency that Control 2 (§4.1b) showed is
substrate-inherited.

Two panels, both fully OFFLINE and cache-free (referee is local; ac_known reads the cached
per-disease Open Targets maps from the main sweep; NO literature lookups, so a run adds zero
cache files):

  Panel A -- ARBITRARY out-of-funnel base rate. The referee's hop-0/1/2 outcome is
    disease-INDEPENDENT, so ONE census over all perturbed Stim8hr genes (12,539 in T4; 11,415
    with a symbol in T1) characterizes the referee's own-edge cull rate on unselected genes.

  Panel B -- FROZEN-nomination hard negatives (F-012: the sample must NOT be chosen by the
    outcome being evaluated). The frozen rule is a naive curated-association nominator: for each
    disease, the top-K perturbed genes by Open Targets association score (ac_known) -- exactly
    the genes a database-driven nominator would advance, chosen with NO reference to the referee.
    We then apply the referee and report the pre-specified verdict decomposition. The "hard
    negatives" are the association-plausible nominations the referee culls at its OWN hops
    (untested / refuted-effect) -- discrimination a literature/association-only pipeline cannot do.

Framing guardrail: a diagnostic of the referee's own discrimination, NOT a precision/recall or a
"confident-no accuracy" claim. Stratified by assay coverage (in-A vs not) and disease.

Run:  PYTHONPATH=src python docs/manuscript/analysis/hard_negatives.py
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

_REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO / "src"))

from arbiter.lbd import sources as S                                   # noqa: E402
from arbiter.lbd.entities import build_a_universe, load_c             # noqa: E402
from arbiter.lbd.referee_triple import load_referee_data, referee_triple  # noqa: E402

CONDITION = "Stim8hr"
TOP_K = 50                       # frozen nominator: top-K genes by ac_known per disease
ARBITRARY_C = "atopic eczema"    # hops 0-2 are disease-independent; use the flagship disease for panel A
_CACHE = _REPO / "data" / "lbd_cache"

# referee `answer` -> the hop at which the referee's OWN discrimination acts (0-2), vs the
# disease hop (3, substrate-inherited per §4.1b), vs a full-chain pass.
OWN_CULL = {"untested", "refuted_effect", "refuted_program"}      # hops 0-2: the referee's own
DISEASE_CULL = {"refuted_for_c", "untested_for_c"}               # hop 3: substrate-inherited
SUPPORTED = {"supported", "supported_weak", "supported_flagged"}


def _perturbed_genes():
    """All perturbed Stim8hr genes with (ensg, symbol) + QC-pass flag."""
    t1 = pd.read_csv(_REPO / "data" / "DE_stats.suppl_table.csv",
                     usecols=["target_contrast", "target_contrast_gene_name", "culture_condition"])
    t1 = t1[t1["culture_condition"] == CONDITION].dropna(subset=["target_contrast_gene_name"])
    t1 = t1.drop_duplicates("target_contrast")
    ens2sym = dict(zip(t1["target_contrast"], t1["target_contrast_gene_name"]))
    t4 = pd.read_csv(_REPO / "data" / "guide_kd_efficiency.suppl_table.csv",
                     usecols=["perturbed_gene_id", "culture_condition", "signif_knockdown"])
    t4 = t4[t4["culture_condition"] == CONDITION].dropna(subset=["perturbed_gene_id"])
    t4["sig"] = t4["signif_knockdown"].astype(str).str.strip().str.lower().eq("true")
    qc_pass = set(t4.groupby("perturbed_gene_id")["sig"].any().pipe(lambda s: s[s].index))
    return ens2sym, qc_pass


def main(log=print):
    n_cache_start = len(list(_CACHE.glob("*.json")))
    data = load_referee_data()
    diseases = load_c()
    known = {d["disease"]: S.opentargets_disease_targets(d["id"]) for d in diseases}
    ens2sym, qc_pass = _perturbed_genes()
    a_symbols = set(build_a_universe(condition=CONDITION, program_significant=True)["symbol"])
    genes = sorted(ens2sym)                      # ENSG ids (referee resolves symbol internally)
    log(f"[hardneg] perturbed Stim8hr genes: {len(genes)}  (QC-pass {len(qc_pass)}, "
        f"A-universe symbols {len(a_symbols)})")

    # ---- Panel A: arbitrary out-of-funnel base rate (hops 0-2 disease-independent) ----
    catA = Counter()
    for i, ensg in enumerate(genes, 1):
        ans = referee_triple(ensg, ARBITRARY_C, CONDITION, data)["answer"]
        if ans in OWN_CULL:
            catA[ans] += 1
        elif ans in DISEASE_CULL:
            catA["reached_disease_hop"] += 1        # passed the referee's own hops 0-2
        elif ans in SUPPORTED:
            catA["reached_disease_hop"] += 1
        else:
            catA[ans] += 1
        if i % 3000 == 0:
            log(f"[hardneg] panel A {i}/{len(genes)}")
    nA = sum(catA.values())
    own_cull_A = catA["untested"] + catA["refuted_effect"] + catA["refuted_program"]
    panelA = {"n_genes": nA, "by_outcome": dict(catA),
              "own_edge_cull": own_cull_A,
              "own_edge_cull_rate": round(own_cull_A / nA, 4) if nA else None,
              "untested_qc_rate": round(catA["untested"] / nA, 4) if nA else None,
              "refuted_effect_rate": round(catA["refuted_effect"] / nA, 4) if nA else None}

    # ---- Panel B: frozen curated-association nominator -> referee decomposition ----
    # For each disease, the top-K perturbed genes by ac_known (chosen with NO referee input).
    sym2ens = {}
    for ensg, sym in ens2sym.items():
        sym2ens.setdefault(sym, ensg)
    nominations = []                              # (symbol, ensg, disease, ac_known)
    for d in diseases:
        dn = d["disease"]
        scored = [(sym, sym2ens[sym], dn, known[dn].get(sym, 0.0))
                  for sym in {ens2sym[e] for e in genes} if sym in sym2ens]
        scored = [x for x in scored if x[3] > 0.0]          # a curated association exists
        scored.sort(key=lambda x: x[3], reverse=True)
        nominations.extend(scored[:TOP_K])
    log(f"[hardneg] frozen nominator: {len(nominations)} association-plausible (gene,disease) pairs "
        f"(top {TOP_K}/disease)")

    catB = Counter()
    hard_negatives = []                           # association-plausible but referee culls at own hops
    strat_inA = Counter(); strat_notA = Counter()
    for sym, ensg, dn, ak in nominations:
        ans = referee_triple(ensg, dn, CONDITION, data)["answer"]
        bucket = ("untested" if ans == "untested" else
                  "refuted_effect" if ans == "refuted_effect" else
                  "refuted_program" if ans == "refuted_program" else
                  "refuted_for_c" if ans in DISEASE_CULL else
                  "supported" if ans in SUPPORTED else ans)
        catB[bucket] += 1
        (strat_inA if sym in a_symbols else strat_notA)[bucket] += 1
        if ans in OWN_CULL:
            hard_negatives.append({"gene": sym, "disease": dn, "ac_known": round(ak, 3),
                                   "referee": ans, "in_A": sym in a_symbols})
    nB = sum(catB.values())
    own_cull_B = catB["untested"] + catB["refuted_effect"] + catB["refuted_program"]
    panelB = {"n_nominations": nB, "top_k_per_disease": TOP_K,
              "by_verdict": dict(catB),
              "own_edge_cull": own_cull_B,
              "own_edge_cull_rate": round(own_cull_B / nB, 4) if nB else None,
              "supported_rate": round(catB["supported"] / nB, 4) if nB else None,
              "stratum_in_A": dict(strat_inA), "stratum_not_in_A": dict(strat_notA),
              "hard_negative_examples": sorted(hard_negatives,
                                               key=lambda h: h["ac_known"], reverse=True)[:15]}

    out = {"condition": CONDITION,
           "panel_A_arbitrary_out_of_funnel": panelA,
           "panel_B_frozen_association_nomination": panelB,
           "cache_files_added": len(list(_CACHE.glob("*.json"))) - n_cache_start}
    dest = Path(__file__).resolve().parent / "hard_negatives_results.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")

    log("\n=== C2 Panel A: arbitrary out-of-funnel genes (referee's OWN hops 0-2) ===")
    log(f"  {panelA['n_genes']} genes -> own-edge cull {panelA['own_edge_cull']} "
        f"({panelA['own_edge_cull_rate']:.1%});  QC-untested {panelA['untested_qc_rate']:.1%}, "
        f"effect-refuted {panelA['refuted_effect_rate']:.1%}")
    log(f"  outcomes: {panelA['by_outcome']}")
    log("=== C2 Panel B: frozen curated-association nominations -> referee ===")
    log(f"  {panelB['n_nominations']} top-{TOP_K}/disease association-plausible pairs")
    log(f"  verdicts: {panelB['by_verdict']}")
    log(f"  own-edge cull {panelB['own_edge_cull']} ({panelB['own_edge_cull_rate']:.1%}); "
        f"supported {panelB['supported_rate']:.1%}")
    log(f"  hard-negative examples (top ac_known the referee untests/refutes): "
        f"{len(panelB['hard_negative_examples'])} shown")
    for h in panelB["hard_negative_examples"][:6]:
        log(f"    {h['gene']:8} x {h['disease']:22} ac_known={h['ac_known']:.3f} -> {h['referee']}")
    log(f"  cache files added (0 = cache-free): {out['cache_files_added']}")
    log(f"\nwrote {dest}")
    return out


if __name__ == "__main__":
    main()
