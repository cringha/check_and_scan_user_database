import os
import re
import argparse
from typing import Optional

# ===================== 配置规则区（新增证书类型可在此补充） =====================
# 证书类型匹配规则：(匹配关键词, 标准证书名)，按关键词长度从长到短排序，优先匹配长文本
CERT_TYPE_RULES = [
    ("信息系统项目管理师", "信息系统项目管理师"),
    ("系统规划与管理师", "系统规划与管理师"),
    ("系统集成项目管理工程师", "系统集成项目管理工程师"),
    ("软件设计师", "软件设计师"),
    ("系统架构师", "系统架构师"),
    ("软考中级证书", "软考证书"),
    ("软考高级证书", "软考证书"),
    ("软考证书", "软考证书"),
    ("软考", "软考证书"),
    ("证书", "证书"),
]

# 证书类型 → 默认等级映射（文件名无显式等级时自动兜底，不需要可注释掉对应行）
CERT_DEFAULT_LEVEL = {
    "信息系统项目管理师": "高级",
    "系统规划与管理师": "高级",
    "系统架构师": "高级",
    "系统集成项目管理工程师": "中级",
    "软件设计师": "中级",
}

# 等级关键词
LEVEL_KEYWORDS = ["高级", "中级", "初级"]

# 提取人名时需要剔除的停用词
STOP_WORDS = set()
for kw, name in CERT_TYPE_RULES:
    STOP_WORDS.add(kw)
    STOP_WORDS.add(name)
STOP_WORDS.update(LEVEL_KEYWORDS)
STOP_WORDS.add("身份证")


# ===================== 工具函数 =====================
def clean_number_suffix(text: str) -> str:
    """
    仅移除「括号+数字」的重复文件后缀（如 (1)、_(2)、 (3) ）
    保留人名后直接跟随的数字（如 杨见2、王鑫1）和括号内的有效文字（如 (软考高级)）
    """
    return re.sub(r'[_\s]*\(\d+\)[_\s]*', '', text).strip()


def extract_person_name(text: str) -> str:
    """
    从清理后的文件名中提取人名：
    - 剔除所有证件/等级相关关键词
    - 保留中文汉字 + 人名尾部数字（用于重名区分）
    - 自动适配人名在前/在后两种命名格式
    """
    processed = text
    # 移除所有停用词
    for word in STOP_WORDS:
        if word:
            processed = processed.replace(word, "")
    # 移除空括号、连接符、空格等无关符号
    processed = re.sub(r'[()（）\-+_\s]', '', processed)
    # 仅保留中文和数字
    name = re.sub(r'[^\u4e00-\u9fa50-9]', '', processed)
    return name.strip()


def detect_cert_type(text: str) -> Optional[str]:
    """识别证书类型，返回标准名称，识别失败返回 None"""
    for keyword, standard_name in CERT_TYPE_RULES:
        if keyword in text:
            return standard_name
    return None


def detect_level(text: str, cert_type: Optional[str]) -> Optional[str]:
    """
    识别证书等级：
    1. 优先匹配文件名中显式的「高级/中级/初级」关键词
    2. 无显式等级时，通过证书类型默认映射兜底（可关闭）
    """
    # 第一步：从文件名中找显式等级
    for lv in LEVEL_KEYWORDS:
        if lv in text:
            return lv
    # 第二步：证书类型默认等级兜底（不需要可注释以下两行）
    if cert_type and cert_type in CERT_DEFAULT_LEVEL:
        return CERT_DEFAULT_LEVEL[cert_type]
    return None


# ===================== 核心命名逻辑 =====================
def generate_new_filename(old_filename: str) -> Optional[str]:
    """
    根据旧文件名生成规范新文件名
    返回 None 表示无法识别或无需处理
    """
    name_no_ext, ext = os.path.splitext(old_filename)
    # 第一步：清理所有 (数字) 后缀
    cleaned_text = clean_number_suffix(name_no_ext)

    # ---------- 身份证文件处理 ----------
    if "身份证" in cleaned_text:
        person_name = extract_person_name(cleaned_text)
        if not person_name:
            return None
        return f"{person_name}-身份证{ext}"

    # ---------- 证书文件处理 ----------
    cert_type = detect_cert_type(cleaned_text)
    if not cert_type:
        return None  # 无法识别为证书文件，跳过

    level = detect_level(cleaned_text, cert_type)
    person_name = extract_person_name(cleaned_text)

    if not person_name:
        return None

    if level:
        return f"{person_name}-{cert_type}-{level}{ext}"
    else:
        return f"{person_name}-{cert_type}{ext}"


# ===================== 主程序 =====================
def main():
    parser = argparse.ArgumentParser(description="批量规范化重命名身份证与软考证书文件")
    parser.add_argument("target_dir", help="待处理文件所在的目录路径（支持相对/绝对路径）")
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="试运行模式：仅打印重命名对照清单，不实际修改文件"
    )
    args = parser.parse_args()

    target_dir = args.target_dir
    if not os.path.isdir(target_dir):
        print(f"错误：目录不存在 → {target_dir}")
        return

    # 收集目录下所有普通文件
    all_files = [
        f for f in os.listdir(target_dir)
        if os.path.isfile(os.path.join(target_dir, f))
    ]

    # 生成重命名计划
    rename_plan = []
    name_count = {}  # 统计新文件名重复情况
    for old_name in all_files:
        new_name = generate_new_filename(old_name)
        if new_name is None or new_name == old_name:
            continue
        rename_plan.append((old_name, new_name))
        name_count[new_name] = name_count.get(new_name, 0) + 1

    if not rename_plan:
        print("没有需要重命名的文件。")
        return

    # 打印重命名预览
    print("=" * 70)
    print(f"共发现 {len(rename_plan)} 个待重命名文件：")
    print("-" * 70)
    for old, new in rename_plan:
        dup_mark = " ⚠️ 重名" if name_count[new] > 1 else ""
        print(f"{old:<42} →  {new}{dup_mark}")
    print("=" * 70)

    # 试运行模式直接结束
    if args.dry_run:
        print("\n【试运行模式】已完成预览，未修改任何文件。")
        return

    # 重复文件名警告
    dup_names = [k for k, v in name_count.items() if v > 1]
    if dup_names:
        print(f"\n警告：存在 {len(dup_names)} 个重复的目标文件名，执行后会自动跳过重复项避免覆盖。")

    # 确认后执行重命名
    confirm = input("\n确认执行重命名？输入 y 继续，其他字符取消：").strip().lower()
    if confirm != "y":
        print("已取消操作。")
        return

    success = 0
    skipped = 0
    for old_name, new_name in rename_plan:
        old_path = os.path.join(target_dir, old_name)
        new_path = os.path.join(target_dir, new_name)

        if os.path.exists(new_path):
            print(f"跳过（目标已存在）：{old_name}")
            skipped += 1
            continue

        try:
            os.rename(old_path, new_path)
            print(f"已重命名：{old_name} → {new_name}")
            success += 1
        except Exception as e:
            print(f"重命名失败：{old_name}，原因：{str(e)}")

    print(f"\n处理完成：成功 {success} 个，跳过 {skipped} 个。")


if __name__ == "__main__":
    main()
