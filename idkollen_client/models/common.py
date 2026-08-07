from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel

ApiErrorCode = Literal[
    "AUTH_FAILED",
    "CANCELLED",
    "INVALID_ID",
    "CONFLICT",
    "INTERNAL_ERROR",
    "SESSION_TIMEOUT",
    "UNSUPPORTED_CLIENT",
]

CallInitiator = Literal["USER", "RP"]

Language = Literal["ENGLISH", "SWEDISH", "NORWEGIAN", "DANISH", "FINNISH"]

Country = str


class UnknownStatus(BaseModel):
    """Returned when the server reports a status this client version does not know."""

    status: str


def status_tag(value: Any) -> str:
    status = value.get("status") if isinstance(value, dict) else getattr(value, "status", None)
    return status if status in ("PENDING", "COMPLETED", "FAILED") else "UNKNOWN"
