from fastapi import FastAPI, File, Form, UploadFile
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc ["http://localhost:5173"] nếu muốn chỉ định cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
MEDIA_SERVICE_URL = "http://media-service:5000/process"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), filename: str = Form(...), timeout: int = Form(...)):
    files = {"file": (file.filename, await file.read())}
    data = {"filename": filename, "timeout": timeout}
    print(f'Request body core: files {files[0][filename]} , data : {data}')
    try:
        response = requests.post(MEDIA_SERVICE_URL, files=files, data=data, timeout=timeout / 1000)
        print(f'Response: {response}')

        return response.json()
    except requests.Timeout:
        return {"message": "Timeout Error"}