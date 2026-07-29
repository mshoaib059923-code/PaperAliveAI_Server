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

        # Image processing
        gray = image.convert("L")

        width, height = gray.size

        pixels = list(gray.getdata())

        dark_pixels = 0

        for p in pixels:
            if p < 150:
                dark_pixels += 1

        total_pixels = len(pixels)

        drawing_ratio = dark_pixels / total_pixels


        # Simple recognition
        if drawing_ratio < 0.05:
            result = "Very light drawing"

        elif drawing_ratio < 0.20:
            result = "Possible Bird or Character Drawing"

        elif drawing_ratio < 0.40:
            result = "Possible Animal/Object Drawing"

        else:
            result = "Heavy Drawing Detected"


        return {
            "status": "success",
            "message": "Image processed",
            "size": f"{width}x{height}",
            "drawing_ratio": round(drawing_ratio, 2),
            "AI_result": result
        }


    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }