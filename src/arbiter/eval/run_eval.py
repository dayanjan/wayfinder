"""G1 orchestrator: enumerate (or load) the frame -> build the 6 orders -> metrics -> results + SUMMARY.

Metrics recompute offline from a committed count_manifest.json (no live API), so `--from-manifest` reproduces
the published numbers deterministically. `null reported straight`: the harness never suppresses a CI that spans 0.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import enumerate_frame as EF
from . import metrics as M
from . import rankers as R

OUT_DIR = EF.OUT_DIR


def run(manifest: dict, condition: str = "Stim8hr", n_boot: int = 2000, seed: int = 20260712) -> dict:
    frame_rows = [r for r in manifest["rows"] if r["in_frame"]]
    pair_meta = {R.pid(r["gene"], r["disease"]): (r["gene"], r["disease"]) for r in frame_rows}
    positives = [R.pid(r["gene"], r["disease"]) for r in frame_rows if r["is_positive"]]
    frame_genes = [r["gene"] for r in frame_rows]
    frame_diseases = [r["disease"] for r in frame_rows]

    orders = R.build_orders(manifest, condition=condition, seed=seed)
    result = M.all_metrics(orders, positives, pair_meta, frame_genes, frame_diseases,
                           n_boot=n_boot, seed=seed)
    result["header"] = manifest.get("header", {})
    result["top20_wayfinder"] = orders["wayfinder"][:20]
    return result


def _summary_md(result: dict) -> str:
    h = result.get("header", {})
    lines = [f"# G1 held-out eval — SUMMARY (T={h.get('T')}, k={h.get('k_establish')}, "
             f"novel<= {h.get('novel_max')})",
             "",
             f"- Frame size: **{result['frame_size']}**  · positives: **{result['positive_count']}** "
             f"(base rate {result['base_rate']:.1%})",
             f"- Primary metric: precision@{result['primary_k']}",
             f"- Retrieval date: {h.get('retrieval_date_utc')}  · manifest sha256 rows: "
             f"{h.get('sha256_of_rows','')[:16]}…",
             "",
             "## Per-method precision (higher = better)",
             "| method | p@5 | p@10 | p@20 | p@50 | MAP |",
             "|---|---|---|---|---|---|"]
    for name, m in result["per_method"].items():
        lines.append(f"| {name} | {m['prec@5']} | {m['prec@10']} | {m['prec@20']} | "
                     f"{m['prec@50']} | {m['MAP']} |")
    cb = result["C_broad_wayfinder_vs_lit_rarity"]
    cm = result["C_mech_wayfinder_vs_disease_hop_only"]
    lines += ["",
              "## Co-primary contrasts (paired prec@20 diff, two-way-clustered bootstrap 95% CI)",
              f"- **C_broad** (Wayfinder − lit-rarity): {cb['point']:+.3f} "
              f"[{cb['ci_lo']:+.3f}, {cb['ci_hi']:+.3f}]  → {'separates' if cb['positive'] else 'NULL'}",
              f"- **C_mech** (Wayfinder − disease-hop-only): {cm['point']:+.3f} "
              f"[{cm['ci_lo']:+.3f}, {cm['ci_hi']:+.3f}]  → {'separates' if cm['positive'] else 'NULL'}",
              "",
              f"### Pre-registered joint outcome: **{result['joint_outcome']}**",
              "",
              "_A CI spanning 0 is reported straight; no metric/cutoff was promoted post-hoc._"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Run the G1 held-out eval end-to-end (or from a manifest).")
    ap.add_argument("--from-manifest", default=None, help="path to a count_manifest_*.json (skip enumeration)")
    ap.add_argument("--t", type=int, default=2016)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--novel", type=int, default=1)
    ap.add_argument("--condition", default="Stim8hr")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-rps", type=float, default=6.0)
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--retrieval-date", default="unset")
    args = ap.parse_args()

    if args.from_manifest:
        manifest = json.loads(Path(args.from_manifest).read_text(encoding="utf-8"))
    else:
        manifest = EF.enumerate_frame(t=args.t, k_establish=args.k, novel_max=args.novel,
                                      condition=args.condition, retrieval_date=args.retrieval_date,
                                      workers=args.workers, max_rps=args.max_rps)
    result = run(manifest, condition=args.condition, n_boot=args.n_boot)

    h = manifest.get("header", {})
    tag = f"T{h.get('T', args.t)}_k{h.get('k_establish', args.k)}"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"eval_results_{tag}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (OUT_DIR / "SUMMARY.md").write_text(_summary_md(result), encoding="utf-8")
    print(_summary_md(result))


if __name__ == "__main__":
    main()
