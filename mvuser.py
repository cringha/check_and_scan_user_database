import os
import shutil
import re

# ===================== 配置区 =====================
# 根目录路径，根据你的实际路径修改
ROOT_DIR = r"D:\新增资料"
# 不需要处理的文件
IGNORE_FILES = {"test.list.txt"}
# 匹配姓名正则：匹配开头中文姓名，分隔符为 - / +
NAME_PATTERN = re.compile(r"^([\u4e00-\u9fa5]+)[-+]")
# ==================================================

def get_person_name(filename: str) -> str | None:
    """从文件名提取人员姓名，无匹配返回None"""
    match = NAME_PATTERN.match(filename)
    if match:
        return match.group(1).strip()
    return None

def scan_all_files(root: str) -> list[str]:
    """递归扫描目录下所有文件，返回完整文件路径列表"""
    file_paths = []
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname in IGNORE_FILES:
                continue
            full_path = os.path.join(dirpath, fname)
            file_paths.append(full_path)
    return file_paths

def move_file_to_person_folder(file_fullpath: str, root: str):
    """将单个文件移动到对应姓名文件夹"""
    filename = os.path.basename(file_fullpath)
    name = get_person_name(filename)
    if not name:
        print(f"【跳过】无法提取姓名：{filename}")
        return

    # 创建目标姓名文件夹
    target_folder = os.path.join(root, name)
    os.makedirs(target_folder, exist_ok=True)
    target_file = os.path.join(target_folder, filename)

    # 存在同名文件则跳过，避免覆盖
    if os.path.exists(target_file):
        print(f"【跳过】目标已存在：{target_file}")
        return

    # 执行移动
    shutil.move(file_fullpath, target_file)
    print(f"【已移动】{file_fullpath} --> {target_file}")

def main():
    print(f"开始扫描目录：{ROOT_DIR}")
    all_files = scan_all_files(ROOT_DIR)
    print(f"共扫描到待处理文件 {len(all_files)} 个\n")

    for file_path in all_files:
        move_file_to_person_folder(file_path, ROOT_DIR)

    print("\n===== 文件整理完成 =====")

if __name__ == "__main__":
    main()