from __future__ import annotations

import time
import asyncio
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from idkollen_client._client import IdkollenError, PollOptions
from idkollen_client.models.age_verification import AgeVerificationRequest, AgeVerificationStatus
from idkollen_client.models.bankid_no import (
    BankIdNoAuthRequest,
    BankIdNoBackchannelAuthRequest,
    BankIdNoSignRequest,
    BankIdNoStatus,
)

if TYPE_CHECKING:
    from idkollen_client._client import IdkollenClient, AsyncIdkollenClient

_status_adapter: TypeAdapter[BankIdNoStatus] = TypeAdapter(BankIdNoStatus)
_age_adapter: TypeAdapter[AgeVerificationStatus] = TypeAdapter(AgeVerificationStatus)


class BankIdNoEndpoint:
    def __init__(self, client: "IdkollenClient") -> None:
        self._client = client

    def auth(self, req: BankIdNoAuthRequest) -> BankIdNoStatus:
        return self._client._post("/v3/bankid-no/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def backchannel_auth(self, req: BankIdNoBackchannelAuthRequest) -> BankIdNoStatus:
        return self._client._post("/v3/bankid-no/backchannel/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def sign(self, req: BankIdNoSignRequest) -> BankIdNoStatus:
        return self._client._post("/v3/bankid-no/sign", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    def auth_status(self, id: str) -> BankIdNoStatus:
        return self._client._get(f"/v3/bankid-no/auth/{id}", _status_adapter)

    def sign_status(self, id: str) -> BankIdNoStatus:
        return self._client._get(f"/v3/bankid-no/sign/{id}", _status_adapter)

    def cancel_auth(self, id: str) -> None:
        return self._client._delete(f"/v3/bankid-no/auth/{id}")

    def cancel_sign(self, id: str) -> None:
        return self._client._delete(f"/v3/bankid-no/sign/{id}")

    def age_verification(self, req: AgeVerificationRequest) -> AgeVerificationStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/bankid-no/age-verification", body, _age_adapter)

    def age_verification_status(self, id: str) -> AgeVerificationStatus:
        return self._client._get(f"/v3/bankid-no/age-verification/{id}", _age_adapter)

    def cancel_age_verification(self, id: str) -> None:
        return self._client._delete(f"/v3/bankid-no/age-verification/{id}")

    def wait_for_age_verification(self, id: str, opts: PollOptions = PollOptions()) -> AgeVerificationStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.age_verification_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)

    def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> BankIdNoStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)

    def wait_for_sign(self, id: str, opts: PollOptions = PollOptions()) -> BankIdNoStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.sign_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)


class AsyncBankIdNoEndpoint:
    def __init__(self, client: "AsyncIdkollenClient") -> None:
        self._client = client

    async def auth(self, req: BankIdNoAuthRequest) -> BankIdNoStatus:
        return await self._client._post("/v3/bankid-no/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def backchannel_auth(self, req: BankIdNoBackchannelAuthRequest) -> BankIdNoStatus:
        return await self._client._post("/v3/bankid-no/backchannel/auth", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def sign(self, req: BankIdNoSignRequest) -> BankIdNoStatus:
        return await self._client._post("/v3/bankid-no/sign", req.model_dump(mode="json", by_alias=True, exclude_none=True), _status_adapter)

    async def auth_status(self, id: str) -> BankIdNoStatus:
        return await self._client._get(f"/v3/bankid-no/auth/{id}", _status_adapter)

    async def sign_status(self, id: str) -> BankIdNoStatus:
        return await self._client._get(f"/v3/bankid-no/sign/{id}", _status_adapter)

    async def cancel_auth(self, id: str) -> None:
        return await self._client._delete(f"/v3/bankid-no/auth/{id}")

    async def cancel_sign(self, id: str) -> None:
        return await self._client._delete(f"/v3/bankid-no/sign/{id}")

    async def age_verification(self, req: AgeVerificationRequest) -> AgeVerificationStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/bankid-no/age-verification", body, _age_adapter)

    async def age_verification_status(self, id: str) -> AgeVerificationStatus:
        return await self._client._get(f"/v3/bankid-no/age-verification/{id}", _age_adapter)

    async def cancel_age_verification(self, id: str) -> None:
        return await self._client._delete(f"/v3/bankid-no/age-verification/{id}")

    async def wait_for_age_verification(self, id: str, opts: PollOptions = PollOptions()) -> AgeVerificationStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.age_verification_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)

    async def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> BankIdNoStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)

    async def wait_for_sign(self, id: str, opts: PollOptions = PollOptions()) -> BankIdNoStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.sign_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)
