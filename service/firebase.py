import firebase_admin
from firebase_admin import credentials, initialize_app, storage

CREDENTIAL_PATH = "sa.json"
BUCKET_NAME = "icee24"

# Initialize Firebase
cred = credentials.Certificate(CREDENTIAL_PATH)
firebase_app = initialize_app(cred)

# Initialize Firebase Storage
firebase_storage = storage.bucket(app=firebase_app, name=BUCKET_NAME)

def get_firebase_app():
    return firebase_app

def get_firebase_storage():
    return firebase_storage