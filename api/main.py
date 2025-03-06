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
connected_clients = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Lưu kết nối WebSocket của client vào dictionary
    connected_clients[websocket.client] = websocket
    logger.info("[Core] WebSocket connected")
    
    try:
        while True:
            # Nhận message từ client
            message = await websocket.receive_text()
            logger.info(f"[Core] Received message: {message}")
            
            # Xử lý message (ví dụ: gọi hàm xử lý gRPC)
            # Bạn có thể gửi lại kết quả cho client tại đây (sẽ làm sau)

    except WebSocketDisconnect:
        # Xóa client khỏi danh sách khi ngắt kết nối
        if websocket.client in connected_clients:
            del connected_clients[websocket.client]
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

    # Sau khi xử lý thành công, gửi thông báo tới tất cả client (hoặc 1 client cụ thể)
    # Bạn có thể gửi message cho client đã upload file
    if connected_clients:
        # Giả sử bạn muốn gửi đến tất cả các client kết nối
        for client_ws in connected_clients.values():
            try:
                await client_ws.send_text(f"File {filename} processed: {message}")
                logger.info("[Core] Sent message to client")
            except WebSocketDisconnect:
                logger.warning("[Core] WebSocket client disconnected")

    return {"message": message}