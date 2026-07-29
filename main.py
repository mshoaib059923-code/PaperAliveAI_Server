from PIL import Image
from io import BytesIO
from PIL import Image
from io import BytesIO
from fastapi import FastAPI, Request
import os
import base64
import uuid

app = FastAPI()
model = models.resnet50(weights="DEFAULT")
model.eval()

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {
        "status": "OK",
        "message": "Naaz Paper Alive AI Server Running"
    }

@app.post("/upload")
async def upload(request: Request):
    try:
        data = await request.body()

        image_data = base64.b64decode(data)

        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        return {
            "status": "success",
            "filename": filename
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.body()

        image_data = base64.b64decode(data)

        image = Image.open(BytesIO(image_data))

        width, height = image.size

        return {
            "status": "success",
            "message": "Image received for AI analysis",
            "width": width,
            "height": height
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }