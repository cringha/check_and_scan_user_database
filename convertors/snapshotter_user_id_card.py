from pathlib import Path
from typing import List

from convertors.common_inf import SnapShoter
from tools.pdf_utils import snap_pdf_page

ID_CARD = "idcard"

class IdCardSnapShotter(SnapShoter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)


    def get_info_key(self)->str :
        return ID_CARD


    def take(self, user_name: str, src_file_name: str|List[str]):

        assert type(src_file_name) == str, f"{src_file_name} is not a string"

        id_card_file_full_name = self.database_user_path / src_file_name

        def gen_id_card_file_name(user_name1: str, page_num, page_count, pdf_filename):
            image_name = f"{user_name1}-身份证-{page_num}.png"
            image_full_name = self.target_user_image_path / image_name
            return str(image_full_name)

        snap_pdf_page(str(id_card_file_full_name), user_name, gen_id_card_file_name)
