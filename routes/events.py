from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models.events import WebinarRegistrationRequest
import os
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from utils import connect, open_worksheet, append_data

credential_path = "sa.json"

cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

db = firestore.Client(project='icee-2023')

event_router = APIRouter(
    tags=["Events"]
)

@event_router.post("/register")
async def register(request: WebinarRegistrationRequest):
    try:
        # Lakukan validasi atau pemrosesan data sesuai kebutuhan

        # Tambahkan data ke spreadsheet menggunakan dependensi yang disediakan
        credentials_file = "sa.json"
        spreadsheet = connect(credentials_file)

        worksheet = open_worksheet(spreadsheet, "[Testing] Registrant", "event1")  # Sesuaikan nama worksheet sesuai kebutuhan

        data_to_append = [request.full_name, request.email, request.phone_number, request.organization, request.webinar_id]
        append_data(worksheet, data_to_append)

        # Mengembalikan respons sukses
        return {"message": "success", "data": request.dict()}

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})