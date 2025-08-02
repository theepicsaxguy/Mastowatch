"""OAuth API endpoints for Mastodon"""

from typing import Any, Dict, Optional, Union

import httpx
from ..client import AuthenticatedClient, Client
from ..models.post_oauth_token_body import PostOauthTokenBody
from ..models.token import Token
from ..models.credential_account import CredentialAccount
from ..types import Response


def post_oauth_token(
    *,
    client: Client,
    body: PostOauthTokenBody,
) -> Response[Token]:
    """Exchange authorization code for access token"""
    url = f"{client._base_url}/oauth/token"
    
    response = client.get_httpx_client().post(
        url,
        data=body.to_dict(),
    )
    
    from ..models.token import Token
    
    if response.status_code == 200:
        parsed = Token.from_dict(response.json())
    else:
        parsed = None
    
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=parsed,
    )


async def async_post_oauth_token(
    *,
    client: Client,
    body: PostOauthTokenBody,
) -> Response[Token]:
    """Exchange authorization code for access token (async)"""
    url = f"{client._base_url}/oauth/token"
    
    async_client = client.get_async_httpx_client()
    response = await async_client.post(
        url,
        data=body.to_dict(),
    )
    
    from ..models.token import Token
    
    if response.status_code == 200:
        parsed = Token.from_dict(response.json())
    else:
        parsed = None
    
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=parsed,
    )
