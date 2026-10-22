# Kết quả TRAIN TEST và quy đổi VND

Giá quy đổi theo tỷ giá cố định 1 USD = 25.000 ₫ từ dữ liệu nhà ở Ames (Iowa, Hoa Kỳ, 2006–2010); chỉ để thống nhất đơn vị, không phản ánh giá thị trường Việt Nam.

- `01_phan_chia_du_lieu.csv`: Danh sách Id và giá nhãn gốc, cho biết từng căn thuộc TRAIN hay TEST.
- `02_ket_qua_TRAIN.csv`: Sai số trên TRAIN đã dùng học; không dùng làm bằng chứng chất lượng tổng quát.
- `03_ket_qua_TEST.csv`: Sai số trên TEST: các dòng không nằm trong phần fit của lần chia này.
- `04_ket_qua_CV_5fold.csv`: CV 5 fold trên TRAIN, cv=5 không shuffle, scoring=neg_mean_absolute_error như repo gốc.
- `05_so_sanh_TRAIN_vs_TEST.csv`: So sánh riêng TRAIN và TEST để nhận diện khoảng cách, ngưỡng chỉ tham khảo.
- `06_du_doan_TEST_chi_tiet.csv`: Từng dự đoán TEST: sai số bằng dự đoán trừ nhãn.
- `07_du_doan_TRAIN_chi_tiet.csv`: Từng dự đoán TRAIN, có thể lạc quan hơn TEST.
- `08_cau_hinh_mo_hinh.csv`: Tham số nhập từ get_models() nguyên trạng, phiên bản và ngày đo lại.
- `09_thong_ke_SalePrice_VND.csv`: Thống kê SalePrice theo VND; count là số căn, không nhân tỷ giá.

Ví dụ đọc một dòng: XGBoost – TEST: sai số tuyệt đối trung bình 395.572.043 ₫ trên 292 căn không thuộc phần fit của lần chia này.

`model_results_VND.csv` quy đổi các số đã làm tròn trong CSV gốc. File 02/03 và chi tiết giữ số tính lại đầy đủ; chênh vài chục đồng là do CSV gốc làm tròn USD đến 2 chữ số. Không dùng số quy đổi từ CSV làm tròn thay số chi tiết.

Mô hình giữ nguyên được huấn luyện trên USD gốc. Nhân giá bằng một hằng số không làm đổi R² và MAPE; MAE và RMSE chỉ đổi đơn vị. MSE nếu xem riêng phải nhân bình phương tỷ giá và ghi VND².

Chia dữ liệu: test_size=0.2; random_state=42. Giữ nguyên Id trong đặc trưng theo yêu cầu bảo toàn bản gốc. Không đổi cấu hình, không tuning, không lưu .pkl.

Ngưỡng mang tính tham khảo: lớn nếu TEST/TRAIN MAE ≥ 2,0 hoặc chênh R² ≥ 0,10; vừa nếu ≥ 1,5 hoặc ≥ 0,06; nhỏ nếu ≥ 1,25 hoặc ≥ 0,03; còn lại chưa thấy dấu hiệu rõ. Ưu tiên mức lớn trước.

Workbook gom các CSV vào sheet riêng, tiền hiển thị nguyên đồng, R² 4 chữ số; MAPE/sai số phần trăm lưu dạng tỷ lệ trong Excel để định dạng phần trăm đúng. CSV giữ tên cột máy đọc theo đặc tả; Excel có tiêu đề tiếng Việt. Ba PNG mới thể hiện MAE TRAIN/TEST, XGBoost TEST và phân phối giá, không thay ảnh cũ.

Hạn chế giữ nguyên: bản gốc chọn best_model bằng MAE TEST; không gọi TEST là đánh giá cuối chưa từng dùng lựa chọn. Id vẫn ảnh hưởng đầu vào. Nhãn là SalePrice trong CSV, chưa xác minh thị trường bên ngoài. Thời gian ở model_results_VND giữ từ CSV gốc, không phải thời gian chạy máy hiện tại.
