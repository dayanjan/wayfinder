#!/usr/bin/env python3
"""
Deterministic DATA REFEREE for a genome-scale CD4+ T-cell CRISPRi Perturb-seq
dataset (clean-room reproduction).

A 4-hop chain producing ONE calibrated verdict per (gene, culture_condition).
Status vocabulary is EXACTLY: supported / refuted / untested / flagged.
Never "proven" / "discovered". alpha = 0.05 throughout. Every hop carries a
RECEIPT of the actual numbers copied from the tables; nothing is hardcoded.
"""
import os
import ast
import json
import math
import pandas as pd

ALPHA = 0.05
DATA_DIR = "/home/dayanjan/pyzobot-data/"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# JSON sanitiser: numpy scalars / NaN -> plain python / None
# ---------------------------------------------------------------------------
def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, bool):
        return bool(o)
    if hasattr(o, "item") and o.__class__.__module__ == "numpy":
        o = o.item()
    if isinstance(o, float):
        return None if math.isnan(o) else float(o)
    if isinstance(o, int):
        return int(o)
    return o


# ---------------------------------------------------------------------------
# Load + prepare the four tables
# ---------------------------------------------------------------------------
def load_tables():
    t1 = pd.read_csv(DATA_DIR + "DE_stats.suppl_table.csv")
    t2 = pd.read_csv(
        DATA_DIR + "Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv"
    )
    t3 = pd.read_csv(DATA_DIR + "cluster_autoimmune_enrichment_results.suppl_table.csv")
    t4 = pd.read_csv(DATA_DIR + "guide_kd_efficiency.suppl_table.csv")

    # T4: drop rows with null perturbed_gene_id, then aggregate to gene x condition
    t4 = t4[t4["perturbed_gene_id"].notna()].copy()
    gate = (
        t4.groupby(["perturbed_gene_id", "culture_condition"])
        .agg(
            n_guides=("signif_knockdown", "size"),
            n_signif=("signif_knockdown", "sum"),
            best_adj_p=("adj_p_value", "min"),
            mean_guide_expr=("guide_mean_expr", "mean"),
            mean_ntc_expr=("ntc_mean_expr", "mean"),
        )
        .reset_index()
    )

    # T3: exclude negative_control_disease, parse + explode intersecting_genes
    t3v = t3[~t3["negative_control_disease"]].copy()
    t3v["gene_list"] = t3v["intersecting_genes"].apply(ast.literal_eval)
    t3exp = t3v.explode("gene_list").rename(columns={"gene_list": "gene"})
    t3exp["gene"] = t3exp["gene"].astype(str)

    # ENSG <-> SYMBOL rosetta from T1
    ros = t1[["target_contrast", "target_contrast_gene_name"]].drop_duplicates()
    sym2ensg = dict(zip(ros["target_contrast_gene_name"], ros["target_contrast"]))

    return t1, t2, t3exp, gate, sym2ensg


# ---------------------------------------------------------------------------
# HOP 0 — KNOCKDOWN-QC GATE (T4). Runs first; can HALT the chain.
# ---------------------------------------------------------------------------
def hop0_gate(gate, ensg, cond):
    row = gate[
        (gate["perturbed_gene_id"] == ensg) & (gate["culture_condition"] == cond)
    ]
    if row.empty:
        return {
            "hop": 0,
            "name": "knockdown-QC gate (T4)",
            "status": "untested",
            "gate_pass": False,
            "claim": "No knockdown-QC gate row exists for this gene+condition; "
            "the perturbation was never assayed here.",
            "receipt": {
                "n_guides": 0,
                "n_signif": 0,
                "best_adj_p": None,
                "mean_guide_expr": None,
                "mean_ntc_expr": None,
            },
            "caveats": [],
        }
    r = row.iloc[0]
    n_guides = int(r["n_guides"])
    n_signif = int(r["n_signif"])
    best_adj_p = float(r["best_adj_p"])
    mge = float(r["mean_guide_expr"])
    mne = float(r["mean_ntc_expr"])
    gate_pass = n_signif > 0

    caveats = []
    if (mge <= mne) and (mne < 0.05):
        caveats.append("target barely expressed — nothing to knock down")

    if gate_pass:
        claim = (
            f"Knockdown QC passed: {n_signif} of {n_guides} guide(s) reached "
            f"signif_knockdown (best adj_p = {best_adj_p:.3g}); "
            f"guide mean expr {mge:.4g} vs NTC {mne:.4g}."
        )
        status = "supported"
    else:
        claim = (
            f"Knockdown QC failed: 0 of {n_guides} guide(s) reached "
            f"signif_knockdown (best adj_p = {best_adj_p:.3g}); "
            f"guide mean expr {mge:.4g} vs NTC {mne:.4g}. "
            "A guide is informative only if it actually silenced the gene, so "
            "any null downstream result here is UNTESTED, never 'no effect'."
        )
        status = "untested"

    return {
        "hop": 0,
        "name": "knockdown-QC gate (T4)",
        "status": status,
        "gate_pass": bool(gate_pass),
        "claim": claim,
        "receipt": {
            "n_guides": n_guides,
            "n_signif": n_signif,
            "best_adj_p": best_adj_p,
            "mean_guide_expr": mge,
            "mean_ntc_expr": mne,
        },
        "caveats": caveats,
    }


# ---------------------------------------------------------------------------
# HOP 1 — EFFECT (T1). Only if gate passed.
# ---------------------------------------------------------------------------
def hop1_effect(t1, ensg, cond):
    row = t1[(t1["target_contrast"] == ensg) & (t1["culture_condition"] == cond)]
    if row.empty:
        return {
            "hop": 1,
            "name": "on-target effect (T1)",
            "status": "untested",
            "claim": "No T1 effect row for this gene+condition.",
            "receipt": {},
            "caveats": [],
        }
    r = row.iloc[0]
    onsig = bool(r["ontarget_significant"])
    eff = float(r["ontarget_effect_size"])
    cat = r["ontarget_effect_category"]
    ndown = int(r["n_downstream"])
    offflag = bool(r["offtarget_flag"])
    caveats = []

    if offflag:
        status = "flagged"
        caveats.append("off-target flag set")
        claim = (
            f"Off-target flag is set for this perturbation "
            f"(ontarget_significant={onsig}, n_downstream={ndown}); "
            "on-target effect cannot be read cleanly."
        )
    elif onsig and ndown > 0:
        status = "supported"
        claim = (
            f"On-target knockdown is significant with {ndown} downstream DE "
            f"gene(s) (effect size {eff:.4g}, category '{cat}')."
        )
    elif onsig and ndown == 0:
        status = "supported"
        claim = (
            f"On-target knockdown is significant with no downstream DE genes "
            f"(effect size {eff:.4g}, category '{cat}'): the KD worked but drove "
            "no detectable downstream program."
        )
    else:
        status = "refuted"
        claim = (
            f"On-target knockdown is not significant in T1 "
            f"(effect size {eff:.4g}, category '{cat}', n_downstream={ndown})."
        )

    return {
        "hop": 1,
        "name": "on-target effect (T1)",
        "status": status,
        "claim": claim,
        "receipt": {
            "ontarget_significant": onsig,
            "ontarget_effect_size": eff,
            "ontarget_effect_category": cat,
            "n_downstream": ndown,
            "offtarget_flag": offflag,
        },
        "caveats": caveats,
    }


# ---------------------------------------------------------------------------
# HOP 2 — PROGRAM (T2). Th1/Th2 shift, faceted by BOTH contrasts.
# ---------------------------------------------------------------------------
def hop2_program(t2, symbol):
    rows = t2[t2["variable"] == symbol]
    contrasts = []
    any_sig = False
    for _, r in rows.iterrows():
        lfc = float(r["log_fc"])
        z = float(r["zscore"])
        p = float(r["adj_p_value"]) if pd.notna(r["adj_p_value"]) else None
        sig = (p is not None) and (p < ALPHA)
        if sig:
            any_sig = True
            direction = "Th2-associated" if lfc < 0 else "Th1-associated"
        else:
            direction = None
        contrasts.append(
            {
                "contrast": r["contrast"],
                "log_fc": lfc,
                "zscore": z,
                "adj_p_value": p,
                "significant": bool(sig),
                "direction": direction,
            }
        )

    if not contrasts:
        return {
            "hop": 2,
            "name": "Th1/Th2 program shift (T2)",
            "status": "untested",
            "claim": f"{symbol} does not appear in the Th1/Th2 polarization "
            "signature table (either contrast).",
            "receipt": {"contrasts": []},
            "caveats": [],
        }

    status = "supported" if any_sig else "refuted"
    sig_bits = [
        f"{c['contrast']}: log_fc={c['log_fc']:.4g}, z={c['zscore']:.4g}, "
        f"adj_p={c['adj_p_value']:.3g}, "
        + (f"significant ({c['direction']})" if c["significant"] else "not significant")
        for c in contrasts
    ]
    if any_sig:
        claim = (
            "Th1/Th2 program shift is significant in at least one reference "
            "contrast — " + "; ".join(sig_bits) + "."
        )
    else:
        claim = (
            "No significant Th1/Th2 program shift in either reference contrast — "
            + "; ".join(sig_bits)
            + "."
        )

    return {
        "hop": 2,
        "name": "Th1/Th2 program shift (T2)",
        "status": status,
        "claim": claim,
        "receipt": {"contrasts": contrasts},
        "caveats": [],
    }


# ---------------------------------------------------------------------------
# HOP 3 — DISEASE (T3). Condition-matched to gene_set "downstream_<cond>".
# ---------------------------------------------------------------------------
def hop3_disease(t3exp, symbol, cond):
    target_set = "downstream_" + cond
    sub = t3exp[(t3exp["gene"] == symbol) & (t3exp["gene_set"] == target_set)]
    in_any_set = (t3exp["gene"] == symbol).any()

    if sub.empty:
        if not in_any_set:
            status = "refuted"
            claim = (
                f"{symbol} is absent from every T3 gene_set (not a member of any "
                "disease-enriched cluster intersection); no disease link to test."
            )
        else:
            status = "untested"
            claim = (
                f"{symbol} does not appear in the condition-matched gene_set "
                f"'{target_set}', though it appears in other gene_sets; disease "
                "link is untested for this condition."
            )
        return {
            "hop": 3,
            "name": "disease enrichment (T3)",
            "status": status,
            "claim": claim,
            "receipt": {
                "gene_set": target_set,
                "n_appearances_in_set": 0,
                "significant_clusters": [],
            },
            "caveats": [],
        }

    sig = sub[sub["p_adj_fdr"] < ALPHA].copy()
    if len(sig) >= 1:
        sig = sig.sort_values("p_adj_fdr")
        sig_records = [
            {
                "disease": rr["disease"],
                "cluster": int(rr["cluster"]),
                "odds_ratio": float(rr["odds_ratio"]),
                "p_adj_fdr": float(rr["p_adj_fdr"]),
            }
            for _, rr in sig.iterrows()
        ]
        diseases = sorted(set(sig["disease"].tolist()))
        top = sig_records[: min(5, len(sig_records))]
        status = "supported"
        claim = (
            f"{symbol} is a member of {len(sig_records)} disease-enriched "
            f"cluster(s) at FDR<{ALPHA} in gene_set '{target_set}', spanning "
            f"disease(s): {', '.join(diseases)}."
        )
        return {
            "hop": 3,
            "name": "disease enrichment (T3)",
            "status": status,
            "claim": claim,
            "receipt": {
                "gene_set": target_set,
                "n_significant_disease_clusters": len(sig_records),
                "diseases_sorted": diseases,
                "top_hits": top,
                "all_significant": sig_records,
            },
            "caveats": [],
        }
    else:
        best = sub.sort_values("p_adj_fdr").iloc[0]
        status = "refuted"
        claim = (
            f"{symbol} appears in {len(sub)} cluster(s) of gene_set "
            f"'{target_set}' but none reach FDR<{ALPHA} "
            f"(best p_adj_fdr={float(best['p_adj_fdr']):.3g}, "
            f"disease '{best['disease']}', odds_ratio={float(best['odds_ratio']):.4g})."
        )
        return {
            "hop": 3,
            "name": "disease enrichment (T3)",
            "status": status,
            "claim": claim,
            "receipt": {
                "gene_set": target_set,
                "n_appearances": int(len(sub)),
                "best_p_adj_fdr": float(best["p_adj_fdr"]),
                "best_odds_ratio": float(best["odds_ratio"]),
                "best_disease": best["disease"],
            },
            "caveats": [],
        }


# ---------------------------------------------------------------------------
# OVERALL — rule-based verdict assembly
# ---------------------------------------------------------------------------
def referee(gene, cond, t1, t2, t3exp, gate, sym2ensg):
    ensg = sym2ensg.get(gene)
    hops = []

    if ensg is None:
        h0 = {
            "hop": 0,
            "name": "knockdown-QC gate (T4)",
            "status": "untested",
            "gate_pass": False,
            "claim": f"{gene} has no ENSG mapping in the T1 rosetta; cannot gate.",
            "receipt": {},
            "caveats": [],
        }
        hops.append(h0)
        overall = (
            "untested — knockdown failed the QC gate; any null downstream result "
            "cannot be read as a negative"
        )
        return {
            "gene": gene,
            "condition": cond,
            "overall": overall,
            "gate_pass": False,
            "hops": hops,
        }

    h0 = hop0_gate(gate, ensg, cond)
    hops.append(h0)

    if not h0["gate_pass"]:
        overall = (
            "untested — knockdown failed the QC gate; any null downstream result "
            "cannot be read as a negative"
        )
        return {
            "gene": gene,
            "condition": cond,
            "overall": overall,
            "gate_pass": False,
            "hops": hops,
        }

    h1 = hop1_effect(t1, ensg, cond)
    hops.append(h1)
    h2 = hop2_program(t2, gene)
    hops.append(h2)
    h3 = hop3_disease(t3exp, gene, cond)
    hops.append(h3)

    if (
        h1["status"] in ("supported", "flagged")
        and h2["status"] == "supported"
        and h3["status"] == "supported"
    ):
        overall = (
            "consistent with a validated gene -> Th1/Th2 program -> disease chain "
            "re-derived from the tables"
        )
        if h1["status"] == "flagged":
            overall += " (with caveats)"
    else:
        first_refuted = next(
            (h for h in [h1, h2, h3] if h["status"] == "refuted"), None
        )
        if first_refuted is not None:
            overall = (
                f"chain breaks at HOP {first_refuted['hop']} "
                f"({first_refuted['name']}): {first_refuted['claim']}"
            )
        else:
            first_untested = next(
                (h for h in [h1, h2, h3] if h["status"] == "untested"), None
            )
            if first_untested is not None:
                overall = (
                    f"chain incomplete at HOP {first_untested['hop']} "
                    f"({first_untested['name']}): {first_untested['claim']}"
                )
            else:
                overall = "chain did not resolve to a supported end-to-end verdict"

    return {
        "gene": gene,
        "condition": cond,
        "overall": overall,
        "gate_pass": True,
        "hops": hops,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    t1, t2, t3exp, gate, sym2ensg = load_tables()
    cases = [("NAB2", "Stim8hr"), ("IL2", "Rest"), ("SLC1A5", "Stim8hr")]
    verdicts = [referee(g, c, t1, t2, t3exp, gate, sym2ensg) for g, c in cases]
    verdicts = clean(verdicts)
    with open(os.path.join(OUT_DIR, "verdicts.json"), "w") as fh:
        json.dump(verdicts, fh, indent=2)
    return verdicts


if __name__ == "__main__":
    v = main()
    print(json.dumps(v, indent=2))
