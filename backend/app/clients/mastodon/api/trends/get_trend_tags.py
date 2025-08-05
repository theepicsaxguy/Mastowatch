from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.tag import Tag
from ...models.validation_error import ValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, int] = 10,
    offset: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/trends/tags",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, ValidationError, list["Tag"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Tag.from_dict(response_200_item_data)

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
) -> Response[Union[Any, Error, ValidationError, list["Tag"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    offset: Union[Unset, int] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Tag"]]]:
    r""" View trending tags

     Tags that are being used more frequently within the past week.

    Version history:

    3.0.0 - added\
    3.5.0 - method signature changed from `GET /api/v1/trends` to `GET /api/v1/trends/tags`. The former
    is a deprecated alias that may be removed in the future.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 10 tags. Max
            20 tags. Default: 10.
        offset (Union[Unset, int]): Skip the first n results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Tag']]]
     """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    offset: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Tag"]]]:
    r""" View trending tags

     Tags that are being used more frequently within the past week.

    Version history:

    3.0.0 - added\
    3.5.0 - method signature changed from `GET /api/v1/trends` to `GET /api/v1/trends/tags`. The former
    is a deprecated alias that may be removed in the future.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 10 tags. Max
            20 tags. Default: 10.
        offset (Union[Unset, int]): Skip the first n results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Tag']]
     """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    offset: Union[Unset, int] = UNSET,
) -> Response[Union[Any, Error, ValidationError, list["Tag"]]]:
    r""" View trending tags

     Tags that are being used more frequently within the past week.

    Version history:

    3.0.0 - added\
    3.5.0 - method signature changed from `GET /api/v1/trends` to `GET /api/v1/trends/tags`. The former
    is a deprecated alias that may be removed in the future.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 10 tags. Max
            20 tags. Default: 10.
        offset (Union[Unset, int]): Skip the first n results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError, list['Tag']]]
     """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, int] = 10,
    offset: Union[Unset, int] = UNSET,
) -> Optional[Union[Any, Error, ValidationError, list["Tag"]]]:
    r""" View trending tags

     Tags that are being used more frequently within the past week.

    Version history:

    3.0.0 - added\
    3.5.0 - method signature changed from `GET /api/v1/trends` to `GET /api/v1/trends/tags`. The former
    is a deprecated alias that may be removed in the future.

    Args:
        limit (Union[Unset, int]): Maximum number of results to return. Defaults to 10 tags. Max
            20 tags. Default: 10.
        offset (Union[Unset, int]): Skip the first n results.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError, list['Tag']]
     """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
