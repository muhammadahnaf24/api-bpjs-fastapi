# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import monitoring 
from app.routers import rencanakontrol 
from app.routers import peserta

app = FastAPI(title="BPJS API Bridge")

# Setup CORS agar Frontend bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Sesuaikan dengan domain frontend Anda
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarkan Router
app.include_router(monitoring.router, prefix="/api/bpjs")
app.include_router(rencanakontrol.router, prefix="/api/bpjs")
app.include_router(peserta.router, prefix="/api/bpjs")

@app.get("/")
def read_root():
    return {"status": "FastAPI BPJS is Running"}