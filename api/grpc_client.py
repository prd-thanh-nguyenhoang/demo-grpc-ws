import grpc
from proto import media_pb2, media_pb2_grpc

MEDIA_SERVICE_HOST = "media-service:50051"  # Địa chỉ của media-service

def process_file(filename: str, timeout: int, file_data: bytes):
    """Gửi request gRPC tới media-service"""
    with grpc.insecure_channel(MEDIA_SERVICE_HOST) as channel:
        stub = media_pb2_grpc.MediaServiceStub(channel)
        request = media_pb2.FileRequest(filename=filename, timeout=timeout, file=file_data)
        response = stub.ProcessFile(request)
        return response.message