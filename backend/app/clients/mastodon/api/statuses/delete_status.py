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
    delete_media: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["delete_media"] = delete_media

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/v1/statuses/{id}".format(
            id=id,
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Status, ValidationError]]:
    if response.status_code == 200:
        response_200 = Status.from_dict(response.json())

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
) -> Response[Union[Any, Error, Status, ValidationError]]:
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
    delete_media: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, Error, Status, ValidationError]]:
    r""" Delete a status

     Delete one of your own statuses.

    Version history:

    0.0.0 - added\
    2.9.0 - return source properties, for use with delete and redraft\
    4.4.0 (`mastodon` [API version] 4) - added `delete_media` optional parameter

    Args:
        id (str):
        delete_media (Union[Unset, bool]): Whether to immediately delete the post's media
            attachments. If omitted or `false`, media attachments may be kept for approximately 24
            hours so they can be re-used in a new post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Status, ValidationError]]
     """

    kwargs = _get_kwargs(
        id=id,
        delete_media=delete_media,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    delete_media: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, Error, Status, ValidationError]]:
    r""" Delete a status

     Delete one of your own statuses.

    Version history:

    0.0.0 - added\
    2.9.0 - return source properties, for use with delete and redraft\
    4.4.0 (`mastodon` [API version] 4) - added `delete_media` optional parameter

    Args:
        id (str):
        delete_media (Union[Unset, bool]): Whether to immediately delete the post's media
            attachments. If omitted or `false`, media attachments may be kept for approximately 24
            hours so they can be re-used in a new post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Status, ValidationError]
     """

    return sync_detailed(
        id=id,
        client=client,
        delete_media=delete_media,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    delete_media: Union[Unset, bool] = UNSET,
) -> Response[Union[Any, Error, Status, ValidationError]]:
    r""" Delete a status

     Delete one of your own statuses.

    Version history:

    0.0.0 - added\
    2.9.0 - return source properties, for use with delete and redraft\
    4.4.0 (`mastodon` [API version] 4) - added `delete_media` optional parameter

    Args:
        id (str):
        delete_media (Union[Unset, bool]): Whether to immediately delete the post's media
            attachments. If omitted or `false`, media attachments may be kept for approximately 24
            hours so they can be re-used in a new post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Status, ValidationError]]
     """

    kwargs = _get_kwargs(
        id=id,
        delete_media=delete_media,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    delete_media: Union[Unset, bool] = UNSET,
) -> Optional[Union[Any, Error, Status, ValidationError]]:
    r""" Delete a status

     Delete one of your own statuses.

    Version history:

    0.0.0 - added\
    2.9.0 - return source properties, for use with delete and redraft\
    4.4.0 (`mastodon` [API version] 4) - added `delete_media` optional parameter

    Args:
        id (str):
        delete_media (Union[Unset, bool]): Whether to immediately delete the post's media
            attachments. If omitted or `false`, media attachments may be kept for approximately 24
            hours so they can be re-used in a new post.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Status, ValidationError]
     """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            delete_media=delete_media,
        )
    ).parsed
