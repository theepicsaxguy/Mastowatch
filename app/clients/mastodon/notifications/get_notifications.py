from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.notification import Notification
from ...models.types_enum import TypesEnum
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    account_id: Union[Unset, str] = UNSET,
    exclude_types: Union[Unset, list[TypesEnum]] = UNSET,
    include_filtered: Union[Unset, bool] = False,
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

    params["include_filtered"] = include_filtered

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
        "url": "/api/v1/notifications",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError, list["Notification"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Notification.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[Any, Error, ValidationError, list["Notification"]]]:
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
    include_filtered: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Notification"]]]:
    r""" Get all notifications

     Notifications concerning the user. This API returns Link headers containing links to the
    next/previous page. However, the links can also be constructed dynamically using query params and
    `id` values.

    Version history:

    0.0.0 - added\
    2.6.0 - added `min_id`\
    2.9.0 - added `account_id`\
    3.1.0 - added `follow_request` type\
    3.3.0 - added `status` type; both `min_id` and `max_id` can be used at the same time now\
    3.5.0 - added `types`; add `update` and `admin.sign_up` types\
    4.0.0 - added `admin.report` type\
    4.1.0 - notification limit changed from 15 (max 30) to 40 (max 80)\
    4.3.0 - added `include_filtered` parameter

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        include_filtered (Union[Unset, bool]): Whether to include notifications filtered by the
            user's [NotificationPolicy]. Defaults to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notifications. Default: 40.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Notification']]]
     """

    kwargs = _get_kwargs(
        account_id=account_id,
        exclude_types=exclude_types,
        include_filtered=include_filtered,
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
    include_filtered: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Notification"]]]:
    r""" Get all notifications

     Notifications concerning the user. This API returns Link headers containing links to the
    next/previous page. However, the links can also be constructed dynamically using query params and
    `id` values.

    Version history:

    0.0.0 - added\
    2.6.0 - added `min_id`\
    2.9.0 - added `account_id`\
    3.1.0 - added `follow_request` type\
    3.3.0 - added `status` type; both `min_id` and `max_id` can be used at the same time now\
    3.5.0 - added `types`; add `update` and `admin.sign_up` types\
    4.0.0 - added `admin.report` type\
    4.1.0 - notification limit changed from 15 (max 30) to 40 (max 80)\
    4.3.0 - added `include_filtered` parameter

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        include_filtered (Union[Unset, bool]): Whether to include notifications filtered by the
            user's [NotificationPolicy]. Defaults to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notifications. Default: 40.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Notification']]
     """

    return sync_detailed(
        client=client,
        account_id=account_id,
        exclude_types=exclude_types,
        include_filtered=include_filtered,
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
    include_filtered: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Notification"]]]:
    r""" Get all notifications

     Notifications concerning the user. This API returns Link headers containing links to the
    next/previous page. However, the links can also be constructed dynamically using query params and
    `id` values.

    Version history:

    0.0.0 - added\
    2.6.0 - added `min_id`\
    2.9.0 - added `account_id`\
    3.1.0 - added `follow_request` type\
    3.3.0 - added `status` type; both `min_id` and `max_id` can be used at the same time now\
    3.5.0 - added `types`; add `update` and `admin.sign_up` types\
    4.0.0 - added `admin.report` type\
    4.1.0 - notification limit changed from 15 (max 30) to 40 (max 80)\
    4.3.0 - added `include_filtered` parameter

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        include_filtered (Union[Unset, bool]): Whether to include notifications filtered by the
            user's [NotificationPolicy]. Defaults to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notifications. Default: 40.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Notification']]]
     """

    kwargs = _get_kwargs(
        account_id=account_id,
        exclude_types=exclude_types,
        include_filtered=include_filtered,
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
    include_filtered: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 40,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    types: Union[Unset, list[TypesEnum]] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Notification"]]]:
    r""" Get all notifications

     Notifications concerning the user. This API returns Link headers containing links to the
    next/previous page. However, the links can also be constructed dynamically using query params and
    `id` values.

    Version history:

    0.0.0 - added\
    2.6.0 - added `min_id`\
    2.9.0 - added `account_id`\
    3.1.0 - added `follow_request` type\
    3.3.0 - added `status` type; both `min_id` and `max_id` can be used at the same time now\
    3.5.0 - added `types`; add `update` and `admin.sign_up` types\
    4.0.0 - added `admin.report` type\
    4.1.0 - notification limit changed from 15 (max 30) to 40 (max 80)\
    4.3.0 - added `include_filtered` parameter

    Args:
        account_id (Union[Unset, str]): Return only notifications received from the specified
            account.
        exclude_types (Union[Unset, list[TypesEnum]]): Types to exclude from the results.
        include_filtered (Union[Unset, bool]): Whether to include notifications filtered by the
            user's [NotificationPolicy]. Defaults to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 40
            notifications. Max 80 notifications. Default: 40.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        types (Union[Unset, list[TypesEnum]]): Types to include in the result.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Notification']]
     """

    return (
        await asyncio_detailed(
            client=client,
            account_id=account_id,
            exclude_types=exclude_types,
            include_filtered=include_filtered,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            since_id=since_id,
            types=types,
        )
    ).parsed
