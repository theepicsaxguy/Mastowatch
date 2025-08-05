from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.relationship import Relationship
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    id: Union[Unset, list[str]] = UNSET,
    with_suspended: Union[Unset, bool] = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_id: Union[Unset, list[str]] = UNSET
    if not isinstance(id, Unset):
        json_id = id

    params["id"] = json_id

    params["with_suspended"] = with_suspended

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/accounts/relationships",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, list["Relationship"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Relationship.from_dict(response_200_item_data)

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
) -> Response[Union[Any, Error, list["Relationship"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, list[str]] = UNSET,
    with_suspended: Union[Unset, bool] = False,
) -> Response[Union[Any, Error, list["Relationship"]]]:
    r""" Check relationships to other accounts

     Find out whether a given account is followed, blocked, muted, etc.

    Version history:

    0.0.0 - added\
    4.3.0 - added `with_suspended` parameter

    Args:
        id (Union[Unset, list[str]]): Check relationships for the provided account IDs.
        with_suspended (Union[Unset, bool]): Whether relationships should be returned for
            suspended users, defaults to false. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, list['Relationship']]]
     """

    kwargs = _get_kwargs(
        id=id,
        with_suspended=with_suspended,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, list[str]] = UNSET,
    with_suspended: Union[Unset, bool] = False,
) -> Optional[Union[Any, Error, list["Relationship"]]]:
    r""" Check relationships to other accounts

     Find out whether a given account is followed, blocked, muted, etc.

    Version history:

    0.0.0 - added\
    4.3.0 - added `with_suspended` parameter

    Args:
        id (Union[Unset, list[str]]): Check relationships for the provided account IDs.
        with_suspended (Union[Unset, bool]): Whether relationships should be returned for
            suspended users, defaults to false. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, list['Relationship']]
     """

    return sync_detailed(
        client=client,
        id=id,
        with_suspended=with_suspended,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, list[str]] = UNSET,
    with_suspended: Union[Unset, bool] = False,
) -> Response[Union[Any, Error, list["Relationship"]]]:
    r""" Check relationships to other accounts

     Find out whether a given account is followed, blocked, muted, etc.

    Version history:

    0.0.0 - added\
    4.3.0 - added `with_suspended` parameter

    Args:
        id (Union[Unset, list[str]]): Check relationships for the provided account IDs.
        with_suspended (Union[Unset, bool]): Whether relationships should be returned for
            suspended users, defaults to false. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, list['Relationship']]]
     """

    kwargs = _get_kwargs(
        id=id,
        with_suspended=with_suspended,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    id: Union[Unset, list[str]] = UNSET,
    with_suspended: Union[Unset, bool] = False,
) -> Optional[Union[Any, Error, list["Relationship"]]]:
    r""" Check relationships to other accounts

     Find out whether a given account is followed, blocked, muted, etc.

    Version history:

    0.0.0 - added\
    4.3.0 - added `with_suspended` parameter

    Args:
        id (Union[Unset, list[str]]): Check relationships for the provided account IDs.
        with_suspended (Union[Unset, bool]): Whether relationships should be returned for
            suspended users, defaults to false. Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, list['Relationship']]
     """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
            with_suspended=with_suspended,
        )
    ).parsed
