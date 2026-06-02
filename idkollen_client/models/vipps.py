from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from idkollen_client.models.common import ApiErrorCode


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class VippsAuthRequest(_Base):
    redirect_url: Optional[str] = None
    request_ssn: Optional[bool] = None
    request_phone: Optional[bool] = None
    request_email: Optional[bool] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None
    app_callback_uri: Optional[str] = None


class VippsBackchannelAuthRequest(_Base):
    phone: str
    request_ssn: Optional[bool] = None
    request_email: Optional[bool] = None
    request_address: Optional[bool] = None
    callback_url: Optional[str] = None
    ref_id: Optional[str] = None


class VippsPending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: Optional[str] = None
    url: Optional[str] = None


class VippsCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    ref_id: Optional[str] = None
    ssn: str
    name: str
    given_name: str
    surname: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[str] = None
    pid: Optional[str] = None
    bank_id: Optional[str] = None


class VippsFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: Optional[str] = None
    error: ApiErrorCode


VippsStatus = Annotated[
    VippsPending | VippsCompleted | VippsFailed,
    Field(discriminator="status"),
]
