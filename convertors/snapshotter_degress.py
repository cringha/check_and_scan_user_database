from pathlib import Path
from typing import List

from convertors.common_inf import SnapShoter
from tools.pdf_utils import snap_pdf_page

ID_CARD = "idcard"


def split_file_name(file_name_path: Path) -> str:
    file_name = file_name_path.stem
    if '-' in file_name:
        return file_name.split('-')[1]
    else:
        return file_name


class BaseDegreeSnapShotter(SnapShoter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)


    def get_degree_order(self)->str :
        return ""

    def take(self, user_name: str, src_file_name: str|List[str]):

        file_list = []
        if type(src_file_name) == str:
            file_list.append(src_file_name)
        else:
            for file_name in src_file_name:
                file_list.append(file_name)

        order = self.get_degree_order()

        for file_name in file_list:
            file_full_name = self.database_user_path / file_name
            file_full_name_path = Path(file_full_name)
            short_name = split_file_name(file_full_name_path)

            def gen_degree_file_name(user_name1: str, page_num, page_count, pdf_filename):
                image_name = f"{user_name1}-毕业证-{order}-{short_name}-{page_num}.png"
                image_full_name = self.target_user_image_path / image_name
                return str(image_full_name)

            snap_pdf_page(str(file_full_name), user_name, gen_degree_file_name)



class DegreeSnapShotter(BaseDegreeSnapShotter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)

    def get_info_key(self)->str :
        return "degreeCertificate"

    def get_degree_order(self)->str :
        return "A"



class GraduationCertificateSnapShotter(BaseDegreeSnapShotter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)

    def get_info_key(self)->str :
        return "graduationCertificate"

    def get_degree_order(self)->str :
        return "G"


class XuexinwangSnapShotter(BaseDegreeSnapShotter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)

    def get_info_key(self)->str :
        return "xuexinwang"

    def get_degree_order(self)->str :
        return "V"
