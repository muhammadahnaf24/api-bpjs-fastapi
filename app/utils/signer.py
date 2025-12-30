# app/utils/signer.py
import time
import hmac
import hashlib
import base64
from app.config import settings

def get_bpjs_headers():
    # 1. Generate Timestamp
    timestamp = str(int(time.time()))
    
    # 2. Generate Signature
    data = settings.BPJS_CONS_ID + "&" + timestamp
    signature = hmac.new(
        settings.BPJS_SECRET_KEY.encode(),
        data.encode(),
        hashlib.sha256
    ).digest()
    encoded_signature = base64.b64encode(signature).decode()

    return {
        "X-cons-id": settings.BPJS_CONS_ID,
        "X-timestamp": timestamp,
        "X-signature": encoded_signature,
        "user_key": settings.BPJS_USER_KEY,
        "Content-Type": "application/json"
    }