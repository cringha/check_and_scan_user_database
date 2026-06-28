import os
import shutil
from pathlib import Path

from tools.excel_utils import read_excel_sheet_values
from tools.user_dir_utils import get_all_users, get_all_certs, find_target_dir




def read_excel_values(dst_root1: str, file_name: str, user_sheet_name: str):
    file_names = read_excel_sheet_values(file_name=file_name, sheet_name=user_sheet_name)

    target_names = get_all_users(dst_root1)

    dst_root = Path(dst_root1)

    for user_obj in file_names:
        src_file_name = user_obj['FILE_NAME']
        user_name = user_obj['USER']
        is_file_overtime = user_obj['OVERTIME']
        new_file_name = user_obj['NEW_FILE_NAME']

        print(
            f" user_name:{user_name} src_file_name:{src_file_name} target_file_name:{is_file_overtime} , new_file_name:{new_file_name} ")

        target_user_name = find_target_dir(user_name, target_names)
        if target_user_name is None:
            print(f"!!!! 没有找到对应的目录 :{user_name}   ")
            continue
        target_user_path = dst_root / target_user_name
        if not target_user_path.exists():
            print(f"!!! Target path , {target_user_name} not exist ")
            continue

        file_path = target_user_path / src_file_name

        new_file_name1 = target_user_path / new_file_name
        try:
            file_path.rename(new_file_name1)

            print(f"{file_path} 已重命名 → {new_file_name1}")

        except Exception as e:

            print(f"Rename error {file_path}  失败：{str(e)}")


if __name__ == "__main__":
    src_dir = r"C:\Users\101202304023\Desktop\工作\投标项目\个人证书+合同\未检查"

    input_excel_file = f"../删除过期合同.xlsx"

    read_excel_values(src_dir,
                      input_excel_file,
                      user_sheet_name="ID",
                      )
