"""
Claude Science MCP capability audit — canonical human gene ID lookup.

This file reproduces the ACTUAL executed code, verbatim across the two cells
that ran. MCP calls run only inside the Claude Science `repl` tool
(control-plane kernel); it shares the workspace filesystem but NOT memory with
the `python` tool, so the MCP response was passed between them via a handoff
JSON file. Cell 1 (repl) made ONE batched query_genes call and wrote the raw
response; cell 2 (python) loaded that file and looped to assemble the rows.
"""

# ============================================================================
# CELL 1 — repl tool (control-plane kernel; the only place host.mcp works)
# ============================================================================
import json, os

genes = ["NAB2", "STAT6", "IL2", "EGR2", "SATB1"]

# ONE programmatic/batched call to mygene.info via the genes-ontologies MCP.
# query_genes accepts a list of terms (batched up to 1000/request).
resp = host.mcp("genes-ontologies", "query_genes",
                terms=genes,
                scopes="symbol",
                fields="symbol,name,taxid,entrezgene,ensembl.gene",
                species="human")

os.makedirs("handoff", exist_ok=True)
json.dump({"genes": genes, "resp": resp}, open("handoff/mygene.json", "w"), indent=2)
print(json.dumps(resp, indent=2)[:3000])

# ============================================================================
# CELL 2 — python tool (reads the handoff file; builds the CSV)
# ============================================================================
import json, csv

d = json.load(open("handoff/mygene.json"))
genes = d["genes"]
records = {r["query"]: r for r in d["resp"]["records"]}
not_found = set(d["resp"]["not_found"])

rows = []
for sym in genes:                                  # <-- the loop
    r = records.get(sym)
    if r and r.get("ensembl", {}).get("gene"):
        rows.append({
            "input_symbol": sym,
            "canonical_symbol": r.get("symbol", ""),
            "database_used": "mygene.info (genes-ontologies MCP: query_genes)",
            "stable_id_or_accession": r["ensembl"]["gene"],  # Ensembl stable gene ID
            "species": "Homo sapiens (taxid 9606)",
            "lookup_status": "success",
        })
    else:
        rows.append({
            "input_symbol": sym, "canonical_symbol": "",
            "database_used": "mygene.info (genes-ontologies MCP: query_genes)",
            "stable_id_or_accession": "", "species": "Homo sapiens (taxid 9606)",
            "lookup_status": "not_found" if sym in not_found else "no_ensembl_id",
        })

cols = ["input_symbol", "canonical_symbol", "database_used",
        "stable_id_or_accession", "species", "lookup_status"]
with open("cs_capability_audit_mcp/gene_id_lookup.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
