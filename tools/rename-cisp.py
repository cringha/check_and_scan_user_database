import os
from pathlib import Path

# ===================== 配置区 按需修改 =====================
# 人员根目录
ROOT_DIR = r"D:\人员资质、身份证"
ROOT_DIR = r"C:\Users\101202304023\Desktop\工作\投标项目\用户身份证、毕业证、合同等信息"
# 跳过的文件夹，不处理里面文件
SKIP_FOLDERS = {"新增资料", "所有照片"}
# 需要统一规范的证书类型，可自行新增
CERT_TYPES = [
    "CISP",
    "CISAW",
    "CISSP"
]
# ==========================================================

def normalize_cert_filename(person_name: str, file_path: Path, cert_key: str):
    """
    统一证书文件名格式：人名-证书.pdf
    :param person_name: 人员文件夹名称（标准人名）
    :param file_path: 文件完整路径
    :param cert_key: 证书标识 CISP/CISAW/CISSP
    """
    file_stem = file_path.stem
    suffix = file_path.suffix  # .pdf/.png等后缀保留
    lower_stem = file_stem.lower()
    lower_cert = cert_key.lower()

    # 判断文件是否属于当前证书类型（包含证书关键词）
    if lower_cert not in lower_stem:
        return

    # 提取"续"标识，如果文件名含续，后缀加-续
    extra_suffix = ""
    if "续" in file_stem:
        extra_suffix = "-续"

    # 目标标准文件名
    new_name = f"{person_name}-{cert_key}{extra_suffix}{suffix}"
    new_path = file_path.parent / new_name

    # 同名文件已存在则跳过，防止覆盖报错
    if new_path.exists():
        print(f"跳过 {file_path.name}，规范文件 {new_name} 已存在")
        return

    # 执行重命名
    file_path.rename(new_path)
    print(f"重命名: {file_path.name}  →  {new_name}")


def process_single_person_folder(folder: Path):
    """处理单个人员文件夹"""
    person_name = folder.name
    # 遍历文件夹内所有文件，不递归子目录
    for file in folder.iterdir():
        if file.is_dir():
            continue
        # 只处理图片、PDF证件文件，过滤其他无关格式
        if file.suffix.lower() not in [".pdf", ".png", ".jpg", ".jpeg"]:
            continue
        # 遍历所有证书类型匹配处理
        for cert in CERT_TYPES:
            normalize_cert_filename(person_name, file, cert)


def main():
    root = Path(ROOT_DIR)
    if not root.exists():
        print(f"错误：根目录不存在 {ROOT_DIR}，请修改路径！")
        return

    # 遍历根目录下一级人员文件夹
    for sub_folder in root.iterdir():
        if not sub_folder.is_dir():
            continue
        folder_name = sub_folder.name
        if folder_name in SKIP_FOLDERS:
            print(f"跳过目录：{folder_name}")
            continue
        print(f"\n正在处理人员目录：{folder_name}")
        process_single_person_folder(sub_folder)

    print("\n==== 全部文件重命名处理完成 ====")


if __name__ == "__main__":
    main()