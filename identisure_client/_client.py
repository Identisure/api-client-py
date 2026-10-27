from __future__ import annotations

import time
import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, TypeVar

if TYPE_CHECKING:
    from identisure_client.endpoints.bankid_se import BankIdSeEndpoint, AsyncBankIdSeEndpoint
    from identisure_client.endpoints.bankid_no import BankIdNoEndpoint, AsyncBankIdNoEndpoint
    from identisure_client.endpoints.freja import FrejaEndpoint, AsyncFrejaEndpoint
    from identisure_client.endpoints.mitid import MitIdEndpoint, AsyncMitIdEndpoint
    from identisure_client.endpoints.ftn import FtnEndpoint, AsyncFtnEndpoint
    from identisure_client.endpoints.vipps import VippsEndpoint, AsyncVippsEndpoint
    from identisure_client.endpoints.document import DocumentEndpoint, AsyncDocumentEndpoint

import httpx
from pydantic import TypeAdapter

T = TypeVar("T")

_PRODUCTION_URL = "https://api.identisure.com"
_STAGING_URL = "https://stgapi.identisure.com"


class IdentisureError(Exception):
    def __init__(
        self,
        code: Literal["http", "api", "poll_timeout", "json"],
        status: int,
        message: str,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status = status
        self.message = message


@dataclass(frozen=True)
class PollOptions:
    interval: float = 2.0
    timeout: float = 300.0


class IdentisureClientBuilder:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url: str | None = None
        self._user_agent = "identisure-client-py/0.1.0"
        self._timeout = 30.0

    def environment(self, env: Literal["production", "staging"]) -> IdentisureClientBuilder:
        if env == "staging":
            self._base_url = _STAGING_URL
        else:
            self._base_url = _PRODUCTION_URL
        return self

    def base_url(self, url: str) -> IdentisureClientBuilder:
        self._base_url = url.rstrip("/")
        return self

    def user_agent(self, ua: str) -> IdentisureClientBuilder:
        self._user_agent = ua
        return self

    def timeout(self, seconds: float) -> IdentisureClientBuilder:
        """Set the timeout for each HTTP request, in seconds. Must be positive. Default: 30."""
        self._timeout = seconds
        return self

    def build(self) -> IdentisureClient:
        return IdentisureClient(
            base_url=self._base_url or _PRODUCTION_URL,
            client_id=self._client_id,
            client_secret=self._client_secret,
            user_agent=self._user_agent,
            timeout=self._timeout,
        )

    def build_async(self) -> AsyncIdentisureClient:
        return AsyncIdentisureClient(
            base_url=self._base_url or _PRODUCTION_URL,
            client_id=self._client_id,
            client_secret=self._client_secret,
            user_agent=self._user_agent,
            timeout=self._timeout,
        )


class IdentisureClient:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        user_agent: str,
        timeout: float,
    ) -> None:
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_agent = user_agent
        self._http = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> IdentisureClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _headers(self) -> dict[str, str]:
        return {"User-Agent": self._user_agent}

    def _auth(self) -> tuple[str, str]:
        return (self._client_id, self._client_secret)

    def _get(self, path: str, adapter: TypeAdapter[T]) -> T:
        try:
            resp = self._http.get(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    def _post(self, path: str, body: Any, adapter: TypeAdapter[T]) -> T:
        try:
            resp = self._http.post(
                self._base_url + path,
                json=body,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    def _delete(self, path: str) -> None:
        try:
            resp = self._http.delete(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdentisureError("api", resp.status_code, _error_message(resp))

    def _post_multipart(self, path: str, files: dict[str, Any], adapter: TypeAdapter[T]) -> T:
        try:
            resp = self._http.post(
                self._base_url + path,
                files=files,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    def _get_bytes(self, path: str) -> bytes:
        try:
            resp = self._http.get(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdentisureError("api", resp.status_code, _error_message(resp))
        return resp.content

    def bankid_se(self) -> "BankIdSeEndpoint":
        from identisure_client.endpoints.bankid_se import BankIdSeEndpoint
        return BankIdSeEndpoint(self)

    def bankid_no(self) -> "BankIdNoEndpoint":
        from identisure_client.endpoints.bankid_no import BankIdNoEndpoint
        return BankIdNoEndpoint(self)

    def freja(self) -> "FrejaEndpoint":
        from identisure_client.endpoints.freja import FrejaEndpoint
        return FrejaEndpoint(self)

    def mitid(self) -> "MitIdEndpoint":
        from identisure_client.endpoints.mitid import MitIdEndpoint
        return MitIdEndpoint(self)

    def ftn(self) -> "FtnEndpoint":
        from identisure_client.endpoints.ftn import FtnEndpoint
        return FtnEndpoint(self)

    def vipps(self) -> "VippsEndpoint":
        from identisure_client.endpoints.vipps import VippsEndpoint
        return VippsEndpoint(self)

    def document(self) -> "DocumentEndpoint":
        from identisure_client.endpoints.document import DocumentEndpoint
        return DocumentEndpoint(self)


class AsyncIdentisureClient:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        user_agent: str,
        timeout: float,
    ) -> None:
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_agent = user_agent
        self._http = httpx.AsyncClient(timeout=timeout)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncIdentisureClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    def _headers(self) -> dict[str, str]:
        return {"User-Agent": self._user_agent}

    def _auth(self) -> tuple[str, str]:
        return (self._client_id, self._client_secret)

    async def _get(self, path: str, adapter: TypeAdapter[T]) -> T:
        try:
            resp = await self._http.get(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    async def _post(self, path: str, body: Any, adapter: TypeAdapter[T]) -> T:
        try:
            resp = await self._http.post(
                self._base_url + path,
                json=body,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    async def _delete(self, path: str) -> None:
        try:
            resp = await self._http.delete(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdentisureError("api", resp.status_code, _error_message(resp))

    async def _post_multipart(self, path: str, files: dict[str, Any], adapter: TypeAdapter[T]) -> T:
        try:
            resp = await self._http.post(
                self._base_url + path,
                files=files,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    async def _get_bytes(self, path: str) -> bytes:
        try:
            resp = await self._http.get(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdentisureError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdentisureError("api", resp.status_code, _error_message(resp))
        return resp.content

    def bankid_se(self) -> "AsyncBankIdSeEndpoint":
        from identisure_client.endpoints.bankid_se import AsyncBankIdSeEndpoint
        return AsyncBankIdSeEndpoint(self)

    def bankid_no(self) -> "AsyncBankIdNoEndpoint":
        from identisure_client.endpoints.bankid_no import AsyncBankIdNoEndpoint
        return AsyncBankIdNoEndpoint(self)

    def freja(self) -> "AsyncFrejaEndpoint":
        from identisure_client.endpoints.freja import AsyncFrejaEndpoint
        return AsyncFrejaEndpoint(self)

    def mitid(self) -> "AsyncMitIdEndpoint":
        from identisure_client.endpoints.mitid import AsyncMitIdEndpoint
        return AsyncMitIdEndpoint(self)

    def ftn(self) -> "AsyncFtnEndpoint":
        from identisure_client.endpoints.ftn import AsyncFtnEndpoint
        return AsyncFtnEndpoint(self)

    def vipps(self) -> "AsyncVippsEndpoint":
        from identisure_client.endpoints.vipps import AsyncVippsEndpoint
        return AsyncVippsEndpoint(self)

    def document(self) -> "AsyncDocumentEndpoint":
        from identisure_client.endpoints.document import AsyncDocumentEndpoint
        return AsyncDocumentEndpoint(self)


def _parse_response(resp: httpx.Response, adapter: TypeAdapter[T]) -> T:
    if resp.is_success:
        try:
            return adapter.validate_json(resp.content)
        except Exception as exc:
            raise IdentisureError("json", 0, str(exc)) from exc
    raise IdentisureError("api", resp.status_code, _error_message(resp))


def _error_message(resp: httpx.Response) -> str:
    try:
        body = resp.json()
    except ValueError:
        return resp.text
    if isinstance(body, dict) and isinstance(body.get("message"), str):
        return body["message"]
    return resp.text
