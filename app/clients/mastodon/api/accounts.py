"""Accounts API endpoints for Mastodon"""

from typing import Any, Dict, List, Optional, Union

import httpx
from ..client import AuthenticatedClient, Client
from ..models.account import Account
from ..models.credential_account import CredentialAccount
from ..models.status import Status
from ..types import Response


def get_account(
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
) -> Response[Account]:
    """Get account information"""
    url = f"{client._base_url}/api/v1/accounts/{id}"
    
    response = client.get_httpx_client().get(url)
    
    if response.status_code == 200:
        parsed = Account.from_dict(response.json())
    else:
        parsed = None
    
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=parsed,
    )


def get_account_statuses(
    *,
    client: Union[AuthenticatedClient, Client],
    id: str,
    limit: Optional[int] = None,
    max_id: Optional[str] = None,
    exclude_reblogs: Optional[bool] = None,
    exclude_replies: Optional[bool] = None,
    only_media: Optional[bool] = None,
    pinned: Optional[bool] = None,
) -> Response[List[Status]]:
    """Get account statuses"""
    url = f"{client._base_url}/api/v1/accounts/{id}/statuses"
    
    params = {}
    if limit is not None:
        params["limit"] = str(limit)
    if max_id is not None:
        params["max_id"] = max_id
    if exclude_reblogs is not None:
        params["exclude_reblogs"] = str(exclude_reblogs).lower()
    if exclude_replies is not None:
        params["exclude_replies"] = str(exclude_replies).lower()
    if only_media is not None:
        params["only_media"] = str(only_media).lower()
    if pinned is not None:
        params["pinned"] = str(pinned).lower()
    
    response = client.get_httpx_client().get(url, params=params)
    
    if response.status_code == 200:
        parsed = [Status.from_dict(item) for item in response.json()]
    else:
        parsed = None
    
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=parsed,
    )


def verify_credentials(
    *,
    client: AuthenticatedClient,
) -> Response[CredentialAccount]:
    """Verify account credentials"""
    url = f"{client._base_url}/api/v1/accounts/verify_credentials"
    
    response = client.get_httpx_client().get(url)
    
    if response.status_code == 200:
        parsed = CredentialAccount.from_dict(response.json())
    else:
        parsed = None
    
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=parsed,
    )


async def async_verify_credentials(
    *,
    client: AuthenticatedClient,
) -> Response[CredentialAccount]:
    """Verify account credentials (async)"""
    url = f"{client._base_url}/api/v1/accounts/verify_credentials"
    
    async_client = client.get_async_httpx_client()
    response = await async_client.get(url)
    
    if response.status_code == 200:
        parsed = CredentialAccount.from_dict(response.json())
    else:
        parsed = None
    
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=parsed,
    )
