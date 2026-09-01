from __future__ import annotations

import asyncio
import base64
from dataclasses import dataclass
from typing import Any, Callable

import pytest
from pydantic import BaseModel

from conftest import MockServer, fixture
from idkollen_client import IdkollenClientBuilder, IdkollenError, PollOptions
from idkollen_client._client import AsyncIdkollenClient, IdkollenClient
from idkollen_client.models import (
    AgeVerificationCompleted,
    AgeVerificationFailed,
    AgeVerificationRequest,
    BankIdNoAuthRequest,
    BankIdNoCompleted,
    BankIdNoFailed,
    BankIdNoSignRequest,
    BankIdSeAuthRequest,
    BankIdSeCompleted,
    BankIdSeFailed,
    BankIdSePhoneAuthRequest,
    BankIdSeSignRequest,
    BankIdSeVerifyRequest,
    BankIdSeVerifyResponse,
    FrejaAuthRequest,
    FrejaCompleted,
    FrejaFailed,
    FrejaSignRequest,
    FtnAuthRequest,
    FtnCompleted,
    FtnFailed,
    MitIdAuthRequest,
    MitIdCompleted,
    MitIdFailed,
    MitIdSignRequest,
    UnknownStatus,
    VippsAuthRequest,
    VippsCompleted,
    VippsFailed,
)
from idkollen_client.models.document import DocumentUploadResponse

POLL = PollOptions(interval=0.01, timeout=5.0)
AUTHORIZATION = "Basic " + base64.b64encode(b"client-id:client-secret").decode()


@dataclass(frozen=True)
class Provider:
    name: str
    segment: str
    endpoint: Callable[[Any], Any]
    auth_request: Callable[[], BaseModel]
    completed: type[BaseModel]
    failed: type[BaseModel]
    sign_request: Callable[[], BaseModel] | None = None


PROVIDERS = [
    Provider("bankid_se", "bankid-se", lambda c: c.bankid_se(), BankIdSeAuthRequest, BankIdSeCompleted,
             BankIdSeFailed, lambda: BankIdSeSignRequest(text="Sign this")),
    Provider("bankid_no", "bankid-no", lambda c: c.bankid_no(), BankIdNoAuthRequest, BankIdNoCompleted,
             BankIdNoFailed, lambda: BankIdNoSignRequest(text="Sign this")),
    Provider("freja", "freja", lambda c: c.freja(), FrejaAuthRequest, FrejaCompleted,
             FrejaFailed, lambda: FrejaSignRequest(text="Sign this")),
    Provider("mitid", "mitid", lambda c: c.mitid(), MitIdAuthRequest, MitIdCompleted,
             MitIdFailed, lambda: MitIdSignRequest(text="Sign this")),
    Provider("ftn", "ftn", lambda c: c.ftn(), FtnAuthRequest, FtnCompleted, FtnFailed),
    Provider("vipps", "vipps", lambda c: c.vipps(), VippsAuthRequest, VippsCompleted, VippsFailed),
]

SIGNING_PROVIDERS = [p for p in PROVIDERS if p.sign_request is not None]


def client(server: MockServer) -> IdkollenClient:
    return IdkollenClientBuilder("client-id", "client-secret").base_url(server.url).build()


def async_client(server: MockServer) -> AsyncIdkollenClient:
    return IdkollenClientBuilder("client-id", "client-secret").base_url(server.url).build_async()


def as_json(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(by_alias=True, mode="json", exclude_none=True)


def without_nulls(data: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


def assert_authorized(server: MockServer) -> None:
    assert all(r.headers.get("Authorization") == AUTHORIZATION for r in server.requests)


@pytest.mark.parametrize("provider", PROVIDERS, ids=lambda p: p.name)
def test_auth_completes(server: MockServer, provider: Provider) -> None:
    server.enqueue(201, f"{provider.name}/auth_pending.json")
    server.enqueue(200, f"{provider.name}/auth_pending.json")
    server.enqueue(200, f"{provider.name}/auth_completed.json")

    with client(server) as c:
        endpoint = provider.endpoint(c)
        session = endpoint.auth(provider.auth_request())
        result = endpoint.wait_for_auth(session.id, POLL)

    assert as_json(session) == fixture(f"{provider.name}/auth_pending.json")
    assert isinstance(result, provider.completed)
    assert as_json(result) == fixture(f"{provider.name}/auth_completed.json")
    assert server.calls() == [
        ("POST", f"/v3/{provider.segment}/auth"),
        ("GET", f"/v3/{provider.segment}/auth/{session.id}"),
        ("GET", f"/v3/{provider.segment}/auth/{session.id}"),
    ]
    assert_authorized(server)


@pytest.mark.parametrize("provider", PROVIDERS, ids=lambda p: p.name)
def test_auth_fails(server: MockServer, provider: Provider) -> None:
    server.enqueue(201, f"{provider.name}/auth_pending.json")
    server.enqueue(200, f"{provider.name}/auth_failed.json")

    with client(server) as c:
        endpoint = provider.endpoint(c)
        session = endpoint.auth(provider.auth_request())
        result = endpoint.wait_for_auth(session.id, POLL)

    assert isinstance(result, provider.failed)
    assert as_json(result) == fixture(f"{provider.name}/auth_failed.json")


@pytest.mark.parametrize("provider", PROVIDERS, ids=lambda p: p.name)
def test_auth_unknown_status(server: MockServer, provider: Provider) -> None:
    server.enqueue(201, f"{provider.name}/auth_pending.json")
    server.enqueue(200, f"{provider.name}/auth_unknown.json")

    with client(server) as c:
        endpoint = provider.endpoint(c)
        session = endpoint.auth(provider.auth_request())
        result = endpoint.wait_for_auth(session.id, POLL)

    assert result == UnknownStatus(status="SOMETHING_NEW")


@pytest.mark.parametrize("provider", SIGNING_PROVIDERS, ids=lambda p: p.name)
def test_sign_completes(server: MockServer, provider: Provider) -> None:
    assert provider.sign_request is not None
    server.enqueue(201, f"{provider.name}/auth_pending.json")
    server.enqueue(200, f"{provider.name}/sign_completed.json")

    with client(server) as c:
        endpoint = provider.endpoint(c)
        session = endpoint.sign(provider.sign_request())
        result = endpoint.wait_for_sign(session.id, POLL)

    assert isinstance(result, provider.completed)
    assert as_json(result) == fixture(f"{provider.name}/sign_completed.json")
    assert server.calls() == [
        ("POST", f"/v3/{provider.segment}/sign"),
        ("GET", f"/v3/{provider.segment}/sign/{session.id}"),
    ]


def test_bankid_se_phone_auth_completes(server: MockServer) -> None:
    server.enqueue(201, "bankid_se/phone_auth_pending.json")
    server.enqueue(200, "bankid_se/auth_completed.json")

    with client(server) as c:
        session = c.bankid_se().phone_auth(BankIdSePhoneAuthRequest(ssn="199001011239", call_initiator="USER"))
        result = c.bankid_se().wait_for_auth(session.id, POLL)

    assert as_json(session) == without_nulls(fixture("bankid_se/phone_auth_pending.json"))
    assert isinstance(result, BankIdSeCompleted)
    assert server.calls() == [
        ("POST", "/v3/bankid-se/phone/auth"),
        ("GET", f"/v3/bankid-se/auth/{session.id}"),
    ]


def test_bankid_se_verify(server: MockServer) -> None:
    server.enqueue(200, "bankid_se/verify.json")

    with client(server) as c:
        result = c.bankid_se().verify(BankIdSeVerifyRequest(qr_code="bankid.qr-code"))

    assert isinstance(result, BankIdSeVerifyResponse)
    assert as_json(result) == fixture("bankid_se/verify.json")
    assert server.calls() == [("POST", "/v3/bankid-se/verify")]


@pytest.mark.parametrize(
    ("final", "expected"),
    [("completed", AgeVerificationCompleted), ("failed", AgeVerificationFailed), ("unknown", UnknownStatus)],
)
def test_age_verification(server: MockServer, final: str, expected: type[BaseModel]) -> None:
    server.enqueue(201, "age_verification/pending.json")
    server.enqueue(200, "age_verification/pending.json")
    server.enqueue(200, f"age_verification/{final}.json")

    with client(server) as c:
        session = c.bankid_se().age_verification(AgeVerificationRequest(min_age=18))
        result = c.bankid_se().wait_for_age_verification(session.id, POLL)

    assert as_json(session) == without_nulls(fixture("age_verification/pending.json"))
    assert isinstance(result, expected)
    if final == "unknown":
        assert result == UnknownStatus(status="SOMETHING_NEW")
    else:
        assert as_json(result) == fixture(f"age_verification/{final}.json")
    assert server.calls()[0] == ("POST", "/v3/bankid-se/age-verification")
    assert server.calls()[1:] == [("GET", f"/v3/bankid-se/age-verification/{session.id}")] * 2


def test_document_upload(server: MockServer) -> None:
    server.enqueue(201, "document/upload.json")

    with client(server) as c:
        result = c.document().upload(b"%PDF-1.7", "contract.pdf")

    assert isinstance(result, DocumentUploadResponse)
    assert as_json(result) == fixture("document/upload.json")
    assert server.calls() == [("POST", "/v3/document")]
    request = server.requests[0]
    assert request.headers["Content-Type"].startswith("multipart/form-data")
    assert b'filename="contract.pdf"' in request.body
    assert b"%PDF-1.7" in request.body
    assert_authorized(server)


def test_api_error(server: MockServer) -> None:
    server.enqueue(400, "error.json")

    with client(server) as c, pytest.raises(IdkollenError) as info:
        c.ftn().auth(FtnAuthRequest())

    assert info.value.code == "api"
    assert info.value.status == 400
    assert "Invalid request" in info.value.message


def test_async_auth_completes(server: MockServer) -> None:
    server.enqueue(201, "bankid_se/auth_pending.json")
    server.enqueue(200, "bankid_se/auth_pending.json")
    server.enqueue(200, "bankid_se/auth_completed.json")

    async def run() -> BaseModel:
        async with async_client(server) as c:
            session = await c.bankid_se().auth(BankIdSeAuthRequest())
            return await c.bankid_se().wait_for_auth(session.id, POLL)

    result = asyncio.run(run())

    assert isinstance(result, BankIdSeCompleted)
    assert as_json(result) == fixture("bankid_se/auth_completed.json")
    assert len(server.requests) == 3
    assert_authorized(server)
