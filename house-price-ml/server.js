/**
 * server.js — Node.js/Express: phục vụ giao diện demo và gọi sang Python service
 * (service/predict_service.py) để lấy kết quả dự đoán giá nhà.
 * Người phụ trách: Nguyễn Văn Thành.
 *
 * Cách chạy:
 *   npm install express node-fetch@2
 *   node server.js
 * Mặc định chạy ở http://localhost:3000
 *
 * Yêu cầu: service/predict_service.py đang chạy ở http://127.0.0.1:5001
 */

const path = require("path");
const express = require("express");
const fetch = require("node-fetch"); // node-fetch@2 (dùng require được, bản 3 chỉ hỗ trợ import)

const app = express();
const PORT = 3000;
const PREDICT_SERVICE_URL = "http://127.0.0.1:5001/predict";

app.use(express.json());
app.use(express.static(path.join(__dirname, "public"))); // phục vụ public/index.html

// Các trường form demo cho phép gửi lên — khớp với feature_defaults.json
const ALLOWED_FIELDS = [
  "LotArea",
  "OverallQual",
  "YearBuilt",
  "GrLivArea",
  "Neighborhood",
  "GarageType",
];

function validateInput(body) {
  const errors = [];
  const cleaned = {};

  for (const field of ALLOWED_FIELDS) {
    if (body[field] === undefined || body[field] === "" || body[field] === null) {
      continue; // để trống -> predict_service sẽ tự điền giá trị mặc định
    }
    cleaned[field] = body[field];
  }

  const numericFields = ["LotArea", "OverallQual", "YearBuilt", "GrLivArea"];
  for (const field of numericFields) {
    if (cleaned[field] !== undefined) {
      const num = Number(cleaned[field]);
      if (Number.isNaN(num)) {
        errors.push(`${field} phải là số.`);
      } else {
        cleaned[field] = num;
      }
    }
  }

  return { errors, cleaned };
}

app.post("/predict", async (req, res) => {
  const { errors, cleaned } = validateInput(req.body || {});

  if (errors.length > 0) {
    return res.status(400).json({ error: errors.join(" ") });
  }

  try {
    const response = await fetch(PREDICT_SERVICE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(cleaned),
    });

    if (!response.ok) {
      const errText = await response.text();
      return res.status(502).json({ error: `Predict service lỗi: ${errText}` });
    }

    const data = await response.json();
    return res.json(data);
  } catch (err) {
    return res.status(500).json({
      error: "Không kết nối được đến predict service. Đã chạy 'python service/predict_service.py' chưa?",
      detail: err.message,
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server demo đang chạy tại http://localhost:${PORT}`);
});