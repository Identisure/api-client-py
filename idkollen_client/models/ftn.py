from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from idkollen_client.models.common import ApiErrorCode


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class FtnAuthRequest(_Base):
    redirect_url: Optional[str] = None
    request_phone: Optional[bool] = None
    request_email: Optional[bool] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class FtnPending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: Optional[str] = None
    url: str


class FtnCompleted(_Base):
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


class FtnFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: Optional[str] = None
    error: ApiErrorCode


FtnStatus = Annotated[
    FtnPending | FtnCompleted | FtnFailed,
    Field(discriminator="status"),
]
