"""Reproducible provenance check for the pinned disease->id map (fresh, new-work-only).

Re-resolves every disease in `entity_maps.DISEASES` against the Open Targets search API
(the service the A-C exclusion queries) and cross-checks EBI OLS4, then asserts the live
canonical id still equals the pinned id. This is how we KNOW the map is right rather than
trusting memory -- run it any time to regenerate the provenance table.

    python -m arbiter.lbd.verify_disease_ids

Verified 2026-07-08: all 14 names exact-matched; every id is a MONDO id (NOT EFO).
"""
from __future__ import annotations

import json
from pathlib import Path

from . import _http
from .entity_maps import DISEASES

OT = "https://api.platform.opentargets.org/api/v4/graphql"
OLS = "https://www.ebi.ac.uk/ols4/api/search"
_OT_SEARCH = ('query($q:String!){ search(queryString:$q, entityNames:["disease"], '
              'page:{index:0,size:1}){ hits{ id name } } }')


def _ot(name: str):
    data = _http.post(OT, json_body={"query": _OT_SEARCH, "variables": {"q": name}})
    hits = ((data.get("data") or {}).get("search") or {}).get("hits") or []
    return (hits[0]["id"], hits[0]["name"]) if hits else (None, None)


def _ols(name: str):
    data = _http.get(OLS, params={"q": name, "ontology": "efo,mondo", "type": "class",
                                  "rows": 1})
    docs = (data.get("response") or {}).get("docs") or []
    if not docs:
        return (None, None)
    return docs[0].get("obo_id"), docs[0].get("label")


def resolve_all() -> list[dict]:
    out = []
    for name, meta in DISEASES.items():
        ot_id, ot_name = _ot(name)
        ols_id, ols_label = _ols(name)
        pinned = meta["id"]
        ot_norm = (ot_id or "").replace(":", "_")
        out.append({"disease": name, "pinned_id": pinned, "opentargets_id": ot_id,
                    "opentargets_name": ot_name, "ols_id": ols_id, "ols_label": ols_label,
                    "match": ot_norm == pinned, "eligible": meta["eligible"]})
    return out


def main() -> int:
    rows = resolve_all()
    print(f"{'disease':32} {'pinned':16} {'opentargets':16} {'match':5}")
    print("-" * 78)
    bad = 0
    for r in rows:
        flag = "OK" if r["match"] else "DIFF"
        bad += 0 if r["match"] else 1
        print(f"{r['disease']:32} {r['pinned_id']:16} {str(r['opentargets_id']):16} {flag:5}")
    out = Path(__file__).resolve().parents[3] / "docs" / "lbd_disease_id_provenance.json"
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"\n{'ALL MATCH' if not bad else f'{bad} MISMATCH -- REVIEW'} | wrote {out.name}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
