import os
import shutil
import hashlib
# 源目录（存放待移动的证书文件）
src_dir = r"C:\Users\101202304023\Desktop\工作\投标项目\学历"

# 目标根目录（下有各人员子文件夹）
dst_root = r"C:\Users\101202304023\Desktop\工作\投标项目\用户身份证、毕业证、合同等信息"


def get_file_md5(file_path: str) -> str:
    """计算文件的MD5值，返回小写字符串"""
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            # 分块读取，适合大文件
            for chunk in iter(lambda: f.read(4096), b''):
                md5.update(chunk)
        return md5.hexdigest().lower()
    except FileNotFoundError:
        return "文件不存在"
    except Exception as e:
        return f"读取错误: {str(e)}"


def move_all_user_certs():
    success_count = 0
    error_count = 0

    tmp_exist_path = os.path.join(src_dir, "已经存在")

    # 遍历源目录所有文件
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)

        # 只处理文件，跳过子文件夹
        if not os.path.isfile(src_path):
            continue

        # 按 "-" 分割人名和证书名
        if "-" not in filename:
            print(f"【跳过】文件名格式不正确：{filename}")
            error_count += 1
            continue

        name_part = filename.split("-", 1)[0]  # 只分割第一个 "-"
        person_dir = os.path.join(dst_root, name_part)

        # 目标人员目录不存在则跳过
        if not os.path.isdir(person_dir):
            print(f"【跳过】人员目录不存在：{name_part}，文件：{filename}")
            error_count += 1
            continue

        dst_path = os.path.join(person_dir, filename)

        # 目标已存在同名文件
        if os.path.exists(dst_path):
            src_path_md5 = get_file_md5(src_path)
            dst_path_md5 = get_file_md5(dst_path)

            if src_path_md5 != dst_path_md5:
                print(f"【错误】目标已存在同名文件，跳过：{dst_path}, MD5 不一致")
            else:


                dst_path1 = os.path.join(tmp_exist_path, filename)
                shutil.move(src_path, dst_path1)
                print(f"【错误】目标已存在同名文件，MD5 一致。 MOVE TO：{dst_path1}")
                error_count += 1
                continue

        # 执行移动
        try:
            shutil.move(src_path, dst_path)
            print(f"【成功】移动：{src_path} -> {dst_path}")
            success_count += 1
        except Exception as e:
            print(f"【失败】移动出错 {filename}：{str(e)}")
            error_count += 1

    # 最终统计
    print("\n==================== 执行完成 ====================")
    print(f"成功移动：{success_count} 条")
    print(f"失败/跳过：{error_count} 条")
    print("===================================================")


move_all_user_certs()