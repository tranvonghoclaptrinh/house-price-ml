# Kiểm chứng dự đoán VND so với bản gốc

Giá quy đổi theo tỷ giá cố định 1 USD = 25.000 ₫ từ dữ liệu nhà ở Ames (Iowa, Hoa Kỳ, 2006–2010); chỉ để thống nhất đơn vị, không phản ánh giá thị trường Việt Nam.

UTC: 2026-10-22T13:41:55.832462+00:00

18 PASS; 0 FAIL.

- PASS — API 1 giữ nguyên kết quả cũ: HTTP cũ/mới=200/200; USD cũ=162012.14; USD mới=162012.14
- PASS — API 1 trường tiền mới: USD đầy đủ=162012.140625; VND=4050303515.625; rate=25000
- PASS — API 2 giữ nguyên kết quả cũ: HTTP cũ/mới=200/200; USD cũ=173391.52; USD mới=173391.52
- PASS — API 2 trường tiền mới: USD đầy đủ=173391.515625; VND=4334787890.625; rate=25000
- PASS — API 3 giữ nguyên kết quả cũ: HTTP cũ/mới=200/200; USD cũ=165278.98; USD mới=165278.98
- PASS — API 3 trường tiền mới: USD đầy đủ=165278.984375; VND=4131974609.375; rate=25000
- PASS — API 4 giữ nguyên kết quả cũ: HTTP cũ/mới=200/200; USD cũ=161677.97; USD mới=161677.97
- PASS — API 4 trường tiền mới: USD đầy đủ=161677.96875; VND=4041949218.75; rate=25000
- PASS — API 5 giữ nguyên kết quả cũ: HTTP cũ/mới=200/200; USD cũ=162012.14; USD mới=162012.14
- PASS — API 5 trường tiền mới: USD đầy đủ=162012.140625; VND=4050303515.625; rate=25000
- PASS — API 6 giữ nguyên kết quả cũ: HTTP cũ/mới=400/400; USD cũ=None; USD mới=None
- PASS — CLI JSON thiếu cột và cột lạ: n=4; max USD delta=0.0
- PASS — CLI CSV toàn bộ TEST so với artifact gốc: n=292; max USD delta=0.0
- PASS — CLI không ghi đè file input: Từ chối output trùng input
- PASS — Chỉ thêm dòng service/predict_service.py: 74 dòng gốc giữ nguyên thứ tự trong 82 dòng mới
- PASS — Chỉ thêm dòng public/index.html: 108 dòng gốc giữ nguyên thứ tự trong 116 dòng mới
- PASS — Định dạng VND nguyên đồng: 25.000 ₫
- PASS — Định dạng triệu và tỷ: 7,8 triệu ₫; 3,69 tỷ ₫
