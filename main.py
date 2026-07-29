from fastapi import FastAPI, UploadFile, File
import os
import shutil

app = FastAPI()

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "Naaz Paper Alive AI Server Running"
    }

from fastapi import Request

@app.post("/upload")
async def upload(request: Request):
    form = await request.form()

    return {
        "fields": list(form.keys())
    }