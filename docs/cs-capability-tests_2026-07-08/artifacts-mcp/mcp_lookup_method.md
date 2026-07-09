# MCP Lookup Method — Gene ID Resolution

## Which MCP / database was used
- **MCP server:** `genes-ontologies` (Claude Science connector)
- **Tool:** `query_genes`
- **Underlying database:** **mygene.info** (MyGene.info gene query service), which
  federates NCBI Gene and Ensembl. Returned identifiers are **Ensembl stable gene
  IDs** (`ENSG...`), cross-checked with NCBI Entrez IDs in the same record.
- **Species filter:** human (NCBI taxid 9606).

All identifiers come from real MCP tool-call responses. None were fabricated.

## Was the lookup looped / programmatic?
Yes. A **single batched, programmatic** call resolved all five symbols at once
(`query_genes` accepts a list of terms, batched up to 1000/request) — preferred
over five separate manual lookups. A `for` loop then mapped each input symbol to
its record to assemble the output rows.

```python
genes = ["NAB2", "STAT6", "IL2", "EGR2", "SATB1"]

# one batched MCP call (run in the repl tool)
resp = host.mcp("genes-ontologies", "query_genes",
                terms=genes, scopes="symbol",
                fields="symbol,name,taxid,entrezgene,ensembl.gene",
                species="human")

records = {r["query"]: r for r in resp["records"]}
for sym in genes:                       # the loop
    r = records[sym]
    stable_id = r["ensembl"]["gene"]    # ENSG... stable ID
```

The MCP response reported `n_input=5, n_records=5, not_found=[]` — every symbol
resolved.

## Results

| input_symbol | canonical_symbol | Ensembl stable ID | Entrez ID | status |
|---|---|---|---|---|
| NAB2  | NAB2  | ENSG00000166886 | 4665 | success |
| STAT6 | STAT6 | ENSG00000166888 | 6778 | success |
| IL2   | IL2   | ENSG00000109471 | 3558 | success |
| EGR2  | EGR2  | ENSG00000122877 | 1959 | success |
| SATB1 | SATB1 | ENSG00000182568 | 6304 | success |

See `gene_id_lookup.csv` for the machine-readable output and
`executed_lookup_code.py` for the exact executed code.
