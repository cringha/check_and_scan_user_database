from typing import Callable
# import fitz  # PyMuPDF，用于PDF处理
import os

import pymupdf

BORDER_WIDTH = 4

# from fitz import open as open_pdf
#
# # 打开PDF文件
# doc = open_pdf("example.pdf")
#
# # 选择页面
# page = doc.load_page(0)  # 例如，选择第一页
#
# # 定义截图区域，例如只截取页面的上半部分
# rect = fitz.Rect(0, 0, page.rect.width, page.rect.height // 2)
# pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False, colorspace=fitz.csGRAY)  # 降低分辨率
# pix = page.get_pixmap(clip=rect)  # 只截取上半部分
# pix.save("output_small.png")  # 保存图片

def snapshot(doc, page_num, filename, user_name, pdf_filename):
    # 2. 截取首页（第一个包含目标人员的页面）
    first_page = doc[page_num]
    # 将页面转为图片（分辨率300dpi，保证清晰度）
    # mat = pymupdf.Matrix(300 / 72, 300 / 72)
    # mat = pymupdf.Matrix(2, 2)
    mat = pymupdf.Matrix(1.2, 1.2)
    first_pix = first_page.get_pixmap(matrix=mat,alpha=False)
    first_pix.save(filename)
    print(f"已保存：{user_name}, {filename}, {pdf_filename}")


def snap_pdf_page(pdf_filename: str, user_name: str, cb_filename):
    # print("Process ", pdf_path)

    # 打开PDF文件
    # pymupdf.open
    doc = pymupdf.open(pdf_filename)
    if doc.page_count == 0:
        print("PDF文件为空，无法处理, {pdf_path}")
        return False

    # 1. 遍历PDF页面，查找目标人员并添加红色框
    for page_num in range(doc.page_count):
        file_name = cb_filename(user_name, page_num, doc.page_count, pdf_filename)
        if file_name is not None:
            snapshot(doc, page_num, file_name, user_name, pdf_filename)
        else:
            print(f"文件不符合策略没有保存：{user_name}, page_num: {page_num}, {pdf_filename}")

    return True
