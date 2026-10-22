# Kiểm tra HTTP và logic hiển thị VND

Giá quy đổi theo tỷ giá cố định 1 USD = 25.000 ₫ từ dữ liệu nhà ở Ames (Iowa, Hoa Kỳ, 2006–2010); chỉ để thống nhất đơn vị, không phản ánh giá thị trường Việt Nam.

UTC: 2026-10-22T13:45:08.160Z

4 PASS; 0 FAIL.

- PASS — Form gốc nguyên trạng: Sáu trường và cách submit giữ nguyên
- PASS — Express chuyển đầy đủ các trường tiền: {"predicted_price":173391.52,"predicted_price_usd":173391.515625,"predicted_price_vnd":4334787890.625,"usd_to_vnd":25000,"used_input":{"GarageType":"Attchd","GrLivArea":1500,"LotArea":8500,"Neighborhood":"CollgCr","OverallQual":6,"YearBuilt":2005}}
- PASS — Validation gốc không thay đổi: {"error":"GrLivArea phải là số."}
- PASS — JavaScript kết quả VND và request giữ nguyên: Giá nhà dự đoán: 4,33 tỷ ₫ (1 USD = 25.000 ₫)

Đã chạy HTTP thật qua Express và Flask, kiểm tra handler JavaScript bằng Node vm. Chưa chạy trình duyệt Chromium vì máy kiểm thử chưa có browser binary; không gọi đây là kiểm tra giao diện bằng trình duyệt.
