"""Shared HTTP session: retries, backoff, polite pacing."""
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

UA = "Mozilla/5.0 (personal NHL research pipeline; non-commercial)"
_MIN_GAP = 1.0  # seconds between requests to the same session
_last = [0.0]


def _session() -> requests.Session:
    s = requests.Session()
    retry = Retry(
        total=4,
        backoff_factor=2,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.headers.update({"User-Agent": UA})
    return s


SESSION = _session()


def get(url: str, params: dict | None = None, timeout: int = 30) -> requests.Response:
    wait = _MIN_GAP - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    r = SESSION.get(url, params=params, timeout=timeout)
    _last[0] = time.time()
    r.raise_for_status()
    return r


def get_json(url: str, params: dict | None = None) -> dict:
    return get(url, params=params).json()
