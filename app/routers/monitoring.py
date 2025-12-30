
from fastapi import APIRouter
from app.services.bpjs_service import BPJSService

router = APIRouter()
service = BPJSService()


@router.get("/monitoring/kunjungan/{tgl}/{jns_layanan}")
async def monitoring_kunjungan(tgl: str, jns_layanan: str):
    data = await service.get_monitoring_kunjungan(tgl, jns_layanan)
    return data

@router.get("/monitoring/historipelayanan/{nokp}/{tgl_mulai}/{tgl_akhir}")
async def histori_pelayanan(nokp: str, tgl_mulai: str, tgl_akhir: str):
    data = await service.get_histori_pelayanan(nokp, tgl_mulai, tgl_akhir)
    return data