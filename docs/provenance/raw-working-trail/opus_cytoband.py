"""Independent locus test: map member genes of NAB2's atopic-eczema clusters to cytobands
via MyGene, count how many are on 12q13 (STAT6's band). Run on the CORRECT significant
clusters (90,100) AND on cluster 74 (which the project script hardcoded). Direct REST, cached.
"""
import ast, json, time, os
import pandas as pd
import urllib.request, urllib.parse

DATA = "data"; GS = "downstream_Stim8hr"; ALPHA = 0.05
CACHE = ".claude/scratch/lbd-debate/mygene_cache.json"
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

t3 = pd.read_csv(f"{DATA}/cluster_autoimmune_enrichment_results.suppl_table.csv")
t3_real = t3[~t3.negative_control_disease].copy()
rows = []
for _, r in t3_real.iterrows():
    try:
        gs = ast.literal_eval(r.intersecting_genes) if isinstance(r.intersecting_genes, str) else []
    except Exception:
        gs = []
    for g in gs:
        rows.append((g, r.cluster, r.gene_set))
t3e = pd.DataFrame(rows, columns=["gene", "cluster", "gene_set"])


def band(sym):
    if sym in cache:
        return cache[sym]
    url = "https://mygene.info/v3/query?" + urllib.parse.urlencode(
        {"q": f"symbol:{sym}", "fields": "map_location", "species": "human", "size": 1})
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            d = json.load(resp)
        hits = d.get("hits", [])
        b = hits[0].get("map_location") if hits else None
    except Exception as e:
        b = None
    cache[sym] = b
    time.sleep(0.1)
    return b


for sym in ["STAT6", "NAB2", "TESPA1"]:
    print(f"reference: {sym} -> {band(sym)}")

for cl in [74, 90, 100]:
    members = sorted(t3e[(t3e.cluster == cl) & (t3e.gene_set == GS)].gene.unique().tolist())
    bands = {g: band(g) for g in members}
    on12q13 = [g for g, b in bands.items() if b and b.startswith("12q13")]
    on12 = [g for g, b in bands.items() if b and str(b).startswith("12")]
    mapped = {g: b for g, b in bands.items() if b}
    print(f"\ncluster {cl}: {len(members)} members, {len(mapped)} mapped")
    print(f"  STAT6 present: {'STAT6' in members}")
    print(f"  on 12q13 (STAT6 band): {on12q13 or 'NONE'}")
    print(f"  anywhere chr12: {on12 or 'NONE'}")
    # distinct chromosomes represented (genome-wide spread test)
    chroms = sorted({str(b).split('p')[0].split('q')[0] for b in mapped.values()})
    print(f"  distinct chromosome arms represented: {len(chroms)} -> {chroms}")

json.dump(cache, open(CACHE, "w"))
print("\ncache size:", len(cache))
