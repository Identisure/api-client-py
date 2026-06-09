from __future__ import annotations

import time
import asyncio
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from idkollen_client._client import IdkollenError, PollOptions
from idkollen_client.models.age_verification import AgeVerificationRequest, AgeVerificationStatus
from idkollen_client.models.mitid import (
    MitIdAuthRequest,
    MitIdBackchannelAuthRequest,
    MitIdSignRequest,
    MitIdStatus,
)

if TYPE_CHECKING:
    from idkollen_client._client import IdkollenClient, AsyncIdkollenClient

_status_adapter: TypeAdapter[MitIdStatus] = TypeAdapter(MitIdStatus)
_age_adapter: TypeAdapter[AgeVerificationStatus] = TypeAdapter(AgeVerificationStatus)


class MitIdEndpoint:
    def __init__(self, client: "IdkollenClient") -> None:
        self._client = client

    def auth(self, req: MitIdAuthRequest) -> MitIdStatus:
        return self._client._post("/v3/mitid/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def backchannel_auth(self, req: MitIdBackchannelAuthRequest) -> MitIdStatus:
        return self._client._post("/v3/mitid/backchannel/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def sign(self, req: MitIdSignRequest) -> MitIdStatus:
        return self._client._post("/v3/mitid/sign", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def auth_status(self, id: str) -> MitIdStatus:
        return self._client._get(f"/v3/mitid/auth/{id}", _status_adapter)

    def sign_status(self, id: str) -> MitIdStatus:
        return self._client._get(f"/v3/mitid/sign/{id}", _status_adapter)

    def cancel_auth(self, id: str) -> None:
        return self._client._delete(f"/v3/mitid/auth/{id}")

    def cancel_sign(self, id: str) -> None:
        return self._client._delete(f"/v3/mitid/sign/{id}")

    def age_verification(self, req: AgeVerificationRequest) -> AgeVerificationStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/mitid/age-verification", body, _age_adapter)

    def age_verification_status(self, id: str) -> AgeVerificationStatus:
        return self._client._get(f"/v3/mitid/age-verification/{id}", _age_adapter)

    def cancel_age_verification(self, id: str) -> None:
        return self._client._delete(f"/v3/mitid/age-verification/{id}")

    def wait_for_age_verification(self, id: str, opts: PollOptions = PollOptions()) -> AgeVerificationStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.age_verification_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)

    def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> MitIdStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)

    def wait_for_sign(self, id: str, opts: PollOptions = PollOptions()) -> MitIdStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.sign_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)


class AsyncMitIdEndpoint:
    def __init__(self, client: "AsyncIdkollenClient") -> None:
        self._client = client

    async def auth(self, req: MitIdAuthRequest) -> MitIdStatus:
        return await self._client._post("/v3/mitid/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def backchannel_auth(self, req: MitIdBackchannelAuthRequest) -> MitIdStatus:
        return await self._client._post("/v3/mitid/backchannel/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def sign(self, req: MitIdSignRequest) -> MitIdStatus:
        return await self._client._post("/v3/mitid/sign", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def auth_status(self, id: str) -> MitIdStatus:
        return await self._client._get(f"/v3/mitid/auth/{id}", _status_adapter)

    async def sign_status(self, id: str) -> MitIdStatus:
        return await self._client._get(f"/v3/mitid/sign/{id}", _status_adapter)

    async def cancel_auth(self, id: str) -> None:
        return await self._client._delete(f"/v3/mitid/auth/{id}")

    async def cancel_sign(self, id: str) -> None:
        return await self._client._delete(f"/v3/mitid/sign/{id}")

    async def age_verification(self, req: AgeVerificationRequest) -> AgeVerificationStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/mitid/age-verification", body, _age_adapter)

    async def age_verification_status(self, id: str) -> AgeVerificationStatus:
        return await self._client._get(f"/v3/mitid/age-verification/{id}", _age_adapter)

    async def cancel_age_verification(self, id: str) -> None:
        return await self._client._delete(f"/v3/mitid/age-verification/{id}")

    async def wait_for_age_verification(self, id: str, opts: PollOptions = PollOptions()) -> AgeVerificationStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.age_verification_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)

    async def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> MitIdStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)

    async def wait_for_sign(self, id: str, opts: PollOptions = PollOptions()) -> MitIdStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.sign_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)
