import os
from pathlib import Path


def get_all_users(target_dir: str):
    target_dirs = set()

    # 遍历源目录所有文件
    for filename in os.listdir(target_dir):

        person_folder = os.path.join(target_dir, filename)
        if os.path.isdir(person_folder):
            target_dirs.add(filename)

    return target_dirs


def find_target_dir(name, target_dir):
    if name in target_dir:
        return name

    find_s = []
    for one in target_dir:
        if name in one:
            find_s.append(one)
    if len(find_s) == 1:
        return find_s[0]
    if len(find_s) > 1:
        raise f"Find more than one user:{find_s}, {name} "
    return None


def get_all_certs(src_dir, file_filter):
    target_files = []
    # 遍历源目录下所有子文件夹
    file_filter = file_filter.lower()
    target_path = Path(src_dir)
    for f in target_path.iterdir():
        if f.is_file() and f.name.lower().endswith(file_filter):
            target_files.append(f.name)

    return target_files
