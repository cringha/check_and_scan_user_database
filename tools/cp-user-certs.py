import os
import json
import shutil

# ====================== 配置 ======================
SOURCE_ROOT = r"C:\Users\101202304023\Desktop\工作\投标项目\用户身份证、毕业证、合同等信息"
TARGET_ROOT = r"C:\Users\101202304023\Desktop\符合的学历证书"

# 需要复制的字段
COPY_FIELDS = [
    "xuexinwang",
    "degreeCertificate",
    "graduationCertificate"
]

# 目标人员名单
TARGET_PEOPLE = {
    "王宁", "朱冰霞", "纪晓乐", "崔宇", "李大健", "王鑫1", "王泽君", "范志华",
    "朱海楠", "赵卫斌1", "陈宇", "崔渊博", "李跃波", "胡兵", "吴涛", "林阳",
    "史祥鹏", "张利强", "刘晟鑫", "王龙", "董清辉", "袁林", "刘武旭", "邸学锋",
    "姚瑞", "贾立军", "刘道林", "苏万龙", "张俊", "范磊波", "季斌", "常宁",
    "钱奇", "董晓晖", "李宁", "许延一", "马栋", "冯亚南", "马洪彬", "姜福利",
    "祁海", "李宁辉", "李智", "王亚辉", "白首骏", "班宏", "卜凡成1", "步学剑",
    "蔡小龙", "藏润强", "曹洋", "岑俊杰", "柴伟", "陈苍山", "陈钊2", "陈振",
    "仇红建1", "从继通", "崔澎", "代城", "邓超", "邓怀俊", "邓辉", "邓尚举",
    "丁凯云", "丁慎炳", "窦晶", "段淇", "凡同飞", "樊昕宇", "范国征", "葛大龙",
    "龚霞", "谷云鹤", "顾星宇", "胡凤", "黄晋健", "黄晶", "黄山山", "黄天成",
    "黄武宝", "计鹏伟", "纪燕飞", "冀中华", "贾永辉", "姜双双", "蒋辉", "蒋鹏程",
    "李洪兴", "李天将", "李晓康", "梁箐洪", "梁庄杰", "林涛", "林益峰1", "林泽琛",
    "刘超", "刘积磊", "刘家楠", "刘嘉伟", "刘鹏飞", "刘庆钊", "刘书", "刘伟伟",
    "刘文添", "刘喜秀", "刘雅萍1", "刘洋2", "陆喜磊", "陆永游", "吕伟平", "罗建龙",
    "罗振顺", "马成林", "马刚", "马恒恒1", "马金磊", "马鹏宇", "马蓉蓉", "马勇",
    "麦倩", "孟海琴", "孟娟", "孟伟", "倪永哲", "张娟", "朱赫1", "李强", "李亚辉",
    "陈庆", "黄世杰", "黄晓青", "梁炳坚", "梁轩", "廖永恒", "林银峰", "林永斌",
    "刘晨1", "刘康", "刘晓洋", "柳伯韬", "柳永明", "陆华明", "陆诗杰", "罗俊杰",
    "罗童", "马赫", "马建鹏", "马强3", "孟艳青", "倪冠", "尚程", "申高1", "沈文彪",
    "沈叶强", "陶明马", "佟瑶", "童刚金", "庹海燕", "万成军", "万达", "汪步江",
    "王博1", "王方圆", "王福永", "王鑫磊", "王炎岩", "韦福", "温德大", "温国强",
    "翁杰", "武胜", "席威居", "夏腾", "夏婷", "夏致昊", "肖衡杰", "肖君", "谢波",
    "谢孔顺", "闫石坚", "闫新祎", "闫羽航", "杨见", "杨见2", "杨军锋", "杨蓝暄",
    "杨梦端", "杨青清", "杨晓年1", "杨洵", "张佳平", "张剑飞", "张朕1", "张文俊",
    "刘畅", "高梁", "张炜5", "张天杰", "李永生", "李彦龙", "周兴友", "周云状",
    "张修灿", "赵保", "赵仕渊", "郑宁", "张涛", "张志琪"
}
# ==================================================

def get_file_list(value):
    """
    统一处理：字符串 / 数组 / None → 返回文件名列表
    """
    if not value:
        return []
    if isinstance(value, list):
        return [str(f).strip() for f in value if f.strip()]
    else:
        return [str(value).strip()]

def main():
    os.makedirs(TARGET_ROOT, exist_ok=True)
    person_count = 0
    file_count = 0

    # 遍历源目录下所有子文件夹
    for entry in os.listdir(SOURCE_ROOT):
        person_folder = os.path.join(SOURCE_ROOT, entry)
        if not os.path.isdir(person_folder):
            continue

        info_json = os.path.join(person_folder, "info.json")
        if not os.path.exists(info_json):
            continue

        # 读取 info.json
        try:
            with open(info_json, 'r', encoding='utf-8') as f:
                info = json.load(f)
        except Exception as e:
            print(f"读取失败 {info_json}: {e}")
            continue

        name = info.get("name", "").strip()
        if not name or name not in TARGET_PEOPLE:
            continue

        print(f"\n===== 处理人员：{name} =====")
        person_count += 1

        # 创建目标目录
        target_person_dir = os.path.join(TARGET_ROOT, name)
        os.makedirs(target_person_dir, exist_ok=True)

        # 复制各类证书
        for field in COPY_FIELDS:
            files = get_file_list(info.get(field))
            for fn in files:
                src = os.path.join(person_folder, fn)
                dst = os.path.join(target_person_dir, fn)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    print(f"已复制：{fn}")
                    file_count += 1
                else:
                    print(f"文件不存在：{fn}")

    print("\n" + "="*60)
    print(f"任务完成！")
    print(f"匹配人员数量：{person_count} 人")
    print(f"成功复制文件：{file_count} 个")
    print(f"保存路径：{TARGET_ROOT}")

if __name__ == "__main__":
    main()