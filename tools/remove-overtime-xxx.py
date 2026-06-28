import sys
import os

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
import argparse
from excel_utils import read_excel_sheet_values
from user_dir_utils import get_all_users, get_all_certs, find_target_dir



IS_OVERTIME = ['已过期','是']

def main(args):
    if args.input_xlsx is None or args.input_xlsx == "":
        print("--input-xlsx 空")

        return False

    if args.user_database is None or args.user_database == "":
        print("--user-database 空")
        return False

    file_name = args.input_xlsx
    data_base_root = args.user_database
    file_sheet_name = args.sheet_name_files

    file_names = read_excel_sheet_values(file_name=file_name, sheet_name=file_sheet_name)

    target_names = get_all_users(data_base_root)

    dst_root = Path(data_base_root)

    for user_obj in file_names:
        src_file_name = user_obj['FILE_NAME']
        user_name = user_obj['USER']
        is_file_overtime = user_obj['OVERTIME']
        new_file_name = user_obj['NEW_FILE_NAME']

        print(
            f" user_name:{user_name} src_file_name:{src_file_name} overtime:{is_file_overtime} , new_file_name:{new_file_name} ")

        target_user_name = find_target_dir(user_name, target_names)
        if target_user_name is None:
            print(f"!!!! 没有找到对应的目录 :{user_name}   ")
            continue
        target_user_path = dst_root / target_user_name
        if not target_user_path.exists():
            print(f"!!! Target path , {target_user_name} not exist ")
            continue

        file_path = target_user_path / src_file_name
        if is_file_overtime in IS_OVERTIME :
            if file_path.exists() :
                try:
                    file_path.unlink()
                    print(f"Remove file : {file_path}   ")
                except Exception as e:
                    print(f"Remove file {str(file_path)}  删除失败：{str(e)}")
        else:
            new_file_name1 = target_user_path / new_file_name
            try:
                file_path.rename(new_file_name1)

                print(f"{file_path} 已重命名 → {new_file_name1}")

            except Exception as e:

                print(f"Rename error {file_path}  失败：{str(e)}")

    return True

if __name__ == "__main__":

    #
    parser = argparse.ArgumentParser(
        description="删除改名过期的证书等文件，读取输入的excel文件，然后按照内容，删除过期文件。并且把文件名改为 XXXX-YYYYMMDD.PDF格式")
    parser.add_argument("-i", "--input-xlsx", help="输入Xlsx文件", default=f"../删除过期合同.xlsx")
    parser.add_argument("-d", "--user-database", help="输入用户文件根目录")
    parser.add_argument("--sheet-name-files", help="Files sheet name", default="FILES")
    parser.add_argument("--col-user-name", help="user column name", default="Name")

    args = parser.parse_args()

    result = main(args)
    if not result:
        parser.print_help()
