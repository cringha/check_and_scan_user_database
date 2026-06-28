from pathlib import Path
from typing import List

from convertors.common_inf import SnapShoter, IMAGE_TYPE
from tools.pdf_utils import snap_pdf_page
import shutil

from userinfo.common import SNAPSHOT_NAME_CERTS, SNAPSHOT_NAME_RUANKAO

KEY_RUANKAO = "ruankao"


def split_file_name(file_name_path: Path) -> str:
    file_name = file_name_path.stem
    if '-' in file_name:
        return file_name.split('-')[1]
    else:
        return file_name


class RuanKaoCertSnapShotter(SnapShoter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)

    def get_info_key(self) -> str:
        return KEY_RUANKAO

    def get_degree_order(self) -> str:
        return ""

    def take(self, user_name: str, src_file_name: str | List[str]):

        file_list = []
        if type(src_file_name) == str:
            file_list.append(src_file_name)
        else:
            for file_name in src_file_name:
                file_list.append(file_name)

        for file_name in file_list:

            file_full_name = self.database_user_path / file_name
            file_full_name_path = Path(file_full_name)
            short_name = split_file_name(file_full_name_path)

            if file_name.lower().endswith(".pdf"):
                def gen_degree_file_name(user_name1: str, page_num, page_count, pdf_filename):
                    image_name = f"{user_name1}-{SNAPSHOT_NAME_CERTS}-{SNAPSHOT_NAME_RUANKAO}_{short_name}-{page_num}{IMAGE_TYPE}"
                    image_full_name = self.target_user_image_path / image_name
                    return str(image_full_name)

                snap_pdf_page(str(file_full_name), user_name, gen_degree_file_name)
            else:

                image_name = f"{user_name}-{SNAPSHOT_NAME_CERTS}-{SNAPSHOT_NAME_RUANKAO}_{short_name}-0{file_full_name_path.suffix}"
                image_full_name = self.target_user_image_path / image_name

                try:
                    shutil.copy2(file_full_name_path, image_full_name)
                    print(f"已复制：{user_name} ,  {image_full_name}")
                except Exception as e:
                    print(f"复制失败 {user_name}  {image_full_name}: {e}")
                    continue
