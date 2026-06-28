from userinfo.user_resume import UserResumeReader
from userinfo.user_resume_beijing_liantong_v1 import BeijingLianTongUserResumeReader


def make_resume_factory( resume_type:str , user_list: list, args ):
    if resume_type == "v1":
        return BeijingLianTongUserResumeReader(user_list, args)
    else:
        return UserResumeReader(user_list, args)