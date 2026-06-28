from pathlib import Path
from typing import List, Dict

from userinfo.common import SNAPSHOT_NAME_SS, SNAPSHOT_NAME_CERTS



class InlineImagePackage:
    def __init__(self , title :str, image ) -> None:
        self.title = title
        self.image = image


class SnapshotImage:
    def __init__(self, title :str , image_path: Path):
        self.title = title
        self.image_path = image_path

    def __str__(self):
        return f"{self.title}"


class UserSnapshot:
    def __init__(self, title: str):
        self.title = title
        self.snapshot : List[SnapshotImage] = []
        self.images : List[InlineImagePackage] = []

    def add_snapshot(self, sub_title:str , snapshot:Path ):
        self.snapshot.append(SnapshotImage(sub_title, snapshot))

    def add_image(self, sub_title:str, image):
        self.images.append(InlineImagePackage(sub_title, image))

    def __str__(self):
        return f"{self.title}: {len(self.snapshot)} snapshots"


def get_last_by_filename_glob(directory, pattern="*"):
    dir_path = Path(directory)
    # 获取所有匹配的文件（排除子目录）
    files = [f for f in dir_path.glob(pattern)]

    if not files:
        print("未找到匹配的文件")
        return None

    # 按文件名（字符串）升序排序，取最后一个
    files_sorted = sorted(files, key=lambda f: f.name)
    return files_sorted


"""
读取用户 证书截图的文件
"""


def read_user_snapshots(snapshot_base_path: Path, user_name: str, snapshot_types: List[str], pattern="*") -> List[
    UserSnapshot]:
    user_snapshot_base_path = snapshot_base_path / user_name

    # 获取所有匹配的文件（排除子目录）
    files = [f for f in user_snapshot_base_path.glob(pattern)]
    # all_files = [f for f in target_path.iterdir() if f.is_file()]

    if not files:
        print(f"未找到 {user_name} 的社保文件, in {snapshot_base_path}, pattern: {pattern}, types: {snapshot_types}")
        return []

    all_snapshot = []

    for snapshot_type in snapshot_types:

        snapshot_file_list = []

        for file in files:
            file_name = file.stem
            if snapshot_type in file_name:
                snapshot_file_list.append(file)

        if len(snapshot_file_list) > 0:
            snapshot_file_list = sorted(snapshot_file_list, key=lambda f: f.name)
            us = UserSnapshot(snapshot_type)
            for file in snapshot_file_list:
                if snapshot_type == SNAPSHOT_NAME_CERTS:
                    sub_type = extra_sub_type_from_file_name(file)
                else:
                    sub_type = ""
                us.add_snapshot( sub_type, file  )
            all_snapshot.append(us)

    return all_snapshot

def extra_sub_type_from_file_name( file:Path ) -> str:
    file_name = file.stem
    if '-' in file_name :
        parts  = file_name.split('-')
        if len(parts) >= 3 :
            return parts[2] # 文件名 林阳-资质证书-CISP-0.png

    return ""

def read_user_ss_snapshots(ss_snapshot_base_path: Path, user_name: str, pattern="*",
                           ss_snapshot_type_name=SNAPSHOT_NAME_SS) ->    None | UserSnapshot:
    user_ss_snapshot_base_path = ss_snapshot_base_path / user_name

    # 获取所有匹配的文件（排除子目录）
    files = [f for f in user_ss_snapshot_base_path.glob(pattern)]
    # all_files = [f for f in target_path.iterdir() if f.is_file()]

    if not files:
        print(f"未找到 {user_name} 的社保文件, in {ss_snapshot_base_path}, pattern: {pattern}")
        return None

    snapshot_file_list = []

    for file in files:
        snapshot_file_list.append(file)

    if len(snapshot_file_list) > 0:
        snapshot_file_list = sorted(snapshot_file_list, key=lambda f: f.name)
        us = UserSnapshot(ss_snapshot_type_name )
        for file in snapshot_file_list:


            us.add_snapshot( "" , file)
        return us

    return None
