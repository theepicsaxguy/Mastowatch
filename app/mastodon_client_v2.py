"""
Type-safe Mastodon client using generated OpenAPI client with fallback to raw HTTP calls.
This provides the best of both worlds: type safety where available, flexibility where needed.
"""

import hashlib
from typing import Any, Dict, List, Optional, Union

import httpx

from app.clients.mastodon import AuthenticatedClient
from app.clients.mastodon.api.accounts import get_account, get_account_statuses
from app.clients.mastodon.api.reports import create_report
from app.clients.mastodon.models import Account, Status
from app.clients.mastodon.models.create_report_body import CreateReportBody
from app.clients.mastodon.models.create_report_body_category import \
    CreateReportBodyCategory
from app.clients.mastodon.models.report import Report
from app.config import get_settings
from app.metrics import api_call_seconds, http_errors
from app.rate_limit import throttle_if_needed, update_from_headers

settings = get_settings()


class MastoClientV2:
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

    def _make_raw_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        """
        Make a raw HTTP request for endpoints not available in the generated client.
        Maintains rate limiting and metrics tracking.
        """
        throttle_if_needed(self._bucket_key)

        with httpx.Client(timeout=30.0, headers={"Authorization": f"Bearer {self._token}", "User-Agent": self._ua}) as client:
            with api_call_seconds.labels(endpoint=path).time():
                if method.upper() == "GET":
                    response = client.get(f"{self._base_url}{path}", params=params)
                elif method.upper() == "POST":
                    response = client.post(f"{self._base_url}{path}", data=data, json=json)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

            update_from_headers(self._bucket_key, response.headers)
            if response.status_code >= 400:
                http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
            response.raise_for_status()
            return response

    # Type-safe methods using generated client

    def get_account(self, account_id: str) -> Account:
        """Get account information with full type safety."""
        throttle_if_needed(self._bucket_key)

        path = f"/api/v1/accounts/{account_id}"
        with api_call_seconds.labels(endpoint=path).time():
            response = get_account.sync_detailed(id=account_id, client=self._api_client)

        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
            response.raise_for_status()

        if not isinstance(response.parsed, Account):
            raise ValueError(f"Unexpected response type: {type(response.parsed)}")

        return response.parsed

    def get_account_statuses(
        self,
        account_id: str,
        limit: int = 20,
        max_id: Optional[str] = None,
        exclude_reblogs: bool = False,
        exclude_replies: bool = False,
        only_media: bool = False,
        pinned: bool = False,
    ) -> List[Status]:
        """Get account statuses with full type safety."""
        throttle_if_needed(self._bucket_key)

        path = f"/api/v1/accounts/{account_id}/statuses"
        with api_call_seconds.labels(endpoint=path).time():
            response = get_account_statuses.sync_detailed(
                id=account_id,
                client=self._api_client,
                limit=limit,
                max_id=max_id,
                exclude_reblogs=exclude_reblogs,
                exclude_replies=exclude_replies,
                only_media=only_media,
                pinned=pinned,
            )

        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
            response.raise_for_status()

        if not isinstance(response.parsed, list):
            raise ValueError(f"Unexpected response type: {type(response.parsed)}")

        return response.parsed

    def create_report(
        self,
        account_id: str,
        comment: str,
        status_ids: Optional[List[str]] = None,
        category: str = "other",
        forward: bool = False,
        rule_ids: Optional[List[str]] = None,
    ) -> Report:
        """Create a report with full type safety."""
        throttle_if_needed(self._bucket_key)

        # Map string category to enum
        category_enum = CreateReportBodyCategory.OTHER
        if category == "spam":
            category_enum = CreateReportBodyCategory.SPAM
        elif category == "violation":
            category_enum = CreateReportBodyCategory.VIOLATION
        elif category == "legal":
            category_enum = CreateReportBodyCategory.LEGAL

        report_body = CreateReportBody(
            account_id=account_id,
            comment=comment,
            status_ids=status_ids or [],
            category=category_enum,
            forward=forward,
            rule_ids=rule_ids or [],
        )

        path = "/api/v1/reports"
        with api_call_seconds.labels(endpoint=path).time():
            response = create_report.sync_detailed(
                client=self._api_client,
                body=report_body,
            )

        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
            response.raise_for_status()

        if not isinstance(response.parsed, Report):
            raise ValueError(f"Unexpected response type: {type(response.parsed)}")

        return response.parsed

    # Fallback methods for admin endpoints (not in community spec)

    def get_admin_accounts(
        self, origin: str = "remote", status: str = "active", limit: int = 100, max_id: Optional[str] = None
    ) -> httpx.Response:
        """
        Get admin accounts - falls back to raw HTTP since not in community OpenAPI spec.
        Returns raw response to maintain backward compatibility.
        """
        params = {
            "origin": origin,
            "status": status,
            "limit": limit,
        }
        if max_id:
            params["max_id"] = max_id

        return self._make_raw_request("GET", "/api/v1/admin/accounts", params=params)

    def get_instance_rules(self) -> List[Dict[str, Any]]:
        """Get instance rules with type information."""
        response = self._make_raw_request("GET", "/api/v1/instance/rules")
        return response.json()

    # Legacy compatibility methods

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """Legacy get method for backward compatibility."""
        return self._make_raw_request("GET", path, params=params)

    def post(self, path: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        """Legacy post method for backward compatibility."""
        return self._make_raw_request("POST", path, data=data, json=json)
