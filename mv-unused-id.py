from pathlib import Path
import shutil

# ===================== 配置区域 =====================
# 人员资质根目录，改成你电脑实际路径
ROOT_DIR = r"C:\Users\101202304023\Desktop\工作\投标项目\员工的身份证"
# 存放身份证的临时文件夹（自动创建，在根目录下）
TEMP_FOLDER = Path(ROOT_DIR) / "临时"
# 需要提取身份证的人员名单
TARGET_NAMES = [
    "于丽敏",
    "付金星",
    "何春凤",
    "史安明",
    "吴党辉",
    "姜德坤",
    "宋雄飞",
    "常银辉",
    "张振涛",
    "张运彩",
    "李博文",
    "李振威",
    "李祺乐",
    "杨宇",
    "林明健",
    "王中汉",
    "王友超1",
    "王姣",
    "王彦果",
    "王晓明",
    "王朋",
    "王欢",
    "王泽发",
    "王赫1",
    "王锐",
    "耿仁伟",
    "蔡骏潇",
    "薛才成",
    "许志俊",
    "贾习龙",
    "赖家豪",
    "赵磊",
    "邓佳",
    "金千俊",
    "陈雅琴",
    "陈高洋",
    "韩国星",
    "马寒军",
    "马爱强",
    "高冲峰",
    "高金",
    "鲍永昌",
    "黄仲小",
    "黄成",
    "黄攀"
]
# ====================================================

def move_id_file(person_dir: Path):
    """在单人目录查找身份证PDF并移动到临时文件夹"""
    # file = person_dir.name

    file_name = person_dir.name.lower()
    # 匹配身份证文件：包含“身份证”且后缀为pdf
    if "身份证" in file_name and person_dir.suffix.lower() == ".pdf":
        dest_file = TEMP_FOLDER / person_dir.name
        # 避免重名覆盖，重复文件改名
        counter = 1
        while dest_file.exists():
            dest_file = TEMP_FOLDER / f"{person_dir.stem}_{counter}{person_dir.suffix}"
            counter += 1
        shutil.move(str(person_dir), str(dest_file))
        print(f"已移动：{file_name} → {person_dir.name}")

def main():
    root_path = Path(ROOT_DIR)
    if not root_path.exists():
        print(f"错误：根目录不存在 {ROOT_DIR}，请修改路径！")
        return
    # 创建临时目录，不存在则自动生成
    TEMP_FOLDER.mkdir(exist_ok=True)
    print(f"临时文件夹路径：{TEMP_FOLDER}\n")

    # 遍历根目录下所有人员文件夹
    for folder in root_path.iterdir():
        # if not folder.is_dir():
        #     continue
        filename = folder.name

        # 只处理 pdf
        if not filename.lower().endswith(".pdf"):
            continue

        # 提取人名：按 "-" 分割，取第一部分并去除空格
        name_part = filename.split("-", 1)[0].strip()

        # 去掉末尾数字（如 王友超1 → 王友超，王赫1 → 王赫）
        name = name_part.rstrip("0123456789")
        # 仅处理名单内人员
        if name not in TARGET_NAMES:
            continue
        move_id_file(folder)

    print("\n==== 所有目标人员身份证迁移完成 ====")

if __name__ == "__main__":
    main()