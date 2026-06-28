import os
import re
from pathlib import Path

def clean_cert_suffix(text: str) -> str:
    """清洗证件名称多余冗余字符：(数字)、下划线、多余空格"""
    # 去除 (1) (2) (3) (4) 这类括号数字
    text = re.sub(r"\s*\(\d+\)", "", text)
    # 去除末尾下划线
    text = re.sub(r"_+$", "", text)
    # 去除多余空格
    text = re.sub(r"\s+", "", text)
    return text

def parse_filename(file_name: str):
    """
    解析文件名，返回 (name, cert_desc, suffix)
    支持分隔符：-、+，兼容各种混乱命名
    """
    file_stem, suffix = os.path.splitext(file_name)
    stem = file_stem.strip()

    # 情况1：包含 + 分隔符 例：刘喜秀+学位证、葛大龙+毕业证
    if "+" in stem:
        parts = stem.split("+", 1)
        name = parts[0].strip()
        cert = clean_cert_suffix(parts[1].strip())
        return name, cert, suffix

    # 情况2：标准 - 分隔 人名在前
    dash_split = stem.split("-", 1)
    if len(dash_split) == 2:
        first, second = dash_split
        # 判断是否是证件在前（例：学位证-刘超）
        cert_keywords = {"学位证", "学位证书", "毕业证", "毕业证书", "学信网", "学历验证", "学历查询", "留学证明", "结业证书"}
        first_part = clean_cert_suffix(first)
        if any(k in first_part for k in cert_keywords):
            # 证件在前，调换顺序
            cert = first_part
            name = second.strip()
        else:
            # 人名在前，正常
            name = first.strip()
            cert = clean_cert_suffix(second.strip())
        return name, cert, suffix

    # 无分隔符，无法拆分，返回None表示不处理
    return None, None, suffix

def rename_cert_files(target_dir: str):
    """
    主逻辑：扫描目录，标准化重命名文件
    :param target_dir: 存放证书文件的文件夹路径
    """
    target_path = Path(target_dir)
    if not target_path.exists() or not target_path.is_dir():
        print(f"[错误] 目录不存在：{target_dir}")
        return

    log_list = []
    all_files = [f for f in target_path.iterdir() if f.is_file()]

    for file in all_files:
        old_full_name = file.name
        log_prefix = f"[{old_full_name}]"

        name, cert_desc, ext = parse_filename(old_full_name)
        # 无法拆分人名和证件，跳过
        if name is None or cert_desc is None or len(name) == 0 or len(cert_desc) == 0:
            log = f"{log_prefix} 跳过：无法拆分人名与证件信息"
            print(log)
            log_list.append(log)
            continue

        # 构造标准文件名
        standard_name = f"{name}-{cert_desc}{ext}"
        if standard_name == old_full_name:
            log = f"{log_prefix} 跳过：命名已符合规范"
            print(log)
            log_list.append(log)
            continue

        # 新文件完整路径
        new_file_path = target_path / standard_name
        if new_file_path.exists():
            log = f"{log_prefix} 跳过：目标文件 {standard_name} 已存在，防止覆盖"
            print(log)
            log_list.append(log)
            continue

        # 执行重命名
        try:
            file.rename(new_file_path)
            log = f"{log_prefix} 已重命名 → {standard_name}"
            print(log)
            log_list.append(log)
        except Exception as e:
            log = f"{log_prefix} 重命名失败：{str(e)}"
            print(log)
            log_list.append(log)

    # 输出汇总日志
    print("\n===== 操作日志汇总 =====")
    for log_item in log_list:
        print(log_item)
    print(f"\n本次共处理文件：{len(all_files)} 个")
    print(f"日志总数：{len(log_list)} 条")

if __name__ == "__main__":
    # ========== 修改此处为你的证书文件夹绝对路径 ==========
    CERT_FOLDER = r"C:\Users\101202304023\Desktop\工作\投标项目\学历"
    # ======================================================
    rename_cert_files(CERT_FOLDER)