from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Discriminator, Tag
from pydantic.alias_generators import to_camel

from idkollen_client.models.common import ApiErrorCode, UnknownStatus, status_tag


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BankIdNoAuthRequest(_Base):
    redirect_url: Optional[str] = None
    request_ssn: Optional[bool] = None
    request_phone: Optional[bool] = None
    request_email: Optional[bool] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None
    app_callback_uri: Optional[str] = None


class BankIdNoBackchannelAuthRequest(_Base):
    ssn: str
    callback_url: Optional[str] = None
    ref_id: Optional[str] = None


class BankIdNoSignRequest(_Base):
    redirect_url: Optional[str] = None
    text: Optional[str] = None
    documents: Optional[list[str]] = None
    ref_id: Optional[str] = None


class BankIdNoPending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: Optional[str] = None
    url: Optional[str] = None
    binding_message: Optional[str] = None


class BankIdNoSignResult(_Base):
    end_user: str
    merchant: str
    hash: str


class BankIdNoSignedDocument(_Base):
    id: str
    hash: str


class BankIdNoCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    ref_id: Optional[str] = None
    ssn: Optional[str] = None
    name: str
    given_name: str
    surname: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[str] = None
    pid: Optional[str] = None
    bank_id: Optional[str] = None
    sign_result: Optional[BankIdNoSignResult] = None
    signed_documents: Optional[list[BankIdNoSignedDocument]] = None
    authenticated_at: Optional[str] = None
    signed_at: Optional[str] = None


class BankIdNoFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: Optional[str] = None
    error: ApiErrorCode


BankIdNoStatus = Annotated[
    Annotated[BankIdNoPending, Tag("PENDING")]
    | Annotated[BankIdNoCompleted, Tag("COMPLETED")]
    | Annotated[BankIdNoFailed, Tag("FAILED")]
    | Annotated[UnknownStatus, Tag("UNKNOWN")],
    Discriminator(status_tag),
]
