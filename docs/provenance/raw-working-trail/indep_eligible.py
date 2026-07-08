"""Reconstruct the ELIGIBLE set from CACHED literature/OpenTargets (B2 given) and
classify each eligible pair with an INDEPENDENT referee (raw CSVs only)."""
import ast, sys
import pandas as pd
from collections import Counter

REPO = r"C:/Users/wijesingheds/Documents/04 Fun with Coding/2026-07-07 PyZoBot-Arbiter"
sys.path.insert(0, REPO + "/src")
from arbiter.lbd import sources as S
from arbiter.lbd.entity_maps import program_terms, DISEASES, ELIGIBLE_DISEASES

D = REPO + "/data"; COND = "Stim8hr"; ALPHA = 0.05

def as_bool(s):
    return s if s.dtype == bool else s.astype(str).str.strip().str.lower().eq("true")

t4 = pd.read_csv(D+"/guide_kd_efficiency.suppl_table.csv",
                 usecols=["perturbed_gene_id","culture_condition","signif_knockdown"]).dropna(subset=["perturbed_gene_id"])
t1 = pd.read_csv(D+"/DE_stats.suppl_table.csv",
                 usecols=["target_contrast","target_contrast_gene_name","culture_condition",
                          "ontarget_significant","n_downstream","offtarget_flag"])
t2 = pd.read_csv(D+"/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv",
                 usecols=["variable","adj_p_value"])
t3 = pd.read_csv(D+"/cluster_autoimmune_enrichment_results.suppl_table.csv")

t4["signif_knockdown"] = as_bool(t4["signif_knockdown"])
gate = t4.groupby(["perturbed_gene_id","culture_condition"])["signif_knockdown"].any().reset_index()
gate = gate[gate["signif_knockdown"]].rename(columns={"perturbed_gene_id":"ensg","culture_condition":"condition"})
t1c = t1.copy(); t1c["ontarget_significant"]=as_bool(t1c["ontarget_significant"])
t1c["n_downstream"]=pd.to_numeric(t1c["n_downstream"],errors="coerce").fillna(0)
eff = t1c[t1c["ontarget_significant"]|(t1c["n_downstream"]>0)].rename(
    columns={"target_contrast":"ensg","target_contrast_gene_name":"symbol","culture_condition":"condition"})
eff = eff.groupby(["ensg","symbol","condition"])["n_downstream"].max().reset_index()
A = gate.merge(eff,on=["ensg","condition"],how="inner")[["ensg","symbol","condition","n_downstream"]].drop_duplicates()
t2["adj_p_value"]=pd.to_numeric(t2["adj_p_value"],errors="coerce")
prog_sig=set(t2.loc[t2["adj_p_value"]<ALPHA,"variable"].dropna().unique())
A=A[A["symbol"].isin(prog_sig)]; A=A[A["condition"]==COND].reset_index(drop=True)
genes=list(dict.fromkeys(A["symbol"].tolist()))

t1s=t1c[t1c["culture_condition"]==COND].copy(); t1s["offtarget_flag"]=as_bool(t1s["offtarget_flag"])
sym2ens=dict(zip(t1["target_contrast_gene_name"],t1["target_contrast"]))
eff_status={}
for sym in genes:
    rows=t1s[t1s["target_contrast"]==sym2ens.get(sym)]
    if len(rows)==0: eff_status[sym]=("untested",0); continue
    r=rows.iloc[0]; n=int(r["n_downstream"])
    st="flagged" if bool(r["offtarget_flag"]) else ("supported" if bool(r["ontarget_significant"]) else "refuted")
    eff_status[sym]=(st,n)

t3r=t3[~t3["negative_control_disease"]]; gs=f"downstream_{COND}"
sup_dis={}
for _,r in t3r.iterrows():
    if r["gene_set"]!=gs: continue
    try: mem=ast.literal_eval(r["intersecting_genes"]) if isinstance(r["intersecting_genes"],str) else []
    except (ValueError,SyntaxError): mem=[]
    if pd.notna(r["p_adj_fdr"]) and r["p_adj_fdr"]<ALPHA:
        for g in mem: sup_dis.setdefault(g,set()).add(r["disease"])

def classify(sym, dis):
    est,n=eff_status[sym]
    if dis not in sup_dis.get(sym,set()): return "refuted_for_c"
    if est=="refuted": return "refuted_effect"
    if not n: return "supported_weak"
    if est=="flagged": return "supported_flagged"
    return "supported"

diseases=[{"disease":n,"id":DISEASES[n]["id"]} for n in ELIGIBLE_DISEASES]
bc={d["disease"]:S.cooccur_count(program_terms("BC"),d["disease"]) for d in diseases}
known={d["disease"]:S.opentargets_disease_targets(d["id"]) for d in diseases}
ab={g:S.cooccur_count(g,program_terms("AB")) for g in genes}
ab_gate=sorted(ab.values())[int(round(0.50*(len(ab)-1)))] if ab else 0
print(f"[gate] ab_gate(50th pct)={ab_gate}  (claim: 26)")
eligible=[(g,d["disease"]) for g in genes for d in diseases
          if ab[g]>=ab_gate and bc[d["disease"]]>=3 and S.opentargets_known(g,known[d["disease"]])<=0.1]
print(f"[gate] eligible pairs={len(eligible)}  (claim B2: 22039)")

cls=Counter(); sup_pairs=[]
for g,d in eligible:
    c=classify(g,d); cls[c]+=1
    if c.startswith("supported"): sup_pairs.append((g,d,c))
print("\n[B3 over ELIGIBLE - INDEPENDENT referee]:")
for k in ["supported","supported_weak","supported_flagged","refuted_effect","refuted_for_c"]:
    print(f"    {k:20} {cls.get(k,0)}")
dcs=sum(v for k,v in cls.items() if k.startswith("supported"))
print(f"    disease_c_supported_total = {dcs}   (claim 43)")
print(f"    clean_supported           = {cls.get('supported',0)}   (claim 30)")
print(f"    supported_weak            = {cls.get('supported_weak',0)}   (claim 10)")
print(f"    supported_flagged         = {cls.get('supported_flagged',0)}   (claim 3)")
print(f"    refuted_effect            = {cls.get('refuted_effect',0)}   (claim 1)")

clean=[(g,d) for g,d,c in sup_pairs if c=="supported"]
pd_clean=[]
for g,d in clean:
    if S.cooccur_count(g,d)==0: pd_clean.append((g,d))
print(f"\n[B4] pure-disjoint (ac_lit==0) among clean supported = {len(pd_clean)}  (claim 1)")
for g,d in pd_clean:
    est,n=eff_status[g]; print(f"    {g} x {d}  effect_n_down={n}")
print("\n[clean supported list]:")
for g,d in sorted(clean):
    print(f"    {g:10} x {d}")
