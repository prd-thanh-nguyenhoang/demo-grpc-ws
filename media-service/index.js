const express = require("express");
const multer = require("multer");
const cors = require("cors");

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(cors());
app.use(express.urlencoded({ extended: true }));

app.post("/process", upload.single("file"), (req, res) => {
  console.log(`Processing ${req.body?.filename}, timeout ${req.body?.timeout}`);
  const { filename, timeout } = req.body;

  setTimeout(() => {
    if (filename === "success.pdf") {
      console.log(`Done ${req.body?.filename}, timeout ${req.body?.timeout}`);

      return res.json({ message: "Success" });
    } else if (filename === "failure.pdf") {
      console.log(`Done ${req.body?.filename}, timeout ${req.body?.timeout}`);

      return res.json({ message: "Failure" });
    } else {
      console.log(`Done ${req.body?.filename}, timeout ${req.body?.timeout}`);

      return res.json({ message: `Processed: ${filename}` });
    }
  }, timeout);
});

app.listen(5000, () => console.log("Media Service running on port 5000"));
