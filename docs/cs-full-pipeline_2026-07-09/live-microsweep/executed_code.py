#!/usr/bin/env python3
"""Live Literature-Based-Discovery (Swanson ABC) candidate-question generator.

A = KD-gated significant T-cell regulator (from perturbation data, Stim8hr).
B = Th1/Th2 polarization program (fixed keyword arms).
C = autoimmune disease (fixed menu).
Novel candidate = strong A-B and B-C literature bridges but WEAK direct A-C
literature and NO curated A-C association (classic ABC disconnected-but-bridgeable).

Everything LIVE: Europe PMC search + Open Targets GraphQL. No cache read/write.
"""
import time, json, math, statistics
import requests
import pandas as pd

DATA = "/home/dayanjan/pyzobot-data"
OUT = "live_microsweep"
SLEEP = 0.3
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OT = "https://api.platform.opentargets.org/api/v4/graphql"

# ---------- Step 1: A-universe from data ----------
T4 = pd.read_csv(f"{DATA}/guide_kd_efficiency.suppl_table.csv")
T1 = pd.read_csv(f"{DATA}/DE_stats.suppl_table.csv")
kd_genes = set(T4[(T4.culture_condition == "Stim8hr") &
                  (T4.signif_knockdown == True)].perturbed_gene_id.unique())
t1s = T1[(T1.culture_condition == "Stim8hr") &
         (T1.target_contrast.isin(kd_genes)) & (T1.n_downstream > 0)].copy()
eff = (t1s.groupby(["target_contrast", "target_contrast_gene_name"], as_index=False)
       .n_downstream.max()
       .sort_values("n_downstream", ascending=False).reset_index(drop=True))
A = eff.head(12)[["target_contrast_gene_name", "n_downstream"]]
GENES = list(A.target_contrast_gene_name)
EFFECT = dict(zip(A.target_contrast_gene_name, A.n_downstream.astype(int)))
print("A set (top 12 by n_downstream, KD-gated @Stim8hr):")
for g in GENES:
    print(f"  {g:8s} effect={EFFECT[g]}")

# ---------- Step 2: fixed B and C ----------
PROGRAM = ["Th2 cells", "T helper 2", "type 2 immunity", "Th2 differentiation",
           "Th1 cells", "T helper 1", "type 1 immunity", "Th1 differentiation",
           "Th1/Th2 polarization", "CD4 T cell polarization",
           "T helper cell differentiation"]
DISEASES = {"asthma": "MONDO_0004979", "atopic eczema": "MONDO_0004980",
            "rheumatoid arthritis": "MONDO_0008383",
            "type 1 diabetes mellitus": "MONDO_0005147"}
PROG_OR = " OR ".join(f'"{t}"' for t in PROGRAM)

# ---------- Step 3: live signal gathering ----------
def epmc_hits(query, retries=1):
    err = None
    for _ in range(retries + 1):
        try:
            r = requests.get(EPMC, params={"query": query, "format": "json",
                                           "pageSize": 1}, timeout=30)
            r.raise_for_status()
            return int(r.json().get("hitCount", 0)), None
        except Exception as e:
            err = str(e)
            time.sleep(SLEEP)
    return None, err

def ot_scores(mondo, retries=1):
    q = ("query($id:String!,$idx:Int!,$size:Int!){ disease(efoId:$id){ "
         "associatedTargets(page:{index:$idx,size:$size}){ rows{ target{ "
         "approvedSymbol } score } } } }")
    err = None
    for _ in range(retries + 1):
        try:
            r = requests.post(OT, json={"query": q, "variables": {
                "id": mondo, "idx": 0, "size": 3000}}, timeout=60)
            r.raise_for_status()
            rows = r.json()["data"]["disease"]["associatedTargets"]["rows"]
            return {row["target"]["approvedSymbol"]: row["score"] for row in rows}, len(rows), None
        except Exception as e:
            err = str(e)
            time.sleep(SLEEP)
    return None, 0, err

liveness = {}

# ab: per gene co-mention gene AND program
ab = {}
for i, g in enumerate(GENES):
    q = f'("{g}") AND ({PROG_OR})'
    h, e = epmc_hits(q)
    ab[g] = h if h is not None else 0
    if i == 0:
        liveness["first_ab_query"] = q
        liveness["first_ab_hitCount"] = h
    print(f"ab  {g:8s} {ab[g]}" + (f"  ERR:{e}" if e else ""))
    time.sleep(SLEEP)

# bc: per disease co-mention program AND disease name
bc = {}
for i, (dname, mondo) in enumerate(DISEASES.items()):
    q = f'({PROG_OR}) AND ("{dname}")'
    h, e = epmc_hits(q)
    bc[dname] = h if h is not None else 0
    if i == 0:
        liveness["first_bc_query"] = q
        liveness["first_bc_hitCount"] = h
    print(f"bc  {dname:26s} {bc[dname]}" + (f"  ERR:{e}" if e else ""))
    time.sleep(SLEEP)

# ac_lit: per gene x disease co-mention gene AND disease name
ac_lit = {}
first_ac = True
for g in GENES:
    for dname in DISEASES:
        q = f'("{g}") AND ("{dname}")'
        h, e = epmc_hits(q)
        ac_lit[(g, dname)] = h if h is not None else 0
        if first_ac:
            liveness["first_ac_lit_query"] = q
            liveness["first_ac_lit_hitCount"] = h
            first_ac = False
        time.sleep(SLEEP)
print("ac_lit gathered:", len(ac_lit), "pairs")

# ac_known: Open Targets curated association score per gene x disease
ot_by_disease = {}
first_ot = True
for dname, mondo in DISEASES.items():
    sc, nrows, e = ot_scores(mondo)
    ot_by_disease[dname] = sc if sc is not None else {}
    if first_ot:
        liveness["opentargets_disease_id"] = mondo
        liveness["opentargets_rows"] = nrows
        first_ot = False
    print(f"OT  {dname:26s} rows={nrows}" + (f"  ERR:{e}" if e else ""))
    time.sleep(SLEEP)
ac_known = {(g, d): ot_by_disease[d].get(g, 0.0) for g in GENES for d in DISEASES}

# ---------- Step 4: gate + novelty score ----------
def zmap(values_dict):
    keys = list(values_dict)
    logs = [math.log1p(values_dict[k]) for k in keys]
    m = statistics.mean(logs)
    sd = statistics.pstdev(logs)
    if sd == 0:
        return {k: 0.0 for k in keys}
    return {k: (math.log1p(values_dict[k]) - m) / sd for k in keys}

z_ab = zmap(ab)
z_bc = zmap(bc)
z_eff = zmap(EFFECT)
ab_median = statistics.median([ab[g] for g in GENES])

records = []
for g in GENES:
    for d in DISEASES:
        _ab, _bc, _al, _ak, _ef = ab[g], bc[d], ac_lit[(g, d)], ac_known[(g, d)], EFFECT[g]
        eligible = (_ab >= ab_median) and (_bc >= 3) and (_ak <= 0.1)
        score = (min(z_ab[g], z_bc[d]) + z_eff[g]
                 - math.log1p(_al) - 3 * _ak)
        records.append({"a_gene": g, "c_disease": d, "ab": _ab, "bc": _bc,
                        "ac_lit": _al, "ac_known": round(_ak, 4),
                        "effect": _ef, "score": round(score, 4),
                        "eligible": bool(eligible)})

ranked = sorted([r for r in records if r["eligible"]],
                key=lambda r: r["score"], reverse=True)
all_ranked = sorted(records, key=lambda r: (r["eligible"], r["score"]), reverse=True)
n_eligible = len(ranked)

# ---------- Step 5: save ----------
out = {"genes": GENES, "diseases": list(DISEASES),
       "liveness": liveness, "ranked_questions": ranked,
       "n_eligible": n_eligible}
with open(f"{OUT}/microsweep.json", "w") as f:
    json.dump(out, f, indent=2)

def md_table(rows, n=None):
    rows = rows[:n] if n else rows
    h = "| rank | A gene | C disease | ab | bc | ac_lit | ac_known | effect | score |\n"
    h += "|---|---|---|---|---|---|---|---|---|\n"
    for i, r in enumerate(rows, 1):
        h += (f"| {i} | {r['a_gene']} | {r['c_disease']} | {r['ab']} | {r['bc']} "
              f"| {r['ac_lit']} | {r['ac_known']} | {r['effect']} | {r['score']} |\n")
    return h

L = liveness
receipt = f"""# Live LBD micro-sweep — generated candidate questions

**These are GENERATED CANDIDATE QUESTIONS to be refereed next — NOT findings.**
Each is of the form: *"Does gene A regulate the Th1/Th2 program (B) and thereby
link to autoimmune disease C?"* surfaced by the Swanson ABC "disconnected but
bridgeable" heuristic. All signals below come from LIVE HTTP calls made this run
(Europe PMC + Open Targets); nothing is cached.

## Top ranked candidate questions (eligible pairs)
{md_table(ranked, 10)}
_ab_ = gene×program co-mentions; _bc_ = program×disease co-mentions;
_ac_lit_ = direct gene×disease co-mentions (low = under-explored);
_ac_known_ = Open Targets curated association score (0 = no curated link);
_effect_ = n_downstream from perturbation data.

## Liveness proof (exact query strings + returned counts this run)
- **first ab query**: `{L.get('first_ab_query')}` → hitCount = **{L.get('first_ab_hitCount')}**
- **first bc query**: `{L.get('first_bc_query')}` → hitCount = **{L.get('first_bc_hitCount')}**
- **first ac_lit query**: `{L.get('first_ac_lit_query')}` → hitCount = **{L.get('first_ac_lit_hitCount')}**
- **Open Targets disease**: `{L.get('opentargets_disease_id')}` → rows returned = **{L.get('opentargets_rows')}**

## Method (as executed)
- A = top 12 KD-gated (signif_knockdown @Stim8hr) regulators by n_downstream effect.
- Gate (eligible): ab ≥ median(ab over 12 genes) AND bc ≥ 3 AND ac_known ≤ 0.1.
- Score = min(z(ab), z(bc)) + z(effect) − log1p(ac_lit) − 3·ac_known.
- z(x) = (log1p(x) − mean(log1p)) / std(log1p), guarded to 0 when std==0.
- n_eligible = {n_eligible} of {len(records)} gene×disease pairs.

**Calibrated summary:** {n_eligible} under-explored A→(Th1/Th2)→disease pairs were *generated* as candidate questions (strong data effect + literature-bridged, no curated direct link); they are candidates for referee review, not discoveries.
"""
with open(f"{OUT}/receipt.md", "w") as f:
    f.write(receipt)

# ---------- stdout summary ----------
print("\n=== TOP 5 RANKED CANDIDATE QUESTIONS ===")
for i, r in enumerate(ranked[:5], 1):
    print(f"{i}. A={r['a_gene']} -> Th1/Th2 -> C={r['c_disease']} | "
          f"score={r['score']} ab={r['ab']} bc={r['bc']} "
          f"ac_lit={r['ac_lit']} ac_known={r['ac_known']} effect={r['effect']}")
print(f"\nn_eligible={n_eligible} / {len(records)} pairs")
print("\n=== LIVENESS BLOCK ===")
print(json.dumps(liveness, indent=2))
