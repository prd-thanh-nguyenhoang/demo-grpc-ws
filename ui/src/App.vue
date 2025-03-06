<script setup>
import { ref } from "vue";
import axios from "axios";

const file = ref(null);
const filename = ref("");
const uploadStatus = ref("");
const timeout = ref(5); // Default timeout 5s
const isLoading = ref(false);

const uploadFile = async () => {
  if (!file.value || !filename.value) {
    uploadStatus.value = "Please select a file and enter a name!";
    return;
  }

  const formData = new FormData();
  formData.append("file", file.value);
  formData.append("filename", filename.value);
  formData.append("timeout", timeout.value * 1000); // Convert to milliseconds

  try {
    isLoading.value = true;
    const response = await axios.post("http://localhost:8000/upload", formData);
    const { message } = response.data;

    setTimeout(() => {
      alert(`Upload Done: ${message}`);
    }, 500); // Delay to show alert

    uploadStatus.value = `Uploaded: ${message}`;
  } catch (error) {
    uploadStatus.value = "Upload failed";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div>
    <h1>Upload File</h1>

    <label>Filename:</label>
    <input v-model="filename" placeholder="Enter filename (e.g. success.pdf)" />

    <label>Timeout (seconds):</label>
    <input type="number" v-model="timeout" min="1" />

    <input type="file" @change="(e) => (file = e.target.files[0])" />

    <button @click="uploadFile" :disabled="isLoading">
      {{ isLoading ? "Uploading..." : "Upload" }}
    </button>

    <p>{{ uploadStatus }}</p>
  </div>
</template>
