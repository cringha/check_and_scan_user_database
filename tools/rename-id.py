import os
from pathlib import Path

# ===================== 配置区域，修改为你的实际根目录 =====================
ROOT_DIR = r"D:\人员资质、身份证"
ROOT_DIR = r"C:\Users\101202304023\Desktop\工作\投标项目\用户身份证、毕业证、合同等信息"
# 不需要处理的文件夹，直接跳过
SKIP_FOLDERS = {"新增资料", "所有照片"}
# ==========================================================================

def rename_id_pdf(person_folder: Path):
    """
    处理单个人员文件夹：
    找到与文件夹同名的pdf，重命名为【人名-身份证.pdf】
    同名pdf指：文件夹名.pdf，大小写兼容
    """
    person_name = person_folder.name
    target_old_name = f"{person_name}.pdf"
    target_new_name = f"{person_name}-身份证.pdf"

    old_file = person_folder / target_old_name
    new_file = person_folder / target_new_name

    # 判断原文件是否存在
    if not old_file.exists():
        return

    # 防止重复改名，避免文件已存在报错
    if new_file.exists():
        print(f"[{person_name}] 已存在{target_new_name}，无需操作")
        return

    # 执行重命名
    old_file.rename(new_file)
    print(f"[{person_name}] 重命名：{target_old_name} → {target_new_name}")


def main():
    root_path = Path(ROOT_DIR)
    if not root_path.exists():
        print(f"错误：根目录不存在，请检查路径：{ROOT_DIR}")
        return

    # 遍历根目录下一级所有文件夹（人员目录）
    for folder in root_path.iterdir():
        if not folder.is_dir():
            continue
        folder_name = folder.name
        # 跳过不需要处理的目录
        if folder_name in SKIP_FOLDERS:
            print(f"跳过目录：{folder_name}")
            continue
        # 执行重命名逻辑
        rename_id_pdf(folder)

    print("\n===== 全部文件夹处理完成 ====")


if __name__ == "__main__":
    main()