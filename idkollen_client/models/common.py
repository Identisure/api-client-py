from __future__ import annotations

from typing import Literal

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
