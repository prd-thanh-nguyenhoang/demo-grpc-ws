const express = require("express");
const multer = require("multer");
const cors = require("cors");
const grpc = require("@grpc/grpc-js");
const protoLoader = require("@grpc/proto-loader");

const app = express();
const upload = multer({ dest: "uploads/" });
app.use(cors());
app.use(express.urlencoded({ extended: true }));

// gRPC Setup
const PROTO_PATH = "./proto/media.proto";
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const mediaProto = grpc.loadPackageDefinition(packageDefinition).media;

function processFile(call, callback) {
  const { filename, timeout } = call.request;
  console.log(`[Media Service] Processing (gRPC): ${filename} (${timeout}s)`);

  let remainingTime = timeout * 2; // Bắt đầu đếm ngược từ timeout

  const interval = setInterval(() => {
    console.log(`[Media Service] Countdown: ${remainingTime}s left`);
    remainingTime--;

    if (remainingTime <= 0) {
      clearInterval(interval); // Dừng interval khi countdown kết thúc
      console.log(`[Media Service] Completed processing: ${filename}`);

      // Gửi response cho Core thông qua callback
      const message = filename == "main.cpp" ? "Error" : "Success";
      callback(null, { message: `Processed (gRPC): ${message}` });
      console.log(
        `[Media Service] Sent response to Core: Processed (gRPC): ${filename}`
      );
    }
  }, 1000);
}

const server = new grpc.Server();
server.addService(mediaProto.MediaService.service, {
  ProcessFile: processFile,
});
server.bindAsync(
  "0.0.0.0:50051",
  grpc.ServerCredentials.createInsecure(),
  () => {
    console.log("[Media Service] gRPC Server running on port 50051");
  }
);

// REST API
app.post("/process", upload.single("file"), (req, res) => {
  console.log(`[Media Service] Processing (REST): ${req.body.filename}`);
  setTimeout(() => {
    res.json({ message: `Processed (REST): ${req.body.filename}` });
  }, 3000);
});

app.listen(5000, () =>
  console.log("[Media Service] REST API running on port 5000")
);
