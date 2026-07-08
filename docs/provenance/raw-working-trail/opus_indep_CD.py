"""Independent re-derivation of CLAIM SET C (STAT6 confounder) + D (EGR mechanism).
Pure pandas over the raw CSVs. Reconstructs each referee hop myself; does NOT import
the project's referee. Method rules taken from reading pyzobot_referee.py, applied to
my own dataframes.
"""
import ast, sys, json
import pandas as pd
import numpy as np

DATA = "data"
COND = "Stim8hr"
GS = f"downstream_{COND}"
ALPHA = 0.05

t1 = pd.read_csv(f"{DATA}/DE_stats.suppl_table.csv")
t2 = pd.read_csv(f"{DATA}/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv")
t3 = pd.read_csv(f"{DATA}/cluster_autoimmune_enrichment_results.suppl_table.csv")
t4 = pd.read_csv(f"{DATA}/guide_kd_efficiency.suppl_table.csv")

sym2ens = dict(zip(t1.target_contrast_gene_name, t1.target_contrast))

# ---- explode T3 (real diseases only) into gene x cluster x disease membership ----
t3_real = t3[~t3.negative_control_disease].copy()
rows = []
for _, r in t3_real.iterrows():
    try:
        genes = ast.literal_eval(r.intersecting_genes) if isinstance(r.intersecting_genes, str) else []
    except (ValueError, SyntaxError):
        genes = []
    for g in genes:
        rows.append((g, r.cluster, r.disease, r.gene_set, r.odds_ratio, r.p_adj_fdr, r.cluster_size))
t3e = pd.DataFrame(rows, columns=["gene", "cluster", "disease", "gene_set",
                                  "odds_ratio", "p_adj_fdr", "cluster_size"])


def gate_status(sym):
    ens = sym2ens.get(sym)
    if ens is None:
        return None
    g = t4[(t4.perturbed_gene_id == ens) & (t4.culture_condition == COND)]
    if len(g) == 0:
        return dict(pass_=False, n_guides=0, n_signif=0, best_p=None,
                    mean_guide=None, mean_ntc=None)
    n_guides = len(g)
    n_signif = int(g.signif_knockdown.sum())
    return dict(pass_=n_signif > 0, n_guides=n_guides, n_signif=n_signif,
                best_p=float(g.adj_p_value.min()),
                mean_guide=float(g.guide_mean_expr.mean()),
                mean_ntc=float(g.ntc_mean_expr.mean()))


def effect_status(sym):
    ens = sym2ens.get(sym)
    r = t1[(t1.target_contrast == ens) & (t1.culture_condition == COND)]
    if len(r) == 0:
        return dict(status="untested", eff=None, n_down=None, offtarget=None, sig=None)
    r = r.iloc[0]
    offt = bool(r.offtarget_flag)
    sig = bool(r.ontarget_significant)
    nd = int(r.n_downstream)
    if offt:
        status = "flagged"
    elif sig:
        status = "supported"
    else:
        status = "refuted"
    return dict(status=status, eff=float(r.ontarget_effect_size), n_down=nd,
                offtarget=offt, sig=sig)


def program_status(sym):
    r = t2[t2.variable == sym]
    facets = {}
    any_sig = False
    for _, row in r.iterrows():
        sig = pd.notna(row.adj_p_value) and row.adj_p_value < ALPHA
        any_sig = any_sig or sig
        direction = ("Th2" if row.log_fc < 0 else "Th1") if sig else "ns"
        facets[row.contrast] = dict(log_fc=float(row.log_fc), z=float(row.zscore),
                                    adjp=float(row.adj_p_value) if pd.notna(row.adj_p_value) else None,
                                    sig=bool(sig), dir=direction)
    return dict(status="supported" if any_sig else ("refuted" if len(r) else "untested"),
                facets=facets)


def disease_membership(sym):
    """Return {disease: (best_OR, best_fdr, n_sig_clusters, clusters_sig)} for FDR<0.05 clusters."""
    sub = t3e[(t3e.gene == sym) & (t3e.gene_set == GS)]
    out = {}
    alld = {}
    for dis, grp in sub.groupby("disease"):
        sig = grp[grp.p_adj_fdr < ALPHA]
        alld[dis] = grp
        if len(sig):
            top = sig.sort_values("p_adj_fdr").iloc[0]
            out[dis] = dict(OR=float(top.odds_ratio), fdr=float(top.p_adj_fdr),
                            n_sig=len(sig), clusters=sorted(sig.cluster.unique().tolist()))
    return out, alld


def supported_profile(sym):
    """Set of diseases where the FULL clean chain holds (answer=='supported')."""
    g = gate_status(sym)
    if g is None or not g["pass_"]:
        return set(), "gate_fail_or_absent"
    e = effect_status(sym)
    p = program_status(sym)
    if e["status"] == "refuted":
        return set(), "effect_refuted"
    if p["status"] == "refuted":
        return set(), "program_refuted"
    if not e["n_down"]:
        return set(), "supported_weak(n_down=0)"
    if e["status"] == "flagged":
        return set(), "supported_flagged(offtarget)"
    mem, _ = disease_membership(sym)
    return set(mem.keys()), "clean"


# ============================ CLAIM SET C ============================
print("=" * 78)
print("CLAIM SET C — STAT6 confounder")
print("=" * 78)

# ---- C1: NAB2's atopic-eczema clusters + locus composition ----
print("\n--- C1: NAB2 atopic-eczema clusters + 12q13 locus test ---")
nab2_ae = t3e[(t3e.gene == "NAB2") & (t3e.gene_set == GS) & (t3e.disease == "atopic eczema")]
nab2_ae_sig = nab2_ae[nab2_ae.p_adj_fdr < ALPHA]
print("NAB2 atopic-eczema cluster rows (all):")
print(nab2_ae[["cluster", "odds_ratio", "p_adj_fdr", "cluster_size"]].to_string(index=False))
print(f"NAB2 atopic-eczema clusters at FDR<0.05: {sorted(nab2_ae_sig.cluster.unique().tolist())}")

# member genes of those clusters (at this gene_set)
for cl in sorted(nab2_ae_sig.cluster.unique().tolist()):
    members = sorted(t3e[(t3e.cluster == cl) & (t3e.gene_set == GS)].gene.unique().tolist())
    print(f"  cluster {cl}: {len(members)} member genes; STAT6 present = {'STAT6' in members}")
    # dump members for cytoband lookup
    with open(f".claude/scratch/lbd-debate/cluster_{cl}_members.json", "w") as fh:
        json.dump(members, fh)

# ---- C2: NAB2 vs STAT6 program z ----
print("\n--- C2: NAB2 vs STAT6 program z-scores (T2) ---")
for g in ["NAB2", "STAT6"]:
    ps = program_status(g)
    print(f"{g}:")
    for contrast, f in ps["facets"].items():
        print(f"    {contrast:30} log_fc={f['log_fc']:+.3f} z={f['z']:+.2f} "
              f"adjp={f['adjp']:.2e} sig={f['sig']} dir={f['dir']}")

# ---- C3: NAB2 vs STAT6 referee-supported disease profile ----
print("\n--- C3: NAB2 vs STAT6 supported disease profile ---")
for g in ["NAB2", "STAT6"]:
    g_gate = gate_status(g); g_eff = effect_status(g); g_prog = program_status(g)
    prof, reason = supported_profile(g)
    mem, _ = disease_membership(g)
    print(f"{g}: gate_pass={g_gate['pass_'] if g_gate else None} "
          f"(n_signif={g_gate['n_signif'] if g_gate else None}/{g_gate['n_guides'] if g_gate else None}), "
          f"effect={g_eff['status']}(eff={g_eff['eff']},n_down={g_eff['n_down']},offt={g_eff['offtarget']}), "
          f"program={g_prog['status']}")
    print(f"    FDR<0.05 disease MEMBERSHIP (pre-chain): {sorted(mem.keys())}")
    print(f"    SUPPORTED profile (full clean chain): {sorted(prof)}  [reason={reason}]")

# ============================ CLAIM SET D ============================
print("\n" + "=" * 78)
print("CLAIM SET D — EGR mechanism")
print("=" * 78)
GENES = ["NAB2", "NAB1", "EGR1", "EGR2", "EGR3"]
print(f"\n{'gene':6} {'gate':16} {'effect':32} | program shift (log_fc; +Th1 -Th2)")
print("-" * 110)
for g in GENES:
    ga = gate_status(g); e = effect_status(g); p = program_status(g)
    gatestr = f"{ga['n_signif']}/{ga['n_guides']} pass={ga['pass_']}" if ga else "ABSENT"
    effstr = f"{e['status']} eff={e['eff']} n_down={e['n_down']} offt={e['offtarget']}"
    progparts = []
    for contrast, f in p["facets"].items():
        short = contrast.split("(")[1][:4] if "(" in contrast else contrast[:4]
        progparts.append(f"{short}:{f['log_fc']:+.2f}({f['dir']})")
    print(f"{g:6} {gatestr:16} {effstr:32} | {'  '.join(progparts)}")

print("\n--- D1: supported-disease breadth per gene ---")
prof = {}
for g in GENES:
    p, reason = supported_profile(g)
    prof[g] = p
    print(f"  {g:6}: n={len(p):2}  {sorted(p)}   [reason={reason}]")

print("\n--- D2/D3: NAB2 vs EGR2 vs NAB1 program directions ---")
for g in ["NAB2", "EGR2", "NAB1", "EGR1", "EGR3"]:
    ps = program_status(g)
    dirs = {c.split("(")[1][:4] if "(" in c else c: (f["dir"], f["log_fc"], f["sig"])
            for c, f in ps["facets"].items()}
    print(f"  {g:6}: {dirs}")
