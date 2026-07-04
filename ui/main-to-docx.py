import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import argparse
import os

def main():
    root = tk.Tk()
    root.title("身份证/证书/合同截图转DOCX工具")
    root.geometry("850x780")

    # ========== 变量定义 ==========
    var_input_xlsx = tk.StringVar()

    # 截图类型多选框变量
    var_id_card = tk.BooleanVar(value=True)
    var_graduation = tk.BooleanVar(value=True)
    var_qualification = tk.BooleanVar(value=True)
    var_contract = tk.BooleanVar(value=True)
    var_social_security = tk.BooleanVar(value=True)

    var_user_snapshot_root = tk.StringVar()
    var_user_ss_snapshot_root = tk.StringVar()
    var_user_resume_type = tk.StringVar(value="")
    var_sheet_user = tk.StringVar(value="Users")
    var_sheet_project = tk.StringVar(value="Projects")
    var_sheet_duty = tk.StringVar(value="Duty")
    var_col_name = tk.StringVar(value="Name")
    var_col_work_exp = tk.StringVar(value="工作年限")
    var_col_duty = tk.StringVar(value="职责")
    var_col_duty_desc = tk.StringVar(value="职责内容")
    var_template = tk.StringVar(value="./data/user_certs_template.docx")
    var_output = tk.StringVar(value="./user-ss-snapshot.docx")

    # ========== 界面布局 ==========
    frame = ttk.Frame(root, padding=12)
    frame.pack(fill=tk.BOTH, expand=True)

    row = 0

    # 1. 输入 XLSX
    ttk.Label(frame, text="输入 XLSX 文件:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_input_xlsx, width=62).grid(row=row, column=1, padx=5)
    ttk.Button(frame, text="选择", command=lambda: select_file(var_input_xlsx, [("Excel 文件", "*.xlsx")])
              ).grid(row=row, column=2)
    row += 1

    # 2. 用户截图类型（多选框）
    ttk.Label(frame, text="用户截图类型:").grid(row=row, column=0, sticky=tk.NW, pady=6)
    type_frame = ttk.Frame(frame)
    type_frame.grid(row=row, column=1, sticky=tk.W, padx=5)

    ttk.Checkbutton(type_frame, text="身份证", variable=var_id_card).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(type_frame, text="毕业证", variable=var_graduation).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(type_frame, text="资质证书", variable=var_qualification).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(type_frame, text="合同", variable=var_contract).pack(side=tk.LEFT, padx=5)
    ttk.Checkbutton(type_frame, text="社保", variable=var_social_security).pack(side=tk.LEFT, padx=5)
    row += 1

    # 3. 用户截图根目录
    ttk.Label(frame, text="用户截图根目录:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_user_snapshot_root, width=62).grid(row=row, column=1, padx=5)
    ttk.Button(frame, text="选择", command=lambda: select_dir(var_user_snapshot_root)
              ).grid(row=row, column=2)
    row += 1

    # 4. 社保截图根目录
    ttk.Label(frame, text="社保截图根目录:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_user_ss_snapshot_root, width=62).grid(row=row, column=1, padx=5)
    ttk.Button(frame, text="选择", command=lambda: select_dir(var_user_ss_snapshot_root)
              ).grid(row=row, column=2)
    row += 1

    # 5. 用户简历版本
    ttk.Label(frame, text="用户简历版本:").grid(row=row, column=0, sticky=tk.W, pady=4)
    resume_combo = ttk.Combobox(frame, textvariable=var_user_resume_type, width=59, state="readonly")
    resume_combo["values"] = ["", "v1"]
    resume_combo.grid(row=row, column=1, padx=5)
    row += 1

    ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
    row += 1

    # Sheet 名称
    ttk.Label(frame, text="User 表名:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_sheet_user, width=32).grid(row=row, column=1, sticky=tk.W, padx=5)
    row += 1

    ttk.Label(frame, text="Project 表名:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_sheet_project, width=32).grid(row=row, column=1, sticky=tk.W, padx=5)
    row += 1

    ttk.Label(frame, text="Duty 表名:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_sheet_duty, width=32).grid(row=row, column=1, sticky=tk.W, padx=5)
    row += 1

    ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
    row += 1

    # 列名配置
    ttk.Label(frame, text="用户名称列:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_col_name, width=32).grid(row=row, column=1, sticky=tk.W, padx=5)
    row += 1

    ttk.Label(frame, text="工作年限列:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_col_work_exp, width=32).grid(row=row, column=1, sticky=tk.W, padx=5)
    row += 1

    ttk.Label(frame, text="职责列:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_col_duty, width=32).grid(row=row, column=1, sticky=tk.W, padx=5)
    row += 1

    ttk.Label(frame, text="职责内容列:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_col_duty_desc, width=32).grid(row=row, column=1, sticky=tk.W, padx=5)
    row += 1

    ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=10)
    row += 1

    # 模板与输出
    ttk.Label(frame, text="DOCX 模板文件:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_template, width=62).grid(row=row, column=1, padx=5)
    ttk.Button(frame, text="选择", command=lambda: select_file(var_template, [("Word 模板", "*.docx")])
              ).grid(row=row, column=2)
    row += 1

    ttk.Label(frame, text="输出 DOCX 文件:").grid(row=row, column=0, sticky=tk.W, pady=4)
    ttk.Entry(frame, textvariable=var_output, width=62).grid(row=row, column=1, padx=5)
    ttk.Button(frame, text="选择", command=lambda: save_file(var_output, [("Word 文档", "*.docx")])
              ).grid(row=row, column=2)
    row += 1

    ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=12)
    row += 1

    # 执行按钮
    ttk.Button(frame, text="生成并导出 DOCX", command=lambda: start_generate(
        var_input_xlsx.get(),
        var_id_card.get(),
        var_graduation.get(),
        var_qualification.get(),
        var_contract.get(),
        var_social_security.get(),
        var_user_snapshot_root.get(),
        var_user_ss_snapshot_root.get(),
        var_user_resume_type.get(),
        var_sheet_user.get(),
        var_sheet_project.get(),
        var_sheet_duty.get(),
        var_col_name.get(),
        var_col_work_exp.get(),
        var_col_duty.get(),
        var_col_duty_desc.get(),
        var_template.get(),
        var_output.get()
    ), width=22).grid(row=row, column=1, pady=10)

    root.mainloop()

def select_file(var, types):
    path = filedialog.askopenfilename(filetypes=types)
    if path:
        var.set(path)

def select_dir(var):
    path = filedialog.askdirectory()
    if path:
        var.set(path)

def save_file(var, types):
    path = filedialog.asksaveasfilename(filetypes=types, defaultextension=".docx")
    if path:
        var.set(path)

def start_generate(input_xlsx,
                   id_card, graduation, qualification, contract, social_security,
                   snap_root, ss_root, resume_type,
                   sheet_user, sheet_proj, sheet_duty,
                   col_name, col_work, col_duty, col_duty_desc,
                   template, output):

    # 基础校验
    if not input_xlsx:
        messagebox.showerror("错误", "请选择输入 XLSX 文件")
        return
    if not os.path.isfile(input_xlsx):
        messagebox.showerror("错误", "XLSX 文件不存在")
        return
    if not template or not os.path.isfile(template):
        messagebox.showerror("错误", "请选择有效的 DOCX 模板")
        return

    # 拼接选中的截图类型（逗号分隔，可直接用于你原来的逻辑）
    selected_types = []
    if id_card:
        selected_types.append("身份证")
    if graduation:
        selected_types.append("毕业证")
    if qualification:
        selected_types.append("资质证书")
    if contract:
        selected_types.append("合同")
    if social_security:
        selected_types.append("社保")

    user_snapshot_types = ",".join(selected_types)

    # 构建 argparse 参数（和你命令行完全一致）
    args = argparse.Namespace(
        input_xlsx=input_xlsx,
        user_snapshot_types=user_snapshot_types,
        user_snapshot_root=snap_root,
        user_ss_snapshot_root=ss_root,
        user_resume_type=resume_type,
        sheet_name_user=sheet_user,
        sheet_name_project=sheet_proj,
        sheet_name_duty=sheet_duty,
        col_user_name=col_name,
        col_work_exp=col_work,
        col_duty=col_duty,
        col_duty_desc=col_duty_desc,
        docx_template_file=template,
        output_docx_file=output
    )

    try:
        # ====================== 你的核心处理逻辑 ======================
        # from your_module import generate_docx
        # generate_docx(args)
        # ============================================================

        messagebox.showinfo("完成",
                           f"已生成 DOCX：\n{output}\n\n选中的截图类型：\n{user_snapshot_types}")
    except Exception as e:
        messagebox.showerror("执行失败", str(e))

if __name__ == "__main__":
    main()