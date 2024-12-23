from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.performer import Performer
from ...types import UNSET, Response


def _get_kwargs(
    *,
    zone_id: UUID,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_zone_id = str(zone_id)
    params["zone_id"] = json_zone_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/performers/nearest",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, List["Performer"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Performer.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, List["Performer"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    zone_id: UUID,
) -> Response[Union[HTTPValidationError, List["Performer"]]]:
    """Get Nearest

     Получить список ближайших к зоне исполнителей.

    Args:
        zone_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['Performer']]]
    """

    kwargs = _get_kwargs(
        zone_id=zone_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    zone_id: UUID,
) -> Optional[Union[HTTPValidationError, List["Performer"]]]:
    """Get Nearest

     Получить список ближайших к зоне исполнителей.

    Args:
        zone_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['Performer']]
    """

    return sync_detailed(
        client=client,
        zone_id=zone_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    zone_id: UUID,
) -> Response[Union[HTTPValidationError, List["Performer"]]]:
    """Get Nearest

     Получить список ближайших к зоне исполнителей.

    Args:
        zone_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, List['Performer']]]
    """

    kwargs = _get_kwargs(
        zone_id=zone_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    zone_id: UUID,
) -> Optional[Union[HTTPValidationError, List["Performer"]]]:
    """Get Nearest

     Получить список ближайших к зоне исполнителей.

    Args:
        zone_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, List['Performer']]
    """

    return (
        await asyncio_detailed(
            client=client,
            zone_id=zone_id,
        )
    ).parsed
