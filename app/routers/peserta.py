
from fastapi import APIRouter
from app.services.bpjs_service import BPJSService

router = APIRouter()
service = BPJSService()

@router.get("/peserta/{nik}/{tglSEP}")
async def peserta(nik: str, tglSEP: str):
    data = await service.get_peserta(nik, tglSEP)
    return data
