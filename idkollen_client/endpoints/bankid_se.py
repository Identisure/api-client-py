from __future__ import annotations

import time
import asyncio
from typing import TYPE_CHECKING

from pydantic import TypeAdapter

from idkollen_client._client import IdkollenError, PollOptions
from idkollen_client.models.age_verification import AgeVerificationRequest, AgeVerificationStatus
from idkollen_client.models.bankid_se import (
    BankIdSeAuthRequest,
    BankIdSePhoneAuthRequest,
    BankIdSePhoneSignRequest,
    BankIdSeSignRequest,
    BankIdSeStatus,
    BankIdSeVerifyRequest,
    BankIdSeVerifyResponse,
)

if TYPE_CHECKING:
    from idkollen_client._client import IdkollenClient, AsyncIdkollenClient

_status_adapter: TypeAdapter[BankIdSeStatus] = TypeAdapter(BankIdSeStatus)
_verify_adapter: TypeAdapter[BankIdSeVerifyResponse] = TypeAdapter(BankIdSeVerifyResponse)
_age_adapter: TypeAdapter[AgeVerificationStatus] = TypeAdapter(AgeVerificationStatus)


class BankIdSeEndpoint:
    def __init__(self, client: "IdkollenClient") -> None:
        self._client = client

    def auth(self, req: BankIdSeAuthRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/bankid-se/auth", body, _status_adapter)

    def phone_auth(self, req: BankIdSePhoneAuthRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/bankid-se/phone/auth", body, _status_adapter)

    def sign(self, req: BankIdSeSignRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/bankid-se/sign", body, _status_adapter)

    def phone_sign(self, req: BankIdSePhoneSignRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/bankid-se/phone/sign", body, _status_adapter)

    def verify(self, req: BankIdSeVerifyRequest) -> BankIdSeVerifyResponse:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/bankid-se/verify", body, _verify_adapter)

    def age_verification(self, req: AgeVerificationRequest) -> AgeVerificationStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return self._client._post("/v3/bankid-se/age-verification", body, _age_adapter)

    def auth_status(self, id: str) -> BankIdSeStatus:
        return self._client._get(f"/v3/bankid-se/auth/{id}", _status_adapter)

    def sign_status(self, id: str) -> BankIdSeStatus:
        return self._client._get(f"/v3/bankid-se/sign/{id}", _status_adapter)

    def age_verification_status(self, id: str) -> AgeVerificationStatus:
        return self._client._get(f"/v3/bankid-se/age-verification/{id}", _age_adapter)

    def cancel_auth(self, id: str) -> None:
        return self._client._delete(f"/v3/bankid-se/auth/{id}")

    def cancel_sign(self, id: str) -> None:
        return self._client._delete(f"/v3/bankid-se/sign/{id}")

    def cancel_age_verification(self, id: str) -> None:
        return self._client._delete(f"/v3/bankid-se/age-verification/{id}")

    def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> BankIdSeStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)

    def wait_for_sign(self, id: str, opts: PollOptions = PollOptions()) -> BankIdSeStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.sign_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)

    def wait_for_age_verification(self, id: str, opts: PollOptions = PollOptions()) -> AgeVerificationStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = self.age_verification_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            time.sleep(opts.interval)


class AsyncBankIdSeEndpoint:
    def __init__(self, client: "AsyncIdkollenClient") -> None:
        self._client = client

    async def auth(self, req: BankIdSeAuthRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/bankid-se/auth", body, _status_adapter)

    async def phone_auth(self, req: BankIdSePhoneAuthRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/bankid-se/phone/auth", body, _status_adapter)

    async def sign(self, req: BankIdSeSignRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/bankid-se/sign", body, _status_adapter)

    async def phone_sign(self, req: BankIdSePhoneSignRequest) -> BankIdSeStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/bankid-se/phone/sign", body, _status_adapter)

    async def verify(self, req: BankIdSeVerifyRequest) -> BankIdSeVerifyResponse:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/bankid-se/verify", body, _verify_adapter)

    async def age_verification(self, req: AgeVerificationRequest) -> AgeVerificationStatus:
        body = req.model_dump(mode="json", by_alias=True, exclude_none=True)
        return await self._client._post("/v3/bankid-se/age-verification", body, _age_adapter)

    async def auth_status(self, id: str) -> BankIdSeStatus:
        return await self._client._get(f"/v3/bankid-se/auth/{id}", _status_adapter)

    async def sign_status(self, id: str) -> BankIdSeStatus:
        return await self._client._get(f"/v3/bankid-se/sign/{id}", _status_adapter)

    async def age_verification_status(self, id: str) -> AgeVerificationStatus:
        return await self._client._get(f"/v3/bankid-se/age-verification/{id}", _age_adapter)

    async def cancel_auth(self, id: str) -> None:
        return await self._client._delete(f"/v3/bankid-se/auth/{id}")

    async def cancel_sign(self, id: str) -> None:
        return await self._client._delete(f"/v3/bankid-se/sign/{id}")

    async def cancel_age_verification(self, id: str) -> None:
        return await self._client._delete(f"/v3/bankid-se/age-verification/{id}")

    async def wait_for_auth(self, id: str, opts: PollOptions = PollOptions()) -> BankIdSeStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.auth_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)

    async def wait_for_sign(self, id: str, opts: PollOptions = PollOptions()) -> BankIdSeStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.sign_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)

    async def wait_for_age_verification(self, id: str, opts: PollOptions = PollOptions()) -> AgeVerificationStatus:
        deadline = time.monotonic() + opts.timeout
        while True:
            status = await self.age_verification_status(id)
            if status.status != "PENDING":
                return status
            if time.monotonic() >= deadline:
                raise IdkollenError("poll_timeout", 0, "Poll timed out")
            await asyncio.sleep(opts.interval)
