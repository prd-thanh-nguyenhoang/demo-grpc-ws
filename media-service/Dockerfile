# Sử dụng Node.js phiên bản mới nhất
FROM node:18-alpine

# Cấu hình thư mục làm việc
WORKDIR /app

# Copy package.json và cài đặt dependencies
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

# Copy thư mục proto trước để Docker cache
COPY proto /app/proto

# Copy toàn bộ source code vào container
COPY . .

# Expose port 4000
EXPOSE 4000

# Chạy ứng dụng
CMD ["pnpm", "start"]