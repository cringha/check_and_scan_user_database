import os
import random
import sys

from uitls.log import get_log
from uitls.utils import get_dict_val
from typing import Dict


class DutyInfo:
    def __init__(self, duty: str, desc: str):
        self.duty = duty
        self.desc = desc


def convert_duty_2_dict(duties):
    out = {}

    logger = get_log()

    for one in duties:
        duty = get_dict_val(one, "Duty")
        desc = get_dict_val(one, "Desc")
        if duty is None or desc is None:
            logger.error(f"user.xlsx: 文件中， Duty sheet 格式不对，应该有 Duty, Desc 字段")
            print("user.xlsx 文件中， Duty sheet 格式不对，应该有 Duty, Desc 字段")
            sys.exit(-1)

        d = DutyInfo(duty, desc)
        out[duty] = d
    return out


def find_user_duty_info(duties: Dict[str, DutyInfo], duty):
    if duty in duties:
        return duties[duty].desc

    return random.choice(list(duties.values()))
