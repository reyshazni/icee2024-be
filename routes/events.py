from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from models.events import WebinarRegistrationRequest
import os
import firebase_admin
from firebase_admin import credentials, storage
from google.cloud import firestore
from utils import connect, open_worksheet, append_data
from pytz import timezone
from datetime import datetime
import pytz

credential_path = "sa.json"

cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# Inisialisasi Firebase Storage
firebase_storage = storage.bucket(name="icee-2023.appspot.com")  # Ganti dengan nama bucket Firebase Anda

db = firestore.Client(project='icee-2023')

event_router = APIRouter(
    tags=["Events"]
)

from pytz import timezone
from datetime import datetime
import pytz

@event_router.post("/uploadFile")
async def upload_file(file: UploadFile):
    allowed_formats = {'pdf', 'jpeg', 'jpg', 'png'}
    max_file_size = 5 * 1024 * 1024  # 5 MB

    try:
        # Validasi format file
        file_format = file.filename.split('.')[-1].lower()
        if file_format not in allowed_formats:
            raise HTTPException(status_code=400, detail="Format file tidak didukung")

        # Validasi ukuran file
        file_size = file.file.seek(0, 2)
        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="Ukuran file terlalu besar")

        # Kembali ke awal file
        file.file.seek(0)

        # Membuat nama file baru dengan menggunakan datetime
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{current_time}.{file.filename}"

        # Upload file ke Firebase Storage dengan nama baru
        blob = firebase_storage.blob(new_filename)
        blob.upload_from_file(file.file)

        # Dapatkan URL file yang diupload
        file_url = f"https://storage.googleapis.com/{firebase_storage.name}/{blob.name}"

        # Mengembalikan respons sukses dengan URL file yang diupload
        return {"message": "success", "file_url": file_url}

    except HTTPException as http_exception:
        return JSONResponse(status_code=http_exception.status_code, content={"message": http_exception.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Terjadi kesalahan: {str(e)}"})

@event_router.post("/uploadData")
async def upload_data(request: WebinarRegistrationRequest):
    try:
        # Lakukan validasi atau pemrosesan data sesuai kebutuhan

        # Tambahkan data ke spreadsheet menggunakan dependensi yang disediakan
        credentials_file = "sa.json"
        spreadsheet = connect(credentials_file)

        worksheet = open_worksheet(spreadsheet, "[Testing] Registrant", request.webinar_id)  # Sesuaikan nama worksheet sesuai kebutuhan

        # Dapatkan waktu saat ini dalam timezone "Asia/Jakarta" (WIB)
        jakarta_timezone = pytz.timezone("Asia/Jakarta")
        current_datetime_wib = datetime.now(jakarta_timezone)

        # Format waktu ke dalam string sesuai dengan format "9/7/2023 16:24:10"
        formatted_datetime = current_datetime_wib.strftime("%m/%d/%Y %H:%M:%S")

        # Tambahkan data ke dalam worksheet, termasuk waktu dalam format yang diinginkan dan URL file
        data_to_append = [formatted_datetime, request.full_name, request.email, request.phone_number, request.organization, request.url_bukti_pembayaran]
        append_data(worksheet, data_to_append)

        # Mengembalikan respons sukses
        return {"message": "success"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})
