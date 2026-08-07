import os
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

import sys

from entries.check_and_export_user_infos import check_and_export_user_infos


def main():
    # 访问特定的命令行参数
    if len(sys.argv) > 2:
        root_path = sys.argv[1]
        output_excel = sys.argv[2]
    else:
        print("Usage: python cmd_scan_all_user.py root_path excel_output")
        return

    root = Path(root_path)
    if not root.exists():
        print(f"错误：根目录不存在，请检查路径 -> {root_path}")
        return

    def cb_info(status, msg):
        print(msg)

    check_and_export_user_infos(root_path, output_excel, cb_info)


if __name__ == "__main__":
    main()


