"""Build the LBD entity sets A / B / C from the local Perturb-seq CSVs.

A = KD-gated significant regulators, derived DETERMINISTICALLY from tables that exist
    (T4 guide_kd gate + T1 DE_stats effect) with NO disease answer in them (F-002/F-011).
B = the single supported program (Th1/Th2 polarization; F-003) -- from entity_maps.
C = the 12 eligible autoimmune diseases read from the enrichment CSV -- from entity_maps.

Answer-free by construction: A never touches T3 (disease) or the referee's ranked output.
Grain of A = gene(SYMBOL, ENSG) x culture_condition, matching the referee's HOP-0/HOP-1.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .entity_maps import DISEASES, ELIGIBLE_DISEASES, PROGRAM

_REPO = Path(__file__).resolve().parents[3]
DATA = _REPO / "data"
_GUIDE_KD = DATA / "guide_kd_efficiency.suppl_table.csv"          # T4
_DE_STATS = DATA / "DE_stats.suppl_table.csv"                     # T1
_T2_PROG = DATA / "Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv"  # T2

CONDITIONS = ["Rest", "Stim8hr", "Stim48hr"]
SIG_ALPHA = 0.05


def _program_significant_genes() -> set[str]:
    """Genes (SYMBOL) with a significant Th1/Th2 program shift in either contrast (T2).

    This is program-level, NOT disease-level -- so intersecting A with it stays
    answer-free while matching the spec's "significant regulators OF the program" intent.
    """
    t2 = pd.read_csv(_T2_PROG, usecols=["variable", "adj_p_value"])
    t2["adj_p_value"] = pd.to_numeric(t2["adj_p_value"], errors="coerce")
    return set(t2.loc[t2["adj_p_value"] < SIG_ALPHA, "variable"].dropna().unique())


def _as_bool(series: pd.Series) -> pd.Series:
    """CSV booleans arrive as bool or as 'True'/'False' strings -- coerce robustly."""
    if series.dtype == bool:
        return series
    return series.astype(str).str.strip().str.lower().eq("true")


def build_a_universe(condition: str | None = None,
                     program_significant: bool = False) -> pd.DataFrame:
    """Return the A universe: gene x condition rows that pass the KD gate AND show effect.

    KD gate  (T4): >=1 guide with signif_knockdown=True for that gene x condition.
    Effect   (T1): ontarget_significant=True OR n_downstream > 0 for that gene x condition.
    program_significant=True additionally intersects with genes that significantly shift
    the Th1/Th2 program (T2 adj_p<0.05) -- the tighter "regulators OF the program" set that
    matches the spec intent (loose ~9.5k genes -> ~4.4k). Still answer-free (program != disease).
    Columns: ensg, symbol, condition. Optionally filter to one condition.
    """
    # T4 gate -> gene(ENSG) x condition that has any significant knockdown
    t4 = pd.read_csv(_GUIDE_KD, usecols=["perturbed_gene_id", "culture_condition",
                                         "signif_knockdown"])
    t4 = t4.dropna(subset=["perturbed_gene_id"])
    t4["signif_knockdown"] = _as_bool(t4["signif_knockdown"])
    gate = (t4.groupby(["perturbed_gene_id", "culture_condition"])["signif_knockdown"]
              .any().reset_index())
    gate = gate[gate["signif_knockdown"]].rename(columns={"perturbed_gene_id": "ensg",
                                                          "culture_condition": "condition"})

    # T1 effect -> gene(ENSG, SYMBOL) x condition with on-target or downstream signal.
    # Keep n_downstream (the dataset effect strength) -- the "not obscure IN THE DATA" prior
    # that lets scoring reward "understudied in literature but strong in the data" (F: novelty
    # != absence of literature). Answer-free: n_downstream is a DE count, not disease info.
    t1 = pd.read_csv(_DE_STATS, usecols=["target_contrast", "target_contrast_gene_name",
                                         "culture_condition", "ontarget_significant",
                                         "n_downstream"])
    t1["ontarget_significant"] = _as_bool(t1["ontarget_significant"])
    t1["n_downstream"] = pd.to_numeric(t1["n_downstream"], errors="coerce").fillna(0)
    effect = t1[t1["ontarget_significant"] | (t1["n_downstream"] > 0)].copy()
    effect = effect.rename(columns={"target_contrast": "ensg",
                                    "target_contrast_gene_name": "symbol",
                                    "culture_condition": "condition"})
    effect = (effect.groupby(["ensg", "symbol", "condition"])["n_downstream"]
                    .max().reset_index())

    a = gate.merge(effect, on=["ensg", "condition"], how="inner")
    a = a[["ensg", "symbol", "condition", "n_downstream"]].drop_duplicates().reset_index(drop=True)
    if program_significant:
        prog = _program_significant_genes()
        a = a[a["symbol"].isin(prog)].reset_index(drop=True)
    if condition is not None:
        a = a[a["condition"] == condition].reset_index(drop=True)
    return a


def load_c(eligible_only: bool = True) -> list[dict]:
    """The C disease list with Open Targets/MONDO ids (eligible specific diseases by default)."""
    names = ELIGIBLE_DISEASES if eligible_only else list(DISEASES)
    return [{"disease": n, "id": DISEASES[n]["id"], "eligible": DISEASES[n]["eligible"]}
            for n in names]


def program_name() -> str:
    return PROGRAM["name"]


if __name__ == "__main__":  # quick smoke report
    a = build_a_universe()
    print(f"A universe: {len(a)} gene x condition rows, "
          f"{a['symbol'].nunique()} unique genes, conditions={sorted(a['condition'].unique())}")
    for cond in CONDITIONS:
        print(f"  {cond}: {len(a[a['condition'] == cond])} genes")
    print(f"C eligible: {len(load_c())} diseases; B program: {program_name()}")
