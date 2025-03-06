from fastapi import FastAPI, File, Form, UploadFile, WebSocket
import logging
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from grpc_client import process_file  # Import gRPC client


# Cấu hình logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA_SERVICE_URL = "http://media-service:5000/process"
MEDIA_SERVICE_GRPC_HOST = "media-service:50051"
executor = ThreadPoolExecutor()

from starlette.websockets import WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # connected_clients.append(websocket)  # Thêm client vào danh sách kết nối khi kết nối thành công
    logger.info("[Core] WebSocket connected")
    
    try:
        while True:
            # Nhận message từ client
            message = await websocket.receive_text()
            logger.info(f"[Core] Received message: {message}")

            # Xử lý message (ví dụ: gọi hàm xử lý gRPC)

            await websocket.send_text(f"Processed (gRPC): {message} from server core")
    except WebSocketDisconnect:
        logger.info("[Core] WebSocket disconnected")
    except Exception as e:
        logger.error(f"[Core] WebSocket error: {e}")
        await websocket.send_text(f"Error: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), filename: str = Form(...), timeout: int = Form(...)):
    file_data = await file.read()  # Đọc dữ liệu file
    logger.info(f"[Core] Received file: {filename} with timeout {timeout}s")
    
    # Gửi file qua gRPC
    message = process_file(filename, timeout, file_data)
    
    # Log thông tin phản hồi từ media-service
    logger.info(f"[Core] Media service response: {message}")
    
    return {"message": message}