from convertors.common_inf import SnapShoter
from convertors.snapshotter_degress import DegreeSnapShotter, GraduationCertificateSnapShotter, XuexinwangSnapShotter
from convertors.snapshotter_user_base_certs import  CISPSnapShotter, PMPSnapShotter, CISAWSnapShotter
from convertors.snapshotter_user_contract import ContractSnapShotter
from convertors.snapshotter_user_id_card import IdCardSnapShotter
from pathlib import Path
from typing import Dict
from typing import List, Any, Set

SNAPSHOT_FACTORY = {
    "idcard": IdCardSnapShotter,
    "contract": ContractSnapShotter,
    "degree":DegreeSnapShotter,
    "grad": GraduationCertificateSnapShotter,
    "xuexinwang": XuexinwangSnapShotter,
    "cisp": CISPSnapShotter,
    "pmp" : PMPSnapShotter,
    "cisaw" : CISAWSnapShotter,

}


class SnapshotManager:
    def __init__(self, database_user_path: Path, target_user_image_path: Path) -> None:
        self.snapshots = {}
        self.database_user_path = database_user_path
        self.target_user_image_path = target_user_image_path

    def get_snapshot(self, flag: str) -> SnapShoter | None:
        if flag not in self.snapshots:
            if flag not in SNAPSHOT_FACTORY:
                print(f"Flag not support,  {flag}, ", SNAPSHOT_FACTORY.keys())
                return None

            snapshot = SNAPSHOT_FACTORY[flag](self.database_user_path, self.target_user_image_path)
            self.snapshots[flag] = snapshot
        return self.snapshots[flag]

    def take_snapshot(self, user_name: str, user_info: Dict[str, Any], flags: Set[Any]):

        for flag in flags:
            snapshot = self.get_snapshot(flag)
            if snapshot is None:
                continue

            info_key = snapshot.get_info_key()
            if info_key not in user_info:
                print(f"User {user_name} info.json, not info {info_key}, for flag {flag}")
                continue

            files = user_info[info_key]
            snapshot.take(user_name, files)
