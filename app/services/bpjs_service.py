# app/services/bpjs_service.py
import httpx
from app.config import settings
from app.utils.signer import get_bpjs_headers
from app.utils.decryptor import decrypt_response

class BPJSService:
    async def process_response(self, response_json, timestamp: str):

        meta_data = response_json.get("metaData", {})
        encrypted_data = response_json.get("response")

        if str(meta_data.get("code")) == "200" and isinstance(encrypted_data, str):
            decrypted = decrypt_response(
                encrypted_data,
                settings.BPJS_CONS_ID,
                settings.BPJS_SECRET_KEY,
                timestamp
            )
            return {"metaData": meta_data, "response": decrypted}
        
        return response_json

    async def get_monitoring_kunjungan(self, tgl: str, jns_layanan: str):
        # 1. Ambil headers (didalamnya ada X-timestamp yang krusial untuk dekripsi)
        headers = get_bpjs_headers()
        url = f"{settings.BASE_URL}/Monitoring/Kunjungan/Tanggal/{tgl}/JnsPelayanan/{jns_layanan}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            # 2. Kirim response ke process_response dengan timestamp asli
            return await self.process_response(response.json(), headers["X-timestamp"])

    async def get_histori_pelayanan(self, nokp: str, tgl_mulai: str, tgl_akhir: str):
        # 1. Ambil headers
        headers = get_bpjs_headers()
        url = f"{settings.BASE_URL}/monitoring/HistoriPelayanan/NoKartu/{nokp}/tglMulai/{tgl_mulai}/tglAkhir/{tgl_akhir}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            # 2. Kirim response ke process_response dengan timestamp asli
            return await self.process_response(response.json(), headers["X-timestamp"])
        
    async def get_rencana_kontrol(self, tgl_mulai: str, tgl_akhir: str, filter: str):
        # 1. Ambil headers
        headers = get_bpjs_headers()
        url = f"{settings.BASE_URL}/RencanaKontrol/ListRencanaKontrol/tglAwal/{tgl_mulai}/tglAkhir/{tgl_akhir}/filter/{filter}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            # 2. Kirim response ke process_response dengan timestamp asli
            return await self.process_response(response.json(), headers["X-timestamp"])

    async def get_rencana_kontrol_nokp(self, bulan:str, tahun:str, nokp:str, filter:str):
        headers = get_bpjs_headers()
        url = f"{settings.BASE_URL}/RencanaKontrol/ListRencanaKontrol/Bulan/{bulan}/Tahun/{tahun}/NoKartu/{nokp}/filter/{filter}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return await self.process_response(response.json(), headers["X-timestamp"])
        
    async def get_peserta(self, nik: str, tglSEP: str):
        headers = get_bpjs_headers()
        url = f"{settings.BASE_URL}/Peserta/nik/{nik}/tglSEP/{tglSEP}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            return await self.process_response(response.json(), headers["X-timestamp"])