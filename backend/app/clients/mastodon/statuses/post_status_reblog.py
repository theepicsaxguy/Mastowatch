from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.post_status_reblog_body import PostStatusReblogBody
from ...models.status import Status
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    body: PostStatusReblogBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/statuses/{id}/reblog".format(
            id=id,
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Status, ValidationError]]:
    if response.status_code == 200:
        response_200 = Status.from_dict(response.json())

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
) -> Response[Union[Any, Error, Status, ValidationError]]:
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
    body: PostStatusReblogBody,
) -> Response[Union[Any, Error, Status, ValidationError]]:
    r""" Boost a status

     Reshare a status on your own profile.

    Version history:

    0.0.0 - added\
    2.8.0 - add `visibility` parameter

    Args:
        id (str):
        body (PostStatusReblogBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Status, ValidationError]]
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
    body: PostStatusReblogBody,
) -> Optional[Union[Any, Error, Status, ValidationError]]:
    r""" Boost a status

     Reshare a status on your own profile.

    Version history:

    0.0.0 - added\
    2.8.0 - add `visibility` parameter

    Args:
        id (str):
        body (PostStatusReblogBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Status, ValidationError]
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
    body: PostStatusReblogBody,
) -> Response[Union[Any, Error, Status, ValidationError]]:
    r""" Boost a status

     Reshare a status on your own profile.

    Version history:

    0.0.0 - added\
    2.8.0 - add `visibility` parameter

    Args:
        id (str):
        body (PostStatusReblogBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Status, ValidationError]]
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
    body: PostStatusReblogBody,
) -> Optional[Union[Any, Error, Status, ValidationError]]:
    r""" Boost a status

     Reshare a status on your own profile.

    Version history:

    0.0.0 - added\
    2.8.0 - add `visibility` parameter

    Args:
        id (str):
        body (PostStatusReblogBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Status, ValidationError]
     """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
