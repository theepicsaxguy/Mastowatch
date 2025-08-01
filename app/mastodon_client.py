import httpx, hashlib
from app.config import get_settings
from app.rate_limit import update_from_headers, throttle_if_needed
from app.metrics import api_call_seconds, http_errors

settings = get_settings()

class MastoClient:
    def __init__(self, token: str):
        self._token = token
        self._base = str(settings.MST_BASE_URL).rstrip("/")
        self._ua = settings.USER_AGENT
        tok = hashlib.sha256(token.encode("utf-8")).hexdigest()
        self._bucket_key = f"{self._base}:{tok}"

    def _client(self):
        return httpx.Client(timeout=30.0, headers={
            "Authorization": f"Bearer {self._token}",
            "User-Agent": self._ua
        })

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
