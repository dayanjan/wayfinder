"""
PyZoBot Stage-0 feasibility probe — the actual code that was run for all four probes.
Environment prep (run once, outside this script):
    pip install requests s3fs h5py
Network note: Probe C required a network grant for the bucket-qualified host
    genome-scale-tcell-perturb-seq.s3.amazonaws.com  (path-style s3.amazonaws.com is denylisted)
    and s3fs must be configured with virtual addressing_style to hit that host.
"""
import json, traceback
import requests


# ---------- Probe A — Europe PMC literature co-mention count (HTTP GET) ----------
ebi_endpoint = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
Q1 = '("NAB2") AND ("atopic eczema")'
Q2 = '("NAB2") AND ("Th2 cells" OR "T helper 2" OR "type 2 immunity")'
probe_A = {"endpoint": ebi_endpoint, "queries": []}
for q in [Q1, Q2]:
    r = requests.get(ebi_endpoint,
                     params={"query": q, "format": "json", "pageSize": 1},
                     timeout=60)
    r.raise_for_status()
    probe_A["queries"].append({"query_string": q, "hitCount": r.json().get("hitCount")})


# ---------- Probe B — Open Targets known gene-disease associations (GraphQL POST) ----------
ot_endpoint = "https://api.platform.opentargets.org/api/v4/graphql"
gql = ("query($id:String!,$idx:Int!,$size:Int!){ disease(efoId:$id){ id name "
       "associatedTargets(page:{index:$idx,size:$size}){ count rows{ target{ approvedSymbol } score } } } }")
resp = requests.post(ot_endpoint,
                     json={"query": gql, "variables": {"id": "MONDO_0004979", "idx": 0, "size": 25}},
                     timeout=60)
resp.raise_for_status()
d = resp.json()["data"]["disease"]
at = d["associatedTargets"]
probe_B = {
    "endpoint": ot_endpoint,
    "disease_id": d["id"],
    "disease_name": d["name"],
    "total_count": at["count"],
    "top_rows": [{"symbol": row["target"]["approvedSymbol"], "score": row["score"]}
                 for row in at["rows"][:10]],
}


# ---------- Probe C — S3 lazy read of deposited genome-wide DE matrix (anon, NO download) ----------
s3_key = "genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad"
probe_C = {"s3_key": s3_key, "opened": False, "top_level_keys": None, "obs_keys": None,
           "var_keys": None, "target_contrast_sample": None, "culture_conditions": None,
           "gene_names_head": None,
           "bytes_downloaded_note": "lazy range reads only, no full download", "error": None}

def dec(x):
    return x.decode() if isinstance(x, (bytes, bytearray)) else str(x)

try:
    import s3fs, h5py
    # virtual addressing routes requests to <bucket>.s3.amazonaws.com (the granted host),
    # NOT path-style s3.amazonaws.com/<bucket> (which is denylisted by the sandbox).
    fs = s3fs.S3FileSystem(anon=True, config_kwargs={"s3": {"addressing_style": "virtual"}})
    with fs.open(s3_key, "rb", block_size=2**20) as fo, h5py.File(fo, "r") as h:
        probe_C["opened"] = True
        probe_C["top_level_keys"] = list(h.keys())                                    # obs / var / layers etc.
        probe_C["obs_keys"] = list(h["obs"].keys())
        probe_C["var_keys"] = list(h["var"].keys())
        # read ONLY small label arrays — never a full matrix layer:
        probe_C["target_contrast_sample"] = [dec(x) for x in h["obs"]["target_contrast_gene_name"]["categories"][:8]]
        probe_C["culture_conditions"] = [dec(x) for x in h["obs"]["culture_condition"]["categories"][:]]
        probe_C["gene_names_head"] = [dec(x) for x in h["var"]["gene_name"][:8]]
except Exception as e:
    probe_C["error"] = f"{type(e).__name__}: {e}"
    traceback.print_exc()


# ---------- Probe D — list the workspace's MCP connectors ----------
# Enumerated via the skill catalog: search_skills(prefix="mcp-") lists the registered
# mcp-* connector docs; connector server name = doc name minus the "mcp-" prefix.
# Reachability confirmed live from the repl (control-plane) kernel with:
#     host.mcp("genes-ontologies", "query_genes", terms=["NAB2"], species="human")  -> returned data
# (host.mcp is only available in the repl tool, not this analysis kernel.)
probe_D = {
    "connectors": ['biomart', 'biorxiv', 'cancer-models', 'cellguide', 'chembl', 'chemistry',
                   'clinical-genomics', 'clinical-trials', 'drug-regulatory', 'expression',
                   'genes-ontologies', 'genomes', 'human-genetics', 'ketcher-chemistry',
                   'literature', 'omics-archives', 'protein-annotation', 'pubmed', 'regulation',
                   'research-resources', 'rna', 'structures-interactions', 'variants', 'zinc'],
    "notes": ("Enumerated via search_skills(prefix='mcp-'): 24 mcp-* connector skill docs registered; "
              "connector server name = doc name minus the 'mcp-' prefix. Confirmed live by a real call "
              "host.mcp('genes-ontologies','query_genes',terms=['NAB2']) which returned gene records."),
}


# ---------- assemble ----------
stage0 = {
    "run_label": "PyZoBot stage0 probe",
    "probe_A_europepmc": probe_A,
    "probe_B_opentargets": probe_B,
    "probe_C_s3": probe_C,
    "probe_D_connectors": probe_D,
    "overall": "see stage0_probe.json",
}
with open("stage0_probe/stage0_probe.json", "w") as f:
    json.dump(stage0, f, indent=2)
print(json.dumps(stage0, indent=2))
