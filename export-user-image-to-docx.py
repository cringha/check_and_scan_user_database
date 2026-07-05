import json
import os
import random

from pathlib import Path

import argparse
from docx.shared import Mm
from jinja2 import Environment
from docxtpl import DocxTemplate, InlineImage

from entries.user_cert_snapshots_to_docx import generate_snapshot_docx
from tools.excel_utils import read_excel_sheet_values
from uitls.log import init_with_conf, get_log, LogConfig
from userinfo.common import SNAPSHOT_PARAMS, SNAPSHOT_NAME_CERTS, SNAPSHOT_NAME_SS, ALL_SNAPSHOT_TYPE
from userinfo.resume_manager import make_resume_factory
from userinfo.user_snapshots import read_user_snapshots, UserSnapshot, read_user_ss_snapshots

image_size = 120


if __name__ == "__main__":
    init_with_conf(LogConfig())
    logger = get_log()
    logger.debug("Convert user info to docx")
    #
    parser = argparse.ArgumentParser(description="将用户身份证、证书、合同截图转换为DOCX文档")
    parser.add_argument("-i", "--input-xlsx", help="输入Xlsx文件")
    parser.add_argument("--user-snapshot-types",
                        help="输入用户截图类型, '身份证', '毕业证', '资质证书', '合同', '社保' ", default="")
    parser.add_argument("-s", "--user-snapshot-root", help="输入用户截图文件根目录")
    parser.add_argument("-x", "--user-ss-snapshot-root", help="输入用户社保截图文件根目录")
    parser.add_argument("-r", "--user-resume-type", help="是否需要用户简历, [v1]", default="")
    parser.add_argument("--sheet-name-user", help="User sheet name; default: %(default)s", default="Users")
    parser.add_argument("--sheet-name-project", help="project sheet name; default: %(default)s", default="Projects")
    parser.add_argument("--sheet-name-duty", help="duty sheet name;default: %(default)s", default="Duty")
    parser.add_argument("--col-user-name", help="user column name;default: %(default)s", default="Name")

    parser.add_argument("--col-work-exp", help="column workExp name in user sheet;default: %(default)s", default="工作年限")
    parser.add_argument("--col-duty", help="column duty name in user sheet;default: %(default)s", default="职责")
    parser.add_argument("--col-duty-desc", help="column duty-desc name in user sheet;default: %(default)s", default="职责内容")
    parser.add_argument("--col-user-cert-list", help="column user-cert-list name in user sheet;default: %(default)s", default="证书列表")



    parser.add_argument("-t", "--docx-template-file", help="docx template filename; default: %(default)s",
                        default="./data/user_certs_template.docx")
    parser.add_argument("-o", "--output-docx-file", help="输出docx文件; default: %(default)s",
                        default="./user-ss-snapshot.docx")
    # parser.add_argument("-h", "--help", help="打印参数信息")

    args = parser.parse_args()

    try:

        def callback_info(status, msg ):
            print(f"{status}: {msg}")
        result = generate_snapshot_docx(args, callback_info)
        if not result:
            parser.print_help()
    except Exception as e:
        print("Exec main error ", e)
