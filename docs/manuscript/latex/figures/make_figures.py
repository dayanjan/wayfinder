#!/usr/bin/env python
r"""
Wayfinder manuscript -- figure generation (deterministic, local render).

All figures are rendered from the committed analysis outputs
(../analysis/{sensitivity_results,gate_grid_results,hard_negatives_results}.json)
and the finding facts recorded in sections/04_results.tex. These are the SAME
numbers reproduced byte-for-byte inside Claude Science (S4.5); rendering here is a
deterministic visualization of the CS-verified outputs, chosen so the journal
figures regenerate at revision time without a UI dependency.

Outputs (PDF for LaTeX \includegraphics + PNG for inspection):
  fig1_architecture.{pdf,png}   -- construction vs. referee, separated (C1/C7)
  fig2_funnel_ledger.{pdf,png}  -- funnel + verdict ledger
  fig3_nab2_chain.{pdf,png}     -- NAB2 4-hop receipt chain + STAT6 + 12q13 caveat
  fig4_diagnostics.{pdf,png}    -- Control1/2 + C10 gate grid + C2 hard negatives

Run:  python make_figures.py
"""
import json
import pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ANALYSIS = HERE.parent.parent / "analysis"   # docs/manuscript/analysis

# ---- palette (Okabe-Ito, colorblind-safe) -------------------------------------
C_SUPPORTED = "#009E73"  # green      -- supported
C_REFUTED   = "#D55E00"  # vermilion  -- refuted
C_UNTESTED  = "#E69F00"  # amber      -- untested / abstention
C_WEAK      = "#66C2A5"  # light green -- supported-weak
C_FLAGGED   = "#0072B2"  # blue       -- supported-flagged
C_ASSOC     = "#7B4FA0"  # purple     -- association receipt (disease hop)
C_EXPT      = "#0072B2"  # blue       -- experimental receipt (hops 0-2)
C_NEUTRAL   = "#BDBDBD"
C_INK       = "#222222"
C_PANEL     = "#F4F4F2"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "axes.edgecolor": "#444444",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})


def load(name):
    return json.loads((ANALYSIS / name).read_text())


def save(fig, stem):
    fig.savefig(HERE / f"{stem}.pdf")
    fig.savefig(HERE / f"{stem}.png", dpi=180)
    plt.close(fig)
    print("wrote", stem)


def box(ax, x, y, w, h, text, fc="white", ec=C_INK, lw=1.3, fs=8.5,
        tc=C_INK, weight="normal", rounded=0.02, ha="center", va="center", pad=0.5):
    # `pad` grows the drawn box outward around its centered text -> visible breathing
    # room between text and the border. Kept small so the growth clears neighbours/arrows.
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={pad},rounding_size={rounded}",
                       linewidth=lw, edgecolor=ec, facecolor=fc, zorder=2, mutation_aspect=1)
    ax.add_patch(p)
    if text:
        ax.text(x + w / 2 if ha == "center" else x + 0.6, y + h / 2, text,
                ha=ha, va=va, fontsize=fs, color=tc, weight=weight, zorder=3)
    return p


def arrow(ax, x1, y1, x2, y2, color=C_INK, lw=1.6, style="-|>", ls="-", mut=12):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=mut,
                        linewidth=lw, color=color, linestyle=ls, zorder=1,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)


# ===============================================================================
# FIGURE 1 -- Architecture: construction (generator) vs. referee (adjudication)
# ===============================================================================
def fig1():
    fig, ax = plt.subplots(figsize=(9.2, 6.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

    box(ax, 2, 3, 96, 94, "", fc="#FBFAF7", ec=C_ASSOC, lw=1.4, rounded=0.015)
    ax.text(50, 95.2, "Agentic scientific workbench (Claude Science): author model + independent critic (language self-audit)",
            ha="center", va="center", fontsize=8.2, color=C_ASSOC, style="italic")

    ax.add_patch(Rectangle((5, 60), 90, 27, facecolor=C_PANEL, edgecolor="none", zorder=0))
    ax.text(7, 84.5, "CONSTRUCTION  (generator -- pre-gate filters)", ha="left", va="center",
            fontsize=9.5, weight="bold", color="#555555")
    box(ax, 7, 66, 17, 13, "Held substrate\nCRISPRi Perturb-seq\nCD4$^+$ T cells\n(aggregated tables)",
        fc="white", ec=C_EXPT, fs=7.6)
    box(ax, 30, 66, 18, 13, "Build universe A\nKD-gated +\nprogram-significant\n= 3,935 genes",
        fc="white", ec="#555555", fs=7.8)
    box(ax, 54, 66, 18, 13, "Literature-novelty\ngate\n(rarity + curated\nassociation floor)",
        fc="white", ec="#555555", fs=7.8)
    box(ax, 78, 66, 15, 13, "22,039\neligible\n(gene, disease)\npairs",
        fc="white", ec="#555555", fs=7.8, weight="bold")
    arrow(ax, 24, 72.5, 30, 72.5); arrow(ax, 48, 72.5, 54, 72.5); arrow(ax, 72, 72.5, 78, 72.5)

    ax.add_patch(Rectangle((5, 20), 90, 33, facecolor="#EEF4F1", edgecolor="none", zorder=0))
    ax.text(7, 50.5, "REFEREE  (deterministic adjudication -- one verdict + receipt per pair)",
            ha="left", va="center", fontsize=9.5, weight="bold", color="#1B6B52")
    hops = [
        ("Hop 0\nKnockdown QC", "guide vs. NTC\nexpression", C_EXPT),
        ("Hop 1\nEffect", "on-target DE\n(effect size, #DE)", C_EXPT),
        ("Hop 2\nProgram", "Th1/Th2 shift\n(z, adj. p)", C_EXPT),
        ("Hop 3\nDisease", "module enrichment\n(OR, FDR)", C_ASSOC),
    ]
    x0 = 8
    for i, (title, sub, col) in enumerate(hops):
        x = x0 + i * 18.5
        box(ax, x, 33, 15.5, 12, f"{title}\n\n{sub}", fc="white", ec=col, fs=7.5, lw=1.6)
        if i < 3:
            arrow(ax, x + 15.5, 39, x + 18.5, 39)
    ax.text(8, 28.5, "experimental receipts (referee-owned)", ha="left", va="center",
            fontsize=7.6, color=C_EXPT, weight="bold")
    ax.text(63.5, 28.5, "association receipt", ha="left", va="center",
            fontsize=7.6, color=C_ASSOC, weight="bold")
    ax.text(63.5, 25.8, "(substrate-inherited stringency)", ha="left", va="center",
            fontsize=6.9, color=C_ASSOC)

    arrow(ax, 82, 39, 88, 39)
    for j, (lab, col) in enumerate([("supported", C_SUPPORTED), ("refuted", C_REFUTED), ("untested", C_UNTESTED)]):
        box(ax, 86.5, 44 - j * 6.5, 11, 5, lab, fc=col, ec=col, tc="white", fs=8, weight="bold")
    arrow(ax, 85.5, 66, 85.5, 45.5, color="#888888", ls=(0, (4, 3)))
    ax.text(88.8, 56, "each pair", ha="center", va="center", fontsize=7, color="#888888", rotation=90)

    box(ax, 6, 6, 88, 8,
        "Cross-vendor independence supplied EXTERNALLY (S4.6): a 5-member replication lab\n"
        "(3 Opus-class + 2 Codex), 2 clean-room re-implementations -- unanimous pass.",
        fc="white", ec="#999999", fs=7.4, tc="#555555", rounded=0.03)
    save(fig, "fig1_architecture")


# ===============================================================================
# FIGURE 2 -- Honest funnel + verdict ledger
# ===============================================================================
def fig2():
    fig = plt.figure(figsize=(9.6, 7.2))
    gsL = fig.add_axes([0.04, 0.06, 0.44, 0.88]); gsL.axis("off")
    gsL.set_xlim(0, 100); gsL.set_ylim(0, 100)
    gsR = fig.add_axes([0.53, 0.06, 0.44, 0.88]); gsR.axis("off")
    gsR.set_xlim(0, 100); gsR.set_ylim(0, 100)

    gsL.text(50, 99, "The funnel (Stim8hr)", ha="center", fontsize=10.5, weight="bold")
    steps = [
        ("3,935", "knockdown-gated, program-significant genes (universe A)", 90, "#4C72B0"),
        ("22,039", "eligible (gene, disease) pairs admitted by the gate", 72, "#5B8F4A"),
        ("43", "positive disease hop + passing effect", 54, "#B0812E"),
        ("30", "clean full-chain survivors", 36, C_SUPPORTED),
    ]
    widths = [86, 68, 34, 22]
    for (num, lab, y, col), w in zip(steps, widths):
        x = 50 - w / 2
        box(gsL, x, y - 5, w, 10, f"{num}", fc=col, ec=col, tc="white", fs=13, weight="bold")
        gsL.text(50, y - 6.6, lab, ha="center", va="top", fontsize=7.9, color="#2A2A2A")
    for i in range(len(steps) - 1):
        gsL.annotate("", xy=(50, steps[i + 1][2] + 5), xytext=(50, steps[i][2] - 9.6),
                     arrowprops=dict(arrowstyle="-|>", color="#888888", lw=1.5))
    gsL.text(50, 24, "43 = 30 clean + 10 supported-weak + 3 supported-flagged", ha="center",
             fontsize=7.4, color="#333333")
    gsL.text(50, 20.5, "(+ 1 refuted-effect; 21,995 refuted for the specific disease)", ha="center",
             fontsize=7.1, color="#666666")
    box(gsL, 4, 2, 92, 16,
        "Caveats (restated in Results):\n"
        "the referee ALONE supports 395/47,220 pairs;\n"
        "the novelty gate culls 395 -> 43. Within the funnel\n"
        "the program hop cannot fail (refuted_program $\\equiv$ 0),\n"
        "and '43 supported' is a JOINT gate$\\times$referee count.",
        fc="#FFF7EC", ec=C_UNTESTED, fs=7.0, tc="#4A3C22", rounded=0.03)

    gsR.text(50, 99, "Verdict ledger (spans the verdict space)", ha="center", fontsize=10.5, weight="bold")
    rows = [
        ("NAB2 -> atopic eczema", "supported", C_SUPPORTED, "full chain; eczema clusters OR 3.90/3.43"),
        ("EGR2 -> asthma", "supported", C_SUPPORTED, "effect -11.06, 854 DE; asthma OR 20.4"),
        ("NUDT1 -> T1D", "supported-weak", C_WEAK, "chain holds, trivial effect (4 DE); only zero-lit survivor"),
        ("IL2 -> (Rest)", "untested", C_UNTESTED, "0/2 guides significant; nothing to knock down"),
        ("SLC1A5 -> T1D", "refuted", C_REFUTED, "9 disease gene-sets, none FDR<0.05 (best 0.054)"),
    ]
    y = 86
    for gene, verdict, col, receipt in rows:
        box(gsR, 4, y - 5, 92, 12.5, "", fc="white", ec="#DDDDDD", lw=1.0, rounded=0.02)
        box(gsR, 6, y - 3.2, 3.4, 8.8, "", fc=col, ec=col)
        gsR.text(12, y + 3.0, gene, ha="left", va="center", fontsize=8.6, weight="bold", color=C_INK)
        gsR.text(94, y + 3.0, verdict, ha="right", va="center", fontsize=8.2, weight="bold", color=col)
        gsR.text(12, y - 1.6, receipt, ha="left", va="center", fontsize=7.6, color="#444444")
        y -= 16
    gsR.text(50, 3, "untested (IL2) = abstention;  refuted (SLC1A5) = the confident, receipt-backed no.",
             ha="center", fontsize=7.3, color="#444444", style="italic")
    save(fig, "fig2_funnel_ledger")


# ===============================================================================
# FIGURE 3 -- NAB2 4-hop receipt chain + STAT6 falsification + 12q13 caveat
# ===============================================================================
def fig3():
    fig, ax = plt.subplots(figsize=(9.8, 6.8))
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    ax.text(50, 97, "NAB2 $\\rightarrow$ Th1/Th2 $\\rightarrow$ atopic eczema, hop by hop",
            ha="center", fontsize=11.5, weight="bold")

    hops = [
        ("HOP 0  Knockdown QC", C_EXPT, "experimental receipt",
         "2/2 guides significant\nbest adj. $p\\approx1\\times10^{-16}$\nguide 0.056 vs NTC 0.567",
         "The perturbation worked."),
        ("HOP 1  Effect", C_EXPT, "experimental receipt",
         "on-target knockdown\neffect $-16.9$\n301 downstream DE genes",
         "Large, clean effect."),
        ("HOP 2  Program", C_EXPT, "experimental receipt",
         "Th2 in Ota contrast\n$z=7.71$, adj. $p=1.96\\times10^{-13}$\nlog-FC $+0.63$",
         "Shifts the T-cell program."),
        ("HOP 3  Disease", C_ASSOC, "association receipt",
         "eczema modules 90 & 100\nOR 3.90 (FDR 0.0028)\nOR 3.43 (FDR 0.0224)",
         "genetic-association\nnomination"),
    ]
    x0, w, gap = 3.5, 21.5, 2.0
    for i, (title, col, klass, receipt, tag) in enumerate(hops):
        x = x0 + i * (w + gap)
        box(ax, x, 62, w, 21, "", fc="white", ec=col, lw=2.0, rounded=0.03)
        ax.text(x + w / 2, 79.8, title, ha="center", va="center", fontsize=8.6, weight="bold", color=col)
        ax.text(x + w / 2, 77.4, klass, ha="center", va="center", fontsize=6.4, style="italic", color=col)
        ax.text(x + w / 2, 70.6, receipt, ha="center", va="center", fontsize=7.3, color=C_INK)
        ax.text(x + w / 2, 64.2, tag, ha="center", va="center", fontsize=6.6, color="#666666")
        if i < 3:
            arrow(ax, x + w, 72.5, x + w + gap, 72.5, lw=2.0)

    box(ax, 17, 52, 66, 6.2, "VERDICT: supported  --  a receipt-backed regulatory nomination",
        fc=C_SUPPORTED, ec=C_SUPPORTED, tc="white", fs=8.2, weight="bold", rounded=0.05)

    hop3x = x0 + 3 * (w + gap)
    arrow(ax, hop3x + w / 2, 62, hop3x + w / 2, 46.5, color=C_ASSOC, lw=1.4, ls=(0, (3, 2)))

    box(ax, 3, 29, 46, 17, "", fc="#EEF4F1", ec=C_SUPPORTED, lw=1.4, rounded=0.03)
    ax.text(26, 44.4, "STAT6 cis-effect: RULED OUT (S4.4)", ha="center", fontsize=8.0, weight="bold", color="#1B6B52")
    ax.text(26, 37.0,
            "Under NAB2-KD (authors' genome-wide DE):\n"
            "STAT6 log$_2$FC $+0.087$, adj. $p$ 0.788 $\\rightarrow$ UNMOVED\n"
            "(ranks 5,444 / 10,282). NAB2 self $-3.078$.\n"
            "A cis-artifact would push STAT6 down;\n"
            "it does not move -- the signal is NAB2-specific.",
            ha="center", va="center", fontsize=7.0, color="#243028")

    box(ax, 51, 29, 46, 17, "", fc="#F3EEF7", ec=C_ASSOC, lw=1.4, rounded=0.03)
    ax.text(74, 44.4, "12q13 caveat (S4.4b)", ha="center", fontsize=8.0, weight="bold", color="#4A3A5A")
    ax.text(74, 37.0,
            "The eczema label is a GWAS association with no\n"
            "colocalization / LD control. NAB2 and STAT6 are\n"
            "convergent neighbors (3$'$ ends overlap; promoters\n"
            "~43 kb apart) in the 12q13 atopy locus, so the\n"
            "disease-label provenance is OPEN -- foregrounded,\n"
            "not claimed discharged.",
            ha="center", va="center", fontsize=7.0, color="#3E2E52")

    box(ax, 3, 4, 94, 20, "", fc="#FBFAF7", ec="#CCCCCC", lw=1.0, rounded=0.02)
    ax.text(50, 21.5, "Two receipt classes, kept distinct", ha="center", fontsize=8.6, weight="bold")
    ax.text(6, 16.2,
            "Hops 0-2 (blue) = EXPERIMENTAL receipts (direct perturbation measurements). They license the claim\n"
            "'consistent with a re-derived NAB2 -> Th1/Th2 regulatory role the literature has not made.'",
            ha="left", va="center", fontsize=7.1, color=C_EXPT)
    ax.text(6, 8.7,
            "Hop 3 (purple) = ASSOCIATION receipt (a GWAS-based disease label). Licenses a NOMINATION, not a claim\n"
            "of experimental disease causality. Independent 4-agent audit: 0 papers link NAB2 to either node.",
            ha="left", va="center", fontsize=7.1, color=C_ASSOC)
    save(fig, "fig4_nab2_chain")


# ===============================================================================
# FIGURE 4 -- Diagnostics: Control 1/2, C10 gate grid, C2 hard negatives
# ===============================================================================
def fig4():
    sens = load("sensitivity_results.json")
    grid = load("gate_grid_results.json")
    hn = load("hard_negatives_results.json")

    fig = plt.figure(figsize=(10.6, 10.8))
    gs = fig.add_gridspec(2, 2, hspace=0.52, wspace=0.30,
                          left=0.075, right=0.95, top=0.935, bottom=0.075)
    axA = fig.add_subplot(gs[0, 0]); axB = fig.add_subplot(gs[0, 1])
    axC = fig.add_subplot(gs[1, 0]); axD = fig.add_subplot(gs[1, 1])
    fig.suptitle("Diagnostics of the referee's behavior (Stim8hr) -- not a validation",
                 fontsize=11.5, weight="bold", y=0.972)

    # ---- Panel A: Control 2 label-shuffle null ----
    c2 = sens["control2_label_shuffle_null"]
    mu, sd = c2["null_mean"], c2["null_sd"]
    obs = c2["observed_disease_hop_supported"]
    xs = np.linspace(mu - 6 * sd, mu + 4.5 * sd, 400)
    ys = np.exp(-0.5 * ((xs - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))
    axA.plot(xs, ys, color="#555555", lw=1.6)
    axA.fill_between(xs, ys, color=C_NEUTRAL, alpha=0.45)
    axA.axvline(mu, color="#555555", ls="--", lw=1.2)
    axA.axvline(obs, color=C_REFUTED, lw=2.2)
    axA.annotate(f"observed = {obs}\n(0.86%)   z = {c2['signed_z']:.1f}",
                 xy=(obs, ys.max() * 0.5), xytext=(mu - 5.8 * sd, ys.max() * 0.66),
                 fontsize=7.6, color=C_REFUTED, weight="bold",
                 arrowprops=dict(arrowstyle="-|>", color=C_REFUTED, lw=1.3))
    axA.text(mu + 1.7 * sd, ys.max() * 0.8, f"null\n{mu:.1f}$\\pm${sd:.1f}\n(0.99%)",
             ha="center", va="center", fontsize=7.6, color="#555555")
    axA.set_title("A. Control 2 -- disease-hop label-shuffle null", loc="left")
    axA.set_xlabel("supported pairs / 47,220   (2,000 permutations)")
    axA.set_ylabel("null density"); axA.set_yticks([])
    axA.text(0.5, -0.27,
             "Observed sits BELOW null (lower-tail p $\\approx$ 5$\\times10^{-4}$): the near-total\n"
             "refutation is substrate-inherited, not the referee's own discrimination.",
             transform=axA.transAxes, ha="center", va="top", fontsize=7.7, color="#333333")
    for s in ("top", "right"):
        axA.spines[s].set_visible(False)

    # ---- Panel B: C10 gate grid (9 x 3 heatmap) ----
    pcts = [0.25, 0.5, 0.75]
    minbcs = [2, 3, 5]; taus = [0.05, 0.10, 0.20]
    rowkeys = [(mb, t) for mb in minbcs for t in taus]
    cells = {(c["ab_gate_pct"], c["min_bc"], c["tau"]): c for c in grid["cells"]}
    M = np.zeros((9, 3))
    for j, pct in enumerate(pcts):
        for i, (mb, t) in enumerate(rowkeys):
            M[i, j] = cells[(pct, mb, t)]["clean_supported"]
    im = axB.imshow(M, aspect="auto", cmap="YlGnBu", vmin=M.min(), vmax=M.max())
    for j, pct in enumerate(pcts):
        for i, (mb, t) in enumerate(rowkeys):
            c = cells[(pct, mb, t)]
            txt = f"{int(M[i, j])}\n" + (f"R{c['nab2_eczema_rank']}" if c["nab2_eczema_survives"] else "×")
            axB.text(j, i, txt, ha="center", va="center", fontsize=7.7,
                     color="white" if M[i, j] > M.max() * 0.6 else "#222222",
                     weight="bold" if c["nab2_eczema_survives"] else "normal")
    axB.set_xticks(range(3)); axB.set_xticklabels([f"{p:.2f}" for p in pcts])
    axB.set_yticks(range(9))
    axB.set_yticklabels([f"bc$\\geq${mb}, $\\tau$={t}" for (mb, t) in rowkeys], fontsize=7)
    axB.set_xlabel("literature floor  ab_gate_pct")
    axB.set_title("B. C10 gate grid -- clean survivors & NAB2 rank", loc="left")
    cb = fig.colorbar(im, ax=axB, fraction=0.046, pad=0.03)
    cb.set_label("clean survivors", fontsize=7.5)
    axB.text(0.5, -0.20,
             "Cell = clean survivors; 'R#' = NAB2$\\times$eczema rank, '×' = pruned. Rank stays\n"
             "1-5 (median 4) wherever eligible; drops out only at the 0.75 literature floor.",
             transform=axB.transAxes, ha="center", va="top", fontsize=7.7, color="#333333")

    # ---- Panel C: C2 hard-negatives decomposition ----
    pB = hn["panel_B_frozen_association_nomination"]
    pA = hn["panel_A_arbitrary_out_of_funnel"]
    nB = pB["n_nominations"]; nA = pA["n_genes"]
    segsB = [
        ("untested (QC)", pB["by_verdict"]["untested"], C_UNTESTED),
        ("refuted-program", pB["by_verdict"]["refuted_program"], "#C08457"),
        ("refuted-effect", pB["by_verdict"]["refuted_effect"], "#8C4A2F"),
        ("refuted-disease / reached hop", pB["by_verdict"]["refuted_for_c"], C_NEUTRAL),
        ("supported", pB["by_verdict"]["supported"], C_SUPPORTED),
    ]
    segsA = [
        ("untested (QC)", pA["by_outcome"]["untested"], C_UNTESTED),
        ("refuted-program", pA["by_outcome"]["refuted_program"], "#C08457"),
        ("refuted-effect", pA["by_outcome"]["refuted_effect"], "#8C4A2F"),
        ("refuted-disease / reached hop", pA["by_outcome"]["reached_disease_hop"], C_NEUTRAL),
    ]

    def stack(y, total, segs):
        left = 0.0
        for name, n, col in segs:
            frac = 100 * n / total
            axC.barh(y, frac, left=left, color=col, edgecolor="white", height=0.6)
            if frac > 6:
                axC.text(left + frac / 2, y, f"{frac:.0f}%", ha="center", va="center",
                         fontsize=7.4, color="white", weight="bold")
            left += frac
    stack(1, nA, segsA)
    stack(0, nB, segsB)
    axC.set_xlim(0, 100); axC.set_ylim(-1.15, 1.75)
    axC.set_yticks([1, 0])
    axC.set_yticklabels([f"arbitrary genes\n(n={nA:,})", f"frozen assoc.\nnominations\n(n={nB})"], fontsize=7.5)
    axC.set_xlabel("% of population")
    axC.set_title("C. C2 -- the referee's own edge (out-of-funnel)", loc="left")
    axC.text(8.5, 1.44, "own-hop cull 16.9%", fontsize=7.0, color="#7A5C2E", ha="center")
    axC.text(8.0, 0.44, "own-hop cull 15.7%", fontsize=7.0, color="#7A5C2E", ha="center")
    for s in ("top", "right"):
        axC.spines[s].set_visible(False)
    handles = [Rectangle((0, 0), 1, 1, color=c) for c in
               [C_UNTESTED, "#C08457", "#8C4A2F", C_NEUTRAL, C_SUPPORTED]]
    axC.legend(handles, ["untested (QC)", "refuted-program", "refuted-effect",
                         "refuted-disease / reached hop", "supported"],
               loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3,
               fontsize=7.1, frameon=False, handlelength=1.1, columnspacing=1.2)
    axC.text(0.5, -0.44,
             "Curated-association top guesses include IL36RN$\\times$psoriasis (0.82), TREX1$\\times$lupus\n"
             "(0.78), PADI4$\\times$RA (0.68) -- all UNTESTED (failed KD QC). Control 1: all 2,430\n"
             "failed-KD genes returned untested (100%, 0 leaks).",
             transform=axC.transAxes, ha="center", va="top", fontsize=7.7, color="#333333")

    # ---- Panel D: NAB2 rank stability ----
    c3 = sens["control3_rank_stability"]
    wranks = [g["nab2_rank"] for g in c3["grid"]]
    granks = [c["nab2_eczema_rank"] for c in grid["cells"] if c["nab2_eczema_survives"]]
    bins = np.arange(0.5, 9.5, 1)
    axD.hist(wranks, bins=bins, color=C_FLAGGED, alpha=0.8, label=f"weight grid (n={len(wranks)})", edgecolor="white")
    axD.hist(granks, bins=bins, color=C_SUPPORTED, alpha=0.6, label=f"gate grid, eligible (n={len(granks)})", edgecolor="white")
    axD.set_ylim(0, 8.2)
    axD.axvline(c3["nab2_rank_median"], color=C_REFUTED, ls="--", lw=1.6)
    axD.text(c3["nab2_rank_median"], 7.7, "median 4", ha="center",
             color=C_REFUTED, fontsize=8, weight="bold")
    axD.set_xticks(range(1, 9))
    axD.set_xlabel("NAB2 $\\times$ eczema rank among survivors")
    axD.set_ylabel("# of parameter settings")
    axD.set_title("D. Control 3 -- flagship rank stability", loc="left")
    axD.legend(fontsize=7, frameon=False, loc="upper right")
    for s in ("top", "right"):
        axD.spines[s].set_visible(False)
    axD.text(0.5, -0.20,
             "Across 27 objective-weight settings NAB2 ranks 1-8 (median 4; top-5 in 89%);\n"
             "across gate cells where eligible, rank 1-5. The verdict is invariant in all.",
             transform=axD.transAxes, ha="center", va="top", fontsize=7.7, color="#333333")

    save(fig, "fig3_diagnostics")


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    print("all figures written to", HERE)
