# Tổng hợp thay đổi chuẩn hóa kết quả

Giá quy đổi theo tỷ giá cố định 1 USD = 25.000 ₫ từ dữ liệu nhà ở Ames (Iowa, Hoa Kỳ, 2006–2010); chỉ để thống nhất đơn vị, không phản ánh giá thị trường Việt Nam.

Nguồn repo: commit `00e2ee36d4f9a8b2d18320644c0b2029860bdfb5`. Thời gian đo lại: 65.24790337399986 giây.

- `KIEM_CHUNG.md`: 140 PASS, 0 FAIL.
- `KIEM_CHUNG_DU_DOAN.md`: 18 PASS, 0 FAIL.
- `KIEM_CHUNG_HTTP.md`: 4 PASS, 0 FAIL.

So sánh XGBoost fit lại với best_model.pkl trên TEST trước xuất CSV: sai khác tối đa 0.0 USD.

| Mô hình | MAE TEST đo lại USD gốc | MAE TEST VND | R² TEST |
|---|---:|---:|---:|
| XGBoost | 15822.881702161814 | 395572042.5540454 | 0.9112799275111118 |
| Gradient Boosting | 17099.275710661237 | 427481892.76653093 | 0.9066707143424279 |
| Random Forest | 17634.87383561644 | 440871845.89041096 | 0.8889619321014003 |
| Linear Regression | 20594.93685294852 | 514873421.32371294 | 0.8735527292834899 |
| Decision Tree | 25754.333182354865 | 643858329.5588716 | 0.785660192589763 |

Dữ liệu, trọng số, mã tiền xử lý/huấn luyện/metrics/EDA/export_defaults, CSV kết quả và ảnh gốc giữ nguyên SHA-256. Không tuning, không bỏ Id. Chỉ service, HTML, requirements và README có bổ sung theo phạm vi, đều có .bak.

Kết quả số học và dữ liệu đã kiểm tra trên Linux với đúng thư viện requirements. Script dùng pathlib và lệnh PowerShell trong README; chưa chạy thực tế trên Windows. HTTP thật và handler JavaScript bằng Node đã kiểm tra; chưa có Chromium để kiểm thử trình duyệt.

Lưu ý: Id và cách chọn model theo TEST là hạn chế của bản gốc, được giữ theo yêu cầu. Không gọi giá quy đổi là giá thị trường Việt Nam. Chưa thay thế mô hình hay đưa code của giao diện HomeValue Lab vào repo này.
