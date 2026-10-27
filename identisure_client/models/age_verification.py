from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Discriminator, Tag
from pydantic.alias_generators import to_camel

from identisure_client.models.common import ApiErrorCode, UnknownStatus, status_tag


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
    Annotated[AgeVerificationPending, Tag("PENDING")]
    | Annotated[AgeVerificationCompleted, Tag("COMPLETED")]
    | Annotated[AgeVerificationFailed, Tag("FAILED")]
    | Annotated[UnknownStatus, Tag("UNKNOWN")],
    Discriminator(status_tag),
]
