"""Build a deduplicated NAB2 literature corpus across facets for the research agent team."""
import json, sys
sys.path.insert(0, "src")
from arbiter.lit import search as L

FACET_QUERIES = {
    "molecular_function": [
        "NAB2 NGFI-A binding protein 2 transcription", "NAB2 EGR2 corepressor",
        "NAB2 EGR1 repression CHD4 NuRD", "NAB2 NAB1 EGR family",
    ],
    "immunology_tcell": [
        "NAB2 T cell", "NAB2 EGR2 T cell tolerance anergy", "NAB2 Th2 differentiation",
        "NAB2 dendritic cell macrophage immune", "EGR2 EGR3 NAB T cell autoimmunity",
    ],
    "disease_allergy": [
        "NAB2 atopic dermatitis eczema", "NAB2 allergy asthma", "NAB2 autoimmune disease",
        "NAB2 inflammation",
    ],
    "genetics_cancer_clinical": [
        "NAB2 STAT6 fusion solitary fibrous tumor", "NAB2 GWAS association",
        "NAB2 mutation disease", "NAB2 expression cancer",
    ],
}

corpus = {}       # key -> record
facet_index = {}  # facet -> list of keys
for facet, queries in FACET_QUERIES.items():
    keys = []
    for q in queries:
        for r in L.search_all(q, n=30):
            k = r.get("doi") or (r.get("title") or "")[:80].lower()
            if not k or not r.get("title"):
                continue
            if k not in corpus:
                corpus[k] = {kk: r.get(kk) for kk in
                             ("title", "abstract", "year", "doi", "venue", "citations",
                              "source", "url", "authors", "tldr")}
            if k not in keys:
                keys.append(k)
    facet_index[facet] = keys
    print(f"{facet}: {len(keys)} unique records")

recs = list(corpus.values())
recs.sort(key=lambda x: (x.get("citations") or 0), reverse=True)
out = {"n_unique": len(recs), "facet_index_counts": {f: len(k) for f, k in facet_index.items()},
       "records": recs}
json.dump(out, open(".claude/scratch/lbd-debate/nab2_corpus.json", "w"), indent=2)
print(f"TOTAL unique NAB2 records: {len(recs)}")
print("top-cited:")
for r in recs[:8]:
    print(f"  [{r.get('citations') or 0:5}] {r.get('year')} {(r.get('title') or '')[:80]}")
