


class DutyInfo:
    def __init__(self,duty:str, desc:str  ):
        self.duty = duty
        self.desc = desc

def convert_duty_2_dict( duties):
    out = {}
    for one in duties:
        duty = one['Duty']
        d = DutyInfo( duty, one['Desc'])
        out[duty] = d
    return out

def find_user_duty_info( duties , duty ):
    if duty in duties:
        return duties[duty].desc
    duty = '软件开发'
    return duties[duty].desc
