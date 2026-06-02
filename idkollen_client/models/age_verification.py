from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from idkollen_client.models.common import ApiErrorCode


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class AgeVerificationRequest(_Base):
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    ref_id: Optional[str] = None
    callback_url: Optional[str] = None
    redirect_url: Optional[str] = None


class AgeVerificationPending(_Base):
    status: Literal["PENDING"]
    id: str
    url: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None


class AgeVerificationCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    age_verified: bool


class AgeVerificationFailed(_Base):
    status: Literal["FAILED"]
    id: str
    error: ApiErrorCode


AgeVerificationStatus = Annotated[
    AgeVerificationPending | AgeVerificationCompleted | AgeVerificationFailed,
    Field(discriminator="status"),
]
