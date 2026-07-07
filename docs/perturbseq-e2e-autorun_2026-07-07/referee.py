"""
referee.py — Calibrated hypothesis referee for CD4+ T-cell immunology
=====================================================================

Traces a single gene through a four-hop evidence chain built from the
Marson/Pritchard genome-scale Perturb-seq supplementary tables:

    HOP 0  knockdown-QC gate   (guide_kd_efficiency)      <-- QUERIED FIRST
    HOP 1  on-target effect    (DE_stats)
    HOP 2  Th1/Th2 program     (Th2_Th1_polarization ...)  [faceted by 2 contrasts]
    HOP 3  autoimmune disease  (cluster_autoimmune_enrichment)

Design principle — UNTESTED is not "no effect"
-----------------------------------------------
HOP 0 is evaluated FIRST. If no guide achieved a significant knockdown for a
gene in the requested condition, the perturbation was never established, so any
downstream "no effect" is uninterpretable. In that case the verdict is
UNTESTED, and HOPs 1-3 are reported as informational context only, never as
evidence of absence.

Calibrated status vocabulary (per hop)
--------------------------------------
    supported  — the table row affirmatively backs the hypothesis
    refuted    — the table row affirmatively contradicts it (only meaningful
                 downstream of a PASSED knockdown gate)
    untested   — the measurement to decide it does not exist / gate not passed
    flagged    — a quality caveat applies (e.g. putative off-target)

Every hop carries the EXACT table receipt (numbers copied verbatim from the
source rows) so a reader can audit the verdict against the supplementary tables.
No claim is asserted that is not present in the tables.

Usage
-----
    from referee import Referee
    ref = Referee.from_dir("~/pyzobot-data")   # or Referee(de, pol, enr, kd)
    verdict = ref.referee("GATA3", "Stim48hr")
    print(verdict.render())                     # human-readable trace
    verdict.to_dict()                           # machine-readable
"""
from __future__ import annotations

import ast
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------
# Constants — the vocabulary is fixed by the source tables (validated in QC)
# --------------------------------------------------------------------------
CONDITIONS = ("Rest", "Stim8hr", "Stim48hr")
CONTRASTS = ("Th2_vs_Th1 (Ota 2021)", "Th2_vs_Th1 (Hollbacker 2021)")
PROGRAM_SIG_ALPHA = 0.05      # adj_p_value threshold for HOP2 program call
DISEASE_FDR_ALPHA = 0.05      # p_adj_fdr threshold for HOP3 disease call

SUPPORTED = "supported"
REFUTED = "refuted"
UNTESTED = "untested"
FLAGGED = "flagged"


def _clean(v: Any) -> Any:
    """Make numpy / NaN values JSON-serializable and None-safe."""
    if isinstance(v, (np.floating, float)) and (v != v):  # NaN
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating,)):
        return float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    return v


@dataclass
class HopResult:
    hop: int
    name: str
    status: str                       # supported / refuted / untested / flagged
    statement: str                    # calibrated, table-grounded sentence
    receipt: dict = field(default_factory=dict)   # EXACT source values
    table: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["receipt"] = {k: _clean(v) for k, v in self.receipt.items()}
        return d


@dataclass
class Verdict:
    gene_query: str
    gene_symbol: str | None
    gene_ensg: str | None
    condition: str
    overall: str                      # YES / UNTESTED / REFUTED / PARTIAL / NO-DATA
    headline: str
    hops: list[HopResult] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "gene_query": self.gene_query,
            "gene_symbol": self.gene_symbol,
            "gene_ensg": self.gene_ensg,
            "condition": self.condition,
            "overall": self.overall,
            "headline": self.headline,
            "hops": [h.to_dict() for h in self.hops],
        }

    def render(self) -> str:
        L = []
        L.append("=" * 78)
        L.append(f"REFEREE  |  gene={self.gene_query}"
                 f"  (symbol={self.gene_symbol}, ENSG={self.gene_ensg})"
                 f"  |  condition={self.condition}")
        L.append(f"OVERALL VERDICT: {self.overall}")
        L.append(f"  {self.headline}")
        L.append("=" * 78)
        for h in self.hops:
            L.append(f"\n[HOP {h.hop}] {h.name}  ->  {h.status.upper()}   (table: {h.table})")
            L.append(f"    {h.statement}")
            if h.receipt:
                L.append("    receipt:")
                for k, v in h.receipt.items():
                    L.append(f"      - {k} = {_clean(v)}")
        L.append("=" * 78)
        return "\n".join(L)


class Referee:
    """Loads the four tables and adjudicates gene x condition hypotheses."""

    FILES = {
        "de": "DE_stats.suppl_table.csv",
        "pol": "Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv",
        "enr": "cluster_autoimmune_enrichment_results.suppl_table.csv",
        "kd": "guide_kd_efficiency.suppl_table.csv",
    }

    def __init__(self, de: pd.DataFrame, pol: pd.DataFrame,
                 enr: pd.DataFrame, kd: pd.DataFrame):
        self.de = de.copy()
        self.pol = pol.copy()
        self.enr = enr.copy()
        self.kd = kd.copy()
        self._build_indices()

    @classmethod
    def from_dir(cls, path: str) -> "Referee":
        path = os.path.expanduser(path)
        return cls(
            de=pd.read_csv(os.path.join(path, cls.FILES["de"])),
            pol=pd.read_csv(os.path.join(path, cls.FILES["pol"])),
            enr=pd.read_csv(os.path.join(path, cls.FILES["enr"])),
            kd=pd.read_csv(os.path.join(path, cls.FILES["kd"])),
        )

    # ------------------------------------------------------------------
    # Index construction: the ENSG<->symbol Rosetta + exploded gene lists
    # ------------------------------------------------------------------
    def _build_indices(self):
        # DE is the ENSG<->symbol Rosetta stone (strictly 1:1, validated in QC)
        ros = self.de[["target_contrast", "target_contrast_gene_name"]].drop_duplicates()
        self.ensg2sym = dict(zip(ros.target_contrast, ros.target_contrast_gene_name))
        self.sym2ensg = dict(zip(ros.target_contrast_gene_name, ros.target_contrast))

        # HOP3: explode intersecting_genes, EXCLUDING negative controls.
        enr = self.enr
        real = enr[~enr.negative_control_disease].copy()
        real = real[real.intersecting_genes.notna()].copy()

        def _parse(x):
            try:
                v = ast.literal_eval(x)
                return v if isinstance(v, list) else []
            except (ValueError, SyntaxError):
                return []

        real["genes"] = real.intersecting_genes.map(_parse)
        exploded = real.explode("genes").dropna(subset=["genes"])
        self._enr_exploded = exploded          # one row per (enrichment row x gene)

        # condition -> gene_set label(s) used by HOP3
        self._condition_gene_sets = {c: [f"downstream_{c}", "regulators"] for c in CONDITIONS}

    # ------------------------------------------------------------------
    # Gene resolution — accept symbol OR ENSG, return both
    # ------------------------------------------------------------------
    def resolve_gene(self, gene: str) -> tuple[str | None, str | None]:
        """Return (symbol, ensg). Either input form is accepted."""
        g = str(gene).strip()
        if g.upper().startswith("ENSG"):
            ensg = g
            return self.ensg2sym.get(ensg), ensg
        # treat as symbol
        return g, self.sym2ensg.get(g)

    # ==================================================================
    # HOP 0 — knockdown-QC gate (QUERIED FIRST)
    # ==================================================================
    def _hop0_gate(self, ensg: str | None, symbol: str | None, condition: str) -> HopResult:
        name = "knockdown-QC gate"
        # Guides are keyed by ENSG (perturbed_gene_id). If we could not resolve
        # an ENSG we cannot even locate the gate -> untested.
        if ensg is None:
            return HopResult(0, name, UNTESTED,
                             f"No Ensembl ID could be resolved for '{symbol}', so the "
                             f"knockdown-QC gate cannot be located. Verdict is UNTESTED, "
                             f"not 'no effect'.", {}, "guide_kd_efficiency")

        sub = self.kd[(self.kd.perturbed_gene_id == ensg) &
                      (self.kd.culture_condition == condition)]
        if len(sub) == 0:
            return HopResult(0, name, UNTESTED,
                             f"No knockdown-QC guides exist for {symbol} ({ensg}) in "
                             f"{condition}. The perturbation was not assayed here; "
                             f"verdict is UNTESTED, not 'no effect'.", {}, "guide_kd_efficiency")

        n_guides = len(sub)
        n_pass = int(sub.signif_knockdown.sum())
        best = sub.sort_values("signif_knockdown", ascending=False).iloc[0]
        receipt = {
            "n_guides": n_guides,
            "n_guides_signif_knockdown": n_pass,
            "guides": sub["Unnamed: 0"].tolist(),
            "signif_knockdown_per_guide": dict(zip(sub["Unnamed: 0"], sub.signif_knockdown.astype(bool))),
            "best_guide": best["Unnamed: 0"],
            "best_guide_mean_expr": best.guide_mean_expr,
            "ntc_mean_expr": best.ntc_mean_expr,
            "best_guide_t_statistic": best.t_statistic,
            "best_guide_p_value": best.p_value,
            "best_guide_adj_p_value": best.adj_p_value,
        }
        if n_pass > 0:
            status = SUPPORTED
            stmt = (f"Knockdown PASSED: {n_pass}/{n_guides} guide(s) achieved a "
                    f"significant knockdown of {symbol} in {condition} "
                    f"(signif_knockdown=True). The perturbation is established; "
                    f"downstream hops are interpretable.")
        else:
            status = UNTESTED
            stmt = (f"Knockdown FAILED the QC gate: 0/{n_guides} guide(s) achieved a "
                    f"significant knockdown of {symbol} in {condition} "
                    f"(signif_knockdown=False for all). The perturbation was NOT "
                    f"established, so any downstream 'no effect' is UNINTERPRETABLE. "
                    f"Verdict is UNTESTED, never 'no effect'.")
        return HopResult(0, name, status, stmt, receipt, "guide_kd_efficiency")

    # ==================================================================
    # HOP 1 — on-target effect
    # ==================================================================
    def _hop1_effect(self, ensg: str | None, symbol: str | None,
                     condition: str, gate_passed: bool) -> HopResult:
        name = "on-target transcriptional effect"
        if ensg is None:
            return HopResult(1, name, UNTESTED,
                             f"No Ensembl ID for '{symbol}'; effect table not queryable.",
                             {}, "DE_stats")
        sub = self.de[(self.de.target_contrast == ensg) &
                      (self.de.culture_condition == condition)]
        if len(sub) == 0:
            return HopResult(1, name, UNTESTED,
                             f"{symbol} ({ensg}) has no DE_stats row in {condition}.",
                             {}, "DE_stats")
        r = sub.iloc[0]
        receipt = {
            "ontarget_significant": bool(r.ontarget_significant),
            "ontarget_effect_size": r.ontarget_effect_size,
            "ontarget_effect_category": r.ontarget_effect_category,
            "offtarget_flag": bool(r.offtarget_flag),
            "n_downstream": r.n_downstream,
            "n_total_de_genes": r.n_total_de_genes,
            "crossdonor_correlation_mean": r.crossdonor_correlation_mean,
            "crossdonor_correlation_min": r.crossdonor_correlation_min,
            "crossguide_correlation": r.crossguide_correlation,
        }
        # Reproducibility annotation (sparse by design)
        repro_bits = []
        if pd.notna(r.crossdonor_correlation_mean):
            repro_bits.append(f"cross-donor r_mean={r.crossdonor_correlation_mean:.3f}")
        if pd.notna(r.crossguide_correlation):
            repro_bits.append(f"cross-guide r={r.crossguide_correlation:.3f}")
        repro = ("; reproducibility: " + ", ".join(repro_bits)) if repro_bits else \
                "; reproducibility metrics not reported for this gene"

        if bool(r.offtarget_flag):
            status = FLAGGED
            stmt = (f"{symbol} in {condition} is FLAGGED as a putative off-target "
                    f"(offtarget_flag=True); on-target effect claims are unreliable. "
                    f"ontarget_effect_category='{r.ontarget_effect_category}'{repro}.")
        elif bool(r.ontarget_significant):
            status = SUPPORTED
            stmt = (f"{symbol} shows a significant on-target effect in {condition} "
                    f"(ontarget_significant=True, category='{r.ontarget_effect_category}', "
                    f"effect_size={r.ontarget_effect_size}, {int(r.n_downstream)} downstream "
                    f"DE genes){repro}.")
        else:
            # Only 'refuted' when the gate passed; otherwise untested context.
            if gate_passed:
                status = REFUTED
                stmt = (f"Despite a passing knockdown, {symbol} shows NO significant "
                        f"on-target effect in {condition} (ontarget_significant=False, "
                        f"category='{r.ontarget_effect_category}'). This refutes a "
                        f"transcriptional-effect hypothesis for this condition.")
            else:
                status = UNTESTED
                stmt = (f"{symbol} shows ontarget_significant=False in {condition}, but "
                        f"because the knockdown gate did not pass this is UNTESTED, "
                        f"not evidence of no effect (category='{r.ontarget_effect_category}').")
        return HopResult(1, name, status, stmt, receipt, "DE_stats")

    # ==================================================================
    # HOP 2 — Th1/Th2 program  (faceted by BOTH contrasts)
    # ==================================================================
    def _hop2_program(self, symbol: str | None, gate_passed: bool) -> HopResult:
        name = "Th1/Th2 polarization program"
        if symbol is None:
            return HopResult(2, name, UNTESTED,
                             "No gene symbol resolved; polarization table not queryable.",
                             {}, "Th2_Th1_polarization")
        facets = {}
        any_sig = False
        directions = []
        for contrast in CONTRASTS:
            row = self.pol[(self.pol.variable == symbol) & (self.pol.contrast == contrast)]
            if len(row) == 0:
                facets[contrast] = {"present": False, "status": UNTESTED,
                                    "note": "gene absent from this contrast"}
                continue
            r = row.iloc[0]
            adjp = r.adj_p_value
            sig = pd.notna(adjp) and adjp < PROGRAM_SIG_ALPHA
            direction = ("Th2-associated (log_fc>0)" if r.log_fc > 0
                         else "Th1-associated (log_fc<0)")
            if sig:
                any_sig = True
                directions.append(f"{contrast.split('(')[1].rstrip(') ')}: {direction}")
            facets[contrast] = {
                "present": True,
                "status": SUPPORTED if sig else REFUTED if gate_passed else UNTESTED,
                "log_fc": _clean(r.log_fc),
                "zscore": _clean(r.zscore),
                "p_value": _clean(r.p_value),
                "adj_p_value": _clean(adjp),
                "direction": direction if sig else None,
            }
        if any_sig:
            status = SUPPORTED
            stmt = (f"{symbol} is a significant member of the Th1/Th2 polarization "
                    f"signature (adj_p<{PROGRAM_SIG_ALPHA}) in at least one contrast — "
                    + "; ".join(directions) + ".")
        elif all(not f.get("present") for f in facets.values()):
            status = UNTESTED
            stmt = (f"{symbol} is absent from both polarization contrasts; "
                    f"program membership is UNTESTED.")
        else:
            status = REFUTED if gate_passed else UNTESTED
            stmt = (f"{symbol} is present but not significant in either polarization "
                    f"contrast (adj_p >= {PROGRAM_SIG_ALPHA}). "
                    + ("Program membership is refuted." if gate_passed
                       else "Reported as UNTESTED context because the knockdown gate did not pass."))
        return HopResult(2, name, status, stmt, {"contrasts": facets}, "Th2_Th1_polarization")

    # ==================================================================
    # HOP 3 — autoimmune disease enrichment
    #   (negative controls excluded; gene lists exploded; condition -> gene_set)
    # ==================================================================
    def _hop3_disease(self, symbol: str | None, condition: str,
                      gate_passed: bool) -> HopResult:
        name = "autoimmune-disease enrichment"
        if symbol is None:
            return HopResult(3, name, UNTESTED,
                             "No gene symbol resolved; enrichment table not queryable.",
                             {}, "cluster_autoimmune_enrichment")
        gene_sets = self._condition_gene_sets[condition]
        hits = self._enr_exploded[
            (self._enr_exploded.genes == symbol) &
            (self._enr_exploded.gene_set.isin(gene_sets))
        ]
        # significant, non-control disease memberships
        sig_hits = hits[(hits.p_adj_fdr < DISEASE_FDR_ALPHA)]
        memberships = []
        for _, r in hits.sort_values("p_adj_fdr").iterrows():
            memberships.append({
                "disease": r.disease,
                "cluster": _clean(r.cluster),
                "gene_set": r.gene_set,
                "odds_ratio": _clean(r.odds_ratio),
                "ci_low": _clean(r.ci_low),
                "ci_high": _clean(r.ci_high),
                "p_adj_fdr": _clean(r.p_adj_fdr),
                "significant": bool(pd.notna(r.p_adj_fdr) and r.p_adj_fdr < DISEASE_FDR_ALPHA),
            })
        receipt = {
            "gene_sets_searched": gene_sets,
            "n_membership_rows": len(hits),
            "n_significant": len(sig_hits),
            "memberships": memberships[:25],   # cap for readability
            "negative_controls_excluded": True,
        }
        if len(sig_hits) > 0:
            status = SUPPORTED
            top = sig_hits.sort_values("p_adj_fdr").iloc[0]
            diseases = sorted(sig_hits.disease.unique())
            stmt = (f"{symbol} is a member of {len(sig_hits)} significant "
                    f"(FDR<{DISEASE_FDR_ALPHA}, negative controls excluded) autoimmune-disease "
                    f"enrichment(s) via {condition} gene sets: {', '.join(diseases)}. "
                    f"Strongest: {top.disease} (cluster {int(top.cluster)}, "
                    f"OR={top.odds_ratio:.2f}, FDR={top.p_adj_fdr:.2e}).")
        elif len(hits) > 0:
            status = REFUTED if gate_passed else UNTESTED
            stmt = (f"{symbol} appears in {len(hits)} disease gene list(s) for {condition} "
                    f"but none reach FDR<{DISEASE_FDR_ALPHA}. "
                    + ("No significant disease enrichment." if gate_passed
                       else "Reported as UNTESTED context (knockdown gate did not pass)."))
        else:
            status = UNTESTED
            stmt = (f"{symbol} is not a member of any non-control disease-enrichment gene "
                    f"list for {condition}; disease association is UNTESTED here.")
        return HopResult(3, name, status, stmt, receipt, "cluster_autoimmune_enrichment")

    # ==================================================================
    # Orchestrator
    # ==================================================================
    def referee(self, gene: str, condition: str) -> Verdict:
        if condition not in CONDITIONS:
            raise ValueError(f"condition must be one of {CONDITIONS}, got {condition!r}")
        symbol, ensg = self.resolve_gene(gene)

        h0 = self._hop0_gate(ensg, symbol, condition)
        gate_passed = (h0.status == SUPPORTED)

        h1 = self._hop1_effect(ensg, symbol, condition, gate_passed)
        h2 = self._hop2_program(symbol, gate_passed)
        h3 = self._hop3_disease(symbol, condition, gate_passed)
        hops = [h0, h1, h2, h3]

        overall, headline = self._synthesize(h0, h1, h2, h3, symbol, condition, gate_passed)
        return Verdict(gene, symbol, ensg, condition, overall, headline, hops)

    @staticmethod
    def _synthesize(h0, h1, h2, h3, symbol, condition, gate_passed) -> tuple[str, str]:
        # Gate governs everything.
        if not gate_passed:
            return ("UNTESTED",
                    f"Knockdown of {symbol} in {condition} did not pass QC "
                    f"(HOP0={h0.status}). The hypothesis is UNTESTED in this condition — "
                    f"downstream signals cannot be read as effect or no-effect.")
        # Gate passed: read the effect hop.
        if h1.status == FLAGGED:
            return ("FLAGGED",
                    f"{symbol} passed knockdown but is flagged as a putative off-target in "
                    f"{condition}; on-target claims are unreliable.")
        if h1.status == REFUTED:
            return ("REFUTED",
                    f"{symbol} passed knockdown QC in {condition} but shows NO on-target "
                    f"transcriptional effect — the perturbation was real and the effect "
                    f"hypothesis is refuted.")
        # Effect supported: grade the downstream chain.
        downstream = [h2.status, h3.status]
        n_support = sum(s == SUPPORTED for s in downstream)
        if n_support == 2:
            return ("YES",
                    f"{symbol} in {condition}: knockdown verified, significant on-target "
                    f"effect, Th1/Th2 program membership, AND autoimmune-disease enrichment — "
                    f"a receipt-backed YES across all four hops.")
        if n_support == 1:
            return ("PARTIAL",
                    f"{symbol} in {condition}: knockdown verified with a significant on-target "
                    f"effect; one of the two downstream links (program / disease) is supported.")
        return ("PARTIAL",
                f"{symbol} in {condition}: knockdown verified with a significant on-target "
                f"effect, but neither downstream program nor disease link reaches significance.")


# --------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "~/pyzobot-data"
    ref = Referee.from_dir(data_dir)
    g = sys.argv[2] if len(sys.argv) > 2 else "GATA3"
    c = sys.argv[3] if len(sys.argv) > 3 else "Stim48hr"
    print(ref.referee(g, c).render())
