from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from google.cloud import firestore
from datetime import datetime, timedelta, timezone
import os
from utils import connect, open_worksheet, append_data
from fastapi.routing import APIRouter
from models.events import SeminarRequest, FileTypeEnum, DataDiriSeminar, EventCategoryEnum
from models.admin import CategoryEnum, ClassEnum
from dotenv import load_dotenv, dotenv_values
from service.sanitizer import filename_url_sanitizer

load_dotenv()
credentials_file = "sa.json"

CREDENTIAL_PATH = "sa.json"
BUCKET_NAME = "icee24"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_PATH

firebase_storage = storage.bucket(name=BUCKET_NAME)

async def upload_file(file: UploadFile, type: FileTypeEnum, event: EventCategoryEnum, owner: str = None):
    allowed_formats = {'pdf': 'application/pdf', 'jpeg': 'image/jpeg', 'jpg': 'image/jpeg', 'png': 'image/png', 'heic': 'image/heic'}
    max_file_size = 20 * 1024 * 1024  # 20 MB

    try:
        file_format = file.filename.split('.')[-1].lower()
        if file_format not in allowed_formats:
            raise HTTPException(status_code=400, detail="Format file tidak didukung")

        file_size = file.file.seek(0, 2)
        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="Ukuran file terlalu besar")

        file.file.seek(0)

        sanitized_file_name = filename_url_sanitizer(file.filename)

        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        if owner:
            new_filename = f"{owner}.{current_time}.{sanitized_file_name}"
        else:
            new_filename = f"{current_time}.{sanitized_file_name}"


        # Get the content type based on the file format
        content_type = allowed_formats[file_format]

        # Construct the destination path with the folder (type) included
        destination_path = f"registration/{type}/{event}/{new_filename}"

        blob = firebase_storage.blob(destination_path)  # Use the destination path

        # Set the content type when uploading the file
        blob.upload_from_file(file.file, content_type=content_type)

        file_url = f"https://storage.googleapis.com/{firebase_storage.name}/{destination_path}"
        
        # Return a JSONResponse with the custom response data and status code
        return file_url

    except HTTPException as http_exception:
        # Create a response dictionary for error cases
        response_data = {"status_code": http_exception.status_code, "status": "failed", "message": http_exception.detail}
        
        # Return a JSONResponse with the custom error response data and status code
        return JSONResponse(content=response_data, status_code=http_exception.status_code)
    except Exception as e:
        # Create a response dictionary for general exceptions
        response_data = {"status_code": 500, "status": "failed", "message": f"Terjadi kesalahan: {str(e)}"}
        
        # Return a JSONResponse with the custom error response data and status code
        return JSONResponse(content=response_data, status_code=500)