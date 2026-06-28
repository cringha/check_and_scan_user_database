from typing import Callable
# import fitz  # PyMuPDF，用于PDF处理
import os

import pymupdf

BORDER_WIDTH = 4


def snapshot(doc, page_num, filename, user_name, pdf_filename):
    # 2. 截取首页（第一个包含目标人员的页面）
    first_page = doc[page_num]
    # 将页面转为图片（分辨率300dpi，保证清晰度）
    mat = pymupdf.Matrix(300 / 72, 300 / 72)
    first_pix = first_page.get_pixmap(matrix=mat)
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
