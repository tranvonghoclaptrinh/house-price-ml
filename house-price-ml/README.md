# Quy trình thực hiện — Dự đoán giá nhà sử dụng mô hình học máy

Nhóm 9 — Học phần Học máy (15DHKHDL05)

Tài liệu này ghi rõ **thứ tự chạy**, **người phụ trách** từng bước và **điều kiện cần có trước** khi chạy, để cả nhóm không giẫm chân nhau và không bị chạy nhầm thứ tự.

---

## 0. Chuẩn bị chung (tất cả thành viên)

| Việc | Lệnh |
|---|---|
| Clone repo về máy | `git clone <link-repo>` |
| Cài thư viện Python | `pip install -r requirements.txt` |
| Cài thư viện Node.js (chỉ cần cho Thành) | `npm install express node-fetch@2` |

Chỉ cần làm 1 lần trên mỗi máy.

---

## 1. Quy trình theo thứ tự

| Bước | Người thực hiện | Việc làm | Lệnh chạy | Điều kiện cần trước |
|---|---|---|---|---|
| 1 | **Khang** | Tải `train.csv` từ Kaggle (House Prices – Advanced Regression Techniques), đặt vào `data/train.csv` | — | Đã có tài khoản Kaggle |
| 2 | **Khang** | Chạy EDA: thống kê dữ liệu, kiểm tra missing values, biểu đồ phân phối `SalePrice`, ma trận tương quan | `python notebooks_or_src_py/eda.py` | Bước 1 xong |
| 3 | **Vinh** | Huấn luyện và so sánh 5 mô hình (Linear Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost) | `python notebooks_or_src_py/train_compare.py` | Bước 1 xong (nên xem qua kết quả EDA ở bước 2 trước) |
| 4 | **Vinh** | Tính giá trị mặc định (median/mode) cho các cột form demo không hỏi tới | `python notebooks_or_src_py/export_defaults.py` | Bước 1 xong |
| 5 | **Thành** | Chạy Python service — nạp mô hình tốt nhất, mở API nội bộ | `python service/predict_service.py` | Bước 3 và 4 đã xong (cần `models/best_model.pkl` và `models/feature_defaults.json`) |
| 6 | **Thành** | Chạy server Node.js/Express — phục vụ giao diện, gọi sang Python service | `node server.js` | Bước 5 đang chạy (mở terminal khác, không tắt terminal bước 5) |
| 7 | **Thành** | Mở trình duyệt kiểm tra demo | Truy cập `http://localhost:3000` | Bước 6 đang chạy |

> Bước 5 và 6 chạy **song song ở 2 terminal khác nhau**, không phải chạy xong bước này mới tắt để chạy bước kia.

---

## 2. Sơ đồ luồng dữ liệu

```
[Khang] data/train.csv
        │
        ▼
[Khang] eda.py  ──► results/ (biểu đồ, báo cáo missing values)
        │
        ▼
[Vinh]  train_compare.py ──► models/best_model.pkl
        │                     results/model_results.csv
        ▼
[Vinh]  export_defaults.py ──► models/feature_defaults.json
        │
        ▼
[Thành] service/predict_service.py  (nạp model, mở API cổng 5001)
        │
        ▼
[Thành] server.js  (giao diện + gọi sang service, cổng 3000)
        │
        ▼
   Trình duyệt: http://localhost:3000
```

---

## 3. Việc của Vọng và Diễm trong giai đoạn này

| Thành viên | Vai trò | Việc làm |
|---|---|---|
| **Vọng** | Leader / Tester | Theo dõi tiến độ 3 bước trên; sau khi có `model_results.csv` và demo chạy được, viết test case kiểm thử (input hợp lệ/thiếu/sai định dạng) cho `/predict` |
| **Diễm** | Tiền xử lý / Metrics | Xem kết quả EDA (bước 2) để đề xuất cách xử lý missing values/encoding nếu `preprocess.py` cần điều chỉnh; đối chiếu `model_results.csv` với công thức MAE/RMSE/R² đã học để viết phần đánh giá trong báo cáo |

---

## 4. Checklist nhanh (tick khi xong)

- [ ] `data/train.csv` đã có (Khang)
- [ ] `results/` có báo cáo EDA (Khang)
- [ ] `models/best_model.pkl` đã có (Vinh)
- [ ] `results/model_results.csv` đã có (Vinh)
- [ ] `models/feature_defaults.json` đã có (Vinh)
- [ ] `predict_service.py` chạy không lỗi (Thành)
- [ ] `server.js` chạy không lỗi (Thành)
- [ ] Demo trả kết quả đúng trên `http://localhost:3000` (Thành, Vọng test)

## Kết quả train/test và quy đổi VND

Phần bổ sung chỉ đo lại **cấu hình gốc** từ `get_models()`, giữ `Id`, cùng split/pipeline/CV của repo; không tuning và không ghi model. Bản gốc CSV, ảnh, dữ liệu và trọng số được kiểm tra SHA-256 trong `results/chuan_hoa/nguon_goc_sha256.json`.

Chạy PowerShell tại thư mục gốc:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe notebooks_or_src_py/chuan_hoa_ket_qua.py
.\.venv\Scripts\python.exe notebooks_or_src_py/verify_chuan_hoa.py
```

Thời gian phụ thuộc CPU; script fit lại 5 mô hình và CV 5 fold nhưng chỉ giữ mô hình trong RAM. Không chạy `train_compare.py` để xuất bảng chuẩn hóa vì script cũ có ghi đè `best_model.pkl`.

Đọc `results/chuan_hoa/00_DOC_TRUOC_TIEN.md` trước. File 02 thuộc TRAIN, file 03 thuộc TEST, file 04 là CV trên TRAIN; file 05 mới đối chiếu khoảng cách. Các file 06/07 là từng căn theo đúng tập, file 01 có danh sách Id. Workbook `BAO_CAO_KET_QUA_TRAIN_TEST.xlsx` có các sheet và dự đoán TEST dạng rộng. File `KIEM_CHUNG.md` chứa PASS/FAIL cùng số thật; script thoát mã lỗi nếu có FAIL.

Bảng `model_results_VND.csv` quy đổi số USD **đã làm tròn** ở CSV gốc. Bảng 02/03 và chi tiết giữ số đo lại đầy đủ; vì vậy có thể chênh vài chục đồng với bản chuyển từ CSV làm tròn. Excel chỉ định dạng hiển thị, không thay số tính; R² không phải tỷ lệ căn dự đoán đúng. Định dạng Excel dùng mã số chuẩn `#,##0`, `0.0000`, `0.00%`; dấu chấm/phẩy hiển thị theo ngôn ngữ Excel của máy.

Dự đoán file mới:

```powershell
.\.venv\Scripts\python.exe notebooks_or_src_py/du_doan_vnd.py data/test.csv --output results/chuan_hoa/du_doan_test_VND.csv
```

CSV/JSON thiếu cột được điền `feature_defaults.json` giống service cũ. Cột lạ bị bỏ qua; không thay cách xử lý dữ liệu cũ. API `/predict` giữ `predicted_price` USD làm tròn 2 chữ số để tương thích và thêm `predicted_price_usd` USD đầy đủ, `predicted_price_vnd`, `usd_to_vnd`. VND dùng giá suy luận đầy đủ; UI chỉ đổi cách trình bày, giữ form và đường gọi API.

Chạy demo bằng hai terminal:

```powershell
.\.venv\Scripts\python.exe service/predict_service.py
# Terminal thứ hai
npm ci
npm start
```

Mở http://localhost:3000. Kiểm tra bổ sung API/CLI:

```powershell
.\.venv\Scripts\python.exe notebooks_or_src_py/verify_du_doan_vnd.py
```

Service, HTML, requirements và README có bản `.bak` nguyên gốc. Các script mới lấy tỷ giá từ `notebooks_or_src_py/tien_te.py`, không huấn luyện trên VND. Script verification kiểm tra các file bị bảo vệ không đổi; README/requirements chỉ được nối thêm và backup phải khớp SHA-256 nguồn.

Hạn chế bản gốc được giữ theo phạm vi: Id vẫn là đặc trưng; mô hình được chọn theo TEST; chưa tìm kiếm tham số. Việc tái lập kết quả không khắc phục các hạn chế này và không xác nhận giá thị trường bên ngoài. Không triển khai thay đổi mô hình của bản HomeValue Lab vào repo huấn luyện này.

Giá quy đổi theo tỷ giá cố định 1 USD = 25.000 ₫ từ dữ liệu nhà ở Ames (Iowa, Hoa Kỳ, 2006–2010); chỉ để thống nhất đơn vị, không phản ánh giá thị trường Việt Nam.

Kiểm tra HTTP thật qua hai server đang chạy và logic hiển thị VND:

```powershell
node notebooks_or_src_py/smoke_chuan_hoa.mjs
```

Log nằm ở `results/chuan_hoa/KIEM_CHUNG_HTTP.md`. Script kiểm tra HTTP và handler JavaScript bằng Node, không thay thế kiểm thử trình duyệt.
