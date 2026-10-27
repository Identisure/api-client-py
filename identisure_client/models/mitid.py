from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, Tag
from pydantic.alias_generators import to_camel

from identisure_client.models.common import ApiErrorCode, UnknownStatus, status_tag


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class MitIdAuthRequest(_Base):
    redirect_url: str | None = None
    reference_text: str | None = None
    request_phone: bool | None = None
    request_email: bool | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class MitIdBackchannelAuthRequest(_Base):
    ssn: str
    binding_message: str
    callback_url: str | None = None
    ref_id: str | None = None


class MitIdSignRequest(_Base):
    text: str
    redirect_url: str | None = None
    ref_id: str | None = None


class MitIdPending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: str | None = None
    url: str | None = None
    binding_message: str | None = None


class MitIdSignResult(_Base):
    checksum: str


class MitIdCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    ref_id: str | None = None
    ssn: str | None = None
    name: str
    given_name: str
    surname: str
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    birth_date: str | None = None
    pid: str | None = None
    bank_id: str | None = None
    sign_result: MitIdSignResult | None = None
    authenticated_at: str | None = None
    signed_at: str | None = None


class MitIdFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: str | None = None
    error: ApiErrorCode


MitIdStatus = Annotated[
    Annotated[MitIdPending, Tag("PENDING")]
    | Annotated[MitIdCompleted, Tag("COMPLETED")]
    | Annotated[MitIdFailed, Tag("FAILED")]
    | Annotated[UnknownStatus, Tag("UNKNOWN")],
    Discriminator(status_tag),
]
