import sys
import hmac
import hashlib
import base64

from config.setting import LineMessageSetting

PY3 = sys.version_info[0] == 3


def safe_compare_digest(val1: str | bytes, val2: str | bytes) -> bool:
    """safe_compare_digest method.

    Args:
        val1 (str | bytes): string or bytes for compare
        val2 (str | bytes): string or bytes for compare

    Returns:
        bool: result
    """
    if len(val1) != len(val2):
        return False

    result = 0
    if PY3 and isinstance(val1, bytes) and isinstance(val2, bytes):
        for i, j in zip(val1, val2):
            result |= i ^ j
    elif PY3 and isinstance(val1, str) and isinstance(val2, str):
        for x, y in zip(val1, val2):
            result |= ord(x) ^ ord(y)
    else:
        return False

    return result == 0


def compare_digest(val1: str | bytes, val2: str | bytes) -> bool:
    """compare_digest function.

    If hmac module has compare_digest function, use it.
    Or not, use linebot.v3.utils.safe_compare_digest.

    Args:
        val1 (str | bytes): string or bytes for compare
        val2 (str | bytes): string or bytes for compare

    Returns:
        bool: result
    """
    if hasattr(hmac, "compare_digest"):
        if isinstance(val1, str):
            val1 = val1.encode("utf-8")
        if isinstance(val2, str):
            val2 = val2.encode("utf-8")
        return hmac.compare_digest(val1, val2)
    else:
        return safe_compare_digest(val1, val2)


def check_signature(body: str, signature: str) -> bool:
    """Check signature.

    Args:
        body (str): The request body from message api webhook.
        signature (str): The signature from the Line header.

    Returns:
        bool: The result of checking the signature.
    """
    gen_signature = hmac.new(LineMessageSetting.secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()

    return compare_digest(signature.encode("utf-8"), base64.b64encode(gen_signature))
