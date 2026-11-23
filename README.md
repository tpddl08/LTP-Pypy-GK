# Bài tập: Tạo phiếu lương nhân viên bằng Python

## Mô tả

Code này có nhiệm vụ đọc dữ liệu nhân viên từ file Excel `LuongNhanVien.xlsx`, tính các khoản lương và bảo hiểm theo tháng, sau đó tự động tạo một phiếu lương định dạng PDF cho từng nhân viên. Các phiếu được lưu trong thư mục `Luong/` với tên file `LuongNV<ma-nhan-vien>.pdf`.

Chương trình hỗ trợ hiển thị tiếng Việt trong PDF bằng font `NotoSans.ttf` và ghi lại quá trình tạo phiếu cũng như các lỗi phát sinh vào file `generation.log`.

## Chức năng

- Đọc thông tin tháng, năm và lương cơ bản theo ngày từ file Excel.
- Đọc danh sách nhân viên gồm:
  - Mã nhân viên
  - Họ và tên
  - Chức vụ
  - Hệ số lương
  - Số ngày đi làm
  - Phụ cấp ăn trưa
  - Phụ cấp di chuyển
- Bỏ qua dòng trống và dòng tổng kết trong bảng dữ liệu.
- Kiểm tra dữ liệu tháng, năm và ô công thức không hợp lệ.
- Tính:
  - Lương cơ bản
  - Tổng Phụ cấp
  - Bảo hiểm xã hội
  - Bảo hiểm y tế
  - Bảo hiểm tai nạn
  - Tổng lương được nhận
- Tạo phiếu lương PDF theo khổ A5 cho từng nhân viên.

## Công thức tính lương

```text
Lương cơ bản = Số ngày đi làm × Hệ số lương × Lương cơ bản/ngày
Khoản cộng  = Lương cơ bản + Phụ cấp ăn trưa + Phụ cấp di chuyển

Bảo hiểm xã hội = Khoản cộng × -8%
Bảo hiểm y tế    = Khoản cộng × -1,5%
Bảo hiểm tai nạn = Khoản cộng × -1%
Khoản trừ        = Tổng các khoản bảo hiểm

Tổng nhận        = Khoản cộng + Khoản trừ
```

## Cấu trúc dự án

```text
LTP-Pypy-GK/
├── README.md
├── LuongNhanVien.xlsx
├── readexcel.py
├── createpdf.py
├── NotoSans.ttf
├── generation.log
└── Luong/
    ├── LuongNV001.pdf
    ├── LuongNV002.pdf
    └── ...
```

### Mô tả file

- `readexcel.py`: đọc và kiểm tra dữ liệu trong file Excel; định nghĩa các dataclass `NHANVIEN` và `TIME`.
- `createpdf.py`: tính lương và tạo phiếu PDF bằng thư viện ReportLab.
- `LuongNhanVien.xlsx`: file dữ liệu đầu vào chứa tháng/năm, lương cơ bản và danh sách nhân viên.
- `Luong/`: thư mục chứa các phiếu lương đã tạo.
- `NotoSans.ttf`: font hỗ trợ chữ tiếng Việt.
- `generation.log`: nhật ký kết quả tạo file và các lỗi.

## Yêu cầu thư viện

Chương trình sử dụng:

- `openpyxl`
- `reportlab`

Cài đặt bằng lệnh:

```bash
pip install openpyxl reportlab
```

## Cách chạy

1. Đặt file `LuongNhanVien.xlsx` cùng thư mục với `createpdf.py`.
2. Cài đặt các thư viện cần thiết.
3. Chạy chương trình:

```bash
python createpdf.py
```

Chương trình sẽ tạo hoặc ghi đè các phiếu PDF trong thư mục `Luong/`. Mã nhân viên có thể có số 3 chữ số, ví dụ `1` được đặt tên thành `LuongNV001.pdf`.
