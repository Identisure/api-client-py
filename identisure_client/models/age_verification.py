from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, Tag
from pydantic.alias_generators import to_camel

from identisure_client.models.common import ApiErrorCode, UnknownStatus, status_tag


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class AgeVerificationRequest(_Base):
    min_age: int | None = None
    max_age: int | None = None
    ref_id: str | None = None
    callback_url: str | None = None
    redirect_url: str | None = None


class AgeVerificationPending(_Base):
    status: Literal["PENDING"]
    id: str
    url: str | None = None
    min_age: int | None = None
    max_age: int | None = None


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
