"""Stage 1 — native port with receipt verification of the LBD proposer sweep.

We import and run the REAL pipeline code unchanged, replaying it entirely from
the staged HTTP receipt cache, and assert the output reproduces the exact known
acceptance targets. No pipeline logic and no statistics are modified here.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 0. Wire up the staged repo tree.
# ---------------------------------------------------------------------------
REPO = "/home/dayanjan/pyzobot-cs-stage1"
sys.path.insert(0, REPO + "/src")
ORIG_CACHE = Path(REPO) / "data" / "lbd_cache"
ART = Path(__file__).resolve().parent   # this script's own dir (stage1_lbd_artifacts/)
ART.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 0b. The staged repo is mounted READ-ONLY, so the guard-free smoke cannot
#     write the occasional live-miss receipt back into data/lbd_cache. Point
#     the HTTP layer's cache dir at a WRITABLE mirror that symlinks to all
#     original receipts (byte-identical) so reads still replay and a rare miss
#     can be persisted. No pipeline logic or statistics change — only the cache
#     directory location. The pure-replay proof (delta==0 under the no-live
#     guard) is enforced against THIS mirror below.
# ---------------------------------------------------------------------------
import arbiter.lbd._http as H

MIRROR = Path("_lbd_cache_mirror").resolve()
MIRROR.mkdir(parents=True, exist_ok=True)
for src in ORIG_CACHE.glob("*.json"):
    link = MIRROR / src.name
    if not link.exists():
        link.symlink_to(src)
H.CACHE_DIR = MIRROR              # cached_request/_cache_key read this at call time
CACHE_GLOB = str(MIRROR / "*.json")

# ---------------------------------------------------------------------------
# 1./2. PLUMBING SMOKE (GUARD-FREE) — proves import + cache + referee + paths
#       wire up. May make a few harmless live calls if a sampled pair was not
#       in the original cache. This is NOT the funnel.
# ---------------------------------------------------------------------------
from arbiter.lbd.cooccur import preflight_sample
from arbiter.lbd.referee_triple import referee_triple, load_referee_data

print("=== PLUMBING ONLY — not the funnel ===")
sm = preflight_sample(n_genes=15, condition="Stim8hr", extra_genes=["NAB2"])
data = load_referee_data()
rt = referee_triple("NAB2", "atopic eczema", "Stim8hr", data)
print("PLUMBING preflight n_eligible_survivors:", sm["n_eligible_survivors"])
print("PLUMBING referee_triple NAB2/atopic eczema answer:", rt["answer"], "(expect 'supported')")

# ---------------------------------------------------------------------------
# 3. PURE-REPLAY GUARD — snapshot cache, then make ANY live HTTP call during the
#    sweep raise. Every sweep response MUST come from data/lbd_cache.
# ---------------------------------------------------------------------------
n0 = len(glob.glob(CACHE_GLOB))
import arbiter.lbd._http as H


def _no_live(*a, **k):
    raise RuntimeError(
        f"LIVE HTTP ATTEMPTED during sweep (cache miss) -> "
        f"{a[:2]} {k.get('params') or k.get('json')}"
    )


H.requests.request = _no_live  # every sweep response must come from cache

# ---------------------------------------------------------------------------
# 4. THE REAL PROOF — full sweep, entirely from cache under the guard.
# ---------------------------------------------------------------------------
from arbiter.lbd.propose import sweep

res = sweep(condition="Stim8hr")
n1 = len(glob.glob(CACHE_GLOB))
assert n1 == n0, f"sweep wrote {n1 - n0} new cache files — NOT a pure replay"
print(f"=== PURE REPLAY confirmed: cache files before={n0} after={n1} (delta=0) ===")

# ---------------------------------------------------------------------------
# 5. ACCEPTANCE CHECKS — assert every target; a mismatch is a FAIL to report.
# ---------------------------------------------------------------------------
funnel = res["funnel"]
params = res["params"]

# locate the NAB2 -> atopic eczema row (1-based rank in ranked_supported)
nab2_row = None
nab2_rank = None
for i, r in enumerate(res["ranked_supported"], 1):
    if r["a_gene"] == "NAB2" and r["c_disease"] == "atopic eczema":
        nab2_row = r
        nab2_rank = i
        break

checks = []  # (name, expected, actual)


def chk(name, expected, actual):
    checks.append((name, expected, actual, expected == actual))


chk("funnel.a_genes", 3935, funnel["a_genes"])
chk("funnel.eligible_pairs", 22039, funnel["eligible_pairs"])
chk("funnel.disease_c_supported_total", 43, funnel["disease_c_supported_total"])
chk("funnel.clean_supported", 30, funnel["clean_supported"])
chk("funnel.pure_disjoint_clean", 1, funnel["pure_disjoint_clean"])
chk("funnel.chain_classes", {"refuted_for_c": 21995, "supported": 30,
                             "supported_weak": 10, "supported_flagged": 3,
                             "refuted_effect": 1}, funnel["chain_classes"])
chk("params.ab_gate_value", 26, params["ab_gate_value"])

# pure-replay guard result
chk("pure_replay_cache_delta", 0, n1 - n0)

# NAB2 row
if nab2_row is None:
    chk("NAB2 row present", True, False)
else:
    chk("NAB2 rank (1-based)", 4, nab2_rank)
    chk("NAB2 ab", 66, nab2_row["ab"])
    chk("NAB2 bc", 2184, nab2_row["bc"])
    chk("NAB2 ac_lit", 6, nab2_row["ac_lit"])
    chk("NAB2 ac_known", 0.0376, nab2_row["ac_known"])
    chk("NAB2 effect", 301, nab2_row["effect"])
    chk("NAB2 referee_answer", "supported", nab2_row["referee_answer"])
    chk("NAB2 score (3dp)", -1.137, round(nab2_row["score"], 3))

ALL_PASS = all(ok for _, _, _, ok in checks)

# ---------------------------------------------------------------------------
# 6. Save artifacts.
# ---------------------------------------------------------------------------
(ART / "sweep_Stim8hr.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
(ART / "lbd_questions_Stim8hr.json").write_text(
    json.dumps(res["ranked_clean_supported"], indent=2), encoding="utf-8")

# receipt.md
lines = []
lines.append("# Stage 1 — LBD Proposer Sweep: Receipt Verification\n")
lines.append("Native port with receipt verification. The real pipeline code "
             "(`arbiter.lbd.propose.sweep`) was imported and run **unchanged**, "
             "replaying entirely from the staged HTTP receipt cache "
             "(`data/lbd_cache/`). No pipeline logic and no statistics were "
             "modified. The numbers below were **reproduced / re-derived** by "
             "executing that code, not discovered.\n")
lines.append(f"**ALL_PASS = {ALL_PASS}**\n")

lines.append("## Pure-replay guard\n")
lines.append(f"- Cache files before sweep: {n0}")
lines.append(f"- Cache files after sweep:  {n1}")
lines.append(f"- Delta: {n1 - n0} (0 == every sweep response came from cache; "
             "the HTTP layer was monkeypatched to raise on any live call)\n")

lines.append("## Funnel (as produced by the code)\n")
lines.append("```json")
lines.append(json.dumps(funnel, indent=2))
lines.append("```\n")
lines.append(f"- ab_gate_value (params): {params['ab_gate_value']}\n")

lines.append("## NAB2 → atopic eczema row (from res['ranked_supported'])\n")
if nab2_row is not None:
    lines.append(f"- Rank (1-based): {nab2_rank}")
    lines.append("```json")
    lines.append(json.dumps(nab2_row, indent=2))
    lines.append("```\n")
else:
    lines.append("- **NOT FOUND** in ranked_supported\n")

lines.append("## Acceptance checks (expected vs actual)\n")
lines.append("| check | expected | actual | pass |")
lines.append("|---|---|---|---|")
for name, expected, actual, ok in checks:
    lines.append(f"| {name} | `{expected}` | `{actual}` | {'✅' if ok else '❌ FAIL'} |")
lines.append("")
lines.append(f"\n**ALL_PASS = {ALL_PASS}**")
(ART / "receipt.md").write_text("\n".join(lines), encoding="utf-8")

# ---------------------------------------------------------------------------
# 7. Print funnel, NAB2 row, ALL_PASS to stdout.
# ---------------------------------------------------------------------------
print("\n=== FULL FUNNEL ===")
print(json.dumps(funnel, indent=2))
print("\n=== NAB2 -> atopic eczema row (rank", nab2_rank, ") ===")
print(json.dumps(nab2_row, indent=2))
print("\n=== ACCEPTANCE CHECKS ===")
for name, expected, actual, ok in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: expected={expected!r} actual={actual!r}")
print(f"\nALL_PASS = {ALL_PASS}")
