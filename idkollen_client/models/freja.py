from __future__ import annotations

from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from idkollen_client.models.common import ApiErrorCode, Country

FrejaRegistrationLevel = Literal["EXTENDED", "PLUS"]


class _Base(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class FrejaAuthRequest(_Base):
    ssn: Optional[str] = None
    callback_url: Optional[str] = None
    min_registration_level: Optional[FrejaRegistrationLevel] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class FrejaBackchannelAuthRequest(_Base):
    ssn: str
    country: Country
    callback_url: Optional[str] = None
    min_registration_level: Optional[FrejaRegistrationLevel] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class FrejaSignRequest(_Base):
    text: str
    ssn: Optional[str] = None
    callback_url: Optional[str] = None
    min_registration_level: Optional[FrejaRegistrationLevel] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class FrejaBackchannelSignRequest(_Base):
    ssn: str
    country: Country
    text: str
    callback_url: Optional[str] = None
    min_registration_level: Optional[FrejaRegistrationLevel] = None
    org_number: Optional[str] = None
    request_address: Optional[bool] = None
    ref_id: Optional[str] = None


class FrejaPending(_Base):
    status: Literal["PENDING"]
    id: str
    ref_id: Optional[str] = None
    auto_start_token: str
    qr_data: str


class FrejaCompleted(_Base):
    status: Literal["COMPLETED"]
    id: str
    ref_id: Optional[str] = None
    ssn: str
    country: Country
    name: str
    given_name: str
    surname: str
    address: Optional[str] = None
    company_signatory_text: Optional[str] = None


class FrejaFailed(_Base):
    status: Literal["FAILED"]
    id: str
    ref_id: Optional[str] = None
    error: ApiErrorCode


FrejaStatus = Annotated[
    FrejaPending | FrejaCompleted | FrejaFailed,
    Field(discriminator="status"),
]
