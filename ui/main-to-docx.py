import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import argparse
import os
import json

from entries.user_cert_snapshots_to_docx import generate_snapshot_docx
from uitls.log import init_with_conf, get_log, LogConfig

CONFIG_FILE = "gui_config.json"


class ConfigMixin:
    """配置保存/加载"""
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_config(self, config):
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass


class ScreenshotToDocxApp(tk.Tk, ConfigMixin):
    def __init__(self):
        super().__init__()
        self.title("身份证/证书/合同截图转DOCX工具")
        self.geometry("750x600")

        self.cfg = self.load_config()
        self.create_variables()
        self.create_widgets()
        self.logger = get_log()

    def create_variables(self):
        self.var_input_xlsx = tk.StringVar(value=self.cfg.get("input_xlsx", ""))

        self.var_id_card = tk.BooleanVar(value=self.cfg.get("id_card", True))
        self.var_graduation = tk.BooleanVar(value=self.cfg.get("graduation", True))
        self.var_qualification = tk.BooleanVar(value=self.cfg.get("qualification", True))
        self.var_contract = tk.BooleanVar(value=self.cfg.get("contract", True))
        self.var_social_security = tk.BooleanVar(value=self.cfg.get("social_security", True))

        self.var_user_snapshot_root = tk.StringVar(value=self.cfg.get("user_snapshot_root", ""))
        self.var_user_ss_snapshot_root = tk.StringVar(value=self.cfg.get("user_ss_snapshot_root", ""))
        self.var_user_resume_type = tk.StringVar(value=self.cfg.get("user_resume_type", ""))

        self.var_sheet_user = tk.StringVar(value=self.cfg.get("sheet_name_user", "Users"))
        self.var_sheet_project = tk.StringVar(value=self.cfg.get("sheet_name_project", "Projects"))
        self.var_sheet_duty = tk.StringVar(value=self.cfg.get("sheet_name_duty", "Duty"))

        self.var_col_name = tk.StringVar(value=self.cfg.get("col_user_name", "Name"))
        self.var_col_work_exp = tk.StringVar(value=self.cfg.get("col_work_exp", "工作年限"))
        self.var_col_duty = tk.StringVar(value=self.cfg.get("col_duty", "职责"))
        self.var_col_duty_desc = tk.StringVar(value=self.cfg.get("col_duty_desc", "职责内容"))

        self.var_template = tk.StringVar(value=self.cfg.get("docx_template_file", "./data/user_certs_template.docx"))
        self.var_output = tk.StringVar(value=self.cfg.get("output_docx_file", "./user-ss-snapshot.docx"))

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.frame = main_frame

        row = 0
        row = self.add_xlsx_input_row(row)
        row = self.add_snapshot_types_row(row)
        row = self.add_snapshot_dir_row(row)
        row = self.add_ss_snapshot_dir_row(row)
        row = self.add_resume_type_row(row)

        row = self.add_separator(row)
        row = self.add_sheet_rows(row)
        row = self.add_separator(row)
        row = self.add_column_rows(row)
        row = self.add_separator(row)
        row = self.add_template_output_rows(row)
        row = self.add_separator(row)
        row = self.add_action_button(row)

        # ========== 状态栏 ==========
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar = status_bar

    def set_status(self, msg):
        """设置普通状态栏消息"""
        self.status_var.set(msg)
        self.status_bar.config(foreground="black")

    def set_status_error(self, msg):
        """设置错误消息（红色）"""
        self.status_var.set(msg)
        self.status_bar.config(foreground="red")

    def add_separator(self, row):
        ttk.Separator(self.frame, orient=tk.HORIZONTAL) \
            .grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
        return row + 1

    def add_xlsx_input_row(self, row):
        ttk.Label(self.frame, text="输入 XLSX 文件:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_input_xlsx, width=62) \
            .grid(row=row, column=1, padx=5)
        ttk.Button(self.frame, text="选择",
                   command=lambda: self.select_file(self.var_input_xlsx, [("Excel 文件", "*.xlsx")])) \
            .grid(row=row, column=2)
        return row + 1

    def add_snapshot_types_row(self, row):
        ttk.Label(self.frame, text="用户截图类型:").grid(row=row, column=0, sticky=tk.NW, pady=6)
        f = ttk.Frame(self.frame)
        f.grid(row=row, column=1, sticky=tk.W, padx=5)

        ttk.Checkbutton(f, text="身份证", variable=self.var_id_card).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(f, text="毕业证", variable=self.var_graduation).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(f, text="资质证书", variable=self.var_qualification).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(f, text="合同", variable=self.var_contract).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(f, text="社保", variable=self.var_social_security).pack(side=tk.LEFT, padx=5)
        return row + 1

    def add_snapshot_dir_row(self, row):
        ttk.Label(self.frame, text="用户截图根目录:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_user_snapshot_root, width=62) \
            .grid(row=row, column=1, padx=5)
        ttk.Button(self.frame, text="选择",
                   command=lambda: self.select_dir(self.var_user_snapshot_root)) \
            .grid(row=row, column=2)
        return row + 1

    def add_ss_snapshot_dir_row(self, row):
        ttk.Label(self.frame, text="社保截图根目录:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_user_ss_snapshot_root, width=62) \
            .grid(row=row, column=1, padx=5)
        ttk.Button(self.frame, text="选择",
                   command=lambda: self.select_dir(self.var_user_ss_snapshot_root)) \
            .grid(row=row, column=2)
        return row + 1

    def add_resume_type_row(self, row):
        ttk.Label(self.frame, text="用户简历版本:").grid(row=row, column=0, sticky=tk.W, pady=4)
        c = ttk.Combobox(self.frame, textvariable=self.var_user_resume_type, width=59, state="readonly")
        c["values"] = ["", "v1"]
        c.grid(row=row, column=1, padx=5)
        return row + 1

    def add_sheet_rows(self, row):
        ttk.Label(self.frame, text="User 表名:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_sheet_user, width=32) \
            .grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1

        ttk.Label(self.frame, text="Project 表名:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_sheet_project, width=32) \
            .grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1

        ttk.Label(self.frame, text="Duty 表名:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_sheet_duty, width=32) \
            .grid(row=row, column=1, sticky=tk.W, padx=5)
        return row + 1

    def add_column_rows(self, row):
        ttk.Label(self.frame, text="用户名称列:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_col_name, width=32) \
            .grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1

        ttk.Label(self.frame, text="工作年限列:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_col_work_exp, width=32) \
            .grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1

        ttk.Label(self.frame, text="职责列:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_col_duty, width=32) \
            .grid(row=row, column=1, sticky=tk.W, padx=5)
        row += 1

        ttk.Label(self.frame, text="职责内容列:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_col_duty_desc, width=32) \
            .grid(row=row, column=1, sticky=tk.W, padx=5)
        return row + 1

    def add_template_output_rows(self, row):
        ttk.Label(self.frame, text="DOCX 模板文件:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_template, width=62) \
            .grid(row=row, column=1, padx=5)
        ttk.Button(self.frame, text="选择",
                   command=lambda: self.select_file(self.var_template, [("Word 模板", "*.docx")])) \
            .grid(row=row, column=2)
        row += 1

        ttk.Label(self.frame, text="输出 DOCX 文件:").grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(self.frame, textvariable=self.var_output, width=62) \
            .grid(row=row, column=1, padx=5)
        ttk.Button(self.frame, text="选择",
                   command=lambda: self.save_file(self.var_output, [("Word 文档", "*.docx")])) \
            .grid(row=row, column=2)
        return row + 1

    def add_action_button(self, row):
        ttk.Button(self.frame, text="生成并导出 DOCX", width=22,
                   command=self.on_start_generate) \
            .grid(row=row, column=1, pady=10)
        return row + 1

    def select_file(self, var, types):
        path = filedialog.askopenfilename(filetypes=types)
        if path:
            var.set(path)

    def select_dir(self, var):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    def save_file(self, var, types):
        path = filedialog.asksaveasfilename(filetypes=types, defaultextension=".docx")
        if path:
            var.set(path)

    def on_start_generate(self):
        self.set_status("正在校验参数...")

        input_xlsx = self.var_input_xlsx.get().strip()
        if not input_xlsx or not os.path.isfile(input_xlsx):
            self.set_status_error("错误：请选择有效的 XLSX 文件")
            messagebox.showerror("错误", "请选择有效的 XLSX 文件")
            return

        template = self.var_template.get().strip()
        if not template or not os.path.isfile(template):
            self.set_status_error("错误：请选择有效的 DOCX 模板")
            messagebox.showerror("错误", "请选择有效的 DOCX 模板")
            return

        selected = []
        if self.var_id_card.get():
            selected.append("身份证")
        if self.var_graduation.get():
            selected.append("毕业证")
        if self.var_qualification.get():
            selected.append("资质证书")
        if self.var_contract.get():
            selected.append("合同")
        if self.var_social_security.get():
            selected.append("社保")
        user_snapshot_types = ",".join(selected)

        self.set_status("正在保存配置...")
        self.save_current_config()

        args = argparse.Namespace(
            input_xlsx=input_xlsx,
            user_snapshot_types=user_snapshot_types,
            user_snapshot_root=self.var_user_snapshot_root.get(),
            user_ss_snapshot_root=self.var_user_ss_snapshot_root.get(),
            user_resume_type=self.var_user_resume_type.get(),
            sheet_name_user=self.var_sheet_user.get(),
            sheet_name_project=self.var_sheet_project.get(),
            sheet_name_duty=self.var_sheet_duty.get(),
            col_user_name=self.var_col_name.get(),
            col_work_exp=self.var_col_work_exp.get(),
            col_duty=self.var_col_duty.get(),
            col_duty_desc=self.var_col_duty_desc.get(),
            docx_template_file=template,
            output_docx_file=self.var_output.get()
        )

        try:
            self.set_status("正在生成 DOCX，请稍候...")

            # ========== 你的业务逻辑 ==========
            def callback_info(status, msg):
                self.set_status(f"{status}: {msg}")

            result = generate_snapshot_docx(args, callback_info)
            if result:
                msg = f"生成完成：{args.output_docx_file}"
                self.set_status(msg)
            # messagebox.showinfo("完成", msg)

        except Exception as e:
            err = f"执行失败：{str(e)}"
            self.set_status_error(err)
            self.logger.exception(e);
            # messagebox.showerror("执行失败", str(e))

    def save_current_config(self):
        config = {
            "input_xlsx": self.var_input_xlsx.get(),
            "id_card": self.var_id_card.get(),
            "graduation": self.var_graduation.get(),
            "qualification": self.var_qualification.get(),
            "contract": self.var_contract.get(),
            "social_security": self.var_social_security.get(),
            "user_snapshot_root": self.var_user_snapshot_root.get(),
            "user_ss_snapshot_root": self.var_user_ss_snapshot_root.get(),
            "user_resume_type": self.var_user_resume_type.get(),
            "sheet_name_user": self.var_sheet_user.get(),
            "sheet_name_project": self.var_sheet_project.get(),
            "sheet_name_duty": self.var_sheet_duty.get(),
            "col_user_name": self.var_col_name.get(),
            "col_work_exp": self.var_col_work_exp.get(),
            "col_duty": self.var_col_duty.get(),
            "col_duty_desc": self.var_col_duty_desc.get(),
            "docx_template_file": self.var_template.get(),
            "output_docx_file": self.var_output.get()
        }
        self.save_config(config)


if __name__ == "__main__":
    init_with_conf(LogConfig())
    logger = get_log()
    logger.debug("Convert user info to docx")
    app = ScreenshotToDocxApp()
    app.mainloop()