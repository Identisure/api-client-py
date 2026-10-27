from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Discriminator, Tag
from pydantic.alias_generators import to_camel

from identisure_client.models.common import ApiErrorCode, Country, UnknownStatus, status_tag

FrejaRegistrationLevel = Literal["EXTENDED", "PLUS"]


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class FrejaAuthRequest(_Base):
    ssn: str | None = None
    callback_url: str | None = None
    min_registration_level: FrejaRegistrationLevel | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class FrejaBackchannelAuthRequest(_Base):
    ssn: str
    country: Country
    callback_url: str | None = None
    min_registration_level: FrejaRegistrationLevel | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class FrejaSignRequest(_Base):
    text: str
    ssn: str | None = None
    callback_url: str | None = None
    min_registration_level: FrejaRegistrationLevel | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class FrejaBackchannelSignRequest(_Base):
    ssn: str
    country: Country
    text: str
    callback_url: str | None = None
    min_registration_level: FrejaRegistrationLevel | None = None
    org_number: str | None = None
    request_address: bool | None = None
    ref_id: str | None = None


class FrejaPending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: str | None = None
    auto_start_token: str
    qr_data: str


class FrejaCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    ref_id: str | None = None
    ssn: str
    country: Country
    name: str
    given_name: str
    surname: str
    address: str | None = None
    company_signatory_text: str | None = None
    authenticated_at: str | None = None
    signed_at: str | None = None


class FrejaFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: str | None = None
    error: ApiErrorCode


FrejaStatus = Annotated[
    Annotated[FrejaPending, Tag("PENDING")]
    | Annotated[FrejaCompleted, Tag("COMPLETED")]
    | Annotated[FrejaFailed, Tag("FAILED")]
    | Annotated[UnknownStatus, Tag("UNKNOWN")],
    Discriminator(status_tag),
]
