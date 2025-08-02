from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.post_oauth_token_body import PostOauthTokenBody
from ...models.token import Token
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: PostOauthTokenBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/oauth/token",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Token, ValidationError]]:
    if response.status_code == 200:
        response_200 = Token.from_dict(response.json())

        return response_200
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == 410:
        response_410 = cast(Any, None)
        return response_410
    if response.status_code == 422:
        response_422 = ValidationError.from_dict(response.json())

        return response_422
    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())

        return response_429
    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())

        return response_503
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Error, Token, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostOauthTokenBody,
) -> Response[Union[Any, Error, Token, ValidationError]]:
    r""" Obtain a token

     Obtain an access token, to be used during API calls that are not public.

    Version history:

    0.1.0 - added\
    4.3.0 - added support for PKCE parameter

    Args:
        body (PostOauthTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Token, ValidationError]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostOauthTokenBody,
) -> Optional[Union[Any, Error, Token, ValidationError]]:
    r""" Obtain a token

     Obtain an access token, to be used during API calls that are not public.

    Version history:

    0.1.0 - added\
    4.3.0 - added support for PKCE parameter

    Args:
        body (PostOauthTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Token, ValidationError]
     """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostOauthTokenBody,
) -> Response[Union[Any, Error, Token, ValidationError]]:
    r""" Obtain a token

     Obtain an access token, to be used during API calls that are not public.

    Version history:

    0.1.0 - added\
    4.3.0 - added support for PKCE parameter

    Args:
        body (PostOauthTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Token, ValidationError]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostOauthTokenBody,
) -> Optional[Union[Any, Error, Token, ValidationError]]:
    r""" Obtain a token

     Obtain an access token, to be used during API calls that are not public.

    Version history:

    0.1.0 - added\
    4.3.0 - added support for PKCE parameter

    Args:
        body (PostOauthTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Token, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
