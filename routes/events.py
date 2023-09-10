from fastapi import FastAPI, HTTPException, UploadFile
from firebase_admin import credentials, initialize_app, storage
from google.cloud import firestore
from datetime import datetime, timedelta, timezone
import os
from utils import connect, open_worksheet, append_data
from fastapi.routing import APIRouter
from models.events import WebinarRegistrationRequest

# Create the FastAPI app
app = FastAPI()

# Create the event_router
event_router = APIRouter(tags=["Event"])

CREDENTIAL_PATH = "sa.json"
BUCKET_NAME = "icee24"

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
        print("fileurl")

        return {"message": "success", "file_url": file_url}

    except HTTPException as http_exception:
        return {"message": http_exception.detail}
    except Exception as e:
        return {"message": f"Terjadi kesalahan: {str(e)}"}

@event_router.post("/uploadData")
async def upload_data(request: WebinarRegistrationRequest):
    try:
        credentials_file = "sa.json"

        print("connecting spreadsheet")
        spreadsheet = connect(credentials_file)

        worksheet = open_worksheet(spreadsheet, "[Testing] Registrant", request.webinar_name)

        # Definisikan zona waktu Asia/Jakarta
        jakarta_timezone = timezone(timedelta(hours=7))  # UTC+7 untuk Asia/Jakarta

        # Dapatkan waktu saat ini dalam zona waktu Asia/Jakarta
        current_datetime_wib = datetime.now(jakarta_timezone)
        formatted_datetime = current_datetime_wib.strftime("%m/%d/%Y %H:%M:%S")

        data_to_append = [
            formatted_datetime,
            request.full_name,
            request.email,
            request.phone_number,
            request.institution,
            request.profession,
            request.address,
            request.url_bukti_pembayaran,
            request.url_bukti_follow
        ]

        print(data_to_append)

        append_data(worksheet, data_to_append)

        # Persiapan respons
        response_data = {
            "message": "success",
            "data": {
                "formatted_datetime": formatted_datetime,
                "full_name": request.full_name,
                "email": request.email,
                "phone_number": request.phone_number,
                "institution": request.institution,
                "profession": request.profession,
                "address": request.address,
                "url_bukti_pembayaran": request.url_bukti_pembayaran,
                "url_bukti_follow": request.url_bukti_follow
            },
            "row_inserted": worksheet.row_count
        }

        print(response_data)

        return response_data

    except Exception as e:
        return {"message": str(e)}
