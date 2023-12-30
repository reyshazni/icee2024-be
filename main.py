from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv, dotenv_values
from routes.events import event_router, admin_router, asset_router

app = FastAPI()

load_dotenv()
config = dotenv_values(".env")
environment_name = config["ENVIRONMENT"]

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router, prefix="/admin")
app.include_router(event_router, prefix="/register")
app.include_router(asset_router, prefix="/asset")

desc = "ICEE 2024 "+environment_name+" Server."

@app.get("/")
async def home():
    return {"message": desc}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")
