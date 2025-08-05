from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.search import Search
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    account_id: Union[Unset, str] = UNSET,
    exclude_unreviewed: Union[Unset, bool] = False,
    following: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    resolve: Union[Unset, bool] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["q"] = q

    params["account_id"] = account_id

    params["exclude_unreviewed"] = exclude_unreviewed

    params["following"] = following

    params["limit"] = limit

    params["max_id"] = max_id

    params["min_id"] = min_id

    params["offset"] = offset

    params["resolve"] = resolve

    params["type"] = type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v2/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Search, ValidationError]]:
    if response.status_code == 200:
        response_200 = Search.from_dict(response.json())

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
) -> Response[Union[Any, Error, Search, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    q: str,
    account_id: Union[Unset, str] = UNSET,
    exclude_unreviewed: Union[Unset, bool] = False,
    following: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    resolve: Union[Unset, bool] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, Search, ValidationError]]:
    r""" Perform a search

     Perform a search for content in accounts, statuses and hashtags with the given parameters.

    Version history:

    2.4.1 - added, limit hardcoded to 5\
    2.8.0 - add `type`, `limit`, `offset`, `min_id`, `max_id`, `account_id`\
    3.0.0 - add `exclude_unreviewed` param\
    3.3.0 - `min_id` and `max_id` can be used together\
    4.0.0 - no longer requires a user token. Without a valid user token, you cannot use the `resolve` or
    `offset` parameters.

    Args:
        q (str): The search query.
        account_id (Union[Unset, str]): If provided, will only return statuses authored by this
            account.
        exclude_unreviewed (Union[Unset, bool]): Filter out unreviewed tags? Defaults to false.
            Use true when trying to find trending tags. Default: False.
        following (Union[Unset, bool]): Only include accounts that the user is following? Defaults
            to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return, per type. Defaults to 20
            results per category. Max 40 results per category. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        offset (Union[Unset, int]): Skip the first n results.
        resolve (Union[Unset, bool]): Only relevant if `type` includes `accounts` or if `query` is
            a HTTPS URL. In the first case, if `true` and (a) the search query is for a remote account
            (e.g., `someaccount@someother.server`) and (b) the local server does not know about the
            account, [WebFinger] is used to try and resolve the account at `someother.server`. This
            provides the best recall at higher latency. If `false`, only accounts the server knows
            about are returned. In the second case, if `true`, resolving the URL and returning the
            matching status is attempted. If `false`, this resolving logic is circumvented and a
            regular search is performed instead.
        type_ (Union[Unset, str]): Specify whether to search for only `accounts`, `hashtags`,
            `statuses`

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Search, ValidationError]]
     """

    kwargs = _get_kwargs(
        q=q,
        account_id=account_id,
        exclude_unreviewed=exclude_unreviewed,
        following=following,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        offset=offset,
        resolve=resolve,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    q: str,
    account_id: Union[Unset, str] = UNSET,
    exclude_unreviewed: Union[Unset, bool] = False,
    following: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    resolve: Union[Unset, bool] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, Search, ValidationError]]:
    r""" Perform a search

     Perform a search for content in accounts, statuses and hashtags with the given parameters.

    Version history:

    2.4.1 - added, limit hardcoded to 5\
    2.8.0 - add `type`, `limit`, `offset`, `min_id`, `max_id`, `account_id`\
    3.0.0 - add `exclude_unreviewed` param\
    3.3.0 - `min_id` and `max_id` can be used together\
    4.0.0 - no longer requires a user token. Without a valid user token, you cannot use the `resolve` or
    `offset` parameters.

    Args:
        q (str): The search query.
        account_id (Union[Unset, str]): If provided, will only return statuses authored by this
            account.
        exclude_unreviewed (Union[Unset, bool]): Filter out unreviewed tags? Defaults to false.
            Use true when trying to find trending tags. Default: False.
        following (Union[Unset, bool]): Only include accounts that the user is following? Defaults
            to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return, per type. Defaults to 20
            results per category. Max 40 results per category. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        offset (Union[Unset, int]): Skip the first n results.
        resolve (Union[Unset, bool]): Only relevant if `type` includes `accounts` or if `query` is
            a HTTPS URL. In the first case, if `true` and (a) the search query is for a remote account
            (e.g., `someaccount@someother.server`) and (b) the local server does not know about the
            account, [WebFinger] is used to try and resolve the account at `someother.server`. This
            provides the best recall at higher latency. If `false`, only accounts the server knows
            about are returned. In the second case, if `true`, resolving the URL and returning the
            matching status is attempted. If `false`, this resolving logic is circumvented and a
            regular search is performed instead.
        type_ (Union[Unset, str]): Specify whether to search for only `accounts`, `hashtags`,
            `statuses`

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Search, ValidationError]
     """

    return sync_detailed(
        client=client,
        q=q,
        account_id=account_id,
        exclude_unreviewed=exclude_unreviewed,
        following=following,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        offset=offset,
        resolve=resolve,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    q: str,
    account_id: Union[Unset, str] = UNSET,
    exclude_unreviewed: Union[Unset, bool] = False,
    following: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    resolve: Union[Unset, bool] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, Search, ValidationError]]:
    r""" Perform a search

     Perform a search for content in accounts, statuses and hashtags with the given parameters.

    Version history:

    2.4.1 - added, limit hardcoded to 5\
    2.8.0 - add `type`, `limit`, `offset`, `min_id`, `max_id`, `account_id`\
    3.0.0 - add `exclude_unreviewed` param\
    3.3.0 - `min_id` and `max_id` can be used together\
    4.0.0 - no longer requires a user token. Without a valid user token, you cannot use the `resolve` or
    `offset` parameters.

    Args:
        q (str): The search query.
        account_id (Union[Unset, str]): If provided, will only return statuses authored by this
            account.
        exclude_unreviewed (Union[Unset, bool]): Filter out unreviewed tags? Defaults to false.
            Use true when trying to find trending tags. Default: False.
        following (Union[Unset, bool]): Only include accounts that the user is following? Defaults
            to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return, per type. Defaults to 20
            results per category. Max 40 results per category. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        offset (Union[Unset, int]): Skip the first n results.
        resolve (Union[Unset, bool]): Only relevant if `type` includes `accounts` or if `query` is
            a HTTPS URL. In the first case, if `true` and (a) the search query is for a remote account
            (e.g., `someaccount@someother.server`) and (b) the local server does not know about the
            account, [WebFinger] is used to try and resolve the account at `someother.server`. This
            provides the best recall at higher latency. If `false`, only accounts the server knows
            about are returned. In the second case, if `true`, resolving the URL and returning the
            matching status is attempted. If `false`, this resolving logic is circumvented and a
            regular search is performed instead.
        type_ (Union[Unset, str]): Specify whether to search for only `accounts`, `hashtags`,
            `statuses`

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Search, ValidationError]]
     """

    kwargs = _get_kwargs(
        q=q,
        account_id=account_id,
        exclude_unreviewed=exclude_unreviewed,
        following=following,
        limit=limit,
        max_id=max_id,
        min_id=min_id,
        offset=offset,
        resolve=resolve,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    q: str,
    account_id: Union[Unset, str] = UNSET,
    exclude_unreviewed: Union[Unset, bool] = False,
    following: Union[Unset, bool] = False,
    limit: Union[Unset, int] = 20,
    max_id: Union[Unset, str] = UNSET,
    min_id: Union[Unset, str] = UNSET,
    offset: Union[Unset, int] = UNSET,
    resolve: Union[Unset, bool] = UNSET,
    type_: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, Search, ValidationError]]:
    r""" Perform a search

     Perform a search for content in accounts, statuses and hashtags with the given parameters.

    Version history:

    2.4.1 - added, limit hardcoded to 5\
    2.8.0 - add `type`, `limit`, `offset`, `min_id`, `max_id`, `account_id`\
    3.0.0 - add `exclude_unreviewed` param\
    3.3.0 - `min_id` and `max_id` can be used together\
    4.0.0 - no longer requires a user token. Without a valid user token, you cannot use the `resolve` or
    `offset` parameters.

    Args:
        q (str): The search query.
        account_id (Union[Unset, str]): If provided, will only return statuses authored by this
            account.
        exclude_unreviewed (Union[Unset, bool]): Filter out unreviewed tags? Defaults to false.
            Use true when trying to find trending tags. Default: False.
        following (Union[Unset, bool]): Only include accounts that the user is following? Defaults
            to false. Default: False.
        limit (Union[Unset, int]): Maximum number of results to return, per type. Defaults to 20
            results per category. Max 40 results per category. Default: 20.
        max_id (Union[Unset, str]): All results returned will be lesser than this ID. In effect,
            sets an upper bound on results.
        min_id (Union[Unset, str]): Returns results immediately newer than this ID. In effect,
            sets a cursor at this ID and paginates forward.
        offset (Union[Unset, int]): Skip the first n results.
        resolve (Union[Unset, bool]): Only relevant if `type` includes `accounts` or if `query` is
            a HTTPS URL. In the first case, if `true` and (a) the search query is for a remote account
            (e.g., `someaccount@someother.server`) and (b) the local server does not know about the
            account, [WebFinger] is used to try and resolve the account at `someother.server`. This
            provides the best recall at higher latency. If `false`, only accounts the server knows
            about are returned. In the second case, if `true`, resolving the URL and returning the
            matching status is attempted. If `false`, this resolving logic is circumvented and a
            regular search is performed instead.
        type_ (Union[Unset, str]): Specify whether to search for only `accounts`, `hashtags`,
            `statuses`

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Search, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            account_id=account_id,
            exclude_unreviewed=exclude_unreviewed,
            following=following,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            offset=offset,
            resolve=resolve,
            type_=type_,
        )
    ).parsed
