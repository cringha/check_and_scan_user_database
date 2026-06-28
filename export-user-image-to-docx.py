import json
import os
import random

from pathlib import Path

import argparse
from docx.shared import Mm
from jinja2 import Environment
import pandas as pd

import json
from docxtpl import DocxTemplate, InlineImage

from tools.excel_utils import read_excel_sheet_values
from userinfo.common import SNAPSHOT_PARAMS, SNAPSHOT_NAME_CERTS, SNAPSHOT_NAME_SS, ALL_SNAPSHOT_TYPE
from userinfo.resume_manager import make_resume_factory
from userinfo.user_resume import UserResumeReader
from userinfo.user_resume_beijing_liantong_v1 import BeijingLianTongUserResumeReader
from userinfo.user_snapshots import read_user_snapshots, UserSnapshot, read_user_ss_snapshots

image_size = 120




def process_user_snapshot(tpl, user_snapshot_root_path: Path, us: UserSnapshot):
    for ss in us.snapshot:

        # full_image = user_snapshot_root_path / ss
        full_image = ss.image_path
        if not full_image.exists():
            print(f"File {full_image} not exist")
            continue
        full_image_str = str(full_image)
        s_image_size = image_size
        if us.title in SNAPSHOT_PARAMS:
            s_image_size = SNAPSHOT_PARAMS[us.title]
        image = InlineImage(tpl, full_image_str, width=Mm(s_image_size))
        us.add_image(ss.title, image)


def main(args):




    if args.input_xlsx is None or args.input_xlsx == "":
        print("--input-xlsx 空")
        return False

    snapshot_types = []
    if args.user_snapshot_types != "":
        snapshot_types = args.user_snapshot_types.split(',')
        for tt in snapshot_types:
            if tt not in ALL_SNAPSHOT_TYPE:
                print(f"user_snapshot_types value , wanted , {ALL_SNAPSHOT_TYPE} ")
                return False

    user_snapshot_root_path = None
    user_ss_snapshot_root_path = None

    if len(snapshot_types)>0:
        if args.user_snapshot_root is None or args.user_snapshot_root == "":
            print("--user-snapshot-root 空")
            return False

        user_snapshot_root_path = Path(args.user_snapshot_root)

        if not user_snapshot_root_path or not user_snapshot_root_path.exists():
            print("用户截图跟目录不存在 ", args.user_snapshot_root)
            return False

        user_ss_snapshot_root_path = None
        if SNAPSHOT_NAME_SS in snapshot_types:

            if args.user_ss_snapshot_root is None or args.user_ss_snapshot_root == "":
                print("--user-ss-snapshot-root 空")
                return False

            user_ss_snapshot_root_path = Path(args.user_ss_snapshot_root)
            if not user_ss_snapshot_root_path.exists():
                print("用户社保截图跟目录不存在 ", args.user_ss_snapshot_root)
                return False

    users = read_excel_sheet_values(file_name=args.input_xlsx, sheet_name=args.sheet_name_user)
     #user-resume-type
    user_resume = make_resume_factory(args.user_resume_type,users, args)
    user_resume.read_user_database(args.input_xlsx)

    # 加载模板文件，使用 DocxTemplate 类将模板文件转换为 docx 文档对象
    docx = DocxTemplate(args.docx_template_file)

    col_user_name = args.col_user_name

    for user in users:
        user_name = user[col_user_name]
        if user_name == "" or user_name is None:
            continue

        if len(snapshot_types) > 0:
            all_user_snapshots = read_user_snapshots(user_snapshot_root_path, user_name, snapshot_types)

            if SNAPSHOT_NAME_SS in snapshot_types:
                us = read_user_ss_snapshots(user_ss_snapshot_root_path, user_name, "*.*", SNAPSHOT_NAME_SS)
                if us is not None:
                    all_user_snapshots.append(us)

            for us in all_user_snapshots:
                process_user_snapshot(docx, user_snapshot_root_path, us)

            user["snapshots"] = all_user_snapshots
        user_resume.process_user(user)

    obj = {
        "users": users
    }

    dest_file = Path(str(args.output_docx_file))
    file_name = dest_file.stem
    base_path = dest_file.parent
    counter = 1
    while dest_file.exists():
        dest_file = dest_file.parent / f"{file_name}_{counter}{dest_file.suffix}"
        counter += 1

    output_file1 = str(dest_file)
    jinja_env = Environment()
    # 获取要插入到文档中的数据
    # 渲染文档

    user_resume.hook_jinja(jinja_env)


    docx.render(obj, jinja_env)
    # 保存生成的文档
    print(f"生成文件 : {output_file1} ")
    docx.save(output_file1)
    return True


if __name__ == "__main__":

    #
    parser = argparse.ArgumentParser(description="将用户身份证、证书、合同截图转换为DOCX文档")
    parser.add_argument("-i", "--input-xlsx", help="输入Xlsx文件")
    parser.add_argument( "--user-snapshot-types", help="输入用户截图类型, '身份证', '毕业证', '资质证书', '合同', '社保' ",default="")
    parser.add_argument("-s", "--user-snapshot-root", help="输入用户截图文件根目录")
    parser.add_argument("-x", "--user-ss-snapshot-root", help="输入用户社保截图文件根目录")
    parser.add_argument("-r", "--user-resume-type", help="是否需要用户简历, [v1]", default="")
    parser.add_argument("--sheet-name-user", help="User sheet name; default: %(default)s", default="Users")
    parser.add_argument("--sheet-name-project", help="project sheet name; default: %(default)s", default="Projects")
    parser.add_argument("--sheet-name-duty", help="duty sheet name;default: %(default)s", default="Duty")
    parser.add_argument("--col-user-name", help="user column name;default: %(default)s", default="Name")
    parser.add_argument("-t", "--docx-template-file", help="docx template filename; default: %(default)s",
                        default="./data/user_certs_template.docx")
    parser.add_argument("-o", "--output-docx-file", help="输出docx文件; default: %(default)s", default="./user-ss-snapshot.docx")
    # parser.add_argument("-h", "--help", help="打印参数信息")

    args = parser.parse_args()

    result = main(args)
    if not result:
        parser.print_help()
