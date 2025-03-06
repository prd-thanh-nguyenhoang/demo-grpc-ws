# Sử dụng Python phiên bản mới nhất
FROM python:3.11

# Cấu hình thư mục làm việc
WORKDIR /app

# Copy file cấu hình dependencies
COPY pyproject.toml poetry.lock README.md ./

# Cài đặt Poetry và các thư viện cần thiết
RUN pip install poetry && poetry install --no-root

# Copy toàn bộ mã nguồn
COPY . .

# Expose port 8000
EXPOSE 8000

# Chạy ứng dụng FastAPI
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]