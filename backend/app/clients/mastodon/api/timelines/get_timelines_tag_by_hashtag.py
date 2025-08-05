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
    hashtag: str,
    *,
    all_: Union[Unset, list[str]] = UNSET,
    any_: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 20,
    local: Union[Unset, bool] = False,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    none: Union[Unset, list[str]] = UNSET,
    only_media: Union[Unset, bool] = False,
    remote: Union[Unset, bool] = False,
    since_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_all_: Union[Unset, list[str]] = UNSET
    if not isinstance(all_, Unset):
        json_all_ = all_

    params["all"] = json_all_

    json_any_: Union[Unset, list[str]] = UNSET
    if not isinstance(any_, Unset):
        json_any_ = any_

    params["any"] = json_any_

    params["limit"] = limit

    params["local"] = local

    params["max_id"] = max_id

    params["min_id"] = min_id

    json_none: Union[Unset, list[str]] = UNSET
    if not isinstance(none, Unset):
        json_none = none

    params["none"] = json_none

    params["only_media"] = only_media

    params["remote"] = remote

    params["since_id"] = since_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/timelines/tag/{hashtag}".format(
            hashtag=hashtag,
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
    hashtag: str,
    *,
    client: AuthenticatedClient,
    all_: Union[Unset, list[str]] = UNSET,
    any_: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 20,
    local: Union[Unset, bool] = False,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    none: Union[Unset, list[str]] = UNSET,
    only_media: Union[Unset, bool] = False,
    remote: Union[Unset, bool] = False,
    since_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" View hashtag timeline

     View public statuses containing the given hashtag.

    Version history:

    0.0.0 - added\
    2.3.0 - added `only_media`\
    2.6.0 - add `min_id`\
    2.7.0 - add `any[]`, `all[]`, `none[]` for additional tags\
    3.0.0 - auth is required if public preview is disabled\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now. add `remote`

    Args:
        hashtag (str):
        all_ (Union[Unset, list[str]]): Return statuses that contain all of these additional tags.
        any_ (Union[Unset, list[str]]): Return statuses that contain any of these additional tags.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        local (Union[Unset, bool]): Return only local statuses? Defaults to false. Default: False.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        none (Union[Unset, list[str]]): Return statuses that contain none of these additional
            tags.
        only_media (Union[Unset, bool]): Return only statuses with media attachments? Defaults to
            false. Default: False.
        remote (Union[Unset, bool]): Return only remote statuses? Defaults to false. Default:
            False.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Status']]]
     """

    kwargs = _get_kwargs(
        hashtag=hashtag,
        all_=all_,
        any_=any_,
        limit=limit,
        local=local,
        max_id=max_id,
        min_id=min_id,
        none=none,
        only_media=only_media,
        remote=remote,
        since_id=since_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    hashtag: str,
    *,
    client: AuthenticatedClient,
    all_: Union[Unset, list[str]] = UNSET,
    any_: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 20,
    local: Union[Unset, bool] = False,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    none: Union[Unset, list[str]] = UNSET,
    only_media: Union[Unset, bool] = False,
    remote: Union[Unset, bool] = False,
    since_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" View hashtag timeline

     View public statuses containing the given hashtag.

    Version history:

    0.0.0 - added\
    2.3.0 - added `only_media`\
    2.6.0 - add `min_id`\
    2.7.0 - add `any[]`, `all[]`, `none[]` for additional tags\
    3.0.0 - auth is required if public preview is disabled\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now. add `remote`

    Args:
        hashtag (str):
        all_ (Union[Unset, list[str]]): Return statuses that contain all of these additional tags.
        any_ (Union[Unset, list[str]]): Return statuses that contain any of these additional tags.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        local (Union[Unset, bool]): Return only local statuses? Defaults to false. Default: False.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        none (Union[Unset, list[str]]): Return statuses that contain none of these additional
            tags.
        only_media (Union[Unset, bool]): Return only statuses with media attachments? Defaults to
            false. Default: False.
        remote (Union[Unset, bool]): Return only remote statuses? Defaults to false. Default:
            False.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Status']]
     """

    return sync_detailed(
        hashtag=hashtag,
        client=client,
        all_=all_,
        any_=any_,
        limit=limit,
        local=local,
        max_id=max_id,
        min_id=min_id,
        none=none,
        only_media=only_media,
        remote=remote,
        since_id=since_id,
    ).parsed


async def asyncio_detailed(
    hashtag: str,
    *,
    client: AuthenticatedClient,
    all_: Union[Unset, list[str]] = UNSET,
    any_: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 20,
    local: Union[Unset, bool] = False,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    none: Union[Unset, list[str]] = UNSET,
    only_media: Union[Unset, bool] = False,
    remote: Union[Unset, bool] = False,
    since_id: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" View hashtag timeline

     View public statuses containing the given hashtag.

    Version history:

    0.0.0 - added\
    2.3.0 - added `only_media`\
    2.6.0 - add `min_id`\
    2.7.0 - add `any[]`, `all[]`, `none[]` for additional tags\
    3.0.0 - auth is required if public preview is disabled\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now. add `remote`

    Args:
        hashtag (str):
        all_ (Union[Unset, list[str]]): Return statuses that contain all of these additional tags.
        any_ (Union[Unset, list[str]]): Return statuses that contain any of these additional tags.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        local (Union[Unset, bool]): Return only local statuses? Defaults to false. Default: False.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        none (Union[Unset, list[str]]): Return statuses that contain none of these additional
            tags.
        only_media (Union[Unset, bool]): Return only statuses with media attachments? Defaults to
            false. Default: False.
        remote (Union[Unset, bool]): Return only remote statuses? Defaults to false. Default:
            False.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Status']]]
     """

    kwargs = _get_kwargs(
        hashtag=hashtag,
        all_=all_,
        any_=any_,
        limit=limit,
        local=local,
        max_id=max_id,
        min_id=min_id,
        none=none,
        only_media=only_media,
        remote=remote,
        since_id=since_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    hashtag: str,
    *,
    client: AuthenticatedClient,
    all_: Union[Unset, list[str]] = UNSET,
    any_: Union[Unset, list[str]] = UNSET,
    limit: Union[Unset, int] = 20,
    local: Union[Unset, bool] = False,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    none: Union[Unset, list[str]] = UNSET,
    only_media: Union[Unset, bool] = False,
    remote: Union[Unset, bool] = False,
    since_id: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Status"]]]:
    r""" View hashtag timeline

     View public statuses containing the given hashtag.

    Version history:

    0.0.0 - added\
    2.3.0 - added `only_media`\
    2.6.0 - add `min_id`\
    2.7.0 - add `any[]`, `all[]`, `none[]` for additional tags\
    3.0.0 - auth is required if public preview is disabled\
    3.3.0 - both `min_id` and `max_id` can be used at the same time now. add `remote`

    Args:
        hashtag (str):
        all_ (Union[Unset, list[str]]): Return statuses that contain all of these additional tags.
        any_ (Union[Unset, list[str]]): Return statuses that contain any of these additional tags.
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 20 statuses.
            Max 40 statuses. Default: 20.
        local (Union[Unset, bool]): Return only local statuses? Defaults to false. Default: False.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        none (Union[Unset, list[str]]): Return statuses that contain none of these additional
            tags.
        only_media (Union[Unset, bool]): Return only statuses with media attachments? Defaults to
            false. Default: False.
        remote (Union[Unset, bool]): Return only remote statuses? Defaults to false. Default:
            False.
        since_id (Union[Unset, str]): All results returned will be greater than this ID. In
            effect, sets a lower bound on results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Status']]
     """

    return (
        await asyncio_detailed(
            hashtag=hashtag,
            client=client,
            all_=all_,
            any_=any_,
            limit=limit,
            local=local,
            max_id=max_id,
            min_id=min_id,
            none=none,
            only_media=only_media,
            remote=remote,
            since_id=since_id,
        )
    ).parsed
