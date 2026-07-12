"""Offline unit tests for the G1 held-out-eval harness (arbiter.eval). NO network.

Run: PYTHONPATH=src python -m unittest discover -s tests -p "test_eval_*.py" -v
"""
from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pandas as pd  # noqa: E402

from arbiter.lbd import sources as S  # noqa: E402
from arbiter.eval import enumerate_frame as EF  # noqa: E402
from arbiter.eval import metrics as M  # noqa: E402
from arbiter.eval import rankers as R  # noqa: E402


# ----------------------------------------------------------------------------- sources / as-of-T
class TestSourcesAsof(unittest.TestCase):
    def test_query_construction_now_vs_asof(self):
        now = S.cooccur_query("NAB2", "atopic eczema")
        self.assertEqual(now, '("NAB2") AND ("atopic eczema")')
        asof = S.cooccur_query("NAB2", "atopic eczema", 2016)
        self.assertEqual(
            asof,
            '(("NAB2") AND ("atopic eczema")) AND (FIRST_PDATE:[1900-01-01 TO 2016-12-31])')

    def test_cutoff_boundary_year_appears_verbatim(self):
        for y in (2015, 2016, 2017):
            self.assertIn(f"TO {y}-12-31]", S.cooccur_query("A", "b", y))

    def test_cooccur_count_asof_uses_windowed_query(self):
        seen = {}

        def fake_count(q):
            seen["q"] = q
            return 1950

        orig = S.europepmc_count
        S.europepmc_count = fake_count
        try:
            self.assertEqual(S.cooccur_count_asof("STAT6", "asthma", 2016), 1950)
        finally:
            S.europepmc_count = orig
        self.assertIn("FIRST_PDATE:[1900-01-01 TO 2016-12-31]", seen["q"])


# ----------------------------------------------------------------------------- rankers
def _fake_referee_data():
    # (gene, gene_set, disease, p_adj_fdr, odds_ratio)
    df = pd.DataFrame([
        {"gene": "G1", "gene_set": "downstream_Stim8hr", "disease": "D", "p_adj_fdr": 0.001, "odds_ratio": 4.0},
        {"gene": "G3", "gene_set": "downstream_Stim8hr", "disease": "D", "p_adj_fdr": 0.20, "odds_ratio": 1.5},
    ])
    ns = types.SimpleNamespace(t3_exploded=df)
    return ns


def _fake_manifest():
    rows = [
        {"gene": "G1", "disease": "D", "ac_lit_asof": 0, "ac_lit_now": 9, "in_frame": True, "is_positive": True},
        {"gene": "G2", "disease": "D", "ac_lit_asof": 1, "ac_lit_now": 0, "in_frame": True, "is_positive": False},
        {"gene": "G3", "disease": "D", "ac_lit_asof": 0, "ac_lit_now": 7, "in_frame": True, "is_positive": True},
    ]
    return {
        "rows": rows,
        "ab_asof": {"G1": 100, "G2": 5, "G3": 40},
        "bc_asof": {"D": 200},
        "effect": {"G1": 500, "G2": 10, "G3": 300},
    }


class TestRankers(unittest.TestCase):
    def setUp(self):
        self.data = _fake_referee_data()
        self.manifest = _fake_manifest()
        self._orig = R.referee_triple
        answers = {"G1": "supported", "G2": "untested", "G3": "supported"}
        R.referee_triple = lambda g, d, cond, data: {"answer": answers[g]}

    def tearDown(self):
        R.referee_triple = self._orig

    def test_wayfinder_class_then_score(self):
        orders = R.build_orders(self.manifest, condition="Stim8hr", data=self.data)
        way = orders["wayfinder"]
        # both supported first (G1 higher ab/effect than G3 -> higher score), untested last
        self.assertEqual(way, ["G1||D", "G3||D", "G2||D"])

    def test_disease_hop_only_supported_first_by_or(self):
        orders = R.build_orders(self.manifest, condition="Stim8hr", data=self.data)
        dh = orders["disease_hop_only"]
        self.assertEqual(dh[0], "G1||D")           # only G1 is FDR<0.05 -> supported first
        self.assertEqual(set(dh), {"G1||D", "G2||D", "G3||D"})

    def test_lit_rarity_and_effect_and_random_cover_frame(self):
        orders = R.build_orders(self.manifest, condition="Stim8hr", data=self.data)
        self.assertEqual(orders["effect"][0], "G1||D")          # highest n_downstream
        self.assertEqual(orders["lit_rarity"][-1], "G2||D")     # ac_lit_asof=1 is least rare -> last
        for name in orders:
            self.assertEqual(set(orders[name]), {"G1||D", "G2||D", "G3||D"}, name)


# ----------------------------------------------------------------------------- metrics
class TestMetrics(unittest.TestCase):
    def test_precision_ap_recall_known_answer(self):
        order = ["a", "b", "c", "d"]
        pos = {"a", "c"}
        self.assertAlmostEqual(M.precision_at_k(order, pos, 2), 0.5)
        self.assertAlmostEqual(M.precision_at_k(order, pos, 4), 0.5)
        self.assertAlmostEqual(M.average_precision(order, pos), (1.0 + 2 / 3) / 2)
        self.assertAlmostEqual(M.recall_at_n(order, pos, 2), 0.5)

    def test_bootstrap_ci_collapses_when_orders_identical(self):
        order = ["g1||d", "g2||d", "g3||e", "g4||e"]
        pos = {"g1||d", "g3||e"}
        pair_meta = {p: tuple(p.split("||")) for p in order}
        genes = [pair_meta[p][0] for p in order]
        dis = [pair_meta[p][1] for p in order]
        r = M.clustered_bootstrap_diff(order, order, pos, pair_meta, genes, dis, k=2, n_boot=200)
        self.assertEqual(r["point"], 0.0)
        self.assertEqual((r["ci_lo"], r["ci_hi"]), (0.0, 0.0))
        self.assertFalse(r["positive"])

    def test_bootstrap_dedups_perpair_lists_and_shows_separation(self):
        # 4 genes x 3 diseases; positives = the d0 column. order_a ranks positives first, b last.
        frame = [f"g{i}||d{j}" for i in range(4) for j in range(3)]
        pos = {p for p in frame if p.endswith("d0")}
        pair_meta = {p: tuple(p.split("||")) for p in frame}
        order_a = sorted(frame, key=lambda p: (p not in pos, p))
        order_b = sorted(frame, key=lambda p: (p in pos, p))
        # pass DUPLICATED per-pair lists (the bug shape) -> dedup inside must still give a cluster bootstrap
        genes_dup = [pair_meta[p][0] for p in frame]
        dis_dup = [pair_meta[p][1] for p in frame]
        r = M.clustered_bootstrap_diff(order_a, order_b, pos, pair_meta, genes_dup, dis_dup,
                                       k=4, n_boot=300)
        self.assertEqual(r["point"], 1.0)      # all 4 positives at top of a, none in top-4 of b
        self.assertGreater(r["ci_hi"], 0.0)
        self.assertGreaterEqual(r["ci_lo"], 0.0)

    def test_joint_outcome_table(self):
        pos = {"ci_lo": 0.1, "ci_hi": 0.3}
        null = {"ci_lo": -0.1, "ci_hi": 0.2}
        self.assertEqual(M.joint_outcome(pos, pos), "full")
        self.assertEqual(M.joint_outcome(pos, null), "narrow_disease_hop_carried")
        self.assertEqual(M.joint_outcome(null, pos), "broad_null")


# ----------------------------------------------------------------------------- enumerate (subset)
class TestEnumerateSubset(unittest.TestCase):
    def test_subset_labels_and_manifest_header(self):
        # tiny synthetic A x C, no network, no data files
        genes = [f"G{i}" for i in range(4)]
        diseases = ["D0", "D1"]
        pairs = [(g, d) for g in genes for d in diseases]
        effect = {g: 10 for g in genes}
        orig_bp = EF.build_pairs
        orig_cm = EF.fetch.count_many
        EF.build_pairs = lambda condition="Stim8hr": (pairs, genes, diseases, effect)

        def fake_count_many(queries, **kw):
            out = {}
            for q in queries:
                # asof queries carry FIRST_PDATE; make all pairs novel-at-T (asof=0) and established-now (now=9)
                out[q] = 0 if "FIRST_PDATE" in q else 9
            res = dict(out)
            res = type("R", (dict,), {})(out)
            res.failures = []
            return res
        EF.fetch.count_many = fake_count_many
        try:
            man = EF.enumerate_frame(t=2016, k_establish=5, novel_max=1, subset=4,
                                     retrieval_date="2026-07-12", out_dir=Path(EF.OUT_DIR))
        finally:
            EF.build_pairs = orig_bp
            EF.fetch.count_many = orig_cm
        h = man["header"]
        self.assertEqual(h["scope"], "subset")
        self.assertEqual(h["frame_size"], 4)          # all 4 sampled pairs novel-at-T
        self.assertEqual(h["positive_count"], 4)      # all now=9 >= 5
        self.assertIn("sha256_of_rows", h)
        self.assertEqual(len(h["sha256_of_rows"]), 64)


if __name__ == "__main__":
    unittest.main()
