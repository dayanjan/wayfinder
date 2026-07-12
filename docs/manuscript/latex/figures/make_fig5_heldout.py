#!/usr/bin/env python
r"""
Wayfinder manuscript -- Figure 5: the time-sliced held-out evaluation (G1).

Deterministic render of the committed G1 result
(../analysis/heldout_eval_results.json, produced by arbiter.eval.run_eval from the
committed count manifest -- no live API). Two panels:
  (A) precision@k per method (Wayfinder vs 5 baselines) over the novel-at-T frame;
      the dashed line is the positive base rate (a random ranker's expectation).
  (B) the two co-primary paired contrasts (prec@20 diff) with gene-and-disease
      two-way-clustered bootstrap 95% CIs; a CI crossing 0 is a null, shown straight.

Run:  python make_fig5_heldout.py
Outputs: fig5_heldout_eval.{pdf,png}
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ANALYSIS = HERE.parent.parent / "analysis"
RESULTS = ANALYSIS / "heldout_eval_results.json"

C_WAY = "#009E73"; C_ASSOC = "#7B4FA0"; C_UNTESTED = "#E69F00"
C_EXPT = "#0072B2"; C_WEAK = "#66C2A5"; C_NEUTRAL = "#BDBDBD"; C_INK = "#222222"

# display name, color, marker, linewidth (Wayfinder emphasised)
METHODS = [
    ("wayfinder", "Wayfinder (LBD + referee)", C_WAY, "o", 2.6),
    ("disease_hop_only", "disease-hop only", C_ASSOC, "s", 1.4),
    ("lit_rarity", "literature-rarity", C_UNTESTED, "^", 1.4),
    ("effect", "effect (downstream DE)", C_EXPT, "v", 1.4),
    ("enrichment_continuous", "enrichment (continuous)", C_WEAK, "D", 1.4),
    ("random", "random", C_NEUTRAL, "x", 1.4),
]
KS = [5, 10, 20, 50]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10,
    "axes.titleweight": "bold", "axes.edgecolor": "#444444",
    "savefig.dpi": 300, "savefig.bbox": "tight", "pdf.fonttype": 42, "ps.fonttype": 42,
})


def main():
    if not RESULTS.exists():
        raise SystemExit(f"results not found: {RESULTS}\n"
                         "Run the eval first, then copy eval_results_*.json here.")
    res = json.loads(RESULTS.read_text())
    per = res["per_method"]
    base = res["base_rate"]
    cb = res["C_broad_wayfinder_vs_lit_rarity"]
    cm = res["C_mech_wayfinder_vs_disease_hop_only"]

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10.2, 4.6),
                                   gridspec_kw={"width_ratios": [1.4, 1.0]})

    # --- Panel A: precision@k curves ---
    for key, label, color, marker, lw in METHODS:
        if key not in per:
            continue
        ys = [per[key][f"prec@{k}"] for k in KS]
        axA.plot(KS, ys, marker=marker, color=color, lw=lw, ms=6, label=label,
                 zorder=5 if key == "wayfinder" else 3)
    axA.axhline(base, ls="--", color=C_INK, lw=1, alpha=0.7)
    axA.text(KS[-1], base, f"  base rate {base:.1%}", va="center", ha="left",
             fontsize=7.5, color=C_INK)
    axA.set_xscale("log"); axA.set_xticks(KS); axA.set_xticklabels([str(k) for k in KS])
    axA.set_xlabel("k (top-ranked pairs)"); axA.set_ylabel("precision@k")
    axA.set_title("(A) Recovery of future-established links (T=2016, k≥5)")
    axA.set_ylim(0, 1.0)
    axA.legend(fontsize=7.2, loc="upper right", framealpha=0.9)
    axA.grid(True, alpha=0.25)

    # --- Panel B: co-primary contrasts with CIs ---
    rows = [("C_broad\nWayfinder − lit-rarity", cb),
            ("C_mech\nWayfinder − disease-hop", cm)]
    ys = [1, 0]
    for (lab, c), y in zip(rows, ys):
        sep = c["ci_lo"] > 0
        col = C_WAY if sep else C_NEUTRAL
        axB.plot([c["ci_lo"], c["ci_hi"]], [y, y], color=col, lw=3, solid_capstyle="round")
        axB.plot(c["point"], y, "o", color=col, ms=9, zorder=5)
        axB.annotate(f"{c['point']:+.3f} [{c['ci_lo']:+.3f}, {c['ci_hi']:+.3f}]",
                     (c["point"], y), textcoords="offset points", xytext=(0, 12),
                     ha="center", fontsize=7.8, color=C_INK)
    axB.axvline(0, color=C_INK, lw=1)
    axB.set_yticks(ys); axB.set_yticklabels([r[0] for r in rows], fontsize=8)
    axB.set_ylim(-0.6, 1.6); axB.set_xlabel("paired Δ precision@20 (95% CI)")
    axB.set_title(f"(B) Co-primary contrasts — {res['joint_outcome']}")
    axB.grid(True, axis="x", alpha=0.25)

    n = res["frame_size"]; p = res["positive_count"]
    fig.suptitle(f"Time-sliced held-out evaluation: frame {n:,} novel-at-2016 pairs, "
                 f"{p:,} became literature-established (≥ 5 co-mentions) by retrieval",
                 fontsize=9.5, y=1.02)
    fig.tight_layout()
    for ext, dpi in (("pdf", 300), ("png", 180)):
        fig.savefig(HERE / f"fig5_heldout_eval.{ext}", dpi=dpi)
    print("wrote fig5_heldout_eval.pdf + .png")


if __name__ == "__main__":
    main()
