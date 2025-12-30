import time
import hmac
import hashlib
import base64
import os
from dotenv import load_dotenv

# Pastikan file .env terbaca
load_dotenv()

def generate_bpjs_headers():
    cons_id = os.getenv("BPJS_CONS_ID")
    secret_key = os.getenv("BPJS_SECRET_KEY")
    user_key = os.getenv("BPJS_USER_KEY")

    # Validasi sederhana agar tidak error jika .env kosong
    if not cons_id or not secret_key:
        raise ValueError("CONS_ID atau BPJS_SECRET_KEY belum diset di file .env")

    # 1. Generate Timestamp (Epoch Time dalam detik)
    t_stamp = str(int(time.time()))

    # 2. Generate Signature (HMAC-SHA256)
    # Format data: ConsID + "&" + Timestamp
    data = f"{cons_id}&{t_stamp}"

    # Buat signature
    # Menggunakan .encode('utf-8') lebih aman daripada bytes(..., 'utf-8')
    signature = hmac.new(
        key=secret_key.encode('utf-8'),
        msg=data.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()

    # Encode ke Base64
    encoded_signature = base64.b64encode(signature).decode('utf-8')

    # Susun Headers
    headers = {
        "X-cons-id": cons_id,
        "X-timestamp": t_stamp,
        "X-signature": encoded_signature,
        "user_key": user_key, # Wajib untuk API VClaim/Antrean terbaru
        "Content-Type": "application/json; charset=utf-8"
    }

    print("✅ Generated BPJS Headers:", headers)

    # 3. Return Headers (Langsung return variable dict, jangan dibungkus kurung kurawal lagi)
    return headers