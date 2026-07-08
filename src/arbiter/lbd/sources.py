"""External data-source clients for the LBD proposer (fresh, new-work-only).

Three keyless services cover v1:
  - Europe PMC  : literature co-mention counts (A-B, B-C, A-C-lit bridges).
  - Open Targets: the KNOWN gene-disease association set to EXCLUDE (A-C-known).
  - MyGene      : gene SYMBOL -> Ensembl id / alias normalization.

`.env` keys (NCBI/OpenAlex/Semantic Scholar) are optional fallbacks/politeness and are
loaded but not required for v1. Every call is cached via `_http`.
"""
from __future__ import annotations

from . import _http

_http.load_env()

EUROPEPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OPENTARGETS = "https://api.platform.opentargets.org/api/v4/graphql"
MYGENE = "https://mygene.info/v3/query"


# --- Europe PMC: co-mention counts ------------------------------------------------
def _phrase(term: str) -> str:
    # ALWAYS quote (incl. bare gene symbols like AAK1/IL2/JUN) so they match as tokens, not
    # substrings -- unquoted symbols produced false-positive co-mentions (Codex consult
    # 2026-07-08). Fielded gene-annotation queries are a future hardening.
    return f'"{term}"'


def europepmc_count(query: str) -> int:
    """Total hit count for a Europe PMC query string."""
    data = _http.get(EUROPEPMC, params={"query": query, "format": "json", "pageSize": 1})
    return int(data.get("hitCount", 0))


def cooccur_count(terms_a, terms_b) -> int:
    """Literature co-mention count for (any of terms_a) AND (any of terms_b).

    terms_a / terms_b may be a str or list[str]; lists are OR-ed. Used for A-B, B-C,
    and A-C-lit bridges. Phrases are quoted so multi-word terms match as phrases.
    """
    if isinstance(terms_a, str):
        terms_a = [terms_a]
    if isinstance(terms_b, str):
        terms_b = [terms_b]
    a = " OR ".join(_phrase(t) for t in terms_a)
    b = " OR ".join(_phrase(t) for t in terms_b)
    return europepmc_count(f"({a}) AND ({b})")


# --- Open Targets: the known gene->disease association set (to EXCLUDE) ------------
# associatedTargets page size is capped at 3000 (size>3000 errors). Rows are ordered by
# score DESC, so we paginate and stop once scores fall below the novelty floor -- a gene
# not in the map has effectively zero known association (the novelty signal we want).
_OT_PAGE = 3000
_ASSOC_QUERY = """query($id:String!,$idx:Int!,$size:Int!){
  disease(efoId:$id){ id name associatedTargets(page:{index:$idx,size:$size}){
    count rows{ target{ approvedSymbol } score } } } }"""


def opentargets_disease_targets(disease_id: str, score_floor: float = 0.05,
                                max_pages: int = 5) -> dict[str, float]:
    """Map approvedSymbol -> association score for a disease (disease-side, paginated).

    Use the DISEASE side: the target-side associatedDiseases(efoIds:[...]) filter returned
    empty for the known GATA3 x asthma pair (verified 2026-07-08). `disease_id` is the
    Open Targets/MONDO id from entity_maps (NOT EFO). Stops paginating once a page's lowest
    score < score_floor (rows are score-DESC) or all rows are read.
    """
    out: dict[str, float] = {}
    for idx in range(max_pages):
        data = _http.post(OPENTARGETS, json_body={
            "query": _ASSOC_QUERY,
            "variables": {"id": disease_id, "idx": idx, "size": _OT_PAGE}})
        dis = (data.get("data") or {}).get("disease")
        if not dis:
            break
        at = dis["associatedTargets"]
        rows = at["rows"]
        for r in rows:
            out[r["target"]["approvedSymbol"]] = float(r["score"])
        if len(rows) < _OT_PAGE or (rows and float(rows[-1]["score"]) < score_floor):
            break
        if (idx + 1) * _OT_PAGE >= at["count"]:
            break
    return out


def opentargets_known(gene_symbol: str, disease_targets: dict[str, float]) -> float:
    """Known-association score for a gene against a prefetched disease->targets map.

    0.0 means "no known association" (a novelty signal). Callers should prefetch each
    disease's map once via opentargets_disease_targets and reuse it across genes.
    """
    return disease_targets.get(gene_symbol, 0.0)


# --- MyGene: symbol -> Ensembl -----------------------------------------------------
def mygene_ensembl(symbol: str) -> str | None:
    """Resolve a human gene SYMBOL to its primary Ensembl gene id (or None)."""
    data = _http.get(MYGENE, params={"q": f"symbol:{symbol}", "species": "human",
                                     "fields": "ensembl.gene", "size": 1})
    hits = data.get("hits", [])
    if not hits:
        return None
    ens = hits[0].get("ensembl")
    if isinstance(ens, list):
        ens = ens[0] if ens else None
    return (ens or {}).get("gene") if isinstance(ens, dict) else None
