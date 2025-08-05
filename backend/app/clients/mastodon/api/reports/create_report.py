from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_report_body import CreateReportBody
from ...models.error import Error
from ...models.report import Report
from ...types import Response


def _get_kwargs(
    *,
    body: CreateReportBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/reports",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Error, Report]]:
    if response.status_code == 200:
        response_200 = Report.from_dict(response.json())

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
) -> Response[Union[Any, Error, Report]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateReportBody,
) -> Response[Union[Any, Error, Report]]:
    r""" File a report

     Report problematic accounts and contents to your moderators.

    Version history:

    1.1 - added\
    2.3.0 - add `forward` parameter\
    3.5.0 - add `category` and `rule_ids` parameters\
    4.0.0 - `category` is now optional if `rule_ids` is provided\
    4.2.0 - add `legal` category

    Args:
        body (CreateReportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Report]]
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
    body: CreateReportBody,
) -> Optional[Union[Any, Error, Report]]:
    r""" File a report

     Report problematic accounts and contents to your moderators.

    Version history:

    1.1 - added\
    2.3.0 - add `forward` parameter\
    3.5.0 - add `category` and `rule_ids` parameters\
    4.0.0 - `category` is now optional if `rule_ids` is provided\
    4.2.0 - add `legal` category

    Args:
        body (CreateReportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Report]
     """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateReportBody,
) -> Response[Union[Any, Error, Report]]:
    r""" File a report

     Report problematic accounts and contents to your moderators.

    Version history:

    1.1 - added\
    2.3.0 - add `forward` parameter\
    3.5.0 - add `category` and `rule_ids` parameters\
    4.0.0 - `category` is now optional if `rule_ids` is provided\
    4.2.0 - add `legal` category

    Args:
        body (CreateReportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Error, Report]]
     """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateReportBody,
) -> Optional[Union[Any, Error, Report]]:
    r""" File a report

     Report problematic accounts and contents to your moderators.

    Version history:

    1.1 - added\
    2.3.0 - add `forward` parameter\
    3.5.0 - add `category` and `rule_ids` parameters\
    4.0.0 - `category` is now optional if `rule_ids` is provided\
    4.2.0 - add `legal` category

    Args:
        body (CreateReportBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Error, Report]
     """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
