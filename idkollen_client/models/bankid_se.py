from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from idkollen_client.models.common import ApiErrorCode, CallInitiator


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BankIdSeAuthRequest(_Base):
    ssn: Optional[str] = None
    ip_address: Optional[str] = None
    callback_url: Optional[str] = None
    pin_required: Optional[bool] = None
    intent: Optional[str] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class BankIdSePhoneAuthRequest(_Base):
    ssn: str
    call_initiator: CallInitiator
    callback_url: Optional[str] = None
    pin_required: Optional[bool] = None
    intent: Optional[str] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class BankIdSeSignRequest(_Base):
    text: str
    ssn: Optional[str] = None
    ip_address: Optional[str] = None
    callback_url: Optional[str] = None
    pin_required: Optional[bool] = None
    digest: Optional[str] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class BankIdSePhoneSignRequest(_Base):
    ssn: str
    call_initiator: CallInitiator
    text: str
    callback_url: Optional[str] = None
    pin_required: Optional[bool] = None
    digest: Optional[str] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class BankIdSeVerifyRequest(_Base):
    qr_code: str


class BankIdSePending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: Optional[str] = None
    auto_start_token: Optional[str] = None
    qr_start_token: Optional[str] = None
    qr_start_secret: Optional[str] = None
    hint_code: Optional[str] = None


class BankIdSeCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    ref_id: Optional[str] = None
    ssn: str
    name: str
    given_name: str
    surname: str
    cert_start_date: Optional[str] = None
    address: Optional[str] = None
    company_signatory_text: Optional[str] = None


class BankIdSeFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: Optional[str] = None
    error: ApiErrorCode


BankIdSeStatus = Annotated[
    BankIdSePending | BankIdSeCompleted | BankIdSeFailed,
    Field(discriminator="status"),
]


class BankIdSeVerifyResponse(_Base):
    ssn: str
    name: str
    given_name: str
    surname: str
    age: Optional[int] = None
    verified_at: Optional[str] = None
