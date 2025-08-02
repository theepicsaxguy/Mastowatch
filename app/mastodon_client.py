"""
DEPRECATED: Legacy Mastodon client.

This module is deprecated and should not be used for new code.
Use app.mastodon_client_v2.MastoClientV2 instead, which uses the generated
OpenAPI client for better type safety and consistency.

TODO: Migrate all existing usage to MastoClientV2 and remove this file.
"""

import hashlib
import warnings

import httpx

from app.config import get_settings
from app.metrics import api_call_seconds, http_errors
from app.rate_limit import throttle_if_needed, update_from_headers

settings = get_settings()


class MastoClient:
    """
    DEPRECATED: Use MastoClientV2 instead.
    
    This legacy client creates its own httpx.Client instances instead of
    using the centralized client from the generated OpenAPI client.
    """
    
    def __init__(self, token: str):
        warnings.warn(
            "MastoClient is deprecated. Use MastoClientV2 instead.",
            DeprecationWarning,
            stacklevel=2
        )
        self._token = token
        self._base = str(settings.INSTANCE_BASE).rstrip("/")
        self._ua = settings.USER_AGENT
        tok = hashlib.sha256(token.encode("utf-8")).hexdigest()
        self._bucket_key = f"{self._base}:{tok}"

    def _client(self):
        return httpx.Client(timeout=30.0, headers={"Authorization": f"Bearer {self._token}", "User-Agent": self._ua})

    def get(self, path: str, params=None):
        throttle_if_needed(self._bucket_key)
        with self._client() as c:
            with api_call_seconds.labels(endpoint=path).time():
                r = c.get(f"{self._base}{path}", params=params)
            update_from_headers(self._bucket_key, r.headers)
            if r.status_code >= 400:
                http_errors.labels(endpoint=path, code=str(r.status_code)).inc()
            r.raise_for_status()
            return r

    def post(self, path: str, data=None, json=None):
        throttle_if_needed(self._bucket_key)
        with self._client() as c:
            with api_call_seconds.labels(endpoint=path).time():
                r = c.post(f"{self._base}{path}", data=data, json=json)
            update_from_headers(self._bucket_key, r.headers)
            if r.status_code >= 400:
                http_errors.labels(endpoint=path, code=str(r.status_code)).inc()
            r.raise_for_status()
            return r
