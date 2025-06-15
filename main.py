import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
import httpx
import shutil
import uuid

load_dotenv()  # Load variables from .env

# Initialize FastAPI app
app = FastAPI()

REMOTE_URL = os.environ.get("REMOTE_URL", "http://localhost:8000/predict")

@app.post("/predict")
async def predict(image: UploadFile = File(...)):
    # Save image temporarily
    temp_filename = f"/tmp/{uuid.uuid4()}_{image.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Send file to remote model endpoint
    with open(temp_filename, "rb") as img_file:
        files = {"file": (image.filename, img_file, image.content_type)}
        async with httpx.AsyncClient() as client:
            response = await client.post(REMOTE_URL, files=files)

    # Remove the temporary file
    os.remove(temp_filename)

    # Return the remote model's response
    return response.json()
