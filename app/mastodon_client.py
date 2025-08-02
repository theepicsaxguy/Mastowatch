"""
Type-safe Mastodon client using generated OpenAPI client with fallback to raw HTTP calls.
This provides the best of both worlds: type safety where available, flexibility where needed.
"""

import hashlib
from typing import Any, Dict, List, Optional, Union

import httpx

from app.clients.mastodon import AuthenticatedClient
from app.config import get_settings
from app.metrics import api_call_seconds, http_errors
from app.rate_limit import throttle_if_needed, update_from_headers

settings = get_settings()


class MastoClient:
    """
    Enhanced Mastodon client with type safety and fallback support.

    Uses the generated OpenAPI client for documented endpoints while maintaining
    backward compatibility for admin endpoints and custom functionality.
    """

    def __init__(self, token: str):
        self._token = token
        self._base_url = str(settings.INSTANCE_BASE).rstrip("/")
        self._ua = settings.USER_AGENT
        tok = hashlib.sha256(token.encode("utf-8")).hexdigest()
        self._bucket_key = f"{self._base_url}:{tok}"

        # Initialize the generated client
        self._api_client = AuthenticatedClient(
            base_url=self._base_url,
            token=token,
            headers={"User-Agent": self._ua},
            timeout=30.0,
        )

    

    # Type-safe methods using generated client

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get account information using the generated client."""
        throttle_if_needed(self._bucket_key)
        with api_call_seconds.labels(endpoint=f"/api/v1/accounts/{account_id}").time():
            response = self._api_client.get_httpx_client().get(f"/api/v1/accounts/{account_id}")
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=f"/api/v1/accounts/{account_id}", code=str(response.status_code)).inc()
        response.raise_for_status()
        return response.json()

    def get_account_statuses(
        self,
        account_id: str,
        limit: int = 20,
        max_id: Optional[str] = None,
        exclude_reblogs: bool = False,
        exclude_replies: bool = False,
        only_media: bool = False,
        pinned: bool = False,
    ) -> List[Dict[str, Any]]:
        """Get account statuses using the generated client."""
        throttle_if_needed(self._bucket_key)
        params = {
            "limit": limit,
            "exclude_reblogs": exclude_reblogs,
            "exclude_replies": exclude_replies,
            "only_media": only_media,
            "pinned": pinned,
        }
        if max_id:
            params["max_id"] = max_id
            
        path = f"/api/v1/accounts/{account_id}/statuses"
        with api_call_seconds.labels(endpoint=path).time():
            response = self._api_client.get_httpx_client().get(path, params=params)
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
        response.raise_for_status()
        return response.json()

    from app.clients.mastodon.models.create_report_body import CreateReportBody

    def create_report(
        self,
        account_id: str,
        comment: str,
        status_ids: Optional[List[str]] = None,
        category: str = "other",
        forward: bool = False,
        rule_ids: Optional[List[str]] = None,
    ) -> httpx.Response:
        """
        Create a report using the generated client and models.
        """
        throttle_if_needed(self._bucket_key)

        report_body = CreateReportBody(
            account_id=account_id,
            comment=comment,
            status_ids=status_ids,
            category=category,
            forward=forward,
            rule_ids=rule_ids,
        )

        path = "/api/v1/reports"
        with api_call_seconds.labels(endpoint=path).time():
            response = self._api_client.get_httpx_client().post(path, json=report_body.to_dict())
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
        response.raise_for_status()
        return response

    

    
