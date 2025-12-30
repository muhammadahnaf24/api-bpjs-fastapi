
from fastapi import APIRouter
from app.services.bpjs_service import BPJSService

router = APIRouter()
service = BPJSService()

@router.get("/rencanakontrol/{tgl_mulai}/{tgl_akhir}/{filter}")
async def rencana_kontrol(tgl_mulai: str, tgl_akhir: str, filter: str):
    data = await service.get_rencana_kontrol(tgl_mulai, tgl_akhir, filter)
    return data

@router.get("/rencanakontrol/nokp/{bulan}/{tahun}/{nokp}/{filter}")
async def rencana_kontrol_nokp(bulan: str, tahun: str, nokp: str, filter: str):
    return await service.get_rencana_kontrol_nokp(bulan, tahun, nokp, filter)
