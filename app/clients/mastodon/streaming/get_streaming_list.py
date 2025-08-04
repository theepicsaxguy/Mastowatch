from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.validation_error import ValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    list_: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["list"] = list_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/streaming/list",
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
    list_: str,
) -> Response[Union[Any, Error, ValidationError]]:
    r""" Watch for list updates

     Returns statuses for a list

    Version history:

    2.1.0 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        list_ (str): The ID of the list to watch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
     """

    kwargs = _get_kwargs(
        list_=list_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    list_: str,
) -> Optional[Union[Any, Error, ValidationError]]:
    r""" Watch for list updates

     Returns statuses for a list

    Version history:

    2.1.0 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        list_ (str): The ID of the list to watch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
     """

    return sync_detailed(
        client=client,
        list_=list_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    list_: str,
) -> Response[Union[Any, Error, ValidationError]]:
    r""" Watch for list updates

     Returns statuses for a list

    Version history:

    2.1.0 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        list_ (str): The ID of the list to watch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
     """

    kwargs = _get_kwargs(
        list_=list_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    list_: str,
) -> Optional[Union[Any, Error, ValidationError]]:
    r""" Watch for list updates

     Returns statuses for a list

    Version history:

    2.1.0 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        list_ (str): The ID of the list to watch.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
            list_=list_,
        )
    ).parsed
