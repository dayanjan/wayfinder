"""Mechanism check: is NAB2's Th1/Th2 effect a generic EGR-module / NAB-corepressor phenotype?
NAB2/NAB1 are corepressors of EGR1/2/3. If NAB2-KD acted through the shared NAB/EGR module, its
program shift should track the module (esp. its own paralog NAB1). Instead NAB2 and NAB1 move in
OPPOSITE directions (the load-bearing D3 distinctness fact), and NAB2's disease profile is specific
where the EGR2 hub is promiscuous. Compares program shift (T2, both contrasts), effect strength (T1),
and referee disease profile across the module.

Emits a COMMITTED receipt (docs/manuscript/analysis/egr_distinctness_results.json) so the R5
distinctness claim is backed by a frozen artifact, not a script-only run (gap G3). Deterministic; local.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, "src")
from arbiter.lbd.referee_triple import referee_triple, load_referee_data
from arbiter.lbd.entities import load_c, build_a_universe

d = load_referee_data()
COND = "Stim8hr"
GENES = ["NAB2", "NAB1", "EGR1", "EGR2", "EGR3"]
a = set(build_a_universe(condition=COND).symbol)
diseases = [c["disease"] for c in load_c()]
t1, t2 = d.t1, d.t2

print(f"{'gene':6} {'KDgated':7} {'eff_size':9} {'n_down':7} {'offtgt':6} | program shift (log_fc; +=Th1, -=Th2)")
print("-" * 100)

genes = {}
for g in GENES:
    r1 = t1[(t1.target_contrast_gene_name == g) & (t1.culture_condition == COND)]
    eff = float(r1.ontarget_effect_size.iloc[0]) if len(r1) else None
    nd = int(r1.n_downstream.iloc[0]) if len(r1) else None
    off = bool(r1.offtarget_flag.iloc[0]) if len(r1) else None
    prog = {}
    prog_str = []
    for _, row in t2[t2.variable == g].iterrows():
        adj = float(row.adj_p_value) if row.adj_p_value == row.adj_p_value else None
        sig = (adj is not None and adj < 0.05)
        tag = ("Th1" if row.log_fc > 0 else "Th2") if sig else "ns"
        key = row.contrast.split("(")[1][:4].strip()
        prog[key] = {"log_fc": round(float(row.log_fc), 4), "adj_p": adj, "sig": sig, "tag": tag}
        prog_str.append(f"{key}: {row.log_fc:+.2f}({tag})")
    genes[g] = {"kd_gated": g in a, "ontarget_effect_size": eff, "n_downstream": nd,
                "offtarget_flag": off, "program_shift": prog}
    effs = f"{eff:+.2f}" if eff is not None else "  NA "
    print(f"{g:6} {str(g in a):7} {effs:9} {str(nd):7} {str(off):6} | {'  '.join(prog_str)}")

print("\ndisease profile (referee-supported among the 12):")
prof = {}
for g in GENES:
    supp = sorted(c for c in diseases if referee_triple(g, c, COND, d)["answer"] == "supported")
    prof[g] = set(supp)
    genes[g]["referee_supported_diseases"] = supp
    print(f"  {g:6}: {supp}")

print("\nNAB2 vs each EGR (shared / NAB2-only / EGR-only diseases):")
nab2_vs_egr = {}
for e in ["EGR1", "EGR2", "EGR3"]:
    entry = {"shared": sorted(prof["NAB2"] & prof[e]),
             "nab2_only": sorted(prof["NAB2"] - prof[e]),
             "egr_only": sorted(prof[e] - prof["NAB2"])}
    nab2_vs_egr[e] = entry
    print(f"  NAB2 vs {e}: shared={entry['shared']} | NAB2-only={entry['nab2_only']} | "
          f"{e}-only={entry['egr_only']}")

# D3 headline: the paralog opposition (both NAB1 contrasts significant, opposite NAB2's Th1 shift)
nab2_p = genes["NAB2"]["program_shift"]
nab1_p = genes["NAB1"]["program_shift"]
nab2_dir = next((v["tag"] for v in nab2_p.values() if v["sig"]), "ns")
nab1_sig_tags = [v["tag"] for v in nab1_p.values() if v["sig"]]
d3 = {
    "claim": "NAB2 and its paralog NAB1 (both EGR corepressors) shift the Th1/Th2 program in OPPOSITE "
             "directions -> NAB2's phenotype is not a shared NAB/EGR-module effect.",
    "nab2_significant_direction": nab2_dir,
    "nab1_significant_directions": nab1_sig_tags,
    "nab1_both_contrasts_significant": len(nab1_sig_tags) == 2 and set(nab1_sig_tags) == {"Th2"},
    "opposition_confirmed": nab2_dir == "Th1" and set(nab1_sig_tags) == {"Th2"},
}
supporting = {
    "d1_effect_and_downstream": "NAB2 eff -16.88 / 301 downstream DE vs NAB1 -15.15 / 0 downstream "
                                "(paralog has no transcriptional consequence here).",
    "d2_disease_specificity": "NAB2 supports {asthma, atopic eczema} only; EGR2 is a promiscuous hub "
                              "(all 11 eligible diseases); NAB1/EGR1/EGR3 support none.",
}

result = {
    "experiment": "G3 — EGR/NAB-module distinctness receipt for NAB2 (serves R5)",
    "condition": COND, "source": "S4 (aggregated supplementary tables T1/T2 + referee)",
    "genes": genes, "nab2_vs_egr": nab2_vs_egr,
    "d3_paralog_opposition_load_bearing": d3, "supporting": supporting,
}
out = Path("docs/manuscript/analysis/egr_distinctness_results.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(f"\nD3 opposition_confirmed={d3['opposition_confirmed']} "
      f"(NAB2 {nab2_dir} vs NAB1 {nab1_sig_tags}); wrote {out}")
