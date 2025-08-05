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
    only_media: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["only_media"] = only_media

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/streaming/public/remote",
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
    only_media: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, Error, ValidationError]]:
    r""" Watch for remote statuses

     Returns all public statuses from remote servers.

    Version history:

    3.1.4 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        only_media (Union[Unset, bool]): If true, return only statuses with media attachments.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
     """

    kwargs = _get_kwargs(
        only_media=only_media,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    only_media: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, Error, ValidationError]]:
    r""" Watch for remote statuses

     Returns all public statuses from remote servers.

    Version history:

    3.1.4 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        only_media (Union[Unset, bool]): If true, return only statuses with media attachments.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
     """

    return sync_detailed(
        client=client,
        only_media=only_media,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    only_media: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, Error, ValidationError]]:
    r""" Watch for remote statuses

     Returns all public statuses from remote servers.

    Version history:

    3.1.4 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        only_media (Union[Unset, bool]): If true, return only statuses with media attachments.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, ValidationError]]
     """

    kwargs = _get_kwargs(
        only_media=only_media,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    only_media: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, Error, ValidationError]]:
    r""" Watch for remote statuses

     Returns all public statuses from remote servers.

    Version history:

    3.1.4 - added\
    3.5.0 - now returns `status.update`\
    4.2.0 - changed to require a User token, removing Public and App token access [#23989]

    Args:
        only_media (Union[Unset, bool]): If true, return only statuses with media attachments.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
            only_media=only_media,
        )
    ).parsed
