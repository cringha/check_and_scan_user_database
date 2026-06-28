import os
import json
from pathlib import Path

# ===================== 可配置扩展区域 =====================
# 根目录，修改为你本地实际路径
ROOT_PATH = r"D:\人员资质、身份证"
ROOT_PATH = r"C:\Users\101202304023\Desktop\工作\投标项目\用户身份证、毕业证、合同等信息"
ROOT_PATH = r"D:\用户身份证、毕业证、合同等信息"
# 需要跳过的文件夹，不生成info.json
SKIP_DIRS = {"新增资料", "所有照片"}
# 文件匹配规则：key=json输出字段，value=匹配关键词列表（大小写忽略）
MATCH_RULES = {
    "idcard": ["身份证"],

    "xuexinwang": [
        "学信网",
        "学历查询",
        "学历验证",
        "电子注册备案表"
    ],
    "graduationCertificate": ["毕业证", "毕业证书"],
    "degreeCertificate": ["学位证", "学位证书"],
    "contract": [
        "劳动合同",
        "脱敏",
        "无固定期限",
        "续签",
        "恒安"
    ],
    "cisp": ["cisp", "CISP"],
    "cisaw": ["cisaw", "CISAW"],
    "cissp": ["cissp", "CISSP"],
    "pmp": ["pmp","PMP"],
    "ruankao": [
        "系统集成",
        "信息系统",
        "软考",
        "职称证书",
        "设计师",
        "工程师",
        "管理师"
    ],

}


# =========================================================

def match_file_name(person_name: str, file_name: str) -> str | None:
    """
    匹配文件对应字段
    特殊规则：仅人名命名的pdf视为身份证
    """
    fn_lower = file_name.lower()
    name_only_pdf = f"{person_name.lower()}.pdf"

    # 纯人名pdf 判定为身份证
    if fn_lower == name_only_pdf:
        return "id"

    # 遍历所有匹配关键词
    for field, keywords in MATCH_RULES.items():
        for kw in keywords:
            if kw.lower() in fn_lower:
                return field
    return None


def build_person_info(person_dir: Path) -> dict:
    """
    遍历单人文件夹，组装info字典
    忽略子文件夹、忽略info.json自身
    """
    info = {
        "name": person_dir.name
    }
    unclassified = []
    person_name = person_dir.name

    for entry in person_dir.iterdir():
        # 跳过子文件夹、跳过已生成的info.json
        if entry.is_dir() or entry.name == "info.json":
            continue
        file_name = entry.name
        field = match_file_name(person_name, file_name)

        if field:
            # 同一类型多个文件自动转为列表存储
            if field in info:
                if isinstance(info[field], list):
                    info[field].append(file_name)
                else:
                    info[field] = [info[field], file_name]
            else:
                info[field] = file_name
        else:
            unclassified.append(file_name)

    # 存在无法归类文件，加入other数组
    if unclassified:
        info["other"] = unclassified
    return info

import sys

def main():

    root_path = ROOT_PATH

    # 访问特定的命令行参数
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        print("Usage: python scan_all_user_info.py root_path")
        return

    root = Path(root_path)
    if not root.exists():
        print(f"错误：根目录不存在，请检查路径 -> {root_path}")
        return

    # 遍历根目录下一级文件夹
    for folder in root.iterdir():
        if not folder.is_dir():
            continue
        folder_name = folder.name
        if folder_name in SKIP_DIRS:
            print(f"跳过文件夹：{folder_name}")
            continue

        print(f"正在处理：{folder_name}")
        info_data = build_person_info(folder)
        json_path = folder / "info.json"

        # 写入格式化json，中文正常显示
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)
        print(f"已生成文件：{json_path.resolve()}\n")

    print("===== 全部人员目录处理完成 ====")


if __name__ == "__main__":



    main()
