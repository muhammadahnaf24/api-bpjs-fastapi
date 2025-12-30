import os
from pydantic_settings import BaseSettings, SettingsConfigDict

# Mendapatkan path absolut ke direktori root proyek
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class Settings(BaseSettings):
    BPJS_CONS_ID: str
    BPJS_SECRET_KEY: str
    BPJS_USER_KEY: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )
settings = Settings()

# Tambahkan ini untuk melihat apa yang ditangkap oleh Python saat start
# app/config.py
print("--- DEBUG BPJS CONFIG ---")
# Cek BPJS_CONS_ID, bukan CONS_ID
print(f"BPJS_CONS_ID terdeteksi: {hasattr(settings, 'BPJS_CONS_ID')}") 
print(f"Keys yang ada: {settings.model_dump().keys()}")
print("--------------------------")