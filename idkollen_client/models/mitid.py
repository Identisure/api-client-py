from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Discriminator, Tag
from pydantic.alias_generators import to_camel

from idkollen_client.models.common import ApiErrorCode, UnknownStatus, status_tag


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class MitIdAuthRequest(_Base):
    redirect_url: Optional[str] = None
    reference_text: Optional[str] = None
    request_phone: Optional[bool] = None
    request_email: Optional[bool] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class MitIdBackchannelAuthRequest(_Base):
    ssn: str
    binding_message: str
    callback_url: Optional[str] = None
    ref_id: Optional[str] = None


class MitIdSignRequest(_Base):
    text: str
    redirect_url: Optional[str] = None
    ref_id: Optional[str] = None


class MitIdPending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: Optional[str] = None
    url: Optional[str] = None
    binding_message: Optional[str] = None


class MitIdSignResult(_Base):
    checksum: str


class MitIdCompleted(_Base):
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
    sign_result: Optional[MitIdSignResult] = None
    authenticated_at: Optional[str] = None
    signed_at: Optional[str] = None


class MitIdFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: Optional[str] = None
    error: ApiErrorCode


MitIdStatus = Annotated[
    Annotated[MitIdPending, Tag("PENDING")]
    | Annotated[MitIdCompleted, Tag("COMPLETED")]
    | Annotated[MitIdFailed, Tag("FAILED")]
    | Annotated[UnknownStatus, Tag("UNKNOWN")],
    Discriminator(status_tag),
]
