import sys, glob, json, time

sys.path.insert(0, "/home/dayanjan/pyzobot-cs-live/src")

CACHE = "/home/dayanjan/pyzobot-cs-live/data/lbd_cache/*.json"

n_start = len(glob.glob(CACHE))
print(f"n_start (cached responses reused) = {n_start}")

from arbiter.lbd.propose import sweep

wall0 = time.time()
results = {}
for cond in ["Stim8hr", "Rest", "Stim48hr"]:
    t0 = time.time()
    res = sweep(condition=cond, program_significant=False)     # LOOSE + LIVE
    results[cond] = res
    json.dump(res, open(f"live_fullsweep_loose/sweep_{cond}.json", "w"), indent=2)
    # CHECKPOINT immediately
    json.dump(res["ranked_clean_supported"], open(f"live_fullsweep_loose/lbd_questions_{cond}.json", "w"), indent=2)
    nc = len(glob.glob(CACHE))
    print(f"[{cond}] funnel {res['funnel']} | cache_now={nc} | {time.time()-t0:.0f}s")

# 5. Merged cross-condition view
merged = []
for cond in ["Stim8hr", "Rest", "Stim48hr"]:
    for r in results[cond]["ranked_clean_supported"]:
        row = dict(r)
        row["condition"] = cond
        merged.append(row)
merged.sort(key=lambda x: x["score"], reverse=True)
json.dump(merged[:50], open("live_fullsweep_loose/all_conditions_top.json", "w"), indent=2)

# per-condition summary
print("\n=== PER-CONDITION SUMMARY ===")
for cond in ["Stim8hr", "Rest", "Stim48hr"]:
    f = results[cond]["funnel"]
    p = results[cond]["params"]
    print(f"{cond}: a_genes={f['a_genes']} eligible_pairs={f['eligible_pairs']} "
          f"disease_c_supported_total={f['disease_c_supported_total']} "
          f"clean_supported={f['clean_supported']} ab_gate_value={p['ab_gate_value']}")

# 6. LIVENESS
n_end = len(glob.glob(CACHE))
print(f"\nLIVENESS: n_start -> n_end = {n_start} -> {n_end}")

wall = time.time() - wall0
print(f"TOTAL WALL: {wall:.0f}s")

# stash a small summary for downstream receipt building
summary = {
    "n_start": n_start, "n_end": n_end, "wall_s": wall,
    "per_condition": {c: {"funnel": results[c]["funnel"], "params": results[c]["params"]}
                       for c in results},
}
json.dump(summary, open("live_fullsweep_loose/run_summary.json", "w"), indent=2)
print("DONE")
