from pathlib import Path
import argparse
import json
import os

from typing import List, Any, Set
from convertors.snapshotter_factory import SnapshotManager
from tools.excel_utils import read_excel_sheet_values
from tools.user_dir_utils import get_all_users, find_target_dir





def convert_user_info_to_images(database_user_path: Path, target_user_image_path: Path,
                                user_name: str,
                                flags: Set[str]):
    json_file = database_user_path / "info.json"

    # 1. 判断info.json是否存在
    if not json_file.exists():
        print(f"User {user_name} 目录下无 info.json")
        return False

    # 2. 读取并解析json
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            info_data = json.load(f)
    except Exception as e:
        print(f"JSON解析失败 {user_name} info.json 格式错误：{str(e)}")
        return False

    ssm = SnapshotManager(database_user_path, target_user_image_path)
    ssm.take_snapshot(user_name, info_data, flags)

    return True


def step_all_user_list(user_database_path1, output_image_dir1,
                       user_list, flags: Set[str]
                       ):
    database_user_list = get_all_users(user_database_path1)

    user_database_path = Path(user_database_path1)

    output_image_dir = Path(output_image_dir1)
    if not output_image_dir.exists():
        output_image_dir.mkdir(exist_ok=True, parents=True)

    for user_name in user_list:

        target_user_name = find_target_dir(user_name, database_user_list)
        if target_user_name is None:
            print(f"!!!! 没有找到对应的目录 :{user_name}   ")
            continue

        database_user_path = user_database_path / target_user_name
        if not database_user_path.exists():
            print(f"!!! database user path , {target_user_name} not exist ")
            continue

        target_user_image_path = output_image_dir / user_name
        if not target_user_image_path.exists():
            os.makedirs(target_user_image_path, exist_ok=True)

        convert_user_info_to_images(database_user_path, target_user_image_path, user_name, flags)

    return user_list


def get_user_list_from_xlsx(excel_file_name, user_sheet_name="Users",
                            col_user_name="Name"):
    users = read_excel_sheet_values(excel_file_name, user_sheet_name)
    user_list = []
    for user in users:
        user_name = user[col_user_name]
        if user_name is not None and len(user_name) > 0:
            user_list.append(user_name)

    return user_list


def main(args):
    if args.input_xlsx is None or args.input_xlsx == "":
        print("--input-xlsx 空")

        return False

    if args.user_database is None or args.user_database == "":
        print("--user-database 空")
        return False

    flags = {"idcard","contract","degree","grad","xuexinwang","cisp","cisaw","pmp","ruankao"}

    user_list = get_user_list_from_xlsx(args.input_xlsx,
                                        args.sheet_name_user,
                                        args.col_user_name
                                        )

    user_list = step_all_user_list(args.user_database,
                                   args.output_user_images,
                                   user_list,
                                   flags
                                   )

    return True


if __name__ == "__main__":

    #
    parser = argparse.ArgumentParser(description="转换用户身份证、证书、合同等转用户截图工具")
    parser.add_argument("-i", "--input-xlsx", help="输入Xlsx文件")
    parser.add_argument("-d", "--user-database", help="输入用户文件根目录")
    parser.add_argument("-s", "--output-user-images", help="输出截图文件根目录", default="./output")
    parser.add_argument("--sheet-name-user", help="User sheet name", default="Users")
    parser.add_argument("--col-user-name", help="user column name", default="Name")
    parser.add_argument("-c", "--convert", action="store_true", help="将截图转换为DOCX文档")
    parser.add_argument("-t", "--docx-template-file", help="docx template filename",
                        default="./data/user_ss_template.docx")
    parser.add_argument("-o", "--output-docx-file", help="输出docx文件", default="./user-ss-snapshot.docx")
    # parser.add_argument("-h", "--help", help="打印参数信息")

    args = parser.parse_args()

    result = main(args)
    if not result:
        parser.print_help()
