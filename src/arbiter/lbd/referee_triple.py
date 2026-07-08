"""`referee_triple` — the thin exact-disease adapter over the built referee (F-001/F-012).

The base referee (`docs/perturbseq-qc_2026-07-07/pyzobot_referee.py`) answers
"is <gene> in >=1 significant disease cluster?" — its HOP-3 (pyzobot_referee.py:249-282)
NEVER filters to a specific disease, and `overall` is synthesized after that generic hop
(:300). An LBD question targets ONE disease C, so this adapter:

  1. runs the base referee (HOP-0/1/2 reused UNCHANGED, condition-specific),
  2. RECOMPUTES HOP-3 for the exact requested C (supported iff C's own cluster row is
     FDR<0.05; refuted-for-C if the gene is in other diseases but not C at FDR<0.05),
  3. RE-SYNTHESIZES `overall` from the exact-C hop, so it can never say supported while C
     is refuted.

Reuses the referee core; adds no new statistics. Condition-specificity is carried by
HOP-0/1 (gate/effect) and HOP-3 (condition-suffixed gene_set) only — NOT HOP-2 (F-004).
"""
from __future__ import annotations

import importlib.util
import sys
from dataclasses import replace
from pathlib import Path

_REPO = Path(__file__).resolve().parents[3]
_REF_DIR = _REPO / "docs" / "perturbseq-qc_2026-07-07"
_REF_PY = _REF_DIR / "pyzobot_referee.py"
_SPEC = _REF_DIR / "pyzobot_join_spec.json"
_DATA = _REPO / "data"
SIG_ALPHA = 0.05


def _load_referee_module():
    if str(_REF_DIR) not in sys.path:
        sys.path.insert(0, str(_REF_DIR))
    spec = importlib.util.spec_from_file_location("pyzobot_referee", _REF_PY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["pyzobot_referee"] = mod   # register before exec so @dataclass can resolve
    spec.loader.exec_module(mod)
    return mod


_REF = _load_referee_module()
Hop = _REF.Hop


def load_referee_data():
    """RefereeData pointed at THIS repo's local data/ + join spec (not the WSL default)."""
    return _REF.RefereeData(data_dir=str(_DATA), spec_path=str(_SPEC))


def _hop3_for_disease(data, sym: str, condition: str, c_disease: str) -> tuple[Hop, str]:
    """Exact-C HOP-3. Returns (hop, classification) where classification in
    {supported, refuted_for_c, untested_for_c}."""
    gs = f"downstream_{condition}"
    sub_c = data.t3_exploded[(data.t3_exploded.gene == sym)
                             & (data.t3_exploded.gene_set == gs)
                             & (data.t3_exploded.disease == c_disease)]
    if len(sub_c) == 0:
        # gene absent from C's cluster gene-set for this condition
        anysub = data.t3_exploded[(data.t3_exploded.gene == sym)
                                  & (data.t3_exploded.gene_set == gs)]
        other = sorted(anysub.disease.unique().tolist())
        status = "refuted"  # for the specific C the link is not present
        cav = [f"gene is in OTHER diseases for this condition: {other}"] if other else \
              ["gene not in any disease cluster gene-set for this condition"]
        return (Hop(3, "DISEASE", status,
                    f"gene is NOT a member of the '{c_disease}' cluster gene-set "
                    f"(gene_set={gs})",
                    receipt={"c_disease": c_disease, "gene_set_checked": gs,
                             "present_in_other_diseases": other}, caveats=cav),
                "refuted_for_c")
    sig = sub_c[sub_c.p_adj_fdr < SIG_ALPHA]
    if len(sig):
        top = sig.sort_values("p_adj_fdr").iloc[0]
        return (Hop(3, "DISEASE", "supported",
                    f"gene is a member of a '{c_disease}'-enriched cluster (FDR<0.05)",
                    receipt={"c_disease": c_disease,
                             "odds_ratio": _REF._fmt(top.odds_ratio),
                             "p_adj_fdr": _REF._fmt(top.p_adj_fdr),
                             "n_significant_clusters": int(len(sig))}),
                "supported")
    best = sub_c.sort_values("p_adj_fdr").iloc[0]
    return (Hop(3, "DISEASE", "refuted",
                f"gene appears in '{c_disease}' cluster gene-set but NONE reach FDR<0.05 "
                "- the specific disease link is not supported",
                receipt={"c_disease": c_disease, "best_p_adj_fdr": _REF._fmt(best.p_adj_fdr),
                         "best_odds_ratio": _REF._fmt(best.odds_ratio)}),
            "refuted_for_c")


def referee_triple(a_gene: str, c_disease: str, condition: str, data,
                   b_program: str = "Th1_Th2_polarization") -> dict:
    """Answer one LBD triple (A gene, B program, C disease, condition) on the exact C.

    Returns a dict with the base hops (HOP-3 replaced by the exact-C hop), a re-synthesized
    `overall`, and `answer` in {supported, refuted_for_c, untested}. `untested` means the
    knockdown gate failed (the hero QC catch) -> the question is unanswerable here.
    """
    v = _REF.referee(a_gene, condition, data)          # HOP-0/1/2 + generic HOP-3
    base = {"a_gene": a_gene, "b_program": b_program, "c_disease": c_disease,
            "condition": condition, "resolved_symbol": v.gene_symbol, "gate_pass": v.gate_pass}

    if not v.gate_pass:                                 # HOP-0 failed -> untested (hero catch)
        return {**base, "answer": "untested",
                "overall": "untested - knockdown failed QC gate",
                "hops": [h.__dict__ for h in v.hops]}

    # swap generic HOP-3 for exact-C HOP-3, then re-synthesize overall from it
    c_hop, classification = _hop3_for_disease(data, v.gene_symbol, condition, c_disease)
    v.hops = [h for h in v.hops if h.name != "DISEASE"] + [c_hop]
    v.hops.sort(key=lambda h: h.hop)
    overall = _REF._synthesize_overall(v)

    # `answer` is a FULL-CHAIN verdict, not the disease hop alone (Codex consult 2026-07-08):
    # a triple is only "supported" if gate+effect+program+disease-C all hold. A disease-C hop
    # can be supported while EFFECT is refuted/flagged upstream -- those are NOT clean money-shots.
    st = {h.name: h.status for h in v.hops}
    eff, prog = st.get("EFFECT"), st.get("PROGRAM")
    n_down = next((h.receipt.get("n_downstream_DE_genes") for h in v.hops
                   if h.name == "EFFECT"), None)
    if classification != "supported":
        answer = "untested_for_c" if classification == "untested_for_c" else "refuted_for_c"
    elif eff == "refuted":
        answer = "refuted_effect"
    elif prog == "refuted":
        answer = "refuted_program"
    elif not n_down:                       # effect=0 downstream -> empty effect, not a clean chain
        answer = "supported_weak"
    elif eff == "flagged":
        answer = "supported_flagged"       # chain holds but off-target caveat
    else:
        answer = "supported"               # clean full chain -- the money-shot class
    return {**base, "answer": answer, "overall": overall, "effect_status": eff,
            "program_status": prog, "n_downstream": n_down,
            "hops": [h.__dict__ for h in v.hops]}
