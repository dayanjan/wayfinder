"""Two STAT6-confounder checks for the NAB2 finding.
A) Locus test: are NAB2's atopic-eczema clusters (74,90) a 12q13 genomic-locus artifact,
   or genome-wide functional co-expression modules?  -> map member genes to cytobands.
B) Distinct-biology test: do NAB2 and STAT6 shift the Th1/Th2 program the same way and
   enrich for the same diseases?  -> compare program vectors + disease profiles.
"""
import sys
sys.path.insert(0, "src")
from arbiter.lbd import _http
from arbiter.lbd.referee_triple import referee_triple, load_referee_data
from arbiter.lbd.entities import load_c

d = load_referee_data()
te = d.t3_exploded
gs = "downstream_Stim8hr"


def cytobands(symbols):
    """MyGene per-gene (cached) symbol -> cytoband (map_location)."""
    out = {}
    for g in symbols:
        data = _http.get("https://mygene.info/v3/query",
                         params={"q": f"symbol:{g}", "fields": "map_location",
                                 "species": "human", "size": 1})
        hits = data.get("hits", [])
        if hits and hits[0].get("map_location"):
            out[g] = hits[0]["map_location"]
    return out


# ---- Check A: locus composition of NAB2's significant atopic-eczema clusters ----
print("=" * 70)
print("CHECK A - are NAB2's atopic-eczema clusters a 12q13 locus artifact?")
for cl in [74, 90]:
    genes = sorted(te[(te.cluster == cl) & (te.gene_set == gs)].gene.unique().tolist())
    bands = cytobands(genes)
    on12q13 = [g for g, b in bands.items() if b and b.startswith("12q13")]
    on12 = [g for g, b in bands.items() if b and b.startswith("12")]
    print(f"\ncluster {cl}: {len(genes)} genes, {len(bands)} mapped")
    print(f"  on 12q13 (STAT6's band): {on12q13 or 'NONE'}")
    print(f"  anywhere on chr12: {on12 or 'NONE'}")
    print(f"  STAT6 present: {'STAT6' in genes}")
    # a few example bands to show genome-wide spread
    ex = list(bands.items())[:8]
    print(f"  example bands: {ex}")

# ---- Check B: NAB2 vs STAT6 program shift + disease profile ----
print("\n" + "=" * 70)
print("CHECK B - do NAB2 and STAT6 have distinct programs / disease profiles?")
t2 = d.t2
for g in ["NAB2", "STAT6"]:
    sub = t2[t2.variable == g]
    print(f"\n{g} Th1/Th2 program shift (T2):")
    for _, r in sub.iterrows():
        sig = (r.adj_p_value < 0.05) if r.adj_p_value == r.adj_p_value else False
        direction = ("Th2-assoc" if r.log_fc < 0 else "Th1-assoc") if sig else "n.s."
        print(f"  {r.contrast:28} log_fc={r.log_fc:+.3f} z={r.zscore:+.2f} adjp={r.adj_p_value:.2e} -> {direction}")

prof = {}
for g in ["NAB2", "STAT6"]:
    supp = [c["disease"] for c in load_c()
            if referee_triple(g, c["disease"], "Stim8hr", d)["answer"] == "supported"]
    prof[g] = set(supp)
    print(f"\n{g} referee-supported diseases ({len(supp)}): {sorted(supp)}")
inter = prof["NAB2"] & prof["STAT6"]
print(f"\nshared diseases: {sorted(inter)}")
print(f"NAB2-only: {sorted(prof['NAB2'] - prof['STAT6'])}")
print(f"STAT6-only: {sorted(prof['STAT6'] - prof['NAB2'])}")
jacc = len(inter) / len(prof["NAB2"] | prof["STAT6"]) if (prof["NAB2"] | prof["STAT6"]) else 0
print(f"Jaccard(disease profiles) = {jacc:.2f}  (low = distinct biology)")
