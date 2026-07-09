# Timing calibration probe — Europe PMC + Open Targets live latency.
# Faithful record of the executed probe. All calls LIVE, no cache, CPU-only.
# Records net time (requests duration ONLY) + status + 429/error/exception flags;
# 0.34s politeness sleep AFTER each call (not counted in net time); one retry on failure.
import time, json, statistics, requests
from collections import Counter

# --- gene slice (built upstream): top-50 Stim8hr genes by n_downstream ---
genes = ['TADA2B','CD3E','LAT','SENP5','PLCG1','ZAP70','CD3D','LCP2','CD3G','VAV1',
         'TAF6L','SUPT7L','CD247','ELOF1','ZBED3','MED12','SGF29','SUPT20H','MED19','BRD8',
         'BCAT2','TADA1','DENR','ATAD5','BCL10','UBXN1','ITK','TAF13','SMARCE1','ATP2A2',
         'ELOB','PGGT1B','LRBA','CREBBP','TAF11','NFRKB','UBE2L3','MED24','ATF7IP2','DNTTIP1',
         'DOLPP1','SMG1','LEO1','ARNT','FITM2','TMED9','EIF1AX','CARMIL2','EIF4G2','SLC3A2']

PROGRAM = ["Th2 cells","T helper 2","type 2 immunity","Th2 differentiation",
           "Th1 cells","T helper 1","type 1 immunity","Th1 differentiation",
           "Th1/Th2 polarization","CD4 T cell polarization","T helper cell differentiation"]
prog_or = " OR ".join(f'"{p}"' for p in PROGRAM)

DISEASES = ["asthma","atopic eczema","rheumatoid arthritis","type 1 diabetes mellitus",
            "Crohn's disease","ulcerative colitis","systemic lupus erythematosus","psoriasis",
            "multiple sclerosis","celiac disease","ankylosing spondylitis","Hashimoto's thyroiditis"]
MONDO = ["MONDO_0004979","MONDO_0004980","MONDO_0008383","MONDO_0005147","MONDO_0005011",
         "MONDO_0005101","MONDO_0007915","MONDO_0005083","MONDO_0005301","MONDO_0005130",
         "MONDO_0005306","MONDO_0007699"]

EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
OT = "https://api.platform.opentargets.org/api/v4/graphql"
OT_QUERY = "query($id:String!,$idx:Int!,$size:Int!){ disease(efoId:$id){ associatedTargets(page:{index:$idx,size:$size}){ count rows{ target{ approvedSymbol } score } } } }"
SLEEP = 0.34

records = []

def epmc_call(call_type, query, meta):
    rec = {"call_type": call_type, "meta": meta, "retried": False}
    for attempt in (1, 2):
        try:
            t0 = time.perf_counter()
            r = requests.get(EPMC, params={"query": query, "format": "json", "pageSize": 1}, timeout=30)
            dt = time.perf_counter() - t0
            rec["net_s"] = dt; rec["status"] = r.status_code
            rec["is_429"] = (r.status_code == 429)
            rec["error"] = (r.status_code != 200); rec["exception"] = False
            if r.status_code == 200:
                rec["hitCount"] = r.json().get("hitCount")
            if r.status_code == 200 or attempt == 2:
                break
        except Exception as e:
            dt = time.perf_counter() - t0 if 't0' in dir() else None
            rec["net_s"] = dt; rec["status"] = None; rec["is_429"] = False
            rec["error"] = True; rec["exception"] = True; rec["exc"] = str(e)[:200]
            if attempt == 2: break
        rec["retried"] = True
        time.sleep(SLEEP)
    records.append(rec); time.sleep(SLEEP); return rec

def ot_call(mondo):
    efo = mondo  # Open Targets accepts MONDO efoId form
    rec = {"call_type": "ot", "meta": mondo, "retried": False}
    for attempt in (1, 2):
        try:
            t0 = time.perf_counter()
            r = requests.post(OT, json={"query": OT_QUERY, "variables": {"id": efo, "idx": 0, "size": 3000}}, timeout=30)
            dt = time.perf_counter() - t0
            rec["net_s"] = dt; rec["status"] = r.status_code
            rec["is_429"] = (r.status_code == 429)
            rec["error"] = (r.status_code != 200); rec["exception"] = False
            if r.status_code == 200:
                d = r.json().get("data", {}).get("disease")
                rec["count"] = d["associatedTargets"]["count"] if d else None
            if r.status_code == 200 or attempt == 2:
                break
        except Exception as e:
            rec["net_s"] = None; rec["status"] = None; rec["is_429"] = False
            rec["error"] = True; rec["exception"] = True; rec["exc"] = str(e)[:200]
            if attempt == 2: break
        rec["retried"] = True
        time.sleep(SLEEP)
    records.append(rec); time.sleep(SLEEP); return rec

probe_t0 = time.perf_counter()
for g in genes:                                   # ab: 50 gene calls
    epmc_call("ab", f'("{g}") AND ({prog_or})', g)
for d in DISEASES:                                # bc: 12 disease calls
    epmc_call("bc", f'({prog_or}) AND ("{d}")', d)
for m in MONDO:                                   # ot: 12 disease->target calls
    ot_call(m)
probe_wall = time.perf_counter() - probe_t0

# --- stats + extrapolation ---
def pct(vals, p):
    vals = sorted(vals); k = (len(vals)-1)*p; f = int(k); c = min(f+1, len(vals)-1)
    return vals[f] + (vals[c]-vals[f])*(k-f)

def summarize(recs):
    nets = [r["net_s"] for r in recs if r.get("net_s") is not None]
    return {"n_calls": len(recs), "mean_net_s": round(statistics.mean(nets),4),
            "median_net_s": round(statistics.median(nets),4), "p95_net_s": round(pct(nets,0.95),4),
            "min_net_s": round(min(nets),4), "max_net_s": round(max(nets),4)}

by_type = {t: summarize([r for r in records if r["call_type"]==t]) for t in ("ab","bc","ot")}
overall = summarize(records)
per_call_wall = probe_wall / len(records)
all_nets = [r["net_s"] for r in records if r.get("net_s")]
med_all = statistics.median(all_nets); p95_all = pct(all_nets, 0.95)
soft_throttle = p95_all > 3*med_all
throttled = any(r["is_429"] for r in records) or any(r.get("exception") for r in records) or soft_throttle
verdict = "THROTTLED" if throttled else "THROTTLE_FREE"
FULL = 4020                                        # 3935 ab + 12 bc + 43 ac_lit + 30 OT
est_a_min = FULL * per_call_wall / 60.0                          # (a) wall-based
est_b_min = FULL * (overall["median_net_s"] + SLEEP) / 60.0      # (b) overall median_net + sleep
est_b_ab_min = FULL * (by_type["ab"]["median_net_s"] + SLEEP) / 60.0  # (b') ab-median + sleep (ab-dominant)
print(by_type, overall, per_call_wall, verdict, est_a_min, est_b_min, est_b_ab_min)
