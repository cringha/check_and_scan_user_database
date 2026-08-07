#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库扫描工具 - Tkinter GUI
功能：
1. 选择并缓存用户数据库根目录
2. 调用外部扫描函数
3. 生成Excel报告
"""

import os
import sys
import json
import logging
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable, Any


class AppConfig:
    """应用配置管理类 - 负责配置的持久化缓存"""

    def __init__(self, app_name: str = "DBScanner"):
        self.app_name = app_name
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_dir()
        self.data = self._load_config()

    def _get_config_dir(self) -> Path:
        """获取系统配置目录（跨平台）"""
        if sys.platform == "win32":
            base = os.environ.get("APPDATA", str(Path.home()))
            return Path(base) / self.app_name
        elif sys.platform == "darwin":
            return Path.home() / "Library" / "Application Support" / self.app_name
        else:
            return Path.home() / f".{self.app_name.lower()}"

    def _ensure_config_dir(self) -> None:
        """确保配置目录存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> dict:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logging.error(f"保存配置失败: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """设置配置项并自动保存"""
        self.data[key] = value
        self.save()


class AppLogger:
    """日志管理类"""

    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or Path.home() / ".dbscanner" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """配置日志记录器"""
        logger = logging.getLogger("DBScanner")
        logger.setLevel(logging.DEBUG)

        # 避免重复添加handler
        if logger.handlers:
            return logger

        # 文件handler
        log_file = self.log_dir / f"scanner_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)

        # 控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 格式化
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)


class StatusBar(ttk.Frame):
    """状态栏组件"""

    def __init__(self, master):
        super().__init__(master, relief=tk.SUNKEN, padding=(5, 2))
        self.status_var = tk.StringVar(value="就绪")
        self.label = ttk.Label(self, textvariable=self.status_var, anchor=tk.W)
        self.label.pack(fill=tk.X, side=tk.LEFT)
        self.pack(side=tk.BOTTOM, fill=tk.X)

    def set(self, text: str) -> None:
        """设置状态栏文本"""
        self.status_var.set(text)
        self.update_idletasks()

    def set_info(self, text: str) -> None:
        self.set(f"ℹ️ {text}")

    def set_success(self, text: str) -> None:
        self.set(f"✅ {text}")

    def set_error(self, text: str) -> None:
        self.set(f"❌ {text}")

    def set_warning(self, text: str) -> None:
        self.set(f"⚠️ {text}")


class DBScannerGUI:
    """主窗口类 - 数据库扫描工具GUI"""

    def __init__(self, root: tk.Tk, scan_function: Optional[Callable] = None):
        self.root = root
        self.scan_function = scan_function  # 外部注入的扫描函数

        # 初始化组件
        self.config = AppConfig()
        self.logger = AppLogger()
        self.status_bar = None

        # 状态变量
        self.root_dir_var = tk.StringVar()
        self.is_scanning = False

        # 初始化UI
        self._setup_window()
        self._create_widgets()
        self._load_last_directory()

        self.logger.info("应用程序启动完成")

    def _setup_window(self) -> None:
        """配置窗口基本属性"""
        self.root.title("数据库扫描工具")
        self.root.geometry("650x220")
        self.root.resizable(True, False)

        # 窗口居中
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 650) // 2
        y = (self.root.winfo_screenheight() - 220) // 2
        self.root.geometry(f"+{x}+{y}")

        # 样式
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TEntry", padding=3)

    def _create_widgets(self) -> None:
        """创建所有界面组件"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="15 15 15 5")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 第一行：目录选择
        dir_frame = ttk.LabelFrame(main_frame, text="数据库根目录", padding="10 8")
        dir_frame.pack(fill=tk.X, pady=(0, 12))

        self.root_dir_entry = ttk.Entry(
            dir_frame,
            textvariable=self.root_dir_var,
            state="readonly",
            font=("Microsoft YaHei UI", 9)
        )
        self.root_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        self.browse_btn = ttk.Button(
            dir_frame,
            text="选择目录",
            command=self._on_browse_click,
            width=12
        )
        self.browse_btn.pack(side=tk.RIGHT)

        # 第二行：操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        self.scan_btn = ttk.Button(
            btn_frame,
            text="🔍 扫描根目录",
            command=self._on_scan_click,
            width=18
        )
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.export_btn = ttk.Button(
            btn_frame,
            text="📊 生成Excel",
            command=self._on_export_click,
            width=18
        )
        self.export_btn.pack(side=tk.LEFT)

        # 第三行：日志输出区
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="5 5")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(
            log_frame,
            height=16,
            wrap=tk.WORD,
            font=("Consolas", 8),
            state=tk.DISABLED,
            background="#f8f8f8"
        )
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 状态栏
        self.status_bar = StatusBar(self.root)

        # 绑定日志重定向
        self._setup_log_redirect()

    def _setup_log_redirect(self) -> None:
        """将日志输出重定向到文本框"""
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def emit(self, record):
                msg = self.format(record) + "\n"
                self.text_widget.configure(state=tk.NORMAL)
                self.text_widget.insert(tk.END, msg)
                self.text_widget.see(tk.END)
                self.text_widget.configure(state=tk.DISABLED)

        text_handler = TextHandler(self.log_text)
        text_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s | %(message)s", datefmt="%H:%M:%S")
        text_handler.setFormatter(formatter)
        self.logger.logger.addHandler(text_handler)

    def _load_last_directory(self) -> None:
        """加载上次选择的目录"""
        last_dir = self.config.get("last_root_dir", "")
        if last_dir and Path(last_dir).exists():
            self.root_dir_var.set(last_dir)
            self.logger.info(f"已加载缓存目录: {last_dir}")
        else:
            self.root_dir_var.set("")
            self.logger.info("未找到缓存目录，请选择数据库根目录")

    def _on_browse_click(self) -> None:
        """选择目录按钮点击事件"""
        initial_dir = self.root_dir_var.get() or str(Path.home())

        selected_dir = filedialog.askdirectory(
            title="请选择数据库根目录",
            initialdir=initial_dir,
            mustexist=True
        )

        if selected_dir:
            self.root_dir_var.set(selected_dir)
            self.config.set("last_root_dir", selected_dir)
            self.status_bar.set_success(f"已选择目录: {Path(selected_dir).name}")
            self.logger.info(f"用户选择目录: {selected_dir}")
            self.logger.info(f"目录已缓存至: {self.config.config_file}")

    def _on_scan_click(self) -> None:
        """扫描按钮点击事件"""
        root_dir = self.root_dir_var.get()

        if not root_dir:
            messagebox.showwarning("提示", "请先选择数据库根目录")
            self.status_bar.set_warning("请先选择目录")
            return

        if not Path(root_dir).exists():
            messagebox.showerror("错误", "所选目录不存在，请重新选择")
            self.status_bar.set_error("目录不存在")
            return

        if self.is_scanning:
            messagebox.showinfo("提示", "扫描正在进行中，请稍候...")
            return

        self._set_buttons_state(tk.DISABLED)
        self.is_scanning = True
        self.status_bar.set_info("正在扫描...")
        self.logger.info(f"开始扫描目录: {root_dir}")

        try:
            if self.scan_function:
                # 调用外部注入的扫描函数
                result = self.scan_function(root_dir)
                self.logger.info(f"扫描完成，发现 {len(result) if result else 0} 个数据库对象")
                self.status_bar.set_success("扫描完成")
                messagebox.showinfo("成功", "扫描完成！")
            else:
                # 演示模式 - 实际使用时替换为真实扫描逻辑
                self._simulate_scan(root_dir)
        except Exception as e:
            self.logger.error(f"扫描失败: {str(e)}")
            self.status_bar.set_error(f"扫描失败: {str(e)}")
            messagebox.showerror("扫描错误", f"扫描过程中发生错误:\n{str(e)}")
        finally:
            self.is_scanning = False
            self._set_buttons_state(tk.NORMAL)

    def _simulate_scan(self, root_dir: str) -> None:
        """模拟扫描（演示用，实际由外部函数替代）"""
        import time
        self.root.update()
        time.sleep(1)  # 模拟扫描耗时
        self.logger.info(f"[模拟] 扫描目录: {root_dir}")
        self.logger.info("[模拟] 发现: 3 个数据库文件, 12 张表")
        self.status_bar.set_success("扫描完成（演示模式）")

    def _on_export_click(self) -> None:
        """生成Excel按钮点击事件"""
        root_dir = self.root_dir_var.get()

        if not root_dir:
            messagebox.showwarning("提示", "请先选择数据库根目录")
            self.status_bar.set_warning("请先选择目录")
            return

        if not Path(root_dir).exists():
            messagebox.showerror("错误", "所选目录不存在，请重新选择")
            self.status_bar.set_error("目录不存在")
            return

        # 默认文件名
        default_name = f"数据库扫描报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        initial_dir = self.config.get("last_export_dir", str(Path.home()))

        save_path = filedialog.asksaveasfilename(
            title="保存Excel文件",
            initialdir=initial_dir,
            initialfile=default_name,
            defaultextension=".xlsx",
            filetypes=[
                ("Excel 文件", "*.xlsx"),
                ("Excel 97-2003", "*.xls"),
                ("所有文件", "*.*")
            ]
        )

        if not save_path:
            self.logger.info("用户取消保存")
            return

        # 记住导出目录
        self.config.set("last_export_dir", str(Path(save_path).parent))

        self._set_buttons_state(tk.DISABLED)
        self.status_bar.set_info("正在生成Excel...")
        self.logger.info(f"开始生成Excel: {save_path}")

        try:
            self._generate_excel(root_dir, save_path)
            self.status_bar.set_success(f"Excel已保存: {Path(save_path).name}")
            self.logger.info(f"Excel生成成功: {save_path}")
            messagebox.showinfo("成功", f"Excel文件已保存至:\n{save_path}")
        except Exception as e:
            self.logger.error(f"生成Excel失败: {str(e)}")
            self.status_bar.set_error(f"生成失败: {str(e)}")
            messagebox.showerror("导出错误", f"生成Excel时发生错误:\n{str(e)}")
        finally:
            self._set_buttons_state(tk.NORMAL)

    def _generate_excel(self, root_dir: str, save_path: str) -> None:
        """
        生成Excel文件
        实际项目中替换为真实的Excel生成逻辑
        """
        try:
            import pandas as pd
        except ImportError:
            raise RuntimeError("需要安装pandas和openpyxl: pip install pandas openpyxl")

        # 示例数据 - 实际使用时替换为扫描结果
        data = {
            "数据库名": ["示例数据库1", "示例数据库2", "示例数据库3"],
            "表名": ["users", "orders", "products"],
            "记录数": [1500, 3200, 890],
            "大小(MB)": [12.5, 45.2, 8.3],
            "最后修改": ["2026-08-01", "2026-08-05", "2026-07-28"],
            "路径": [
                str(Path(root_dir) / "db1.db"),
                str(Path(root_dir) / "db2.db"),
                str(Path(root_dir) / "db3.db")
            ]
        }

        df = pd.DataFrame(data)

        # 写入Excel并格式化
        with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="数据库清单", index=False)

            # 自动调整列宽
            worksheet = writer.sheets["数据库清单"]
            for idx, col in enumerate(df.columns):
                max_len = max(
                    df[col].astype(str).map(len).max(),
                    len(str(col))
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_len, 50)

    def _set_buttons_state(self, state: str) -> None:
        """统一设置按钮状态"""
        self.browse_btn.configure(state=state)
        self.scan_btn.configure(state=state)
        self.export_btn.configure(state=state)


def main():
    """程序入口"""
    root = tk.Tk()

    # ============================================
    # 在这里注入你的扫描函数
    # def my_scan_function(root_dir):
    #     # 你的扫描逻辑，返回扫描结果列表
    #     return scan_results
    #
    # app = DBScannerGUI(root, scan_function=my_scan_function)
    # ============================================

    app = DBScannerGUI(root)  # 使用演示模式
    root.mainloop()


if __name__ == "__main__":
    main()
