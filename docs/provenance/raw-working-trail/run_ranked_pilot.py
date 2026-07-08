"""Ranked pilot: effect-ranked sample -> gated novelty score -> referee_triple cull.
Reports generated -> survived (disjoint) -> referee-supported counts (the honest funnel).
"""
import json, sys
sys.path.insert(0, "src")
from arbiter.lbd.cooccur import preflight_sample
from arbiter.lbd.referee_triple import referee_triple, load_referee_data

COND = "Stim8hr"
pf = preflight_sample(n_genes=15, condition=COND, ab_gate_pct=0.50,
                      rank_genes_by_effect=True,
                      extra_genes=["GATA3", "EGR2", "STAT4", "IL4", "BATF"])

d = load_referee_data()
# cull the top eligible survivors through the referee (exact-C)
culled = []
for t in pf["top_survivors"]:
    r = referee_triple(t["gene"], t["disease"], COND, d)
    culled.append({**t, "referee": r["answer"], "overall": r["overall"]})

supported = [c for c in culled if c["referee"] == "supported"]
report = {
    "condition": COND,
    "gene_selection": pf["gene_selection"],
    "funnel": {
        "generated_triples": pf["n_triples"],
        "disjoint_survivors": pf["n_eligible_survivors"],
        "top_culled": len(culled),
        "referee_supported": len(supported),
    },
    "params": pf["params"],
    "supported_money_shots": supported,
    "all_culled_top": culled,
    "genes": pf["genes"],
}
json.dump(report, open(".claude/scratch/lbd-debate/ranked_pilot.json", "w"), indent=2)

print("=== RANKED PILOT FUNNEL ===")
print(f"generated {report['funnel']['generated_triples']} -> disjoint {report['funnel']['disjoint_survivors']}"
      f" -> top-culled {report['funnel']['top_culled']} -> referee-SUPPORTED {report['funnel']['referee_supported']}")
print(f"ab_gate value = {pf['params']['ab_gate_value']}")
print("\n=== top culled candidates (gene x disease | score | ab bc ac_lit ac_known effect | referee) ===")
for c in culled:
    print(f"  {c['gene']:8} x {c['disease']:26} | s={c['score']:6} | ab={c['ab']:5} bc={c['bc']:6} "
          f"acL={c['ac_lit']:4} acK={c['ac_known']:.3f} eff={c['effect']:5} | {c['referee']}")
print("\n=== MONEY SHOTS (disjoint in lit + referee-supported on the specific disease) ===")
for c in supported:
    print(f"  {c['gene']} x {c['disease']} @ {COND}: {c['overall'][:70]}")
if not supported:
    print("  (none in this sample -- expected; strong regulators are usually already known)")
