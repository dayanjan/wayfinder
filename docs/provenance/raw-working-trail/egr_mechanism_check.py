"""Mechanism check: is NAB2's Th1/Th2 effect EGR-mediated?
NAB2/NAB1 are corepressors of EGR1/2/3. If NAB2-KD acts by DE-REPRESSING EGR, its phenotype
should look OPPOSITE to EGR-KD (removing the brake -> more EGR activity). Compare program shift
(T2, both contrasts), effect strength (T1), and disease profile (referee) across the module.
"""
import sys
sys.path.insert(0, "src")
from arbiter.lbd.referee_triple import referee_triple, load_referee_data
from arbiter.lbd.entities import load_c, build_a_universe

d = load_referee_data()
COND = "Stim8hr"
GENES = ["NAB2", "NAB1", "EGR1", "EGR2", "EGR3"]
a = set(build_a_universe(condition=COND).symbol)
diseases = [c["disease"] for c in load_c()]

print(f"{'gene':6} {'KDgated':7} {'eff_size':9} {'n_down':7} {'offtgt':6} | program shift (log_fc; +=Th1, -=Th2)")
print("-" * 100)
t1, t2 = d.t1, d.t2
for g in GENES:
    r1 = t1[(t1.target_contrast_gene_name == g) & (t1.culture_condition == COND)]
    eff = r1.ontarget_effect_size.iloc[0] if len(r1) else None
    nd = int(r1.n_downstream.iloc[0]) if len(r1) else None
    off = bool(r1.offtarget_flag.iloc[0]) if len(r1) else None
    prog = []
    for _, row in t2[t2.variable == g].iterrows():
        sig = (row.adj_p_value < 0.05) if row.adj_p_value == row.adj_p_value else False
        tag = ("Th1" if row.log_fc > 0 else "Th2") if sig else "ns"
        prog.append(f"{row.contrast.split('(')[1][:4]}: {row.log_fc:+.2f}({tag})")
    effs = f"{eff:+.2f}" if eff is not None else "  NA "
    print(f"{g:6} {str(g in a):7} {effs:9} {str(nd):7} {str(off):6} | {'  '.join(prog)}")

print("\ndisease profile (referee-supported among the 12):")
prof = {}
for g in GENES:
    supp = [c for c in diseases if referee_triple(g, c, COND, d)["answer"] == "supported"]
    prof[g] = set(supp)
    print(f"  {g:6}: {sorted(supp)}")

print("\nNAB2 vs each EGR (shared / NAB2-only / EGR-only diseases):")
for e in ["EGR1", "EGR2", "EGR3"]:
    sh = prof["NAB2"] & prof[e]
    print(f"  NAB2 vs {e}: shared={sorted(sh)} | NAB2-only={sorted(prof['NAB2']-prof[e])} | {e}-only={sorted(prof[e]-prof['NAB2'])}")
