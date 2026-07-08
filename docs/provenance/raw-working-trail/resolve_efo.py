"""Deterministic disease -> EFO/MONDO resolver. Authoritative sources:
   1. Open Targets Platform GraphQL search (the exact id the A-C exclusion step will query).
   2. EBI OLS4 (canonical EFO label cross-check).
No API key needed for either. Mirrors the LightsOut-R01 tools/*.py house style.
"""
import json, requests, sys

OT = "https://api.platform.opentargets.org/api/v4/graphql"
OLS = "https://www.ebi.ac.uk/ols4/api/search"

DISEASES = [
    "asthma", "Crohn's disease", "ulcerative colitis", "rheumatoid arthritis",
    "systemic lupus erythematosus", "psoriasis", "multiple sclerosis",
    "type 1 diabetes mellitus", "celiac disease", "ankylosing spondylitis",
    "atopic eczema", "Hashimoto's thyroiditis",
    # umbrella / context-only
    "autoimmune disease", "inflammatory bowel disease",
]

MY_DRAFT = {
    "asthma": "EFO_0000270", "Crohn's disease": "EFO_0000384",
    "ulcerative colitis": "EFO_0000729", "rheumatoid arthritis": "EFO_0000685",
    "systemic lupus erythematosus": "EFO_0002690", "psoriasis": "EFO_0000676",
    "multiple sclerosis": "EFO_0003885", "type 1 diabetes mellitus": "EFO_0001359",
    "celiac disease": "EFO_0001060", "ankylosing spondylitis": "EFO_0003898",
    "atopic eczema": "EFO_0000274", "Hashimoto's thyroiditis": "EFO_1001459",
    "autoimmune disease": "EFO_0005140", "inflammatory bowel disease": "EFO_0003767",
}

OT_QUERY = """query($q:String!){ search(queryString:$q, entityNames:["disease"], page:{index:0,size:1}){ hits{ id name } } }"""

def ot_search(name):
    try:
        r = requests.post(OT, json={"query": OT_QUERY, "variables": {"q": name}}, timeout=30)
        hits = r.json().get("data", {}).get("search", {}).get("hits", [])
        return (hits[0]["id"], hits[0]["name"]) if hits else (None, None)
    except Exception as e:
        return ("ERR", str(e)[:60])

def ols_search(name):
    try:
        r = requests.get(OLS, params={"q": name, "ontology": "efo,mondo", "type": "class",
                                      "exact": "false", "rows": 1}, timeout=30)
        docs = r.json().get("response", {}).get("docs", [])
        if not docs:
            return (None, None)
        d = docs[0]
        return (d.get("obo_id") or d.get("short_form"), d.get("label"))
    except Exception as e:
        return ("ERR", str(e)[:60])

rows = []
for d in DISEASES:
    ot_id, ot_name = ot_search(d)
    ols_id, ols_label = ols_search(d)
    draft = MY_DRAFT[d]
    ot_norm = (ot_id or "").replace("_", ":") if ot_id and ot_id != "ERR" else ot_id
    draft_norm = draft.replace("_", ":")
    match = "OK" if ot_norm == draft_norm else "DIFF"
    rows.append((d, draft, ot_id, ot_name, ols_id, ols_label, match))

print(f"{'disease':32} {'my_draft':13} {'opentargets_id':14} {'ot_name':30} {'ols_id':14} {'match':5}")
print("-" * 130)
for d, draft, ot_id, ot_name, ols_id, ols_label, match in rows:
    print(f"{d:32} {draft:13} {str(ot_id):14} {str(ot_name)[:30]:30} {str(ols_id):14} {match:5}")

out = [{"disease": d, "my_draft": draft, "opentargets_id": ot_id, "opentargets_name": ot_name,
        "ols_id": ols_id, "ols_label": ols_label, "match": match}
       for d, draft, ot_id, ot_name, ols_id, ols_label, match in rows]
json.dump(out, open(".claude/scratch/lbd-debate/efo_resolution.json", "w"), indent=2)
print("\nwrote efo_resolution.json")
