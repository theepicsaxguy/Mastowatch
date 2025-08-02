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
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[str]] = UNSET,
    grouped_types: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 100,
    types: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["account_id"] = account_id

    json_exclude_types: Union[Unset, list[str]] = UNSET
    if not isinstance(exclude_types, Unset):
        json_exclude_types = exclude_types

    params["exclude_types"] = json_exclude_types

    json_grouped_types: Union[Unset, list[str]] = UNSET
    if not isinstance(grouped_types, Unset):
        json_grouped_types = grouped_types

    params["grouped_types"] = json_grouped_types

    params["limit"] = limit

    json_types: Union[Unset, list[str]] = UNSET
    if not isinstance(types, Unset):
        json_types = types

    params["types"] = json_types

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2_alpha/notifications/unread_count",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError]]:
    if response.status_code == 200:
        response_200 = cast(Any, None)
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
) -> Response[Union[Any, Error, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[str]] = UNSET,
    grouped_types: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 100,
    types: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Any, Error, ValidationError]]:
    """Get the number of unread notifications

     Get the (capped) number of unread notification groups for the current user.

    Args:
        account_id (Union[Unset, str]): Only count unread notifications received from the
            specified account.
        exclude_types (Union[Unset, list[str]]): Types of notifications that should not count
            towards unread notifications.
        grouped_types (Union[Unset, list[str]]): Restrict which notification types can be grouped.
            Use this if there are notification types for which your client does not support grouping.
            If omitted, the server will group notifications of all types it supports (currently,
            `favourite` and `reblog`). If you do not want any notification grouping, use [GET
            `/api/v1/notifications/unread_count`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100
            notifications. Max 1000 notifications. Default: 100.
        types (Union[Unset, list[str]]): Types of notifications that should count towards unread
            notifications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        exclude_types=exclude_types,
        grouped_types=grouped_types,
        limit=limit,
        types=types,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[str]] = UNSET,
    grouped_types: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 100,
    types: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Any, Error, ValidationError]]:
    """Get the number of unread notifications

     Get the (capped) number of unread notification groups for the current user.

    Args:
        account_id (Union[Unset, str]): Only count unread notifications received from the
            specified account.
        exclude_types (Union[Unset, list[str]]): Types of notifications that should not count
            towards unread notifications.
        grouped_types (Union[Unset, list[str]]): Restrict which notification types can be grouped.
            Use this if there are notification types for which your client does not support grouping.
            If omitted, the server will group notifications of all types it supports (currently,
            `favourite` and `reblog`). If you do not want any notification grouping, use [GET
            `/api/v1/notifications/unread_count`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100
            notifications. Max 1000 notifications. Default: 100.
        types (Union[Unset, list[str]]): Types of notifications that should count towards unread
            notifications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
    """

    return sync_detailed(
        client=client,
        account_id=account_id,
        exclude_types=exclude_types,
        grouped_types=grouped_types,
        limit=limit,
        types=types,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[str]] = UNSET,
    grouped_types: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 100,
    types: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Any, Error, ValidationError]]:
    """Get the number of unread notifications

     Get the (capped) number of unread notification groups for the current user.

    Args:
        account_id (Union[Unset, str]): Only count unread notifications received from the
            specified account.
        exclude_types (Union[Unset, list[str]]): Types of notifications that should not count
            towards unread notifications.
        grouped_types (Union[Unset, list[str]]): Restrict which notification types can be grouped.
            Use this if there are notification types for which your client does not support grouping.
            If omitted, the server will group notifications of all types it supports (currently,
            `favourite` and `reblog`). If you do not want any notification grouping, use [GET
            `/api/v1/notifications/unread_count`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100
            notifications. Max 1000 notifications. Default: 100.
        types (Union[Unset, list[str]]): Types of notifications that should count towards unread
            notifications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
    """

    kwargs = _get_kwargs(
        account_id=account_id,
        exclude_types=exclude_types,
        grouped_types=grouped_types,
        limit=limit,
        types=types,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[str]] = UNSET,
    grouped_types: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 100,
    types: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Any, Error, ValidationError]]:
    """Get the number of unread notifications

     Get the (capped) number of unread notification groups for the current user.

    Args:
        account_id (Union[Unset, str]): Only count unread notifications received from the
            specified account.
        exclude_types (Union[Unset, list[str]]): Types of notifications that should not count
            towards unread notifications.
        grouped_types (Union[Unset, list[str]]): Restrict which notification types can be grouped.
            Use this if there are notification types for which your client does not support grouping.
            If omitted, the server will group notifications of all types it supports (currently,
            `favourite` and `reblog`). If you do not want any notification grouping, use [GET
            `/api/v1/notifications/unread_count`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 100
            notifications. Max 1000 notifications. Default: 100.
        types (Union[Unset, list[str]]): Types of notifications that should count towards unread
            notifications.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
            exclude_types=exclude_types,
            grouped_types=grouped_types,
            limit=limit,
            types=types,
        )
    ).parsed
