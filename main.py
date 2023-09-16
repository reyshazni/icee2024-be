from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from routes.events import event_router, admin_router

app = FastAPI()

app.include_router(admin_router, prefix="/admin")
app.include_router(event_router, prefix="/register")

@app.get("/")
async def home():
    return {"message": "Hello Hacker!"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")
