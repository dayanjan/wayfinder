#!/usr/bin/env python
r"""
Wayfinder manuscript -- Figure 6: independent reproduction of the held-out evaluation
inside Claude Science (the agentic workbench), driven headlessly and blind.

Deterministic render from two committed artifacts: the local metric harness output
(../analysis/heldout_eval_results.json) and Claude Science's own blind recomputation
(../analysis/cs_verify_result.json, produced by CS from the committed manifest with the
expected values withheld). Two panels:
  (A) precision@k per method -- local (lines) vs Claude Science (open markers); they coincide.
  (B) the two co-primary contrasts -- local vs CS point + 95% CI; both span zero (concordant null).
This visualises the S4.5 self-audit discipline applied to the evaluation itself (S4.7).

Run:  python make_fig6_cs_reproduction.py
Outputs: fig6_cs_reproduction.{pdf,png}
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ANALYSIS = HERE.parent.parent / "analysis"

C_WAY = "#009E73"; C_ASSOC = "#7B4FA0"; C_UNTESTED = "#E69F00"
C_EXPT = "#0072B2"; C_WEAK = "#66C2A5"; C_NEUTRAL = "#BDBDBD"; C_INK = "#222222"
C_LOCAL = "#0072B2"; C_CS = "#D55E00"

METHODS = [("wayfinder", "Wayfinder", C_WAY, "o"),
           ("disease_hop_only", "disease-hop", C_ASSOC, "s"),
           ("lit_rarity", "lit-rarity", C_UNTESTED, "^"),
           ("effect", "effect", C_EXPT, "v"),
           ("enrichment_continuous", "enrichment", C_WEAK, "D"),
           ("random", "random", C_NEUTRAL, "x")]
KS = [5, 10, 20, 50]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10,
    "axes.titleweight": "bold", "axes.edgecolor": "#444444",
    "savefig.dpi": 300, "savefig.bbox": "tight", "pdf.fonttype": 42, "ps.fonttype": 42,
})


def main():
    loc = json.loads((ANALYSIS / "heldout_eval_results.json").read_text())["per_method"]
    locc = json.loads((ANALYSIS / "heldout_eval_results.json").read_text())
    cs = json.loads((ANALYSIS / "cs_verify_result.json").read_text())
    csp = cs["precision"]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.2, 4.5),
                                   gridspec_kw={"width_ratios": [1.35, 1.0]})

    # --- Panel A: precision@k, local lines vs CS markers ---
    for key, label, color, _m in METHODS:
        ly = [loc[key][f"prec@{k}"] for k in KS]
        cy = [csp[key][f"prec@{k}"] for k in KS]
        axA.plot(KS, ly, "-", color=color, lw=2.0 if key == "wayfinder" else 1.3, zorder=3)
        axA.plot(KS, cy, "o", color=color, mfc="white", mec=color, ms=7, mew=1.4, zorder=5)
    axA.set_xscale("log"); axA.set_xticks(KS); axA.set_xticklabels([str(k) for k in KS])
    axA.set_xlabel("k (top-ranked pairs)"); axA.set_ylabel("precision@k")
    axA.set_title("(A) precision@k: local (lines) vs Claude Science (markers)")
    axA.set_ylim(0, 1.0); axA.grid(True, alpha=0.25)
    axA.plot([], [], "-", color=C_INK, label="local harness")
    axA.plot([], [], "o", color=C_INK, mfc="white", mec=C_INK, label="Claude Science (blind)")
    axA.legend(fontsize=7.6, loc="upper right", framealpha=0.9)

    # --- Panel B: co-primary contrasts, local vs CS ---
    pairs = [("C_broad\nWf - lit-rarity", "C_broad_wayfinder_vs_lit_rarity", "C_broad"),
             ("C_mech\nWf - disease-hop", "C_mech_wayfinder_vs_disease_hop_only", "C_mech")]
    y0 = [1.0, 0.0]
    for (lab, lkey, ckey), y in zip(pairs, y0):
        lc = locc[lkey]; cc = cs[ckey]
        axB.plot([lc["ci_lo"], lc["ci_hi"]], [y + 0.12, y + 0.12], color=C_LOCAL, lw=3,
                 solid_capstyle="round")
        axB.plot(lc["point"], y + 0.12, "o", color=C_LOCAL, ms=8, zorder=5)
        axB.plot([cc["ci_lo"], cc["ci_hi"]], [y - 0.12, y - 0.12], color=C_CS, lw=3,
                 solid_capstyle="round")
        axB.plot(cc["point"], y - 0.12, "s", color=C_CS, ms=8, zorder=5)
        axB.text(max(lc["ci_hi"], cc["ci_hi"]) + 0.03, y,
                 f"pt {lc['point']:+.2f}", va="center", fontsize=7.6, color=C_INK)
    axB.axvline(0, color=C_INK, lw=1)
    axB.set_yticks(y0); axB.set_yticklabels([p[0] for p in pairs], fontsize=8)
    axB.set_ylim(-0.6, 1.6); axB.set_xlabel(r"paired $\Delta$ precision@20 (95% CI)")
    axB.set_title("(B) co-primary contrasts: local vs CS")
    axB.plot([], [], "o", color=C_LOCAL, label="local")
    axB.plot([], [], "s", color=C_CS, label="Claude Science")
    axB.legend(fontsize=7.6, loc="lower right", framealpha=0.9)
    axB.grid(True, axis="x", alpha=0.25)

    fig.suptitle("Independent reproduction of the held-out evaluation inside Claude Science "
                 "(blind, headless): points + verdict identical, intervals concordant",
                 fontsize=9.3, y=1.02)
    fig.tight_layout()
    for ext, dpi in (("pdf", 300), ("png", 180)):
        fig.savefig(HERE / f"fig6_cs_reproduction.{ext}", dpi=dpi)
    print("wrote fig6_cs_reproduction.pdf + .png")


if __name__ == "__main__":
    main()
