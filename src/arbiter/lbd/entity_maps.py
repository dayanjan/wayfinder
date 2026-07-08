"""Pinned entity maps for the LBD question-proposer (v2 spec, hand-pinned step).

The one non-mechanical step in `docs/lbd-proposer-spec.md`. Disease IDs were resolved
AUTHORITATIVELY on 2026-07-08 against the Open Targets Platform search API (the exact
service the A-C "known association" exclusion queries) and cross-checked with EBI OLS4 --
NOT from memory. All 14 disease names matched exactly; every canonical ID is a **MONDO**
ID (Open Targets' current disease-ontology id system), not EFO. Resolver + raw results:
`.claude/scratch/lbd-debate/resolve_efo.py` / `efo_resolution.json`.

Verified usable: `disease(efoId:"MONDO_0004979")` (asthma) is accepted by the association
query and returns 7403 associated targets with scores (FLG/IL4R/IL33/TSLP ~0.72-0.74).
NOTE for the client build: pull associations from the DISEASE side
(`disease(id).associatedTargets`); the target-side `associatedDiseases(efoIds:[...])`
filter returned empty for the known GATA3 x asthma pair.
"""

# --- C entities: the 14 non-negative-control diseases from
#     data/cluster_autoimmune_enrichment_results.suppl_table.csv ---
# Each maps to its Open Targets/MONDO id. `eligible=True` => a valid specific-disease C
# claim; `eligible=False` => umbrella term, used only for B-C sanity context (F-006).
DISEASES = {
    # eligible specific diseases (12)
    "asthma":                        {"id": "MONDO_0004979", "eligible": True},
    "Crohn's disease":               {"id": "MONDO_0005011", "eligible": True},
    "ulcerative colitis":            {"id": "MONDO_0005101", "eligible": True},
    "rheumatoid arthritis":          {"id": "MONDO_0008383", "eligible": True},
    "systemic lupus erythematosus":  {"id": "MONDO_0007915", "eligible": True},
    "psoriasis":                     {"id": "MONDO_0005083", "eligible": True},
    "multiple sclerosis":            {"id": "MONDO_0005301", "eligible": True},
    "type 1 diabetes mellitus":      {"id": "MONDO_0005147", "eligible": True},
    "celiac disease":                {"id": "MONDO_0005130", "eligible": True},
    "ankylosing spondylitis":        {"id": "MONDO_0005306", "eligible": True},
    "atopic eczema":                 {"id": "MONDO_0004980", "eligible": True},
    "Hashimoto's thyroiditis":       {"id": "MONDO_0007699", "eligible": True},
    # umbrella / context-only (2) -- NOT eligible as specific-disease C claims
    "autoimmune disease":            {"id": "MONDO_0007179", "eligible": False},
    "inflammatory bowel disease":    {"id": "MONDO_0005265", "eligible": False},
}

ELIGIBLE_DISEASES = [d for d, m in DISEASES.items() if m["eligible"]]
UMBRELLA_DISEASES = [d for d, m in DISEASES.items() if not m["eligible"]]

# True negative-control diseases in the same CSV -- use to sanity-check that the B-C
# co-mention signal is not spurious (a real Th1/Th2 program should NOT co-mention these).
NEGATIVE_CONTROL_DISEASES = [
    "age-related macular degeneration", "chronic kidney disease", "coronary artery disease",
]

# --- B entity: the single program the substrate supports (Th1/Th2 polarization only; F-003) ---
# Keyword arms for literature co-mention. AB_TERMS (gene<->program) intentionally OMITS the
# marker genes so a gene's program link is not inflated by mere proximity to a canonical
# marker; BC_TERMS (program<->disease) KEEPS markers because disease literature legitimately
# cites them. (Default per round-3 recommendation; adjust `PROGRAM["ab_use_markers"]` to flip.)
PROGRAM = {
    "name": "Th1_Th2_polarization",
    "th2_process": ["Th2 cells", "T helper 2", "type 2 immunity", "Th2 differentiation"],
    "th1_process": ["Th1 cells", "T helper 1", "type 1 immunity", "Th1 differentiation"],
    "umbrella":    ["Th1/Th2 polarization", "CD4 T cell polarization",
                    "T helper cell differentiation"],
    "th2_markers": ["GATA3", "IL-4", "IL-13"],
    "th1_markers": ["T-bet", "IFN-gamma", "interferon gamma"],
    "ab_use_markers": False,   # gene<->program: process terms only (stricter bridge)
}

def program_terms(for_link: str) -> list[str]:
    """Keyword set for a co-mention link. for_link in {"AB","BC"}."""
    base = PROGRAM["th2_process"] + PROGRAM["th1_process"] + PROGRAM["umbrella"]
    markers = PROGRAM["th2_markers"] + PROGRAM["th1_markers"]
    if for_link == "BC":
        return base + markers
    if for_link == "AB":
        return base + (markers if PROGRAM["ab_use_markers"] else [])
    raise ValueError(f"for_link must be AB or BC, got {for_link!r}")
