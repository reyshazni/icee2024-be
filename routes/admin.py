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
from models.events import SeminarRequest, FileTypeEnum, DataDiri
from models.admin import CategoryEnum, ClassEnum
from dotenv import load_dotenv, dotenv_values
from service.firebase import get_firebase_storage

load_dotenv()
config = dotenv_values(".env")
spreadsheet_name = config["SPREADSHEET_NAME"]
access_code1 = config["ACCESS_CODE1"]
access_code2 = config["ACCESS_CODE2"]
access_code3 = config["ACCESS_CODE3"]
allowed_formats = {'jpeg', 'jpg', 'png'}
credentials_file = "sa.json"

# Create a list of access codes
allowed_access_codes = [access_code1, access_code2, access_code3]

# Create the FastAPI app
app = FastAPI()

# Create the event_router
admin_router = APIRouter(tags=["Admin"])
asset_router = APIRouter(tags=["Assets"])

CREDENTIAL_PATH = "sa.json"
BUCKET_NAME = "icee24"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIAL_PATH

db = firestore.Client()

content_types = {
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
}

@admin_router.post("/upload-partner")
async def upload_sponsor(access_code: str, kelas: ClassEnum, category: CategoryEnum, file: UploadFile, nama_sponsor: str):
    max_mb_file_size = 20
    
    max_file_size = max_mb_file_size * 1024 * 1024
    try:
        # Validate the access_code
        if access_code not in allowed_access_codes:
            raise HTTPException(status_code=400, detail="Access code is not valid")
        file_format = file.filename.split('.')[-1].lower()
        if file_format not in allowed_formats:
            raise HTTPException(status_code=400, detail="Format file tidak didukung")

        file_size = file.file.seek(0, 2)
        if file_size > max_file_size:
            raise HTTPException(status_code=400, detail="Ukuran file terlalu besar")

        file.file.seek(0)

        current_time = datetime.now().strftime("%Y%m%d%H%M%S")

        # Modify the filename by appending the file format and replacing spaces with underscores
        new_filename = f"{nama_sponsor.replace(' ', '_')}.{file_format}"

        destination_path = f"{kelas}/{category}/{new_filename}"

        blob = get_firebase_storage.blob(destination_path)


        if file_format in content_types:
            blob.content_type = content_types[file_format]

        blob.upload_from_file(file.file)

        file_url = f"https://storage.googleapis.com/{firebase_storage.name}/{destination_path}"

        # Create a new document with an auto-generated ID in the "partners" collection
        data = {
            "name": nama_sponsor,
            "category": kelas,
            "size": category,
            "file_url": file_url,
        }

        db.collection("partners").add(data)

        return {"message": "success", "file_url": file_url}

    except HTTPException as http_exception:
        return {"message": http_exception.detail}
    except Exception as e:
        return {"message": f"Terjadi kesalahan: {str(e)}"}

@admin_router.get("/all-partner-name")
async def get_all_partner_names():
    try:
        # Query Firestore to get all documents in the "partners" collection
        query = db.collection("partners").stream()

        partner_names = []

        for doc in query:
            data = doc.to_dict()
            partner_name = data.get("name")
            if partner_name:
                partner_names.append(partner_name)

        return partner_names

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

@admin_router.get("/partner-detail/")
async def get_partner_detail(partner_name: str):
    try:
        # Query Firestore to find a document with the specified partner name
        query = db.collection("partners").where("name", "==", partner_name).stream()

        partner_detail = None

        for doc in query:
            partner_detail = doc.to_dict()
            break  # Assuming there is only one partner with the given name

        if partner_detail:
            return partner_detail
        else:
            raise HTTPException(status_code=404, detail="Partner not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

@admin_router.delete("/delete-partner/")
async def delete_partner(access_code:str, partner_name: str):
    try:
        # Validate the access_code
        if access_code not in allowed_access_codes:
            raise HTTPException(status_code=400, detail="Access code is not valid")
        # Query Firestore to find a document with the specified partner name
        query = db.collection("partners").where("name", "==", partner_name).stream()

        for doc in query:
            # Delete the document with the matching partner name
            doc.reference.delete()
            return {"message": f"Partner '{partner_name}' deleted successfully"}

        # If no matching document is found, raise a 404 Not Found exception
        raise HTTPException(status_code=404, detail="Partner not found")

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

## ASSETS ROUTER
@asset_router.get("/url-media")
async def url_media_partners():
    try:
        # Query Firestore to get all documents in "partners" collection with category "media_partner"
        query = db.collection("partners").where("category", "==", "media_partner").stream()

        media_partners = []

        for doc in query:
            media_partners.append(doc.to_dict())

        # Prepare the success response
        response_data = {
            "status_code": 200,
            "status": "success",
            "data": media_partners
        }

        return response_data

    except Exception as e:
        # Prepare the error response
        response_data = {
            "status_code": 500,
            "status": "failed",
            "message": f"Terjadi kesalahan: {str(e)}"
        }

        raise HTTPException(status_code=500, detail=response_data)

# Modify the url_sponsors endpoint
@asset_router.get("/url-sponsor")
async def url_sponsors():
    try:
        # Query Firestore to get all documents in "partners" collection with category "sponsor"
        query = db.collection("partners").where("category", "==", "sponsor").stream()

        sponsors = []

        for doc in query:
            sponsors.append(doc.to_dict())

        # Prepare the success response
        response_data = {
            "status_code": 200,
            "status": "success",
            "data": sponsors
        }

        return response_data

    except Exception as e:
        # Prepare the error response
        response_data = {
            "status_code": 500,
            "status": "failed",
            "message": f"Terjadi kesalahan: {str(e)}"
        }

        raise HTTPException(status_code=500, detail=response_data)