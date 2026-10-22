"""Đơn vị hiển thị; không đổi thang đo huấn luyện của mô hình gốc."""
TY_GIA_USD_VND = 25000


def sang_vnd(x):
    """Nhận số, numpy array hoặc pandas Series chứa USD."""
    return x * TY_GIA_USD_VND


def _so_viet(x, decimals):
    return f"{float(x):,.{decimals}f}".translate(str.maketrans({",": ".", ".": ","}))


def dinh_dang_vnd(x):
    """x đã ở VND; hiển thị tiền nguyên đồng, giữ số gốc khi tính."""
    return _so_viet(x, 0) + " ₫"


def dinh_dang_trieu(x):
    return _so_viet(float(x) / 1_000_000, 1) + " triệu ₫"


def dinh_dang_ty(x):
    return _so_viet(float(x) / 1_000_000_000, 2) + " tỷ ₫"


def ghi_chu_quy_doi():
    return (f"Giá quy đổi theo tỷ giá cố định 1 USD = {dinh_dang_vnd(TY_GIA_USD_VND)} "
            "từ dữ liệu nhà ở Ames (Iowa, Hoa Kỳ, 2006–2010); chỉ để thống nhất đơn vị, "
            "không phản ánh giá thị trường Việt Nam.")
