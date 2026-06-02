from __future__ import annotations

import time
import asyncio
from dataclasses import dataclass
from typing import Any, Literal, TypeVar

import httpx
from pydantic import TypeAdapter

T = TypeVar("T")

_PRODUCTION_URL = "https://api.idkollen.se"
_STAGING_URL = "https://stgapi.idkollen.se"


class IdkollenError(Exception):
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


@dataclass
class PollOptions:
    interval: float = 2.0
    timeout: float = 300.0


class IdkollenClientBuilder:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._base_url: str | None = None
        self._user_agent = "idkollen-client-py/0.1.0"

    def environment(self, env: Literal["production", "staging"]) -> IdkollenClientBuilder:
        if env == "staging":
            self._base_url = _STAGING_URL
        else:
            self._base_url = _PRODUCTION_URL
        return self

    def base_url(self, url: str) -> IdkollenClientBuilder:
        self._base_url = url
        return self

    def user_agent(self, ua: str) -> IdkollenClientBuilder:
        self._user_agent = ua
        return self

    def build(self) -> IdkollenClient:
        return IdkollenClient(
            base_url=self._base_url or _PRODUCTION_URL,
            client_id=self._client_id,
            client_secret=self._client_secret,
            user_agent=self._user_agent,
        )

    def build_async(self) -> AsyncIdkollenClient:
        return AsyncIdkollenClient(
            base_url=self._base_url or _PRODUCTION_URL,
            client_id=self._client_id,
            client_secret=self._client_secret,
            user_agent=self._user_agent,
        )


class IdkollenClient:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        user_agent: str,
    ) -> None:
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_agent = user_agent
        self._http = httpx.Client(timeout=30.0)

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
            raise IdkollenError("http", 0, str(exc)) from exc
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
            raise IdkollenError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    def _delete(self, path: str) -> None:
        try:
            resp = self._http.delete(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdkollenError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdkollenError("api", resp.status_code, resp.text)

    def _post_multipart(self, path: str, files: dict[str, Any], adapter: TypeAdapter[T]) -> T:
        try:
            resp = self._http.post(
                self._base_url + path,
                files=files,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdkollenError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    def _get_bytes(self, path: str) -> bytes:
        try:
            resp = self._http.get(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdkollenError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdkollenError("api", resp.status_code, resp.text)
        return resp.content

    def bankid_se(self) -> "BankIdSeEndpoint":
        from idkollen_client.endpoints.bankid_se import BankIdSeEndpoint
        return BankIdSeEndpoint(self)

    def bankid_no(self) -> "BankIdNoEndpoint":
        from idkollen_client.endpoints.bankid_no import BankIdNoEndpoint
        return BankIdNoEndpoint(self)

    def freja(self) -> "FrejaEndpoint":
        from idkollen_client.endpoints.freja import FrejaEndpoint
        return FrejaEndpoint(self)

    def mitid(self) -> "MitIdEndpoint":
        from idkollen_client.endpoints.mitid import MitIdEndpoint
        return MitIdEndpoint(self)

    def ftn(self) -> "FtnEndpoint":
        from idkollen_client.endpoints.ftn import FtnEndpoint
        return FtnEndpoint(self)

    def vipps(self) -> "VippsEndpoint":
        from idkollen_client.endpoints.vipps import VippsEndpoint
        return VippsEndpoint(self)

    def document(self) -> "DocumentEndpoint":
        from idkollen_client.endpoints.document import DocumentEndpoint
        return DocumentEndpoint(self)


class AsyncIdkollenClient:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        user_agent: str,
    ) -> None:
        self._base_url = base_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._user_agent = user_agent
        self._http = httpx.AsyncClient(timeout=30.0)

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
            raise IdkollenError("http", 0, str(exc)) from exc
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
            raise IdkollenError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    async def _delete(self, path: str) -> None:
        try:
            resp = await self._http.delete(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdkollenError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdkollenError("api", resp.status_code, resp.text)

    async def _post_multipart(self, path: str, files: dict[str, Any], adapter: TypeAdapter[T]) -> T:
        try:
            resp = await self._http.post(
                self._base_url + path,
                files=files,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdkollenError("http", 0, str(exc)) from exc
        return _parse_response(resp, adapter)

    async def _get_bytes(self, path: str) -> bytes:
        try:
            resp = await self._http.get(
                self._base_url + path,
                auth=self._auth(),
                headers=self._headers(),
            )
        except httpx.HTTPError as exc:
            raise IdkollenError("http", 0, str(exc)) from exc
        if not resp.is_success:
            raise IdkollenError("api", resp.status_code, resp.text)
        return resp.content

    def bankid_se(self) -> "AsyncBankIdSeEndpoint":
        from idkollen_client.endpoints.bankid_se import AsyncBankIdSeEndpoint
        return AsyncBankIdSeEndpoint(self)

    def bankid_no(self) -> "AsyncBankIdNoEndpoint":
        from idkollen_client.endpoints.bankid_no import AsyncBankIdNoEndpoint
        return AsyncBankIdNoEndpoint(self)

    def freja(self) -> "AsyncFrejaEndpoint":
        from idkollen_client.endpoints.freja import AsyncFrejaEndpoint
        return AsyncFrejaEndpoint(self)

    def mitid(self) -> "AsyncMitIdEndpoint":
        from idkollen_client.endpoints.mitid import AsyncMitIdEndpoint
        return AsyncMitIdEndpoint(self)

    def ftn(self) -> "AsyncFtnEndpoint":
        from idkollen_client.endpoints.ftn import AsyncFtnEndpoint
        return AsyncFtnEndpoint(self)

    def vipps(self) -> "AsyncVippsEndpoint":
        from idkollen_client.endpoints.vipps import AsyncVippsEndpoint
        return AsyncVippsEndpoint(self)

    def document(self) -> "AsyncDocumentEndpoint":
        from idkollen_client.endpoints.document import AsyncDocumentEndpoint
        return AsyncDocumentEndpoint(self)


def _parse_response(resp: httpx.Response, adapter: TypeAdapter[T]) -> T:
    if resp.is_success:
        try:
            return adapter.validate_json(resp.content)
        except Exception as exc:
            raise IdkollenError("json", 0, str(exc)) from exc
    raise IdkollenError("api", resp.status_code, resp.text)
