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


def recognize_drawing(width, height):
    if width > height:
        return "Possible Animal or Object Drawing"
    elif height > width:
        return "Possible Bird or Character Drawing"
    else:
        return "Possible Face or Round Object Drawing"
@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.body()

        image_data = base64.b64decode(data)

        image = Image.open(BytesIO(image_data))

        width, height = image.size

        # Basic AI preparation
        result = recognize_drawing(width, height)

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