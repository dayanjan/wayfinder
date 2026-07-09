# PyZoBot Stage-0 Probe — Receipt

One line per probe: request -> outcome.

## Probe A — Europe PMC literature co-mention (HTTP GET)
- Endpoint: `https://www.ebi.ac.uk/europepmc/webservices/rest/search` (params: format=json, pageSize=1)
- GET query=`("NAB2") AND ("atopic eczema")` -> hitCount = **6**
- GET query=`("NAB2") AND ("Th2 cells" OR "T helper 2" OR "type 2 immunity")` -> hitCount = **31**

## Probe B — Open Targets associated targets (GraphQL POST)
- Endpoint: `https://api.platform.opentargets.org/api/v4/graphql`
- POST efoId=`MONDO_0004979` (asthma), page size 25 -> total_count = **7403**
- top rows (score-DESC): FLG(0.745), IL4R(0.744), ADORA1(0.723), ... (10 returned)

## Probe C — S3 anonymous lazy HDF5 read (NO download)
- S3 key: `genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad`
- Open (anon, virtual addressing, range reads) -> opened = **True**, error = None
- top-level keys: ['X', 'layers', 'obs', 'obsm', 'obsp', 'uns', 'var', 'varm', 'varp']
- obs perturbation labels (first 8): ['A1BG', 'A2M', 'AAAS', 'AACS', 'AAGAB', 'AAK1', 'AAMDC', 'AAR2']
- culture conditions: ['Rest', 'Stim8hr', 'Stim48hr']
- var gene_name head: ['DPM1', 'SCYL3', 'C1orf112', 'CFH', 'FUCA2', 'GCLC', 'STPG1', 'NIPAL3']
- lazy range reads only, no full download
- NOTE: initial attempt hit proxy 403 (path-style s3.amazonaws.com is denylisted); resolved by granting the bucket-qualified host `genome-scale-tcell-perturb-seq.s3.amazonaws.com` + s3fs virtual addressing_style.

## Probe D — MCP connectors
- Enumerated 24 connectors: biomart, biorxiv, cancer-models, cellguide, chembl, chemistry, clinical-genomics, clinical-trials, drug-regulatory, expression, genes-ontologies, genomes, human-genetics, ketcher-chemistry, literature, omics-archives, protein-annotation, pubmed, regulation, research-resources, rna, structures-interactions, variants, zinc
- Enumerated via search_skills(prefix='mcp-'): 24 mcp-* connector skill docs are registered; connector server name = doc name minus the 'mcp-' prefix. Confirmed live by a real call host.mcp('genes-ontologies','query_genes',terms=['NAB2']) -> reachable=True.

## Overall
All four paths succeeded: A (Europe PMC HTTP GET) and B (Open Targets GraphQL POST) worked directly; C (anonymous lazy S3 HDF5 range-read) required installing s3fs/h5py AND a network grant for the bucket-qualified host genome-scale-tcell-perturb-seq.s3.amazonaws.com plus virtual addressing_style, then opened and read tiny label arrays with no full download; D enumerated 24 live MCP connectors. C was ultimately a success (initial proxy 403 was resolved by the granted bucket-qualified endpoint — no genuine network blocker remains).