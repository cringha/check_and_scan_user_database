from pathlib import Path
from typing import Dict
from typing import List, Any, Set


class SnapShoter:
    def __init__(self, database_user_path: Path, target_user_image_path: Path):
        self.database_user_path = database_user_path
        self.target_user_image_path = target_user_image_path

    def get_info_key(self)->str :
        pass

    def take(self, user_name: str, id_card_file_name: str|List[str]):
        pass
