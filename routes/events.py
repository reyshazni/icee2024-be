from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, Form, Depends, File
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from google.cloud import firestore
from datetime import datetime, timedelta, timezone
import os
from utils import connect, open_worksheet, append_data
from fastapi.routing import APIRouter
from models.events import EventCategoryEnum, SeminarRequest, FileTypeEnum, DataDiri
from models.admin import CategoryEnum, ClassEnum
from dotenv import load_dotenv, dotenv_values
from service.firebase import get_firebase_storage
from service.storage import upload_file

load_dotenv()
config = dotenv_values(".env")
spreadsheet_name = config["SPREADSHEET_NAME"]
allowed_formats = {'jpeg', 'jpg', 'png'}
credentials_file = "sa.json"

# Create the FastAPI app
app = FastAPI()

# Create the event_router
event_router = APIRouter(tags=["Registration"])
admin_router = APIRouter(tags=["Admin"])
asset_router = APIRouter(tags=["Assets"])

CREDENTIAL_PATH = "sa.json"
BUCKET_NAME = "icee24"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_PATH

db = firestore.Client()

@event_router.post("/seminar")
async def upload_data_seminar(request: SeminarRequest):
    try:
        print("connecting to spreadsheet")
        spreadsheet = connect(credentials_file)

        worksheet = open_worksheet(spreadsheet, spreadsheet_name, "seminar")
        jakarta_timezone = timezone(timedelta(hours=7))

        for data_diri in request.data_diri:
            current_datetime_wib = datetime.now(jakarta_timezone)
            formatted_datetime = current_datetime_wib.strftime("%m/%d/%Y %H:%M:%S")

            nim_value = data_diri.nim if data_diri.nim else "-"
            data_to_append = [
                formatted_datetime,
                data_diri.nama_lengkap,
                data_diri.email,
                data_diri.no_telp,
                data_diri.institusi,
                data_diri.pekerjaan,
                data_diri.alamat,
                nim_value,
                request.file_url
            ]

            print(data_to_append)
            append_data(worksheet, data_to_append)

        response_data = {
            "status_code": 200,
            "status": "success",
            "data": {
                "message": "Data berhasil diupload",
                "number_of_participants": len(request.data_diri),
                "row_inserted": worksheet.row_count
            }
        }

        print(response_data)
        return response_data

    except Exception as e:
        response_data = {
            "status_code": 500,
            "status": "failed",
            "data": {
                "message": f"Error occurred: {str(e)}"
            }
        }

        print(response_data)
        return response_data

# Define a route to test the upload_file function
@event_router.post("/upload-registrant/")
async def test_upload_file(
    file: UploadFile = File(...),
    type: FileTypeEnum = Form(...),
    event: EventCategoryEnum = Form(...),
    owner: str = Form(None),
):
    try:
        # Call the upload_file function with the provided parameters
        file_url = await upload_file(file, type, event, owner)

        response_data = {
            "status_code": 200,
            "status": "success",
            "data": {
                "message": "file berhasil diupload",
                "file_url": file_url
            }
        }
        
        # Return a JSONResponse with the file URL
        return response_data
    except Exception as e:
        # Handle any exceptions and return an error response
        response_data = {
            "status_code": 500,
            "status": "failed",
            "data": {
                "message": str(e)
            }
        }
        return response_data