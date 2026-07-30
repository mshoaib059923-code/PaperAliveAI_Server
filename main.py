from PIL import Image, ImageEnhance
from io import BytesIO
from fastapi import FastAPI, Request
import os
import base64
import uuid
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
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
@app.post("/animate")
async def animate(request: Request):
    try:
        data = await request.body()

        image_data = base64.b64decode(data)

        image = Image.open(BytesIO(image_data)).convert("RGBA")

        frames = []

        # 6 animation frames
        for i in range(6):

            frame = image.copy()

            # zoom effect
            if i % 2 == 0:
                frame = frame.resize(
                    (frame.width + 10, frame.height + 10)
                )

            # brightness effect
            enhancer = ImageEnhance.Brightness(frame)
            frame = enhancer.enhance(1 + (i * 0.03))

            frames.append(frame)


        filename = f"{uuid.uuid4()}.gif"

        filepath = os.path.join(
            "uploads",
            filename
        )


        frames[0].save(
            filepath,
            save_all=True,
            append_images=frames[1:],
            duration=300,
            loop=0
        )


      return filename


    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }