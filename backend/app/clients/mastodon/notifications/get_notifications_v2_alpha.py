from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.grouped_notifications_results import GroupedNotificationsResults
from ...models.types_enum import TypesEnum
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[TypesEnum]] = UNSET,
    expand_accounts: Union[Unset, str] = UNSET,
    grouped_types: Union[Unset, list[TypesEnum]] = UNSET,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["account_id"] = account_id

    json_exclude_types: Union[Unset, list[str]] = UNSET
    if not isinstance(exclude_types, Unset):
        json_exclude_types = []
        for exclude_types_item_data in exclude_types:
            exclude_types_item = exclude_types_item_data.value
            json_exclude_types.append(exclude_types_item)

    params["exclude_types"] = json_exclude_types

    params["expand_accounts"] = expand_accounts

    json_grouped_types: Union[Unset, list[str]] = UNSET
    if not isinstance(grouped_types, Unset):
        json_grouped_types = []
        for grouped_types_item_data in grouped_types:
            grouped_types_item = grouped_types_item_data.value
            json_grouped_types.append(grouped_types_item)

    params["grouped_types"] = json_grouped_types

    params["limit"] = limit

    params["max_id"] = max_id

    params["min_id"] = min_id

    params["since_id"] = since_id

    json_types: Union[Unset, list[str]] = UNSET
    if not isinstance(types, Unset):
        json_types = []
        for types_item_data in types:
            types_item = types_item_data.value
            json_types.append(types_item)

    params["types"] = json_types

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2_alpha/notifications",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    if response.status_code == 200:
        response_200 = GroupedNotificationsResults.from_dict(response.json())

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
) -> Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
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
    exclude_types: Union[Unset, list[TypesEnum]] = UNSET,
    expand_accounts: Union[Unset, str] = UNSET,
    grouped_types: Union[Unset, list[TypesEnum]] = UNSET,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    r""" Get all grouped notifications

     Return grouped notifications concerning the user. This API returns Link headers containing links to
    the next/previous page. However, the links can also be constructed dynamically using query params
    and `id` values.

    Version history:

    4.3.0-beta.1 - added\
    4.3.0-beta.2 - deprecated

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        expand_accounts (Union[Unset, str]): One of `full` (default) or `partial_avatars`. When
            set to `partial_avatars`, some accounts will not be rendered in full in the returned
            `accounts` list but will be instead returned in stripped-down form in the
            `partial_accounts` list. The most recent account in a notification group is always
            rendered in full in the `accounts` attribute.
        grouped_types (Union[Unset, list[TypesEnum]]): Restrict which notification types can be
            grouped. Use this if there are notification types for which your client does not support
            grouping. If omitted, the server will group notifications of all types it supports
            (currently, `favourite` and `reblog`). If you do not want any notification grouping, use
            [GET `/api/v1/notifications`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notification groups. Default: 40.
        max_id (Union[Unset, str]): All results returned will be about notifications strictly
            older than this notification ID. In effect, sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results about notifications immediately newer than
            this notification ID. In effect, sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be about notifications strictly
            newer than this notification ID. In effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]
     """

    kwargs = _get_kwargs(
        account_id=account_id,
        exclude_types=exclude_types,
        expand_accounts=expand_accounts,
        grouped_types=grouped_types,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        since_id=since_id,
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
    exclude_types: Union[Unset, list[TypesEnum]] = UNSET,
    expand_accounts: Union[Unset, str] = UNSET,
    grouped_types: Union[Unset, list[TypesEnum]] = UNSET,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Optional[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    r""" Get all grouped notifications

     Return grouped notifications concerning the user. This API returns Link headers containing links to
    the next/previous page. However, the links can also be constructed dynamically using query params
    and `id` values.

    Version history:

    4.3.0-beta.1 - added\
    4.3.0-beta.2 - deprecated

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        expand_accounts (Union[Unset, str]): One of `full` (default) or `partial_avatars`. When
            set to `partial_avatars`, some accounts will not be rendered in full in the returned
            `accounts` list but will be instead returned in stripped-down form in the
            `partial_accounts` list. The most recent account in a notification group is always
            rendered in full in the `accounts` attribute.
        grouped_types (Union[Unset, list[TypesEnum]]): Restrict which notification types can be
            grouped. Use this if there are notification types for which your client does not support
            grouping. If omitted, the server will group notifications of all types it supports
            (currently, `favourite` and `reblog`). If you do not want any notification grouping, use
            [GET `/api/v1/notifications`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notification groups. Default: 40.
        max_id (Union[Unset, str]): All results returned will be about notifications strictly
            older than this notification ID. In effect, sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results about notifications immediately newer than
            this notification ID. In effect, sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be about notifications strictly
            newer than this notification ID. In effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, GroupedNotificationsResults, ValidationError]
     """

    return sync_detailed(
        client=client,
        account_id=account_id,
        exclude_types=exclude_types,
        expand_accounts=expand_accounts,
        grouped_types=grouped_types,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        since_id=since_id,
        types=types,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[TypesEnum]] = UNSET,
    expand_accounts: Union[Unset, str] = UNSET,
    grouped_types: Union[Unset, list[TypesEnum]] = UNSET,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    r""" Get all grouped notifications

     Return grouped notifications concerning the user. This API returns Link headers containing links to
    the next/previous page. However, the links can also be constructed dynamically using query params
    and `id` values.

    Version history:

    4.3.0-beta.1 - added\
    4.3.0-beta.2 - deprecated

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        expand_accounts (Union[Unset, str]): One of `full` (default) or `partial_avatars`. When
            set to `partial_avatars`, some accounts will not be rendered in full in the returned
            `accounts` list but will be instead returned in stripped-down form in the
            `partial_accounts` list. The most recent account in a notification group is always
            rendered in full in the `accounts` attribute.
        grouped_types (Union[Unset, list[TypesEnum]]): Restrict which notification types can be
            grouped. Use this if there are notification types for which your client does not support
            grouping. If omitted, the server will group notifications of all types it supports
            (currently, `favourite` and `reblog`). If you do not want any notification grouping, use
            [GET `/api/v1/notifications`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notification groups. Default: 40.
        max_id (Union[Unset, str]): All results returned will be about notifications strictly
            older than this notification ID. In effect, sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results about notifications immediately newer than
            this notification ID. In effect, sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be about notifications strictly
            newer than this notification ID. In effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, GroupedNotificationsResults, ValidationError]]
     """

    kwargs = _get_kwargs(
        account_id=account_id,
        exclude_types=exclude_types,
        expand_accounts=expand_accounts,
        grouped_types=grouped_types,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        since_id=since_id,
        types=types,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[TypesEnum]] = UNSET,
    expand_accounts: Union[Unset, str] = UNSET,
    grouped_types: Union[Unset, list[TypesEnum]] = UNSET,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Optional[Union[Any, Error, GroupedNotificationsResults, ValidationError]]:
    r""" Get all grouped notifications

     Return grouped notifications concerning the user. This API returns Link headers containing links to
    the next/previous page. However, the links can also be constructed dynamically using query params
    and `id` values.

    Version history:

    4.3.0-beta.1 - added\
    4.3.0-beta.2 - deprecated

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        expand_accounts (Union[Unset, str]): One of `full` (default) or `partial_avatars`. When
            set to `partial_avatars`, some accounts will not be rendered in full in the returned
            `accounts` list but will be instead returned in stripped-down form in the
            `partial_accounts` list. The most recent account in a notification group is always
            rendered in full in the `accounts` attribute.
        grouped_types (Union[Unset, list[TypesEnum]]): Restrict which notification types can be
            grouped. Use this if there are notification types for which your client does not support
            grouping. If omitted, the server will group notifications of all types it supports
            (currently, `favourite` and `reblog`). If you do not want any notification grouping, use
            [GET `/api/v1/notifications`] instead.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notification groups. Default: 40.
        max_id (Union[Unset, str]): All results returned will be about notifications strictly
            older than this notification ID. In effect, sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results about notifications immediately newer than
            this notification ID. In effect, sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be about notifications strictly
            newer than this notification ID. In effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, GroupedNotificationsResults, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
            exclude_types=exclude_types,
            expand_accounts=expand_accounts,
            grouped_types=grouped_types,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            since_id=since_id,
            types=types,
        )
    ).parsed
