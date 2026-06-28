from pathlib import Path
import shutil

from tools.user_dir_utils import get_all_users

import re

SUFFIX_LIST = [".pdf", ".jpg", ".png"]


def make_dir_and_copy_file_to(target_dir: Path, user_name: str, src_path: Path, file_name: str):
    target_person_dir = target_dir / user_name
    target_file_path = target_person_dir / file_name

    # 情况1：该人员文件夹不存在，跳过，记错误
    if not target_person_dir.exists():
        print(f"创建目录：{target_person_dir} ")
        target_person_dir.mkdir(exist_ok=True)

    # 情况2：目标目录已存在同名身份证，跳过，记错误
    if target_file_path.exists():
        print(f"【错误】{user_name} 目录已存在{file_name}，不予覆盖 ")
        return
    source_file_path = src_path / file_name
    # 情况3：正常移动文件
    shutil.move(str(source_file_path), str(target_file_path))
    print(f"【成功】源：{source_file_path}  →  目标：{target_file_path}")


def re_org_user_certs(source_dir: str, target_dir: str, center_user_cert_root):
    # 统计计数器
    move_success = 0
    error_count = 0

    # ===================== 配置路径，按需修改 =====================
    # 存放所有身份证的源文件夹
    source_path = Path(source_dir)

    target_path = Path(target_dir)
    if not target_path.exists():
        target_path.mkdir(exist_ok=True)

    TARGET_ROOT_PATH = Path(center_user_cert_root)

    # 校验源文件夹是否存在
    if not source_path.exists():
        print(f"错误：源身份证目录不存在 -> {source_path}")
        return
    # 校验目标根目录是否存在
    if not TARGET_ROOT_PATH.exists():
        print(f"错误：目标人员根目录不存在 -> {center_user_cert_root}")
        return

    # 在 目标目录找到，所有的 人员子目录列表
    all_user_names = get_all_users(center_user_cert_root)

    # 遍历源目录所有文件
    for file in source_path.iterdir():
        # 只处理pdf文件，跳过文件夹
        if file.is_dir() :
            print(f"Error, file {file.name} is dir")
            continue
        suffix = file.suffix.lower()
        if suffix not in SUFFIX_LIST:
            print(f"Error, file {file.name} is not in {SUFFIX_LIST}")
            continue

        filename = file.name
        # 只匹配 人名-身份证.pdf 格式文件
        if "-" not in filename:
            print(f"Error, file {file.name} is not a ID or cert file")
            continue

        # 切割人名：按"-身份证.pdf"分割，前面就是人名
        person_name = filename.split("-")[0]

        if person_name not in all_user_names:
            # 创建子目录 ， 把文件移到目录中去
            make_dir_and_copy_file_to(target_path, person_name, source_path, filename)
        else:
            # 保留
            pass


def main():
    source_dir = r"C:\Users\101202304023\Desktop\工作\投标项目\个人证书+合同"
    target_dir = f"{source_dir}\\目标目录"
    CENTER_TARGET_ROOT = r"C:\Users\101202304023\Desktop\工作\投标项目\用户身份证、毕业证、合同等信息"
    #
    re_org_user_certs(source_dir, target_dir, CENTER_TARGET_ROOT)
    pass


if __name__ == "__main__":
    main()
