import argparse

from entries.user_info_to_snapshots import SUPPORT_FLAGS, step_all_user_list, get_user_list_from_xlsx, \
    do_export_user_info_to_snapshots
from uitls.log import init_with_conf, get_log, LogConfig


def main(args):
    if args.input_xlsx is None or args.input_xlsx == "":
        print("--input-xlsx 空")

        return False

    if args.user_database is None or args.user_database == "":
        print("--user-database 空")
        return False

    snapshot_types = []
    if args.cert_type != "":
        snapshot_types = args.cert_type.split(',')
        for tt in snapshot_types:
            if tt not in SUPPORT_FLAGS:
                print(f"-t, --cert-type value , wanted , {SUPPORT_FLAGS} ")
                return False

    # flags = {"idcard","contract","degree","grad","xuexinwang","cisp","cisaw","pmp","ruankao"}
    flags = set(snapshot_types)

    init_with_conf(LogConfig())
    logger = get_log()
    logger.debug("user info to snapshot start")

    user_list = do_export_user_info_to_snapshots(args.input_xlsx, args.user_database, args.output_user_images, flags,
                                                 None,
                                                 args.sheet_name_user,
                                                 args.col_user_name)

    return True


if __name__ == "__main__":
    init_with_conf(LogConfig())
    logger = get_log()
    logger.debug("user info to snapshot start")
    #
    parser = argparse.ArgumentParser(description="转换用户身份证、证书、合同等转用户截图工具")
    parser.add_argument("-i", "--input-xlsx", help="输入Xlsx文件")
    parser.add_argument("-d", "--user-database", help="输入用户文件根目录")
    parser.add_argument("-s", "--output-user-images", help="输出截图文件根目录; default: %(default)s",
                        default="./output")
    parser.add_argument("-t", "--cert-type", help="要转换的类型; default: %(default)s",
                        default="idcard,contract,degree,grad,xuexinwang,cisp,cisaw,pmp,ruankao")
    parser.add_argument("--sheet-name-user", help="User sheet name; default: %(default)s", default="Users")
    parser.add_argument("--col-user-name", help="user column name; default: %(default)s", default="Name")

    args = parser.parse_args()

    try:
        result = main(args)
        if not result:
            parser.print_help()
    except Exception as e:
        print("Exec main error ", e)
