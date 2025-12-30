import hashlib
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from lzstring import LZString

def decrypt_response(encrypted_data: str, cons_id: str, secret_key: str, timestamp: str):
    try:
        # 1. Kunci dekripsi adalah gabungan consId + secretKey + timestamp
        key_plain = f"{cons_id}{secret_key}{timestamp}"
        
        # 2. Hash SHA256 dari key_plain untuk mendapatkan key 32 bytes (256 bits)
        key_hash = hashlib.sha256(key_plain.encode('utf-8')).digest()
        
        # 3. IV adalah 16 bytes pertama dari key_hash
        iv = key_hash[:16]
        
        # 4. Decode Base64 data terenkripsi
        encrypted_bytes = base64.b64decode(encrypted_data)
        
        # 5. Setup AES-256-CBC Decipher
        cipher = AES.new(key_hash, AES.MODE_CBC, iv)
        
        # 6. Decrypt dan hilangkan padding (PKCS7)
        # unpad sangat krusial agar data bisa dibaca sebagai string UTF-8
        decrypted_raw = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        decrypted_str = decrypted_raw.decode('utf-8')
        
        # 7. Decompress menggunakan LZString (identik dengan Node.js)
        lz = LZString()
        decompressed = lz.decompressFromEncodedURIComponent(decrypted_str)
        
        # Jika hasil decompressURIComponent null, coba decompress biasa
        if not decompressed:
            decompressed = lz.decompress(decrypted_str)

        return json.loads(decompressed)
        
    except Exception as e:
        print(f"❌ Gagal Decrypt: {str(e)}")
        return None