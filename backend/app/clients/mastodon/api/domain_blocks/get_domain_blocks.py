from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 100,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["max_id"] = max_id

    params["min_id"] = min_id

    params["since_id"] = since_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/domain_blocks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError, list[str]]]:
    if response.status_code == 200:
        response_200 = cast(list[str], response.json())

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
) -> Response[Union[Any, Error, ValidationError, list[str]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 100,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list[str]]]:
    """Get domain blocks

     View domains the user has blocked.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100 domain
            blocks. Max 200 domain blocks. Default: 100.
        max_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        min_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        since_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list[str]]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        since_id=since_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 100,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list[str]]]:
    """Get domain blocks

     View domains the user has blocked.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100 domain
            blocks. Max 200 domain blocks. Default: 100.
        max_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        min_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        since_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list[str]]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        since_id=since_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 100,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list[str]]]:
    """Get domain blocks

     View domains the user has blocked.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100 domain
            blocks. Max 200 domain blocks. Default: 100.
        max_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        min_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        since_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list[str]]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        since_id=since_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: Union[Unset, int] = 100,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list[str]]]:
    """Get domain blocks

     View domains the user has blocked.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100 domain
            blocks. Max 200 domain blocks. Default: 100.
        max_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        min_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.
        since_id (Union[Unset, str]): Internal parameter. Use HTTP `Link` header for pagination.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list[str]]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            since_id=since_id,
        )
    ).parsed
