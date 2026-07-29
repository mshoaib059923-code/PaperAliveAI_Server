from PIL import Image
from io import BytesIO
from fastapi import FastAPI, Request
import os
import base64
import uuid

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "Naaz Paper Alive AI Server Running"
    }


@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.body()

        image_data = base64.b64decode(data)

        image = Image.open(BytesIO(image_data))

        width, height = image.size

        # Basic AI preparation
        result = "Drawing detected"

        return {
            "status": "success",
            "message": "Image analyzed",
            "image_size": f"{width}x{height}",
            "AI_result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }