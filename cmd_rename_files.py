# -*- coding: utf-8 -*-
"""
证书文件批量重命名工具
================================
适用场景：一个目录下存放了多个用户的"身份证扫描件 + 各类证书（软考等）"，
文件名命名混乱（顺序不一、带 (1) (2) 序号、+ / _ / - 分隔符混用等）。

规则：
  1. 身份证文件   ->  <人名>-身份证.<原扩展名>
  2. 证书文件     ->  <人名>-<证书类型>-<高级|中级|初级>.<原扩展名>
                     若文件名中无法识别等级，则为 <人名>-<证书类型>.<原扩展名>
  3. 自动去掉文件名中的 (1) (2) 等序号后缀
  4. 不写死任何用户名：姓名、证书类型、等级全部从文件名中规则识别，
     因此将来新增用户文件后直接再跑一次本脚本即可
  5. 目录通过命令行参数传入

用法：
  python rename_certs.py <证书目录> [--dry-run] [--list users.txt]

  --dry-run   只预览改名计划，不真正修改文件
  --list      可选的清单文件（如 users.txt，GBK/UTF-8 均可），
              用于核对哪些文件是新文件（不在清单中）
"""
import argparse
import re
import sys
from pathlib import Path

# 证书类型关键词（按长度降序优先匹配，长的必须先匹配）
CERT_TYPES = [
    "信息系统项目管理师",
    "系统集成项目管理工程师",
    "系统规划与管理师",
    "系统架构设计师",
    "数据库系统工程师",
    "信息安全工程师",
    "信息系统监理师",
    "嵌入式系统设计师",
    "电子商务设计师",
    "系统架构师",
    "软件评测师",
    "软件设计师",
    "系统分析师",
    "网络工程师",
    "网络管理员",
    "软件过程能力评估师",
    "计算机硬件工程师",
    "多媒体应用设计师",
    "信息处理技术员",
    "软考证书",
    "程序员",
    "架构师",
    "软考",
    "系统集成",
    "规划师",
    "软件设计",
    "证书",
]
CERT_TYPES = sorted(set(CERT_TYPES), key=lambda s: (-len(s), s))

# 等级词（"高级职称"要整体优先于"高级"，避免残留"职称"）
LEVEL_WORDS = ("高级", "中级", "初级")
LEVEL_RE = re.compile(r"(高级职称|初级职称|中级职称|高级|中级|初级)")

SEQ_RE = re.compile(r"[\(\（]\s*\d+\s*[\)\）]")
CHINESE_RE = re.compile(r"[\u4e00-\u9fa5]")


def strip_seq_no(s: str) -> str:
    """去掉 (1)、（2）、( 3 ) 等序号后缀，反复清理直到稳定，再去掉首尾分隔符号"""
    while True:
        new = SEQ_RE.sub("", s)
        if new == s:
            return s.strip(" _-+")
        s = new


def detect_level(s: str):
    """返回文件名中出现的等级词（高级/中级/初级），没有则返回 None"""
    for lv in LEVEL_WORDS:
        if lv in s:
            return lv
    return None


def find_cert(s: str):
    """返回 (证书类型, 位置)；找不到返回 (None, -1)"""
    for t in CERT_TYPES:
        pos = s.find(t)
        if pos >= 0:
            return t, pos
    return None, -1


def extract_name(seg: str) -> str:
    """从姓名片段中提取人名（2-4 个连续汉字）。
    先剔除数字与残留的证书类型词（如"软考"），再取第一段纯汉字。"""
    seg = re.sub(r"\d+", "", seg)
    for t in CERT_TYPES:
        seg = seg.replace(t, "")
    seg = re.sub(r"[^\u4e00-\u9fa5]", "", seg)
    m = re.search(r"[\u4e00-\u9fa5]{2,4}", seg)
    return m.group() if m else ""


def has_name(seg: str) -> bool:
    """片段去符号后是否恰好是 2-4 个汉字（用于判断姓名在前还是在后）"""
    n = len(CHINESE_RE.findall(seg))
    return 2 <= n <= 4


def read_lines(path: Path):
    """自动识别 GBK / UTF-8 编码读取文本清单"""
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            return [l.strip() for l in raw.decode(enc).splitlines() if l.strip()]
        except UnicodeDecodeError:
            continue
    return []


def main():
    parser = argparse.ArgumentParser(description="证书文件批量重命名工具")
    parser.add_argument("directory", help="存放证书文件的目录")
    parser.add_argument("--dry-run", "-n", action="store_true", help="只预览，不实际改名")
    parser.add_argument("--list", default=None, help="可选清单文件（如 users.txt），用于标记新文件")
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        sys.exit(f"错误：目录不存在 -> {root}")

    listed = set(read_lines(root / args.list)) if args.list else None

    files = sorted(
        p for p in root.iterdir()
        if p.is_file() and p.name != Path(__file__).name
    )

    action = "将改名" if args.dry_run else "改名"
    stats = {"renamed": 0, "skipped_ok": 0, "skip_dup": 0, "unrecognized": 0}
    print(f"处理目录：{root}  共 {len(files)} 个文件\n")

    for p in files:
        orig = p.name
        if listed is not None and orig not in listed:
            print(f"  [未在清单中] {orig}")

        body, ext = p.stem, p.suffix

        if orig.lower().endswith(".txt"):
            continue  # users.txt 等清单文件跳过

        # ---- 身份证 ----
        if "身份证" in body:
            name = extract_name(body.replace("身份证", ""))
            if not name:
                print(f"  [无法识别] 身份证姓名无法解析: {orig}")
                stats["unrecognized"] += 1
                continue
            new_body = f"{name}-身份证"

        # ---- 证书 ----
        else:
            body = strip_seq_no(body)
            level = detect_level(body)
            b2 = LEVEL_RE.sub("", body)          # 移除等级词，便于识别证书类型
            cert, pos = find_cert(b2)
            if not cert:
                print(f"  [无法识别] 找不到证书类型，请手工处理: {orig}")
                stats["unrecognized"] += 1
                continue
            prefix, suffix = b2[:pos], b2[pos + len(cert):]
            name = extract_name(prefix if has_name(prefix) else suffix)
            if not name:
                print(f"  [无法识别] 姓名无法解析: {orig}")
                stats["unrecognized"] += 1
                continue
            new_body = f"{name}-{cert}" + (f"-{level}" if level else "")

        new_name = new_body + ext
        if new_name == orig:
            print(f"  [已是规范名] {orig}")
            stats["skipped_ok"] += 1
            continue

        target = root / new_name
        if target.exists():
            print(f"  [冲突跳过] 目标已存在: {orig} -> {new_name}（可能是重复文件）")
            stats["skip_dup"] += 1
            continue

        print(f"  [{action}] {orig}\n         -> {new_name}")
        if not args.dry_run:
            p.rename(target)
        stats["renamed"] += 1

    print(
        f"\n汇总：{'（预览模式，未实际修改）' if args.dry_run else ''}\n"
        f"  将改名/已改名 {stats['renamed']}，已是规范名 {stats['skipped_ok']}，"
        f"冲突跳过 {stats['skip_dup']}，无法识别 {stats['unrecognized']}"
    )


if __name__ == "__main__":
    main()
