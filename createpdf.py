import logging
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from readexcel import load_excel


logger = logging.getLogger(__name__)
def format_amount(amount):
    return f"{amount:,.0f}".replace(",", ".")

def build_style():
    font_path = Path(__file__).resolve().with_name("NotoSans.ttf")
    pdfmetrics.registerFont(TTFont("NotoSans", str(font_path)))
    normal = ParagraphStyle("NormalVietnamese", fontName="NotoSans", fontSize=10)
    return (
        ParagraphStyle("TitleVietnamese", parent=normal, fontSize=14, alignment=TA_CENTER),
        normal,
        ParagraphStyle("MonthVietnamese", parent=normal, alignment=TA_CENTER),
        ParagraphStyle("RightVietnamese", parent=normal, alignment=TA_RIGHT),
        ParagraphStyle("CenterVietnamese", parent=normal, alignment=TA_CENTER),
    )


def build_pdf(nv, time_info, luong_co_ban_ngay, styles, output_path):
    title_style, normal_style, month_style, right_style, header_style = styles
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A5,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )
    manv = f"{nv.manv:03d}"
    content = [
        Paragraph("<b>PHIẾU BÁO LƯƠNG NHÂN VIÊN</b>", title_style),
        Spacer(1, 5),
        Paragraph(f"Tháng {time_info.thang} - Năm {time_info.nam}", month_style),
        Spacer(1, 30),
        Paragraph(f"Mã nhân viên: {manv}", normal_style),
        Spacer(1, 5),
        Paragraph(f"Tên nhân viên: {escape(nv.hovaten)}", normal_style),
        Spacer(1, 5),
        Paragraph(f"Chức vụ: {escape(nv.chucvu)}", normal_style),
        Spacer(1, 5),
        Paragraph(f"Hệ số lương: {nv.hesoluong}", normal_style),
        Spacer(1, 5),
        Paragraph(f"Số ngày đi làm: {nv.ngaycong}", normal_style),
        Spacer(1, 10),
        Paragraph("Chi tiết các khoản của lương:", normal_style),
        Spacer(1, 5),
    ]

    luong_co_ban = nv.ngaycong * nv.hesoluong * luong_co_ban_ngay
    pc_an_trua = nv.pcantrua or 0
    pc_di_chuyen = nv.pcdichuyen or 0
    tong_nhan = luong_co_ban + pc_an_trua + pc_di_chuyen
    bhxh = -tong_nhan * 0.08
    bhyt = -tong_nhan * 0.015
    bhtn = -tong_nhan * 0.01
    tong_tru = bhxh + bhyt + bhtn
    tien_den_tay = tong_nhan + tong_tru

    def money_row(label, amount, bold=False):
        label = f"<b>{label}</b>" if bold else label
        value = format_amount(amount)
        value = f"<b>{value}</b>" if bold else value
        return [Paragraph(label, normal_style), Paragraph(value, right_style)]

    table_data = [
        [Paragraph("<b>Tên khoản tiền</b>", header_style), Paragraph("<b>Số tiền</b>", header_style)],
        money_row("Lương cơ bản", luong_co_ban),
        money_row("Phụ cấp ăn trưa", pc_an_trua),
        money_row("Phụ cấp di chuyển", pc_di_chuyen),
        money_row("Bảo hiểm xã hội", bhxh),
        money_row("Bảo hiểm y tế", bhyt),
        money_row("Bảo hiểm tai nạn", bhtn),
        money_row("Khoản cộng:", tong_nhan, bold=True),
        money_row("Khoản trừ:", tong_tru, bold=True),
        money_row("Tổng nhận:", tien_den_tay, bold=True),
    ]
    detail_table = Table(
        table_data,
        colWidths=[document.width * 0.62, document.width * 0.38],
        hAlign="LEFT",
    )
    detail_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF7")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#9AA7B5")),
                ("LINEABOVE", (0, 7), (-1, 7), 1, colors.HexColor("#536579")),
                ("LINEABOVE", (0, 9), (-1, 9), 1, colors.HexColor("#536579")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    content.append(detail_table)
    document.build(content)


def main():
    output_dir = Path(__file__).resolve().with_name("Luong")
    mnv, time_info, luong_co_ban_ngay = load_excel()
    output_dir.mkdir(parents=True, exist_ok=True)
    styles = build_style()

    failtime = 0
    for nv in mnv:
        manv = f"{nv.manv:03d}"
        output_path = output_dir / f"LuongNV{manv}.pdf"

        try:
            build_pdf(nv, time_info, luong_co_ban_ngay, styles, output_path)
            logger.info("TẠO FILE THÀNH CÔNG: %s", f"LuongNV{manv}.pdf")

        except Exception:
            failtime += 1
            logger.exception("TẠO FILE THẤT BẠI: %s", {manv})

    logger.info("Hoàn tất tạo phiếu lương: %s thành công, %s thất bại", len(mnv) - failtime, failtime)
    return 1 if failtime else 0


if __name__ == "__main__":
    raise SystemExit(main())
