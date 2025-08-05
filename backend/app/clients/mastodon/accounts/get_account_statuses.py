from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.status import Status
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    exclude_reblogs: Union[Unset, bool] = UNSET,
    exclude_replies: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    only_media: Union[Unset, bool] = UNSET,
    pinned: Union[Unset, bool] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    tagged: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["exclude_reblogs"] = exclude_reblogs

    params["exclude_replies"] = exclude_replies

    params["limit"] = limit

    params["max_id"] = max_id

    params["min_id"] = min_id

    params["only_media"] = only_media

    params["pinned"] = pinned

    params["since_id"] = since_id

    params["tagged"] = tagged

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/accounts/{id}/statuses".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError, list["Status"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Status.from_dict(response_200_item_data)

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
) -> Response[Union[Any, Error, ValidationError, list["Status"]]]:
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
    exclude_reblogs: Union[Unset, bool] = UNSET,
    exclude_replies: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    only_media: Union[Unset, bool] = UNSET,
    pinned: Union[Unset, bool] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    tagged: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" Get account's statuses

     Statuses posted to the given account.

    Version history:

    0.0.0 - added\
    1.4.2 - add `only_media` and `exclude_replies`\
    1.6.0 - add `pinned`\
    2.6.0 - add `min_id`\
    2.7.0 - add `exclude_reblogs` and allow unauthed use\
    2.8.0 - add `tagged` parameter\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now

    Args:
        id (str):
        exclude_reblogs (Union[Unset, bool]): Filter out boosts from the response.
        exclude_replies (Union[Unset, bool]): Filter out statuses in reply to a different account.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        only_media (Union[Unset, bool]): Filter out statuses without attachments.
        pinned (Union[Unset, bool]): Filter for pinned statuses only. Defaults to false, which
            includes all statuses. Pinned statuses do not receive special priority in the order of the
            returned results.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        tagged (Union[Unset, str]): Filter for statuses using a specific hashtag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Status']]]
     """

    kwargs = _get_kwargs(
        id=id,
        exclude_reblogs=exclude_reblogs,
        exclude_replies=exclude_replies,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        only_media=only_media,
        pinned=pinned,
        since_id=since_id,
        tagged=tagged,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    exclude_reblogs: Union[Unset, bool] = UNSET,
    exclude_replies: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    only_media: Union[Unset, bool] = UNSET,
    pinned: Union[Unset, bool] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    tagged: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" Get account's statuses

     Statuses posted to the given account.

    Version history:

    0.0.0 - added\
    1.4.2 - add `only_media` and `exclude_replies`\
    1.6.0 - add `pinned`\
    2.6.0 - add `min_id`\
    2.7.0 - add `exclude_reblogs` and allow unauthed use\
    2.8.0 - add `tagged` parameter\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now

    Args:
        id (str):
        exclude_reblogs (Union[Unset, bool]): Filter out boosts from the response.
        exclude_replies (Union[Unset, bool]): Filter out statuses in reply to a different account.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        only_media (Union[Unset, bool]): Filter out statuses without attachments.
        pinned (Union[Unset, bool]): Filter for pinned statuses only. Defaults to false, which
            includes all statuses. Pinned statuses do not receive special priority in the order of the
            returned results.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        tagged (Union[Unset, str]): Filter for statuses using a specific hashtag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Status']]
     """

    return sync_detailed(
        id=id,
        client=client,
        exclude_reblogs=exclude_reblogs,
        exclude_replies=exclude_replies,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        only_media=only_media,
        pinned=pinned,
        since_id=since_id,
        tagged=tagged,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    exclude_reblogs: Union[Unset, bool] = UNSET,
    exclude_replies: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    only_media: Union[Unset, bool] = UNSET,
    pinned: Union[Unset, bool] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    tagged: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" Get account's statuses

     Statuses posted to the given account.

    Version history:

    0.0.0 - added\
    1.4.2 - add `only_media` and `exclude_replies`\
    1.6.0 - add `pinned`\
    2.6.0 - add `min_id`\
    2.7.0 - add `exclude_reblogs` and allow unauthed use\
    2.8.0 - add `tagged` parameter\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now

    Args:
        id (str):
        exclude_reblogs (Union[Unset, bool]): Filter out boosts from the response.
        exclude_replies (Union[Unset, bool]): Filter out statuses in reply to a different account.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        only_media (Union[Unset, bool]): Filter out statuses without attachments.
        pinned (Union[Unset, bool]): Filter for pinned statuses only. Defaults to false, which
            includes all statuses. Pinned statuses do not receive special priority in the order of the
            returned results.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        tagged (Union[Unset, str]): Filter for statuses using a specific hashtag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Status']]]
     """

    kwargs = _get_kwargs(
        id=id,
        exclude_reblogs=exclude_reblogs,
        exclude_replies=exclude_replies,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        only_media=only_media,
        pinned=pinned,
        since_id=since_id,
        tagged=tagged,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    exclude_reblogs: Union[Unset, bool] = UNSET,
    exclude_replies: Union[Unset, bool] = UNSET,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    only_media: Union[Unset, bool] = UNSET,
    pinned: Union[Unset, bool] = UNSET,
    since_id: Union[Unset, str] = UNSET,
    tagged: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" Get account's statuses

     Statuses posted to the given account.

    Version history:

    0.0.0 - added\
    1.4.2 - add `only_media` and `exclude_replies`\
    1.6.0 - add `pinned`\
    2.6.0 - add `min_id`\
    2.7.0 - add `exclude_reblogs` and allow unauthed use\
    2.8.0 - add `tagged` parameter\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now

    Args:
        id (str):
        exclude_reblogs (Union[Unset, bool]): Filter out boosts from the response.
        exclude_replies (Union[Unset, bool]): Filter out statuses in reply to a different account.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        only_media (Union[Unset, bool]): Filter out statuses without attachments.
        pinned (Union[Unset, bool]): Filter for pinned statuses only. Defaults to false, which
            includes all statuses. Pinned statuses do not receive special priority in the order of the
            returned results.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.
        tagged (Union[Unset, str]): Filter for statuses using a specific hashtag.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Status']]
     """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            exclude_reblogs=exclude_reblogs,
            exclude_replies=exclude_replies,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            only_media=only_media,
            pinned=pinned,
            since_id=since_id,
            tagged=tagged,
        )
    ).parsed
