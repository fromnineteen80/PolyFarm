import os
import time
import hmac
import hashlib
import base64


def generate_ws_headers(path: str) -> dict:
    """
    Generate authenticated WebSocket headers
    for Polymarket US API.
    """
    key_id = os.environ["POLYMARKET_KEY_ID"]
    secret_key = os.environ["POLYMARKET_SECRET_KEY"]

    timestamp = str(int(time.time() * 1000))
    message = timestamp + "GET" + path
    signature = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    sig_b64 = base64.b64encode(signature).decode()

    return {
        "X-PM-Access-Key": key_id,
        "X-PM-Timestamp": timestamp,
        "X-PM-Signature": sig_b64,
    }
