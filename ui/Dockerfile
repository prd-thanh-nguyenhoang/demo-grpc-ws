# Sử dụng Node.js phiên bản mới nhất
FROM node:18-alpine

# Cấu hình thư mục làm việc
WORKDIR /app

# Copy package.json và cài đặt dependencies
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

# Copy toàn bộ source code vào container
COPY . .

# Expose port 3000
EXPOSE 3000

# Chạy ứng dụng
CMD ["pnpm", "dev"]