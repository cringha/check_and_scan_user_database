import os
import sys

from tools.utils import get_dict_val


class DutyInfo:
    def __init__(self, duty: str, desc: str):
        self.duty = duty
        self.desc = desc


def convert_duty_2_dict(duties):
    out = {}
    for one in duties:
        duty = get_dict_val(one, "Duty")
        desc = get_dict_val(one, "Desc")
        if duty is None or desc is None:
            print("user.xlsx 文件中， Duty sheet 格式不对，应该有 Duty, Desc 字段")
            sys.exit(-1)

        d = DutyInfo(duty, desc)
        out[duty] = d
    return out


def find_user_duty_info(duties, duty):
    if duty in duties:
        return duties[duty].desc
    duty = '软件开发'
    return duties[duty].desc
