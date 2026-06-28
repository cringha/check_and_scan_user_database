from pathlib import Path
from typing import List

from convertors.common_inf import SnapShoter
from tools.pdf_utils import snap_pdf_page

KEY_CONTRACT = "contract"

class ContractSnapShotter(SnapShoter):
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        super().__init__(database_user_path, target_user_image_path)


    def get_info_key(self)->str :
        return KEY_CONTRACT


    def take(self, user_name: str, src_file_name: str|List[str]):

        assert type(src_file_name) == str, f"{src_file_name} is not a string"

        id_card_file_full_name = self.database_user_path / src_file_name

        def gen_id_card_file_name(user_name1: str, page_num, page_count, pdf_filename):
            if page_num in [0,2,8]:
                image_name = f"{user_name1}-合同-{page_num}.png"
                image_full_name = self.target_user_image_path / image_name
                return str(image_full_name)
            return None

        snap_pdf_page(str(id_card_file_full_name), user_name, gen_id_card_file_name)

