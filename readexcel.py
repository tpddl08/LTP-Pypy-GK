import logging
from dataclasses import dataclass
from pathlib import Path

import openpyxl as xlsx

logging.basicConfig(
    filename=str(Path(__file__).resolve().with_name("generation.log")),
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


@dataclass
class NHANVIEN:
    manv: int
    hovaten: str
    chucvu: str
    hesoluong: float
    ngaycong: int
    pcantrua: float
    pcdichuyen: float


@dataclass
class TIME:
    thang: int
    nam: int

def load_excel(file_path=None):
    source = Path(file_path) if file_path else Path(__file__).resolve().with_name("LuongNhanVien.xlsx")
    try:
        workbook = xlsx.load_workbook(source, data_only=True, read_only=True)
        sheet = workbook["Sheet1"]

        month = sheet["F2"].value
        year = sheet["G2"].value
        if int(month) != month or not 1 <= month <= 12:
            raise ValueError(f"Tháng không hợp lệ: {month!r} (chỉ nhận từ 1 đến 12)")
        if int(year) != year or year < 1:
            raise ValueError(f"Năm không hợp lệ: {year!r}")

        luong_co_ban_ngay = sheet["C3"].value
        mnv = []
        for row in sheet.iter_rows(min_row=6, min_col=1, max_col=7):
            row_number = row[0].row
            values = [cell.value for cell in row]
            if all(value is None for value in values):
                continue
            if isinstance(values[0], str) and values[0].strip().upper() == "TỔNG":
                logger.info("Bỏ qua dòng tổng kết tại dòng %s", row_number)
                continue
            if any(cell.data_type == "f" for cell in row):
                logger.warning("Bỏ qua dòng %s vì có ô công thức", row_number)
                continue

            manv = values[0]
            mnv.append(
                NHANVIEN(
                    int(manv),
                    str(values[1]),
                    str(values[2]),
                    values[3],
                    values[4],
                    values[5] or 0,
                    values[6] or 0,
                )
            )

        if not mnv:
            raise ValueError("Không tìm thấy nhân viên hợp lệ trong bảng lương!")

        return mnv, TIME(int(month), int(year)), luong_co_ban_ngay
    except Exception:
        logger.exception("Không thể đọc dữ liệu bảng lương!",)
        raise
