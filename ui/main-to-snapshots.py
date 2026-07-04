import tkinter as tk
from tkinter import ttk, filedialog, messagebox


from entries.user_info_to_snapshots import do_export_user_info_to_snapshots
from uitls.log import init_with_conf, get_log,LogConfig


class ScreenshotConverterUI:
    def __init__(self, root):
        self.logger = get_log()
        self.root = root
        self.root.title("身份证/证书/合同用户截图转换工具")
        self.root.resizable(False, False)  # 禁止缩放，无最大化最小化

        # 证书类型列表（与命令行默认一致）
        self.cert_types = [
            "idcard", "contract", "degree", "grad",
            "xuexinwang", "cisp", "cisaw", "pmp", "ruankao"
        ]
        # 用于存储每个类型的勾选状态
        self.cert_vars = {}

        # 组件变量
        self.entry_xlsx = None
        self.entry_user_db = None
        self.entry_output = None
        self.entry_sheet = None
        self.entry_col = None

        self._create_widgets()

    def _create_widgets(self):
        padx = 5
        pady = 4

        # 1. 输入 XLSX
        ttk.Label(self.root, text="输入 XLSX 文件 (-i/--input-xlsx)").grid(
            row=0, column=0, padx=padx, pady=pady, sticky=tk.W
        )
        self.entry_xlsx = ttk.Entry(self.root, width=50)
        self.entry_xlsx.grid(row=0, column=1, padx=padx, pady=pady)
        ttk.Button(self.root, text="选择", command=self._select_xlsx).grid(
            row=0, column=2, padx=padx, pady=pady
        )

        # 2. 用户文件根目录
        ttk.Label(self.root, text="用户文件根目录 (-d/--user-database)").grid(
            row=1, column=0, padx=padx, pady=pady, sticky=tk.W
        )
        self.entry_user_db = ttk.Entry(self.root, width=50)
        self.entry_user_db.grid(row=1, column=1, padx=padx, pady=pady)
        ttk.Button(self.root, text="选择", command=self._select_user_db).grid(
            row=1, column=2, padx=padx, pady=pady
        )

        # 3. 输出目录
        ttk.Label(self.root, text="输出截图根目录 (-s/--output-user-images)").grid(
            row=2, column=0, padx=padx, pady=pady, sticky=tk.W
        )
        self.entry_output = ttk.Entry(self.root, width=50)
        self.entry_output.grid(row=2, column=1, padx=padx, pady=pady)
        self.entry_output.insert(0, "./output")
        ttk.Button(self.root, text="选择", command=self._select_output).grid(
            row=2, column=2, padx=padx, pady=pady
        )

        # 4. 证书类型（多选框）
        ttk.Label(self.root, text="转换类型 (-t/--cert-type)").grid(
            row=3, column=0, padx=padx, pady=pady, sticky=tk.NW
        )

        # 用 frame 放多选框，方便排版
        cert_frame = ttk.Frame(self.root)
        cert_frame.grid(row=3, column=1, columnspan=2, padx=padx, pady=pady, sticky=tk.W)

        # 生成多选框，默认全选
        row_cb = 0
        col_cb = 0
        for ct in self.cert_types:
            var = tk.BooleanVar(value=True)
            self.cert_vars[ct] = var
            cb = ttk.Checkbutton(
                cert_frame,
                text=ct,
                variable=var
            )
            cb.grid(row=row_cb, column=col_cb, sticky=tk.W, padx=3, pady=2)
            col_cb += 1
            if col_cb >= 3:
                col_cb = 0
                row_cb += 1

        # 5. Sheet name
        ttk.Label(self.root, text="User Sheet 名称 (--sheet-name-user)").grid(
            row=4, column=0, padx=padx, pady=pady, sticky=tk.W
        )
        self.entry_sheet = ttk.Entry(self.root, width=50)
        self.entry_sheet.grid(row=4, column=1, padx=padx, pady=pady)
        self.entry_sheet.insert(0, "人员")

        # 6. 用户名列
        ttk.Label(self.root, text="用户名列名称 (--col-user-name)").grid(
            row=5, column=0, padx=padx, pady=pady, sticky=tk.W
        )
        self.entry_col = ttk.Entry(self.root, width=50)
        self.entry_col.grid(row=5, column=1, padx=padx, pady=pady)
        self.entry_col.insert(0, "姓名")

        # 执行按钮
        ttk.Button(
            self.root,
            text="开始转换",
            command=self._run_convert
        ).grid(row=6, column=0, columnspan=3, pady=12)

        # ================== 状态栏 ==================
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=7, column=0, columnspan=3, sticky=tk.EW, padx=1, pady=1)
        # 让状态栏横向拉伸
        self.root.grid_columnconfigure(1, weight=1)

    def set_status(self, msg):
        """更新状态栏消息"""
        self.status_bar.config(text=msg)
        self.root.update_idletasks()  # 立即刷新界面

    def _select_xlsx(self):
        path = filedialog.askopenfilename(
            title="选择输入XLSX",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")]
        )
        if path:
            self.entry_xlsx.delete(0, tk.END)
            self.entry_xlsx.insert(0, path)

    def _select_user_db(self):
        path = filedialog.askdirectory(title="选择用户文件根目录")
        if path:
            self.entry_user_db.delete(0, tk.END)
            self.entry_user_db.insert(0, path)

    def _select_output(self):
        path = filedialog.askdirectory(title="选择输出截图根目录")
        if path:
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, path)

    def _get_selected_cert_types(self):
        """获取选中的证书类型，拼接成逗号分隔字符串"""
        selected = [ct for ct, var in self.cert_vars.items() if var.get()]
        # return ",".join(selected)
        return set(selected)

    def _run_convert(self):

        input_xlsx = self.entry_xlsx.get().strip()
        user_database = self.entry_user_db.get().strip()
        output_user_images = self.entry_output.get().strip()
        cert_type = self._get_selected_cert_types()
        sheet_name_user = self.entry_sheet.get().strip()
        col_user_name = self.entry_col.get().strip()

        if not input_xlsx:
            messagebox.showwarning("提示", "请选择输入 XLSX 文件")
            return
        if not user_database:
            messagebox.showwarning("提示", "请选择用户文件根目录")
            return
        if not cert_type:
            messagebox.showwarning("提示", "请至少选择一种证书类型")
            return

        try:

            def cb_user_info( status , user_name, path_name ):
                if status:
                    self.set_status(f"User: {user_name}, path :{path_name}")
                else:
                    self.set_status(f"User: {user_name}, path :{path_name}")
                pass

            user_list = do_export_user_info_to_snapshots(input_xlsx,
                                                     user_database,
                                                     output_user_images,
                                                     cert_type,
                                                         cb_user_info,
                                                     sheet_name_user,
                                                     col_user_name)
            self.set_status( "任务执行完成！")
        except Exception as e:
            self.logger.error(e)
            self.set_status( f"执行错误：{e}")


if __name__ == "__main__":
    init_with_conf(LogConfig())
    logger = get_log()
    logger.debug("user info to snapshot start")
    main_root = tk.Tk()
    app = ScreenshotConverterUI(main_root)
    main_root.mainloop()