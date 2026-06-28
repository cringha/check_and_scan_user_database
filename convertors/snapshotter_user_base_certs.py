from pathlib import Path
from typing import List

from convertors.common_inf import SnapShoter, IMAGE_TYPE
from tools.pdf_utils import snap_pdf_page
from userinfo.common import SNAPSHOT_NAME_CERTS

SNAP_SHOT_NAME_CISP = "cisp"
SNAP_SHOT_NAME_CISAW = "cisaw"
SNAP_SHOT_NAME_PMP = "pmp"



class BaseCertSnapShotter(SnapShoter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)


    def get_cert_type(self)->str :
        return "A"

    def take(self, user_name: str, src_file_name: str|List[str]):

        assert type(src_file_name) == str, f"{src_file_name} is not a string"

        id_card_file_full_name = self.database_user_path / src_file_name
        cert_type = self.get_cert_type()
        def gen_id_card_file_name(user_name1: str, page_num, page_count, pdf_filename):
            image_name = f"{user_name1}-{SNAPSHOT_NAME_CERTS}-{cert_type}-{page_num}{IMAGE_TYPE}"
            image_full_name = self.target_user_image_path / image_name
            return str(image_full_name)

        snap_pdf_page(str(id_card_file_full_name), user_name, gen_id_card_file_name)


class CISPSnapShotter(BaseCertSnapShotter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)

    def get_info_key(self)->str :
        return SNAP_SHOT_NAME_CISP

    def get_cert_type(self)->str :
        return "CISP"

class CISAWSnapShotter(BaseCertSnapShotter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)

    def get_info_key(self)->str :
        return SNAP_SHOT_NAME_CISAW

    def get_cert_type(self)->str :
        return "CISAW"

class PMPSnapShotter(BaseCertSnapShotter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)

    def get_info_key(self)->str :
        return SNAP_SHOT_NAME_PMP

    def get_cert_type(self)->str :
        return "PMP"

