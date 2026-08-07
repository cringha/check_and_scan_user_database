import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import sys
from datetime import datetime
from argparse import Namespace


class DBScannerGUI:
    def __init__(self, master, scan_function=None):
        self.master = master
        self.master.title("数据库目录扫描工具")
        self.master.geometry("720x580")
        self.master.resizable(True, True)

        # 外部传入扫描函数
        self.scan_func = scan_function
        self.args = Namespace(root_dir="", scan_result=None)
        self.is_running = False

        # 配置缓存路径
        self.config_dir = self._get_config_path()
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.load_config()

        self.create_widgets()
        self.set_root_dir_display(self.args.root_dir)

    def _get_config_path(self):
        if sys.platform.startswith("win"):
            cfg = os.path.join(os.environ["APPDATA"], "DBScanner")
        else:
            cfg = os.path.join(os.path.expanduser("~"), ".dbscanner")
        os.makedirs(cfg, exist_ok=True)
        return cfg

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    cfg_data = json.load(f)
                self.args.root_dir = cfg_data.get("root_dir", "")
            except Exception:
                self.args.root_dir = ""

    def save_config(self):
        cfg_data = {"root_dir": self.args.root_dir}
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(cfg_data, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        # 根目录显示区域
        frame_top = ttk.Frame(self.master, padding=8)
        frame_top.pack(fill=tk.X)

        ttk.Label(frame_top, text="数据库根目录：").pack(side=tk.LEFT)
        self.var_root_path = tk.StringVar()
        entry_root = ttk.Entry(frame_top, textvariable=self.var_root_path, state="readonly")
        entry_root.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 8))

        # 按钮行
        frame_btn = ttk.Frame(self.master, padding=8)
        frame_btn.pack(fill=tk.X)

        self.btn_select = ttk.Button(frame_btn, text="1.选择根目录", command=self.on_select_dir)
        self.btn_select.pack(side=tk.LEFT, padx=4)

        self.btn_scan = ttk.Button(frame_btn, text="2.扫描根目录", command=self.on_scan)
        self.btn_scan.pack(side=tk.LEFT, padx=4)

        self.btn_export = ttk.Button(frame_btn, text="3.生成Excel", command=self.on_export_excel)
        self.btn_export.pack(side=tk.LEFT, padx=4)

        # 日志区域，height=20，至少20行
        frame_log = ttk.Frame(self.master, padding=8)
        frame_log.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame_log, text="运行日志：").pack(anchor=tk.W)
        self.log_text = tk.Text(frame_log, height=20, wrap="word")
        scroll_log = ttk.Scrollbar(frame_log, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll_log.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_log.pack(side=tk.RIGHT, fill=tk.Y)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.master, textvariable=self.status_var, anchor=tk.W, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X)

    def set_root_dir_display(self, path):
        self.var_root_path.set(path)

    def log(self, msg):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{now}] {msg}\n"
        self.log_text.insert(tk.END, line)
        self.log_text.see(tk.END)
        self.master.update_idletasks()

    def set_status(self, text):
        self.status_var.set(text)

    def set_buttons_state(self, enable: bool):
        state = tk.NORMAL if enable else tk.DISABLED
        self.btn_select.config(state=state)
        self.btn_scan.config(state=state)
        self.btn_export.config(state=state)

    def on_select_dir(self):
        selected = filedialog.askdirectory(title="选择用户数据库根目录", initialdir=self.args.root_dir or None)
        if selected:
            self.args.root_dir = selected
            self.set_root_dir_display(selected)
            self.save_config()
            self.log(f"已选择根目录：{selected}")
        else:
            self.log("取消选择目录")

    def on_scan(self):
        if self.is_running:
            return
        if not self.args.root_dir or not os.path.isdir(self.args.root_dir):
            messagebox.showwarning("提示", "请先选择有效的数据库根目录")
            return

        self.is_running = True
        self.set_buttons_state(False)
        self.set_status("正在扫描...")
        self.log("开始扫描根目录...")
        try:
            if self.scan_func is None:
                self.log("警告：外部扫描函数未传入！")
                self.args.scan_result = []
            else:
                self.args.scan_result = self.scan_func(self.args.root_dir)
            self.log(f"扫描完成，获取 {len(self.args.scan_result)} 条记录")
            self.set_status("扫描完成")
        except Exception as e:
            self.log(f"扫描异常：{str(e)}")
            self.set_status("扫描失败")
            messagebox.showerror("扫描错误", str(e))
        finally:
            self.is_running = False
            self.set_buttons_state(True)

    def on_export_excel(self):
        if self.is_running:
            return
        if not self.args.root_dir:
            messagebox.showwarning("提示", "请先选择数据库根目录")
            return
        if self.args.scan_result is None:
            messagebox.showwarning("提示", "请先执行扫描操作")
            return

        save_path = filedialog.asksaveasfilename(
            title="保存Excel文件",
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        if not save_path:
            self.log("取消保存Excel")
            return

        self.set_buttons_state(False)
        self.set_status("正在生成Excel...")
        self.log(f"开始导出Excel：{save_path}")
        try:
            import pandas as pd
            df = pd.DataFrame(self.args.scan_result)
            df.to_excel(save_path, index=False, engine="openpyxl")
            self.log(f"Excel导出成功 -> {save_path}")
            self.set_status("导出成功")
            messagebox.showinfo("完成", f"文件已保存：{save_path}")
        except ImportError:
            self.log("错误：缺少依赖，请执行 pip install pandas openpyxl")
            messagebox.showerror("依赖缺失", "需要安装 pandas openpyxl")
        except Exception as e:
            self.log(f"导出Excel异常：{str(e)}")
            self.set_status("导出失败")
            messagebox.showerror("导出错误", str(e))
        finally:
            self.set_buttons_state(True)


# ========== 示例：你的外部扫描函数（放到其他py文件里） ==========
# from other_module import your_scan_func
def demo_scan(root_dir):
    """模拟外部扫描函数，实际使用时替换为你其他文件的函数"""
    return [{"path": root_dir, "info": "demo数据"}]


def main():
    root = tk.Tk()
    app = DBScannerGUI(root, scan_function=demo_scan)
    root.mainloop()


if __name__ == "__main__":
    main()