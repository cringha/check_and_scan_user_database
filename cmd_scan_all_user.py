import os
import json
from pathlib import Path

from entries.scan_all_user_info import scan_all_user_paths

ROOT_PATH = r"E:\Tools\用户身份信息库"

import sys


def main():
    root_path = ROOT_PATH

    # 访问特定的命令行参数
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        print("Usage: python cmd_scan_all_user.py root_path")
        return

    def cb_info(status, msg):
        print(msg)

    scan_all_user_paths(root_path, cb_info)


if __name__ == "__main__":
    main()
