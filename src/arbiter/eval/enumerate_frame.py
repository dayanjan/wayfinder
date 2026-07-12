"""Enumerate the FULL A x C novel-at-T frame, label positives, write the count manifest (G1).

Frame (plan v3, F-001/F-002/F-003): the FULL A x C set (3,935 genes x 12 diseases = 47,220) subset to
`ac_lit_asof(T) <= novel_max` (default 1) -- NOT the gated funnel. Every ranker later ranks this same frame.

Positives: frame pairs with `ac_lit_now >= k_establish` (default 5) -- links that became literature-established
after T. Monotonicity (asof <= now) => the current-novel frame {now<=1} is a SUBSET of the novel-at-T frame,
so `now` is only queried for frame members (halves the run) and Jaccard = |now<=novel_max within frame| / |frame|.

The `count_manifest.json` is a COMMITTED, non-sensitive research receipt (F-009): sufficient to recompute every
metric offline, no live API. A gitignored cache is not a receipt; the manifest is.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from ..lbd import sources as S
from ..lbd.entities import build_a_universe, load_c
from ..lbd.entity_maps import program_terms
from . import fetch

_REPO = Path(__file__).resolve().parents[3]
OUT_DIR = _REPO / "data" / "eval_out"
CONDITION = "Stim8hr"
BASE_AXC = 47220


def build_pairs(condition: str = CONDITION):
    """The canonical gene-major A x C pair list + per-gene effect + disease id map."""
    a = build_a_universe(condition=condition, program_significant=True)
    genes = sorted(a["symbol"].unique().tolist())
    effect = a.groupby("symbol")["n_downstream"].max().astype(int).to_dict()
    diseases = [d["disease"] for d in load_c()]
    pairs = [(g, d) for g in genes for d in diseases]
    return pairs, genes, diseases, effect


def _progress(tag, done, total, hits, misses, failures):
    print(f"[enum:{tag}] {done}/{total} (cache_hit={hits} live={misses} fail={failures})", flush=True)


def enumerate_frame(t: int = 2016, k_establish: int = 5, novel_max: int = 1,
                    condition: str = CONDITION, retrieval_date: str = "unset",
                    workers: int = 4, max_rps: float = 6.0, subset: int | None = None,
                    seed: int = 20260712, out_dir: Path = OUT_DIR) -> dict:
    pairs, genes, diseases, effect = build_pairs(condition)
    # Full-scope runs must see the complete A x C; subset/synthetic runs are exempt.
    assert subset is not None or len(pairs) == BASE_AXC, len(pairs)

    if subset:  # blinded feasibility gate: a deterministic sample, LABEL COUNTS ONLY
        idx = random.Random(seed).sample(range(len(pairs)), subset)
        pairs = [pairs[i] for i in idx]

    # 1) as-of-T for every pair in scope -> defines the novel-at-T frame.
    asof_q = {(g, d): S.cooccur_query(g, d, t) for g, d in pairs}
    asof_counts = fetch.count_many(list(asof_q.values()), workers=workers, max_rps=max_rps,
                                   on_progress=lambda *a: _progress("asof", *a))
    asof = {gd: asof_counts.get(q) for gd, q in asof_q.items()}
    frame = [gd for gd in pairs if asof[gd] is not None and asof[gd] <= novel_max]

    # 2) now for frame members only (monotonicity) -> positives + current-novel for Jaccard.
    now_q = {gd: S.cooccur_query(gd[0], gd[1]) for gd in frame}
    now_counts = fetch.count_many(list(now_q.values()), workers=workers, max_rps=max_rps,
                                  on_progress=lambda *a: _progress("now", *a))
    now = {gd: now_counts.get(q) for gd, q in now_q.items()}
    # A failed now-fetch is UNKNOWN, not negative: drop it from the labelled frame (record the count)
    # rather than silently label it a negative (would bias the positives). Usually empty (fail=0).
    labeled_frame = [gd for gd in frame if now[gd] is not None]
    excluded_now_fail = [gd for gd in frame if now[gd] is None]
    positives = [gd for gd in labeled_frame if now[gd] >= k_establish]
    current_novel = [gd for gd in labeled_frame if now[gd] <= novel_max]
    jaccard = (len(current_novel) / len(labeled_frame)) if labeled_frame else 0.0

    # 3) as-of-T ab (per gene) + bc (per disease) for the Wayfinder ranker score.
    frame_genes = sorted({g for g, _ in labeled_frame})
    frame_dis = sorted({d for _, d in labeled_frame})
    ab_q = {g: S.cooccur_query(g, program_terms("AB"), t) for g in frame_genes}
    bc_q = {d: S.cooccur_query(program_terms("BC"), d, t) for d in frame_dis}
    ab_counts = fetch.count_many(list(ab_q.values()), workers=workers, max_rps=max_rps,
                                 on_progress=lambda *a: _progress("ab", *a))
    bc_counts = fetch.count_many(list(bc_q.values()), workers=workers, max_rps=max_rps,
                                 on_progress=lambda *a: _progress("bc", *a))
    ab_asof = {g: ab_counts.get(q) for g, q in ab_q.items()}
    bc_asof = {d: bc_counts.get(q) for d, q in bc_q.items()}

    n_failures = (len(asof_counts.failures) + len(now_counts.failures)
                  + len(ab_counts.failures) + len(bc_counts.failures))

    frame_set = set(labeled_frame)   # build membership sets ONCE, not per-row (P2 perf)
    pos_set = set(positives)
    rows = [{"gene": g, "disease": d, "ac_lit_asof": asof[(g, d)],
             "ac_lit_now": now.get((g, d)),
             "in_frame": (g, d) in frame_set,
             "is_positive": (g, d) in pos_set}
            for (g, d) in pairs]
    rows.sort(key=lambda r: (r["gene"], r["disease"]))
    sha = hashlib.sha256(json.dumps(rows, sort_keys=True).encode("utf-8")).hexdigest()

    manifest = {
        "header": {
            "experiment": "G1 time-sliced held-out evaluation",
            "T": t, "k_establish": k_establish, "novel_max": novel_max, "condition": condition,
            "base_AxC": BASE_AXC, "scope": "subset" if subset else "full",
            "subset_n": subset, "seed": seed, "retrieval_date_utc": retrieval_date,
            "europepmc_query_template": '(("<gene>") AND ("<disease>")) [AND (FIRST_PDATE:[1900-01-01 TO T-12-31])]',
            "frame_size": len(labeled_frame), "positive_count": len(positives),
            "novel_at_T_asof_count": len(frame),
            "excluded_now_fetch_fail": len(excluded_now_fail),
            "current_novel_frame_size": len(current_novel),
            "jaccard_novelAtT_vs_currentNovel": round(jaccard, 4),
            "n_failures": n_failures, "sha256_of_rows": sha,
            "note": "COMMITTED RECEIPT: metrics recompute from this file with no live API. now queried "
                    "for frame members only (asof<=now monotonicity).",
        },
        "ab_asof": ab_asof, "bc_asof": bc_asof,
        "effect": {g: int(effect.get(g, 0)) for g in frame_genes},
        "rows": rows,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"subset{subset}" if subset else f"full_T{t}_k{k_establish}"
    path = out_dir / f"count_manifest_{tag}.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[enum] frame={len(frame)} positives={len(positives)} "
          f"jaccard={jaccard:.3f} failures={n_failures} -> {path.name}")
    return manifest


def main():
    ap = argparse.ArgumentParser(description="Enumerate the G1 novel-at-T frame + labels.")
    ap.add_argument("--t", type=int, default=2016)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--novel", type=int, default=1)
    ap.add_argument("--condition", default=CONDITION)
    ap.add_argument("--subset", type=int, default=None)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-rps", type=float, default=6.0)
    ap.add_argument("--retrieval-date", default="unset")
    args = ap.parse_args()
    enumerate_frame(t=args.t, k_establish=args.k, novel_max=args.novel, condition=args.condition,
                    retrieval_date=args.retrieval_date, workers=args.workers, max_rps=args.max_rps,
                    subset=args.subset)


if __name__ == "__main__":
    main()
