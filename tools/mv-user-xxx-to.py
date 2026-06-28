import os
import shutil
from pathlib import Path

import pandas as pd

from tools.excel_utils import read_excel_sheet_values
from tools.user_dir_utils import get_all_users, get_all_certs, find_target_dir



def rename_and_remove_overtime_files (dst_root1: str, src_dir1: str, file_name: str, user_sheet_name: str):
    file_names = read_excel_sheet_values(file_name=file_name, sheet_name=user_sheet_name)

    target_names = get_all_users(dst_root1)

    backup_list = []

    dst_root = Path(dst_root1)
    src_dir = Path(src_dir1)

    for user_obj in file_names:
        src_file_name = user_obj['SRC_FILENAME']
        user_name  = user_obj['USER']
        target_file_name = user_obj['TARGET_FILENAME']

        print(f" user_name:{user_name} src_file_name:{src_file_name} target_file_name:{target_file_name} ")

        target_user_name = find_target_dir(user_name, target_names)
        if target_user_name is None:
            print(f" 没有找到对应的目录 :{user_name}   ")
            continue
        target_user_path = dst_root / target_user_name
        if not target_user_path.exists():
            print(f" Target path , {target_user_name} not exist ")
            continue

        old_file_path = target_user_path / src_file_name
        if old_file_path.exists() and src_file_name != target_file_name:
            backup_list.append(old_file_path)

        src_file_path = src_dir / src_file_name
        target_file_path = target_user_path / target_file_name

        try:
            shutil.copy2(src_file_path, target_file_path)
        except Exception as e:
            print(f"Copy {str(src_file_path)} to {str(target_file_path)} 删除失败：{str(e)}")



    # 把源文件删了
    for one in backup_list:
        try:
            one.unlink()
        except Exception as e:
            print(f"{str(one)} 删除失败：{str(e)}")


if __name__ == "__main__":
    dst_root = r"D:\用户身份证、毕业证、合同等信息"
    src_dir = r"C:\Users\101202304023\Desktop\测试"

    input_excel_file = f"../证书名转换.xlsx"

    rename_and_remove_overtime_files(dst_root,
                                     src_dir,
                      input_excel_file,
                      user_sheet_name="CERTS",
                      )
