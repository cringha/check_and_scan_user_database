import os
import random
import sys

from tools.excel_utils import read_excel_sheet_values
from tools.utils import get_dict_val
from userinfo.dutyinfo import convert_duty_2_dict, find_user_duty_info
from userinfo.user_resume import UserResumeReader
from jinja2 import Environment


class Project:
    def __init__(self, year: str, name: str, summary: str, begin,end,scope: str = ""):
        self.year = year
        self.name = name
        self.summary = summary
        self.scope = scope
        self.begin = begin
        self.end = end


class YearProjects:
    def __init__(self, year: str):
        self.year = year
        self.projects = []

    def add(self, v: Project):
        self.projects.append(v)

    def get_random_project(self):
        one = random.sample(self.projects, 1)
        return one[0]


def build_projects(projects):
    project_cache = {}
    for pro in projects:
        year = get_dict_val(pro,"Year")
        name = get_dict_val(pro, "Name")
        summary = get_dict_val(pro,"Summary")
        end = get_dict_val(pro, "End")
        begin = get_dict_val(pro, "Begin")
        scope = get_dict_val(pro, "Scope")

        if year is None or name is None or summary is None or end is None or begin is None or scope is None:
            print("user.xlsx 文件中， Project sheet 格式不对，应该有 Year, Name, Summary, Begin, End, Scope 字段")
            sys.exit(-1)


        p = Project(year, name,summary, begin,end, scope)
        if year not in project_cache:
            obj = YearProjects(year)
            project_cache[year] = obj
            obj.add(p)
        else:
            obj = project_cache[year]
            obj.add(p)

    return project_cache


# 根据工作年限，返回随机的 项目数
def gen_rand_project_by_work_exp(work_exp: int):
    if work_exp < 1:
        return [0, 1]

    if work_exp >= 5:
        return [4, 5]

    return [2, 5]


def pick_rand_project(project_cache, pick_year):
    keys = list(project_cache.keys())
    num = random.choice(pick_year)
    yy = random.sample(keys, num)

    yy.sort()

    out_list = []
    for y in yy:
        if y not in project_cache:
            print("Year {y} not in project ")
            exit(-1)
            return
        prj = project_cache[y].get_random_project()
        out = {
            "Year": y,
            "Name": prj.name,
            "Summary": prj.summary,
            "Begin": prj.begin ,
            "End": prj.end ,
            "Scope": prj.scope
        }
        out_list.append(out)
    return out_list


def user_project_exp(user, project):
    username = get_dict_val(user, "Name")
    projectname = get_dict_val(project, "Name")

    print("user name ", username, " project ", projectname)

    begin = get_dict_val(project, 'Begin', 1)
    end = get_dict_val(project, 'End', 2)

    print("begin  ", begin , " " , type(begin), " end  ", end, " ", type(end))

    return int((end - begin + 1) * 12)


class BeijingLianTongUserResumeReader(UserResumeReader):

    def __init__(self, user_list: list, args):
        super().__init__(user_list, args)
        self.user_list = user_list
        self.args = args
        self.sheet_name_project = args.sheet_name_project
        self.sheet_name_duty = args.sheet_name_duty
        self.project_cache = None
        self.duties_info = None

    def hook_jinja(self, jinja_env: Environment):
        jinja_env.globals['user_project_exp'] = user_project_exp

    def read_user_database(self, input_xlsx: str):

        if self.sheet_name_project is not None:
            project = read_excel_sheet_values(file_name=input_xlsx, sheet_name=self.sheet_name_project)
            self.project_cache = build_projects(project)

        if self.sheet_name_duty is not None and self.sheet_name_duty != "":
            duties = read_excel_sheet_values(file_name=input_xlsx, sheet_name=self.sheet_name_duty)
            self.duties_info = convert_duty_2_dict(duties)

    def process_user(self, user):
        if self.project_cache is not None:
            work_exp = user['工作年限']
            pick_years = gen_rand_project_by_work_exp(work_exp)

            prj = pick_rand_project(self.project_cache, pick_years)
            user["Project"] = prj

        if self.duties_info is not None:
            duty = user['职责']
            user['职责内容'] = find_user_duty_info(self.duties_info, duty)
