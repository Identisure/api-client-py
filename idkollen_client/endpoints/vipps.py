from __future__ import annotations

import time
import asyncio
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from idkollen_client._client import IdkollenError, PollOptions
from idkollen_client.models.vipps import VippsAuthRequest, VippsBackchannelAuthRequest, VippsStatus

if TYPE_CHECKING:
    from idkollen_client._client import IdkollenClient, AsyncIdkollenClient

_status_adapter: TypeAdapter[VippsStatus] = TypeAdapter(VippsStatus)


class VippsEndpoint:
    def __init__(self, client: "IdkollenClient") -> None:
        self._client = client

    def auth(self, req: VippsAuthRequest) -> VippsStatus:
        return self._client._post("/v3/vipps/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def backchannel_auth(self, req: VippsBackchannelAuthRequest) -> VippsStatus:
        return self._client._post("/v3/vipps/backchannel/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def auth_status(self, id: str) -> VippsStatus:
        return self._client._get(f"/v3/vipps/auth/{id}", _status_adapter)

    def cancel_auth(self, id: str) -> None:
        return self._client._delete(f"/v3/vipps/auth/{id}")

    def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> VippsStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)


class AsyncVippsEndpoint:
    def __init__(self, client: "AsyncIdkollenClient") -> None:
        self._client = client

    async def auth(self, req: VippsAuthRequest) -> VippsStatus:
        return await self._client._post("/v3/vipps/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def backchannel_auth(self, req: VippsBackchannelAuthRequest) -> VippsStatus:
        return await self._client._post("/v3/vipps/backchannel/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def auth_status(self, id: str) -> VippsStatus:
        return await self._client._get(f"/v3/vipps/auth/{id}", _status_adapter)

    async def cancel_auth(self, id: str) -> None:
        return await self._client._delete(f"/v3/vipps/auth/{id}")

    async def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> VippsStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)
