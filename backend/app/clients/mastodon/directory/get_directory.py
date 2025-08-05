from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.account import Account
from ...models.error import Error
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 40,
    local: Union[Unset, bool] = UNSET,
    offset: Union[Unset, int] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["local"] = local

    params["offset"] = offset

    params["order"] = order

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/directory",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError, list["Account"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Account.from_dict(response_200_item_data)

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
) -> Response[Union[Any, Error, ValidationError, list["Account"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 40,
    local: Union[Unset, bool] = UNSET,
    offset: Union[Unset, int] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Account"]]]:
    """View profile directory

     List accounts visible in the directory.

    Version history:

    3.0.0 - added

    Args:
        limit (Union[Unset, int]): How many accounts to load. Defaults to 40 accounts. Max 80
            accounts. Default: 40.
        local (Union[Unset, bool]): If true, returns only local accounts.
        offset (Union[Unset, int]): Skip the first n results.
        order (Union[Unset, str]): Use `active` to sort by most recently posted statuses (default)
            or `new` to sort by most recently created profiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Account']]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        local=local,
        offset=offset,
        order=order,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 40,
    local: Union[Unset, bool] = UNSET,
    offset: Union[Unset, int] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Account"]]]:
    """View profile directory

     List accounts visible in the directory.

    Version history:

    3.0.0 - added

    Args:
        limit (Union[Unset, int]): How many accounts to load. Defaults to 40 accounts. Max 80
            accounts. Default: 40.
        local (Union[Unset, bool]): If true, returns only local accounts.
        offset (Union[Unset, int]): Skip the first n results.
        order (Union[Unset, str]): Use `active` to sort by most recently posted statuses (default)
            or `new` to sort by most recently created profiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Account']]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        local=local,
        offset=offset,
        order=order,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 40,
    local: Union[Unset, bool] = UNSET,
    offset: Union[Unset, int] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Account"]]]:
    """View profile directory

     List accounts visible in the directory.

    Version history:

    3.0.0 - added

    Args:
        limit (Union[Unset, int]): How many accounts to load. Defaults to 40 accounts. Max 80
            accounts. Default: 40.
        local (Union[Unset, bool]): If true, returns only local accounts.
        offset (Union[Unset, int]): Skip the first n results.
        order (Union[Unset, str]): Use `active` to sort by most recently posted statuses (default)
            or `new` to sort by most recently created profiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Account']]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        local=local,
        offset=offset,
        order=order,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 40,
    local: Union[Unset, bool] = UNSET,
    offset: Union[Unset, int] = UNSET,
    order: Union[Unset, str] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Account"]]]:
    """View profile directory

     List accounts visible in the directory.

    Version history:

    3.0.0 - added

    Args:
        limit (Union[Unset, int]): How many accounts to load. Defaults to 40 accounts. Max 80
            accounts. Default: 40.
        local (Union[Unset, bool]): If true, returns only local accounts.
        offset (Union[Unset, int]): Skip the first n results.
        order (Union[Unset, str]): Use `active` to sort by most recently posted statuses (default)
            or `new` to sort by most recently created profiles.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Account']]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            local=local,
            offset=offset,
            order=order,
        )
    ).parsed
