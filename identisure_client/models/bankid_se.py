from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, Tag
from pydantic.alias_generators import to_camel

from identisure_client.models.common import ApiErrorCode, CallInitiator, UnknownStatus, status_tag


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BankIdSeAuthRequest(_Base):
    ssn: str | None = None
    ip_address: str | None = None
    callback_url: str | None = None
    pin_required: bool | None = None
    intent: str | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class BankIdSePhoneAuthRequest(_Base):
    ssn: str
    call_initiator: CallInitiator
    callback_url: str | None = None
    pin_required: bool | None = None
    intent: str | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class BankIdSeSignRequest(_Base):
    text: str
    ssn: str | None = None
    ip_address: str | None = None
    callback_url: str | None = None
    pin_required: bool | None = None
    digest: str | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class BankIdSePhoneSignRequest(_Base):
    ssn: str
    call_initiator: CallInitiator
    text: str
    callback_url: str | None = None
    pin_required: bool | None = None
    digest: str | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class BankIdSeVerifyRequest(_Base):
    qr_code: str


class BankIdSePending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: str | None = None
    auto_start_token: str | None = None
    qr_start_token: str | None = None
    qr_start_secret: str | None = None
    hint_code: str | None = None


class BankIdSeDevice(_Base):
    ip_address: str | None = None
    uhi: str | None = None


class BankIdSeStepUp(_Base):
    mrtd: bool | None = None
    face: bool | None = None


class BankIdSeCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    ref_id: str | None = None
    ssn: str
    name: str
    given_name: str
    surname: str
    cert_start_date: str | None = None
    ocsp_response: str
    risk: str | None = None
    device: BankIdSeDevice | None = None
    step_up: BankIdSeStepUp | None = None
    address: str | None = None
    company_signatory_text: str | None = None
    authenticated_at: str | None = None
    signed_at: str | None = None


class BankIdSeFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: str | None = None
    error: ApiErrorCode


BankIdSeStatus = Annotated[
    Annotated[BankIdSePending, Tag("PENDING")]
    | Annotated[BankIdSeCompleted, Tag("COMPLETED")]
    | Annotated[BankIdSeFailed, Tag("FAILED")]
    | Annotated[UnknownStatus, Tag("UNKNOWN")],
    Discriminator(status_tag),
]


class BankIdSeVerifyResponse(_Base):
    ssn: str
    name: str
    given_name: str
    surname: str
    age: int | None = None
    verified_at: str | None = None
