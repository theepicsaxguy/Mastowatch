from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error import Error
from ...models.v1_instance import V1Instance
from ...models.validation_error import ValidationError
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/instance",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, V1Instance, ValidationError]]:
    if response.status_code == 200:
        response_200 = V1Instance.from_dict(response.json())

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
) -> Response[Union[Any, Error, V1Instance, ValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error, V1Instance, ValidationError]]:
    r""" View server information (v1)

     Obtain general information about the server. See [api/v2/instance]({{< relref
    \"methods/Instance#v2\">}}) instead.

    Version history:

    1.1.0 - added\
    3.0.0 - requires user token if instance is in whitelist mode\
    3.1.4 - added `invites_enabled` to response\
    3.4.0 - added `rules`\
    3.4.2 - added `configuration`\
    4.0.0 - deprecated. added `configuration[accounts]`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, V1Instance, ValidationError]]
     """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error, V1Instance, ValidationError]]:
    r""" View server information (v1)

     Obtain general information about the server. See [api/v2/instance]({{< relref
    \"methods/Instance#v2\">}}) instead.

    Version history:

    1.1.0 - added\
    3.0.0 - requires user token if instance is in whitelist mode\
    3.1.4 - added `invites_enabled` to response\
    3.4.0 - added `rules`\
    3.4.2 - added `configuration`\
    4.0.0 - deprecated. added `configuration[accounts]`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, V1Instance, ValidationError]
     """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[Any, Error, V1Instance, ValidationError]]:
    r""" View server information (v1)

     Obtain general information about the server. See [api/v2/instance]({{< relref
    \"methods/Instance#v2\">}}) instead.

    Version history:

    1.1.0 - added\
    3.0.0 - requires user token if instance is in whitelist mode\
    3.1.4 - added `invites_enabled` to response\
    3.4.0 - added `rules`\
    3.4.2 - added `configuration`\
    4.0.0 - deprecated. added `configuration[accounts]`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, V1Instance, ValidationError]]
     """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[Any, Error, V1Instance, ValidationError]]:
    r""" View server information (v1)

     Obtain general information about the server. See [api/v2/instance]({{< relref
    \"methods/Instance#v2\">}}) instead.

    Version history:

    1.1.0 - added\
    3.0.0 - requires user token if instance is in whitelist mode\
    3.1.4 - added `invites_enabled` to response\
    3.4.0 - added `rules`\
    3.4.2 - added `configuration`\
    4.0.0 - deprecated. added `configuration[accounts]`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, V1Instance, ValidationError]
     """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
