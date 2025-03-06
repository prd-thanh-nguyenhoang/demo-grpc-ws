<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const file = ref(null);
const filename = ref("");
const timeout = ref(5); // Giá trị mặc định là 5
const uploadStatus = ref("Chưa upload");
const isLoading = ref(false);
const socket = ref(null);
const wsStatus = ref("Đang kết nối..."); // Trạng thái WebSocket

// Hàm upload file
const uploadFile = async () => {
  if (!file.value || !filename.value) {
    uploadStatus.value = "Vui lòng chọn file và nhập tên!";
    return;
  }

  const formData = new FormData();
  formData.append("file", file.value);
  formData.append("filename", filename.value);
  formData.append("timeout", timeout.value); // Thêm timeout vào request

  try {
    isLoading.value = true;
    uploadStatus.value = "File đang được xử lý..."; // Cập nhật trạng thái ngay khi gọi API
    // Gửi request upload đến server
    await axios.post(import.meta.env.VITE_API_URL + "/upload", formData);
    console.log("[UI] Upload request sent successfully.");

    // Sau khi upload thành công, gửi thông điệp WebSocket
    socket.value.send(`File uploaded: ${filename.value}`);
  } catch (error) {
    console.error("[UI] Upload error:", error);
    uploadStatus.value = "Lỗi khi upload file!";
    isLoading.value = false;
  }
};

onMounted(() => {
  // Kết nối WebSocket khi component được mount
  socket.value = new WebSocket(import.meta.env.VITE_WS_URL);

  socket.value.onopen = () => {
    console.log("[UI] WebSocket connected");
    wsStatus.value = "WebSocket connected"; // Cập nhật trạng thái khi kết nối thành công
  };

  socket.value.onmessage = (event) => {
    console.log("[UI] WebSocket message received:", event);
    uploadStatus.value = event.data; // Cập nhật trạng thái với dữ liệu từ server
    isLoading.value = false; // Dừng trạng thái loading
  };

  socket.value.onerror = () => {
    console.error("[UI] WebSocket error");
    wsStatus.value = "Lỗi kết nối WebSocket!"; // Cập nhật trạng thái nếu có lỗi kết nối
    isLoading.value = false;
  };

  socket.value.onclose = () => {
    wsStatus.value = "WebSocket closed"; // Cập nhật trạng thái khi WebSocket bị đóng
    console.log("[UI] WebSocket closed");
  };
});
</script>

<template>
  <div>
    <h1>Upload File</h1>
    <!-- Nhập tên file -->
    <input v-model="filename" placeholder="Nhập tên file (e.g. success.pdf)" />
    <!-- Chọn file -->
    <input type="file" @change="(e) => (file = e.target.files[0])" />
    <!-- Nhập timeout -->
    <input
      type="number"
      v-model="timeout"
      min="1"
      placeholder="Nhập timeout (mặc định 5)"
    />
    <!-- Nút upload -->
    <button @click="uploadFile" :disabled="isLoading">
      {{ isLoading ? "Uploading..." : "Upload" }}
    </button>
    <!-- Hiển thị trạng thái -->
    <p>Trạng thái upload: {{ uploadStatus }}</p>
    <p>Trạng thái WebSocket: {{ wsStatus }}</p>
  </div>
</template>
