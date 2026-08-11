from __future__ import annotations

import base64
import binascii
import hashlib
import hmac


def verify_callback_signature(body: bytes | str, signature: str, secret: str) -> bool:
    """Verify the ``X-Signature-SHA256`` header of a callback request.

    Pass the raw request body exactly as received. Verify before parsing and
    never re-serialize the JSON.
    """
    if isinstance(body, str):
        body = body.encode("utf-8")
    try:
        expected = base64.b64decode(signature, validate=True)
    except (binascii.Error, ValueError):
        return False
    actual = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).digest()
    return hmac.compare_digest(actual, expected)
