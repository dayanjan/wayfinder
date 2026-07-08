"""Shared cached HTTP for the LBD tool layer.

Deterministic, keyed off the project `.env`, caches every response to
`data/lbd_cache/` (gitignored) so a demo run is offline-reproducible and rate limits
are hit once. Politeness sleep between live calls. No heavy deps beyond `requests`.
Fresh code (new-work-only); mirrors the house pattern of the sibling `tools/*.py`.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path

import requests

_REPO = Path(__file__).resolve().parents[3]
CACHE_DIR = _REPO / "data" / "lbd_cache"
_POLITE_SLEEP_S = 0.34  # ~3 req/s default; NCBI key path may go faster


def load_env(env_path: Path | None = None) -> dict[str, str]:
    """Minimal .env loader (KEY=VALUE lines) -> os.environ; returns the parsed dict.

    Avoids a python-dotenv dependency. Ignores comments / blank lines. Does not
    overwrite an already-set environment variable.
    """
    path = env_path or (_REPO / ".env")
    parsed: dict[str, str] = {}
    if not path.exists():
        return parsed
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        parsed[key] = val
        os.environ.setdefault(key, val)
    return parsed


def _cache_key(method: str, url: str, payload) -> Path:
    blob = json.dumps({"m": method, "u": url, "p": payload}, sort_keys=True)
    h = hashlib.sha1(blob.encode("utf-8")).hexdigest()[:20]
    return CACHE_DIR / f"{h}.json"


def cached_request(method: str, url: str, *, params=None, json_body=None,
                   headers=None, timeout=30, use_cache=True):
    """GET/POST with on-disk JSON caching. Returns the parsed JSON (or {'_text': ...})."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"params": params, "json": json_body}
    key = _cache_key(method, url, payload)
    if use_cache and key.exists():
        return json.loads(key.read_text(encoding="utf-8"))

    time.sleep(_POLITE_SLEEP_S)
    resp = requests.request(method, url, params=params, json=json_body,
                            headers=headers, timeout=timeout)
    resp.raise_for_status()
    try:
        data = resp.json()
    except ValueError:
        data = {"_text": resp.text}
    key.write_text(json.dumps(data), encoding="utf-8")
    return data


def get(url, **kw):
    return cached_request("GET", url, **kw)


def post(url, **kw):
    return cached_request("POST", url, **kw)
