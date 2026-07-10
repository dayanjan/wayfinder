"""
PyzoBot Hypothesis-Referee (the Validator)
==========================================

Traces one CD4+ T-cell gene through a 4-table Perturb-seq evidence chain and
returns a STRUCTURED VERDICT in which every status is backed by an explicit
data receipt. Join contract is read from `pyzobot_join_spec.json`.

Chain:
  HOP 0  knockdown-QC GATE (T4)  -- is the perturbation valid at all?
  HOP 1  gene -> EFFECT (T1)     -- on-target KD + downstream effect
  HOP 2  effect -> PROGRAM (T2)  -- Th1/Th2 shift, faceted by contrast
  HOP 3  program -> DISEASE (T3) -- membership in disease-enriched clusters

Calibrated status vocabulary ONLY (never "proven"/"discovered"):
  supported   -- a receipt in the tables is consistent with the claim
  refuted     -- a receipt in the tables contradicts the claim
  untested    -- the perturbation is invalid/absent; claim cannot be evaluated
  flagged     -- a caveat (off-target, low reproducibility, missing mapping)

Design rule (the hero feature): HOP 0 runs FIRST. If the knockdown failed,
downstream nulls are UNTESTED, never "no effect".
"""
from __future__ import annotations
import os, ast, json
from dataclasses import dataclass, field, asdict
from typing import Optional
import pandas as pd
import numpy as np

# ----------------------------------------------------------------------------- config
DEFAULT_DATA_DIR = "/home/dayanjan/pyzobot-data"
DEFAULT_SPEC     = "pyzobot_join_spec.json"
CONDITIONS       = ("Rest", "Stim8hr", "Stim48hr")
SIG_ALPHA        = 0.05   # adj-p / FDR threshold used throughout


# ----------------------------------------------------------------------------- data holder
class RefereeData:
    """Loads and pre-indexes the four tables once, per the join spec."""

    def __init__(self, data_dir: str = DEFAULT_DATA_DIR, spec_path: str = DEFAULT_SPEC):
        self.spec = json.load(open(spec_path))
        f = {k: v["file"] for k, v in self.spec["tables"].items()}
        self.t1 = pd.read_csv(os.path.join(data_dir, f["T1_DE_stats"]))
        self.t2 = pd.read_csv(os.path.join(data_dir, f["T2_Th2_Th1"]))
        self.t3 = pd.read_csv(os.path.join(data_dir, f["T3_cluster_enrichment"]))
        self.t4 = pd.read_csv(os.path.join(data_dir, f["T4_guide_kd"]))

        # ENSG <-> SYMBOL (T1 is 1:1 and carries both)
        self.sym2ens = dict(zip(self.t1.target_contrast_gene_name, self.t1.target_contrast))
        self.ens2sym = {v: k for k, v in self.sym2ens.items()}

        # HOP 0 gate: aggregate guides -> gene x condition (spec join "gate")
        t4v = self.t4.dropna(subset=["perturbed_gene_id"])
        self.gate = (t4v.groupby(["perturbed_gene_id", "culture_condition"])
                        .agg(n_guides=("signif_knockdown", "size"),
                             n_signif=("signif_knockdown", "sum"),
                             best_adj_p=("adj_p_value", "min"),
                             mean_guide_expr=("guide_mean_expr", "mean"),
                             mean_ntc_expr=("ntc_mean_expr", "mean"))
                        .reset_index())
        self.gate["gate_pass"] = self.gate.n_signif > 0

        # HOP 3: explode T3 intersecting_genes (real diseases only), keep neg-controls aside
        self.t3_real = self.t3[~self.t3.negative_control_disease].copy()
        rows = []
        for _, r in self.t3_real.iterrows():
            for g in self._parse_list(r.intersecting_genes):
                rows.append((g, r.cluster, r.disease, r.gene_set,
                             r.odds_ratio, r.p_adj_fdr, r.cluster_size))
        self.t3_exploded = pd.DataFrame(
            rows, columns=["gene", "cluster", "disease", "gene_set",
                           "odds_ratio", "p_adj_fdr", "cluster_size"])

    @staticmethod
    def _parse_list(s):
        try:
            return ast.literal_eval(s) if isinstance(s, str) else []
        except (ValueError, SyntaxError):
            return []

    def resolve(self, gene: str):
        """Accept a SYMBOL or an ENSG; return (symbol, ensg) or (None, None)."""
        if gene in self.sym2ens:
            return gene, self.sym2ens[gene]
        if gene in self.ens2sym:
            return self.ens2sym[gene], gene
        # tolerate ENSG with version suffix
        base = gene.split(".")[0]
        if base in self.ens2sym:
            return self.ens2sym[base], base
        return None, None


# ----------------------------------------------------------------------------- verdict schema
@dataclass
class Hop:
    hop: int
    name: str
    status: str                       # supported | refuted | untested | flagged
    claim: str
    receipt: dict = field(default_factory=dict)   # the exact table values
    caveats: list = field(default_factory=list)


@dataclass
class Verdict:
    gene_symbol: Optional[str]
    gene_ensg: Optional[str]
    condition: str
    overall: str                      # calibrated one-liner
    gate_pass: bool
    hops: list = field(default_factory=list)

    def to_dict(self):
        d = asdict(self)
        return d

    def summary(self) -> str:
        lines = [f"REFEREE VERDICT  {self.gene_symbol or '?'} ({self.gene_ensg or '?'})  @ {self.condition}",
                 f"  overall: {self.overall}"]
        for h in self.hops:
            lines.append(f"  HOP {h.hop} {h.name:<16} [{h.status:^9}] {h.claim}")
            for k, v in h.receipt.items():
                lines.append(f"        - {k}: {v}")
            for c in h.caveats:
                lines.append(f"        ! {c}")
        return "\n".join(lines)


# ----------------------------------------------------------------------------- the referee
def referee(gene: str, condition: str, data: RefereeData) -> Verdict:
    """Trace `gene` (SYMBOL or ENSG) at `condition` through the evidence chain."""
    if condition not in CONDITIONS:
        raise ValueError(f"condition must be one of {CONDITIONS}, got {condition!r}")

    sym, ens = data.resolve(gene)
    v = Verdict(gene_symbol=sym, gene_ensg=ens, condition=condition,
                overall="", gate_pass=False)

    if sym is None:
        v.overall = "untested - gene identifier not found in the perturbation panel"
        v.hops.append(Hop(0, "GATE", "untested",
                          "gene not in dataset",
                          receipt={"query": gene}))
        return v

    # ---------------------------------------------------------------- HOP 0: GATE (T4)
    gp = data.gate[(data.gate.perturbed_gene_id == ens) &
                   (data.gate.culture_condition == condition)]
    if len(gp) == 0:
        v.hops.append(Hop(0, "GATE", "untested",
            "no guides for this gene x condition in the KD-QC table",
            receipt={"n_guides": 0}))
        v.overall = "untested - no knockdown data for this gene at this condition"
        return v

    gp = gp.iloc[0]
    v.gate_pass = bool(gp.gate_pass)
    gate_receipt = {
        "n_guides": int(gp.n_guides),
        "n_signif_knockdown_guides": int(gp.n_signif),
        "best_guide_adj_p": _fmt(gp.best_adj_p),
        "mean_guide_expr": _fmt(gp.mean_guide_expr),
        "mean_ntc_expr": _fmt(gp.mean_ntc_expr),
    }
    if not v.gate_pass:
        # THE HERO FEATURE: failed KD => everything downstream is UNTESTED
        cav = []
        if gp.mean_guide_expr <= gp.mean_ntc_expr * 1.0 and gp.mean_ntc_expr < 0.05:
            cav.append("target barely expressed at this condition - nothing to knock down")
        v.hops.append(Hop(0, "GATE", "untested",
            "knockdown did NOT reach significance for any guide - "
            "downstream absence of effect is UNINTERPRETABLE, not 'no effect'",
            receipt=gate_receipt, caveats=cav))
        v.overall = ("untested - knockdown failed the QC gate; "
                     "any null downstream result cannot be read as a negative")
        return v

    v.hops.append(Hop(0, "GATE", "supported",
        f"knockdown confirmed: {int(gp.n_signif)}/{int(gp.n_guides)} guides "
        f"significant (best adj-p {_fmt(gp.best_adj_p)})",
        receipt=gate_receipt))

    # ---------------------------------------------------------------- HOP 1: EFFECT (T1)
    t1r = data.t1[(data.t1.target_contrast == ens) &
                  (data.t1.culture_condition == condition)]
    if len(t1r) == 0:
        v.hops.append(Hop(1, "EFFECT", "untested",
            "gene absent from DE_stats at this condition", receipt={}))
    else:
        r = t1r.iloc[0]
        rc = {
            "ontarget_significant": bool(r.ontarget_significant),
            "ontarget_effect_size": _fmt(r.ontarget_effect_size),
            "ontarget_effect_category": r.ontarget_effect_category,
            "n_downstream_DE_genes": int(r.n_downstream),
            "offtarget_flag": bool(r.offtarget_flag),
        }
        cav = []
        # reproducibility caveats only where populated
        if pd.notna(r.crossdonor_correlation_mean):
            rc["crossdonor_correlation_mean"] = _fmt(r.crossdonor_correlation_mean)
            if r.crossdonor_correlation_mean < 0.1:
                cav.append("low cross-donor reproducibility (<0.1)")
        if pd.notna(r.crossguide_correlation):
            rc["crossguide_correlation"] = _fmt(r.crossguide_correlation)
            if r.crossguide_correlation < 0.1:
                cav.append("low cross-guide reproducibility (<0.1)")
        if r.offtarget_flag:
            cav.append("off-target flag set in DE_stats")
            status = "flagged"
        elif r.ontarget_significant and r.n_downstream > 0:
            status = "supported"
        elif r.ontarget_significant and r.n_downstream == 0:
            status = "supported"   # KD worked, simply no downstream DE
        else:
            status = "refuted"     # KD confirmed by gate but T1 sees no on-target effect
        claim = ("perturbation produces a downstream transcriptional effect"
                 if r.n_downstream > 0 else
                 "on-target KD detected but no downstream DE genes at this condition")
        v.hops.append(Hop(1, "EFFECT", status, claim, receipt=rc, caveats=cav))

    # ---------------------------------------------------------------- HOP 2: PROGRAM (T2)
    t2r = data.t2[data.t2.variable == sym]
    if len(t2r) == 0:
        v.hops.append(Hop(2, "PROGRAM", "untested",
            "gene not measured in the Th1/Th2 polarization contrast", receipt={}))
    else:
        facets = {}
        any_sig = False
        for _, row in t2r.iterrows():
            sig = pd.notna(row.adj_p_value) and row.adj_p_value < SIG_ALPHA
            any_sig = any_sig or sig
            # Polarity of the Th2_vs_Th1 contrast: log_fc > 0 == Th2-associated.
            # Validated 2026-07-09 against canonical markers in the signature itself --
            # Th2 markers (GATA3/IL4/IL13/IL5) are strongly POSITIVE (Ota mean +1.74),
            # Th1 markers (TBX21/IFNG) strongly negative (mean -4.10). (Prior code had this
            # inverted: it labeled log_fc>0 "Th1-associated". Verdicts are unaffected -- HOP-2
            # status keys on significance, not direction -- only this descriptive label changed.)
            direction = ("Th2-associated" if row.log_fc > 0 else "Th1-associated") \
                if sig else "no significant shift"
            facets[row.contrast] = {
                "log_fc": _fmt(row.log_fc), "zscore": _fmt(row.zscore),
                "adj_p_value": _fmt(row.adj_p_value),
                "significant": bool(sig), "direction": direction,
            }
        status = "supported" if any_sig else "refuted"
        claim = ("gene shifts the Th1/Th2 program in >=1 reference contrast"
                 if any_sig else
                 "gene does not significantly shift the Th1/Th2 program in either contrast")
        v.hops.append(Hop(2, "PROGRAM", status, claim, receipt=facets))

    # ---------------------------------------------------------------- HOP 3: DISEASE (T3)
    gs = f"downstream_{condition}"
    sub = data.t3_exploded[(data.t3_exploded.gene == sym) &
                           (data.t3_exploded.gene_set == gs)]
    if len(sub) == 0:
        # also report if the gene appears in ANY condition's set, as a caveat
        anysub = data.t3_exploded[data.t3_exploded.gene == sym]
        cav = ([f"appears in other gene_sets: "
                f"{sorted(anysub.gene_set.unique())}"] if len(anysub) else [])
        v.hops.append(Hop(3, "DISEASE", "untested" if len(anysub) else "refuted",
            "gene is not a member of any disease-cluster gene-set for this condition",
            receipt={"gene_set_checked": gs}, caveats=cav))
    else:
        sig = sub[sub.p_adj_fdr < SIG_ALPHA]
        if len(sig):
            top = sig.sort_values("p_adj_fdr")
            rc = {"n_significant_disease_clusters": int(len(sig)),
                  "diseases": sorted(sig.disease.unique()),
                  "top_hits": [
                      {"disease": r.disease, "cluster": int(r.cluster),
                       "odds_ratio": _fmt(r.odds_ratio), "p_adj_fdr": _fmt(r.p_adj_fdr)}
                      for _, r in top.head(5).iterrows()]}
            v.hops.append(Hop(3, "DISEASE", "supported",
                "gene is a member of >=1 autoimmune-disease-enriched cluster",
                receipt=rc))
        else:
            best = sub.sort_values("p_adj_fdr").iloc[0]
            v.hops.append(Hop(3, "DISEASE", "refuted",
                "gene appears in disease cluster gene-sets but NONE reach FDR<0.05 - "
                "the disease link is not supported by the enrichment",
                receipt={"n_appearances": int(len(sub)),
                         "best_p_adj_fdr": _fmt(best.p_adj_fdr),
                         "best_odds_ratio": _fmt(best.odds_ratio),
                         "best_disease": best.disease}))

    v.overall = _synthesize_overall(v)
    return v


# ----------------------------------------------------------------------------- helpers
def _fmt(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    if isinstance(x, (float, np.floating)):
        ax = abs(x)
        if ax != 0 and (ax < 1e-3 or ax >= 1e4):
            return float(f"{x:.3e}")
        return round(float(x), 4)
    return x


def _synthesize_overall(v: Verdict) -> str:
    """One calibrated sentence from the hop statuses (never 'proven')."""
    hs = {h.name: h.status for h in v.hops}
    if not v.gate_pass:
        return "untested - knockdown failed QC gate"
    eff = hs.get("EFFECT"); prog = hs.get("PROGRAM"); dis = hs.get("DISEASE")
    if eff in ("supported", "flagged") and prog == "supported" and dis == "supported":
        tail = " (with caveats)" if eff == "flagged" else ""
        return ("consistent with a gene -> program -> disease chain "
                "re-derived from the tables" + tail)
    if dis == "refuted":
        return "gene->disease link refuted: gene in cluster gene-sets but enrichment not significant"
    if prog == "refuted":
        return "program link refuted: knockdown valid but no significant Th1/Th2 shift"
    if eff == "refuted":
        return "effect refuted: knockdown valid by gate but DE_stats shows no on-target effect"
    parts = [f"{h.name.lower()}:{h.status}" for h in v.hops if h.hop > 0]
    return "partial chain - " + ", ".join(parts)


def referee_json(gene: str, condition: str, data: RefereeData) -> str:
    return json.dumps(referee(gene, condition, data).to_dict(), indent=2, default=str)


if __name__ == "__main__":
    d = RefereeData()
    for g, c in [("EGR2", "Stim8hr"), ("IL2", "Rest"), ("SLC1A5", "Stim8hr")]:
        print("=" * 78)
        print(referee(g, c, d).summary())
