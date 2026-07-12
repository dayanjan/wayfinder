"""Bounded-concurrent, cached, resumable Europe PMC count fetcher (G1).

Why this exists: the full held-out frame is ~47k as-of-T queries + ~frame-size now queries.
The serial `arbiter.lbd._http` path (0.34 s politeness sleep) would take many hours. This module
overlaps network latency with a small worker pool while a shared token-bucket keeps the TOTAL request
rate bounded (politeness independent of worker count).

Cache-compatible + resumable: every count is read from / written to the SAME on-disk cache as the serial
path (`_http._cache_key` / `_http.CACHE_DIR`), keyed by the exact query string, so (a) a re-run returns
cached values instantly (the cache IS the checkpoint), (b) a crash mid-run loses only in-flight calls, and
(c) counts computed here are reused by the serial `sources.cooccur_count*` and vice-versa.
"""
from __future__ import annotations

import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

from ..lbd import _http
from ..lbd import sources as S

_EUROPEPMC = S.EUROPEPMC


def _cache_path(query: str):
    """The cache file `europepmc_count(query)` would use (identical key to the serial path)."""
    params = {"query": query, "format": "json", "pageSize": 1}
    return _http._cache_key("GET", _EUROPEPMC, {"params": params, "json": None})


def cached_count(query: str):
    """Return the cached hitCount for `query`, or None if not yet cached (no network)."""
    key = _cache_path(query)
    if key.exists():
        data = json.loads(key.read_text(encoding="utf-8"))
        return int(data.get("hitCount", 0))
    return None


class _RateLimiter:
    """Global min-interval limiter shared across worker threads -> bounded aggregate req/s."""

    def __init__(self, max_rps: float):
        self._interval = (1.0 / max_rps) if max_rps and max_rps > 0 else 0.0
        self._lock = threading.Lock()
        self._next = 0.0

    def acquire(self):
        if self._interval <= 0:
            return
        with self._lock:
            now = time.monotonic()
            wait = self._next - now
            if wait > 0:
                time.sleep(wait)
                now = time.monotonic()
            self._next = max(now, self._next) + self._interval


def _fetch_one(query: str, limiter: _RateLimiter, retries: int, timeout: int):
    """Network fetch of one count (cache miss path). Writes the cache in `_http` format.

    Retries with exponential backoff on transport / 429 / 5xx. Returns int, or raises on
    final failure (the caller records the failure and continues -- a run never aborts).
    """
    params = {"query": query, "format": "json", "pageSize": 1}
    key = _cache_path(query)
    backoff = 1.0
    last = None
    for _ in range(retries + 1):
        limiter.acquire()
        try:
            resp = requests.get(_EUROPEPMC, params=params, timeout=timeout)
            if resp.status_code == 429 or resp.status_code >= 500:
                raise requests.HTTPError(f"status {resp.status_code}")
            resp.raise_for_status()
            data = resp.json()
            key.parent.mkdir(parents=True, exist_ok=True)
            key.write_text(json.dumps(data), encoding="utf-8")
            return int(data.get("hitCount", 0))
        except Exception as exc:  # noqa: BLE001 - transient network; retry then record
            last = exc
            time.sleep(min(backoff, 30.0))
            backoff *= 2
    raise last if last else RuntimeError("fetch failed")


def count_many(queries, workers: int = 4, max_rps: float = 6.0, retries: int = 3,
               timeout: int = 30, on_progress=None, progress_every: int = 500) -> dict:
    """Resolve many Europe PMC count queries -> {query: int}. Cached + concurrent + resumable.

    `on_progress(done, total, hits, misses, failures)` is called every `progress_every`.
    Failed queries (after retries) are omitted from the result and returned via the `.failures`
    attribute on the returned dict-subclass. Deterministic: no randomness, no wall-clock in output.
    """
    uniq = list(dict.fromkeys(queries))  # de-dupe, preserve order
    total = len(uniq)
    result: dict[str, int] = {}
    failures: list[str] = []
    hits = misses = 0
    lock = threading.Lock()
    limiter = _RateLimiter(max_rps)

    # 1) serve cache hits first (free, no threads) -> minimises live calls after a partial run.
    todo = []
    for q in uniq:
        c = cached_count(q)
        if c is None:
            todo.append(q)
        else:
            result[q] = c
            hits += 1

    # 2) fetch the misses concurrently.
    def _work(q):
        nonlocal misses
        try:
            c = _fetch_one(q, limiter, retries, timeout)
            with lock:
                result[q] = c
                misses += 1
                done = hits + misses
                if on_progress and done % progress_every == 0:
                    on_progress(done, total, hits, misses, len(failures))
        except Exception:  # noqa: BLE001 - record + continue
            with lock:
                failures.append(q)

    if todo:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
            list(ex.map(_work, todo))

    if on_progress:
        on_progress(hits + misses, total, hits, misses, len(failures))

    class _Result(dict):
        pass

    out = _Result(result)
    out.failures = failures  # type: ignore[attr-defined]
    out.hits = hits          # type: ignore[attr-defined]
    out.misses = misses      # type: ignore[attr-defined]
    return out
