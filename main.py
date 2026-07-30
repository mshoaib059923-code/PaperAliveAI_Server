from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse
from PIL import Image, ImageEnhance
from io import BytesIO
import base64
import uuid
import os

app = FastAPI()

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")


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

        gray = image.convert("L")

        width, height = gray.size

        pixels = list(gray.getdata())

        dark_pixels = 0

        for p in pixels:
            if p < 150:
                dark_pixels += 1

        total_pixels = len(pixels)

        drawing_ratio = dark_pixels / total_pixels

        if drawing_ratio < 0.05:
            result = "Very Light Drawing"

        elif drawing_ratio < 0.20:
            result = "Possible Bird or Character Drawing"

        elif drawing_ratio < 0.40:
            result = "Possible Animal or Object Drawing"

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


@app.post("/animate")
async def animate(request: Request):

    try:

        data = await request.body()

        image_data = base64.b64decode(data)

        image = Image.open(BytesIO(image_data)).convert("RGBA")

        frames = []

        for i in range(6):

            frame = image.copy()

            if i % 2 == 0:
                frame = frame.resize(
                    (frame.width + 10, frame.height + 10)
                )

            enhancer = ImageEnhance.Brightness(frame)

            frame = enhancer.enhance(1 + (i * 0.03))

            frames.append(frame)

        filename = f"{uuid.uuid4()}.gif"

        filepath = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        frames[0].save(
            filepath,
            save_all=True,
            append_images=frames[1:],
            duration=250,
            loop=0
        )

        return PlainTextResponse(filename)

    except Exception as e:

        return PlainTextResponse(str(e), status_code=500)