from fastapi import FastAPI, HTTPException, UploadFile
from firebase_admin import credentials, initialize_app, storage
from google.cloud import firestore
from datetime import datetime, timezone
import os
from utils import connect, open_worksheet, append_data
from fastapi.routing import APIRouter
from models.events import WebinarRegistrationRequest

# Create the FastAPI app
app = FastAPI()

# Create the event_router
event_router = APIRouter(tags=["Event"])

CREDENTIAL_PATH = "sa.json"
BUCKET_NAME = "icee-2023.appspot.com"

cred = credentials.Certificate(CREDENTIAL_PATH)
initialize_app(cred)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_PATH

firebase_storage = storage.bucket(name=BUCKET_NAME)
db = firestore.Client()

@event_router.post("/uploadFile")
async def upload_file(file: UploadFile):
    allowed_formats = {'pdf', 'jpeg', 'jpg', 'png'}
    max_file_size = 5 * 1024 * 1024  # 5 MB

    try:
        file_format = file.filename.split('.')[-1].lower()
        if file_format not in allowed_formats:
            raise HTTPException(status_code=400, detail="Format file tidak didukung")

        file_size = file.file.seek(0, 2)
        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="Ukuran file terlalu besar")

        file.file.seek(0)

        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{current_time}.{file.filename}"

        blob = firebase_storage.blob(new_filename)
        blob.upload_from_file(file.file)

        file_url = f"https://storage.googleapis.com/{firebase_storage.name}/{blob.name}"

        return {"message": "success", "file_url": file_url}

    except HTTPException as http_exception:
        return {"message": http_exception.detail}
    except Exception as e:
        return {"message": f"Terjadi kesalahan: {str(e)}"}

@event_router.post("/uploadData")
async def upload_data(request: WebinarRegistrationRequest):
    try:
        credentials_file = "sa.json"
        spreadsheet = connect(credentials_file)

        worksheet = open_worksheet(spreadsheet, "[Testing] Registrant", request["webinar_id"])

        jakarta_timezone = timezone("Asia/Jakarta")
        current_datetime_wib = datetime.now(jakarta_timezone)
        formatted_datetime = current_datetime_wib.strftime("%m/%d/%Y %H:%M:%S")

        data_to_append = [
            formatted_datetime,
            request["webinar_name"],  # Mengganti dengan "webinar_name" sesuai model
            request["full_name"],
            request["email"],
            request["phone_number"],
            request["institution"],  # Mengganti dengan "institution" sesuai model
            request["profession"],   # Mengganti dengan "profession" sesuai model
            request["address"],      # Mengganti dengan "address" sesuai model
            request["url_bukti_pembayaran"]
        ]

        append_data(worksheet, data_to_append)

        return {"message": "success"}

    except Exception as e:
        return {"message": str(e)}