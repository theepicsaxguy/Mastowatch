from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.post_account_mute_body import PostAccountMuteBody
from ...models.relationship import Relationship
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: PostAccountMuteBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/accounts/{id}/mute".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Relationship]]:
    if response.status_code == 200:
        response_200 = Relationship.from_dict(response.json())

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
        response_422 = Error.from_dict(response.json())

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
) -> Response[Union[Any, Error, Relationship]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: PostAccountMuteBody,
) -> Response[Union[Any, Error, Relationship]]:
    r""" Mute account

     Mute the given account. Clients should filter statuses and notifications from this account, if
    received (e.g. due to a boost in the Home timeline).

    Version history:

    0.0.0 - added\
    3.3.0 - added `duration`\
    3.5.0 - deprecated `follow` scope. now additionally accepts `write`

    Args:
        id (str):
        body (PostAccountMuteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Relationship]]
     """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: PostAccountMuteBody,
) -> Optional[Union[Any, Error, Relationship]]:
    r""" Mute account

     Mute the given account. Clients should filter statuses and notifications from this account, if
    received (e.g. due to a boost in the Home timeline).

    Version history:

    0.0.0 - added\
    3.3.0 - added `duration`\
    3.5.0 - deprecated `follow` scope. now additionally accepts `write`

    Args:
        id (str):
        body (PostAccountMuteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Relationship]
     """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: PostAccountMuteBody,
) -> Response[Union[Any, Error, Relationship]]:
    r""" Mute account

     Mute the given account. Clients should filter statuses and notifications from this account, if
    received (e.g. due to a boost in the Home timeline).

    Version history:

    0.0.0 - added\
    3.3.0 - added `duration`\
    3.5.0 - deprecated `follow` scope. now additionally accepts `write`

    Args:
        id (str):
        body (PostAccountMuteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Relationship]]
     """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: PostAccountMuteBody,
) -> Optional[Union[Any, Error, Relationship]]:
    r""" Mute account

     Mute the given account. Clients should filter statuses and notifications from this account, if
    received (e.g. due to a boost in the Home timeline).

    Version history:

    0.0.0 - added\
    3.3.0 - added `duration`\
    3.5.0 - deprecated `follow` scope. now additionally accepts `write`

    Args:
        id (str):
        body (PostAccountMuteBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Relationship]
     """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
