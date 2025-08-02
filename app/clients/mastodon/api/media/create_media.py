from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_media_body import CreateMediaBody
from ...models.error import Error
from ...models.media_attachment import MediaAttachment
from ...types import Response


def _get_kwargs(
    *,
    body: CreateMediaBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/media",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, MediaAttachment]]:
    if response.status_code == 200:
        response_200 = MediaAttachment.from_dict(response.json())

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
) -> Response[Union[Any, Error, MediaAttachment]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateMediaBody,
) -> Response[Union[Any, Error, MediaAttachment]]:
    r""" Upload media as an attachment (v1)

     Creates an attachment to be used with a new status. This method will return after the full sized
    media is done processing.

    Version history:

    0.0.0 - added\
    2.3.0 - add `focus` parameter\
    3.1.3 - deprecated in favor of [POST /api/v2/media], which is equal to v1 in all aspects, except it
    returns HTTP 202, and the returned JSON object has a url of null. This is because while the
    thumbnail is prepared synchronously, the full version of the media attachment will be processed in
    the background.\
    3.2.0 - add `thumbnail` parameter

    Args:
        body (CreateMediaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, MediaAttachment]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateMediaBody,
) -> Optional[Union[Any, Error, MediaAttachment]]:
    r""" Upload media as an attachment (v1)

     Creates an attachment to be used with a new status. This method will return after the full sized
    media is done processing.

    Version history:

    0.0.0 - added\
    2.3.0 - add `focus` parameter\
    3.1.3 - deprecated in favor of [POST /api/v2/media], which is equal to v1 in all aspects, except it
    returns HTTP 202, and the returned JSON object has a url of null. This is because while the
    thumbnail is prepared synchronously, the full version of the media attachment will be processed in
    the background.\
    3.2.0 - add `thumbnail` parameter

    Args:
        body (CreateMediaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, MediaAttachment]
     """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateMediaBody,
) -> Response[Union[Any, Error, MediaAttachment]]:
    r""" Upload media as an attachment (v1)

     Creates an attachment to be used with a new status. This method will return after the full sized
    media is done processing.

    Version history:

    0.0.0 - added\
    2.3.0 - add `focus` parameter\
    3.1.3 - deprecated in favor of [POST /api/v2/media], which is equal to v1 in all aspects, except it
    returns HTTP 202, and the returned JSON object has a url of null. This is because while the
    thumbnail is prepared synchronously, the full version of the media attachment will be processed in
    the background.\
    3.2.0 - add `thumbnail` parameter

    Args:
        body (CreateMediaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, MediaAttachment]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateMediaBody,
) -> Optional[Union[Any, Error, MediaAttachment]]:
    r""" Upload media as an attachment (v1)

     Creates an attachment to be used with a new status. This method will return after the full sized
    media is done processing.

    Version history:

    0.0.0 - added\
    2.3.0 - add `focus` parameter\
    3.1.3 - deprecated in favor of [POST /api/v2/media], which is equal to v1 in all aspects, except it
    returns HTTP 202, and the returned JSON object has a url of null. This is because while the
    thumbnail is prepared synchronously, the full version of the media attachment will be processed in
    the background.\
    3.2.0 - add `thumbnail` parameter

    Args:
        body (CreateMediaBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, MediaAttachment]
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
