"""
Type-safe Mastodon client using generated OpenAPI client with fallback to raw HTTP calls.
This provides the best of both worlds: type safety where available, flexibility where needed.
"""

import hashlib
from typing import Any, Dict, List, Optional

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

    def _parse_next_cursor(self, link_header: Optional[str]) -> Optional[str]:
        """Parses the Link header to extract the next_max_id for pagination."""
        if not link_header:
            return None
        import re
        for link in link_header.split(","):
            if 'rel="next"' in link:
                match = re.search(r'max_id=(\\d+)', link)
                if match:
                    return match.group(1)
        return None

    # Type-safe methods using generated client

    from app.clients.mastodon.api.accounts import get_account as api_get_account

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get account information using the generated client."""
        throttle_if_needed(self._bucket_key)
        with api_call_seconds.labels(endpoint=f"/api/v1/accounts/{account_id}").time():
            response = api_get_account.sync_detailed(client=self._api_client, id=account_id)
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=f"/api/v1/accounts/{account_id}", code=str(response.status_code)).inc()
        response.raise_for_status()
        return response.parsed.to_dict()

    from app.clients.mastodon.api.accounts import get_account_statuses as api_get_account_statuses

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
        with api_call_seconds.labels(endpoint=f"/api/v1/accounts/{account_id}/statuses").time():
            response = api_get_account_statuses.sync_detailed(
                client=self._api_client,
                id=account_id,
                limit=limit,
                max_id=max_id,
                exclude_reblogs=exclude_reblogs,
                exclude_replies=exclude_replies,
                only_media=only_media,
                pinned=pinned,
            )
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=f"/api/v1/accounts/{account_id}/statuses", code=str(response.status_code)).inc()
        response.raise_for_status()
        return [s.to_dict() for s in response.parsed]

    from app.clients.mastodon.api.reports import create_report as api_create_report

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
            response = api_create_report.sync_detailed(client=self._api_client, body=report_body)
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
        response.raise_for_status()
        return response

    from app.clients.mastodon.api.admin import get_admin_accounts as api_get_admin_accounts

    def get_admin_accounts(
        self,
        origin: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
        max_id: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Get admin accounts using the generated client, with pagination."""
        throttle_if_needed(self._bucket_key)
        with api_call_seconds.labels(endpoint="/api/v1/admin/accounts").time():
            response = api_get_admin_accounts.sync_detailed(
                client=self._api_client,
                origin=origin,
                status=status,
                limit=limit,
                max_id=max_id,
            )
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint="/api/v1/admin/accounts", code=str(response.status_code)).inc()
        response.raise_for_status()

        accounts = [a.to_dict() for a in response.parsed]
        next_max_id = self._parse_next_cursor(response.headers.get("Link"))
        return accounts, next_max_id

    from app.clients.mastodon.api.instance import get_instance_rules as api_get_instance_rules

    def get_instance_rules(self) -> List[Dict[str, Any]]:
        """Get instance rules using the generated client."""
        throttle_if_needed(self._bucket_key)
        path = "/api/v1/instance/rules"
        with api_call_seconds.labels(endpoint=path).time():
            response = api_get_instance_rules.sync_detailed(client=self._api_client)
        update_from_headers(self._bucket_key, response.headers)
        if response.status_code >= 400:
            http_errors.labels(endpoint=path, code=str(response.status_code)).inc()
        response.raise_for_status()
        return [r.to_dict() for r in response.parsed]

    

    
