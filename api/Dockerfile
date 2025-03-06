# Sử dụng Python 3.11
FROM python:3.11

# Cấu hình thư mục làm việc
WORKDIR /app

# Cài đặt Poetry
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Thêm Poetry vào PATH
ENV PATH="/root/.local/bin:$PATH"

# Kiểm tra Poetry đã được cài chưa
RUN poetry --version

# Copy file cấu hình dependencies trước để tối ưu cache Docker
COPY pyproject.toml poetry.lock ./

# Cài đặt dependencies đầy đủ
RUN poetry install --no-root

# Copy thư mục proto (quan trọng)
COPY ./proto /app/proto

# **Chạy lệnh compile gRPC đúng cách**
RUN poetry run python -m grpc_tools.protoc -I/app/proto --python_out=/app --grpc_python_out=/app /app/proto/media.proto

# Copy toàn bộ mã nguồn
COPY . .

# Expose port 8000
EXPOSE 8000

# Chạy ứng dụng FastAPI bằng Poetry
CMD ["sh", "-c", "poetry run uvicorn main:app --host 0.0.0.0 --port 8000"]