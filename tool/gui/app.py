import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional

# 将上级目录加入 sys.path 以便模块导入
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from core.patcher import AntigravityPatcher
from core.customizer import Customizer
from core.version import APP_NAME, APP_VERSION, APP_AUTHOR, WINDOW_TITLE, FOOTER_TEXT

class AntigravityGuiApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry("520x430")
        self.root.minsize(500, 420)
        self.root.configure(bg="#f8fafc")

        # 1. 设置原生窗口图标 (去除 Tkinter 默认蓝色羽毛)
        self._setup_window_icon()

        # 2. 定位项目资产根目录 (支持独立打包环境)
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(parent_dir)

        self.i18n_source = os.path.join(self.base_dir, "i18n.js")
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.patcher = AntigravityPatcher()
        self.custom_icon_path = None
        self.is_advanced_open = False

        self._init_styles()
        self._create_widgets()
        self._refresh_status()

    def _setup_window_icon(self):
        # 寻找 app.ico 优先设置
        candidates = [
            os.path.join(parent_dir, "app.ico"),
            os.path.join(getattr(sys, '_MEIPASS', ''), "app.ico") if hasattr(sys, '_MEIPASS') else "",
            os.path.join(os.path.dirname(sys.executable), "app.ico") if getattr(sys, 'frozen', False) else ""
        ]
        for p in candidates:
            if p and os.path.exists(p):
                try:
                    self.root.iconbitmap(p)
                    break
                except Exception:
                    pass

    def _init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure("TCombobox", fieldbackground="#ffffff", background="#f1f5f9", padding=4)
        self.style.map("TCombobox", fieldbackground=[('readonly', '#ffffff')])

    def _create_widgets(self):
        # 主外层边距容器
        self.main_box = tk.Frame(self.root, bg="#f8fafc", padx=20, pady=16)
        self.main_box.pack(fill="both", expand=True)

        # -------------------------------------------------------------
        # 1. 顶部 Header 区 (极简、轻量、高辨识度)
        # -------------------------------------------------------------
        header_bar = tk.Frame(self.main_box, bg="#f8fafc")
        header_bar.pack(fill="x", pady=(0, 14))

        # 标题与 Logo
        title_left = tk.Frame(header_bar, bg="#f8fafc")
        title_left.pack(side="left")

        lbl_logo = tk.Label(title_left, text="⚡", font=("Segoe UI Emoji", 14), bg="#f8fafc", fg="#2563eb")
        lbl_logo.pack(side="left", padx=(0, 6))

        lbl_app_name = tk.Label(title_left, text=APP_NAME, font=("Microsoft YaHei UI", 13, "bold"), bg="#f8fafc", fg="#0f172a")
        lbl_app_name.pack(side="left")

        # 右侧作者与版本精致胶囊
        badge_box = tk.Frame(header_bar, bg="#e2e8f0", padx=1, pady=1)
        badge_box.pack(side="right")
        
        badge_inner = tk.Frame(badge_box, bg="#f8fafc", padx=8, pady=3)
        badge_inner.pack()

        lbl_badge = tk.Label(
            badge_inner,
            text=f"{APP_VERSION} · {APP_AUTHOR}",
            font=("Microsoft YaHei UI", 8, "bold"),
            bg="#f8fafc", fg="#475569"
        )
        lbl_badge.pack()

        # -------------------------------------------------------------
        # 2. 核心状态卡片 (Status Hero Card)
        # -------------------------------------------------------------
        self.status_card = tk.Frame(self.main_box, bg="#ffffff", padx=16, pady=14, highlightbackground="#e2e8f0", highlightthickness=1)
        self.status_card.pack(fill="x", pady=(0, 14))

        # 状态主行
        row_status = tk.Frame(self.status_card, bg="#ffffff")
        row_status.pack(fill="x")

        self.lbl_status_dot = tk.Label(row_status, text="●", font=("Microsoft YaHei UI", 13), bg="#ffffff", fg="#94a3b8")
        self.lbl_status_dot.pack(side="left")

        self.lbl_status_title = tk.Label(row_status, text="正在侦测客户端状态...", font=("Microsoft YaHei UI", 10, "bold"), bg="#ffffff", fg="#1e293b")
        self.lbl_status_title.pack(side="left", padx=(6, 0))

        self.lbl_version_tag = tk.Label(row_status, text="", font=("Microsoft YaHei UI", 8), bg="#f1f5f9", fg="#64748b", padx=6, pady=1)
        self.lbl_version_tag.pack(side="right")

        # 状态副行 (极简路径与修改入口)
        row_path = tk.Frame(self.status_card, bg="#ffffff")
        row_path.pack(fill="x", pady=(8, 0))

        self.var_path = tk.StringVar(value=self.patcher.install_dir or "")
        self.lbl_path_display = tk.Label(
            row_path,
            text="路径: 自动侦测中...",
            font=("Consolas", 8),
            bg="#ffffff", fg="#64748b",
            anchor="w"
        )
        self.lbl_path_display.pack(side="left", fill="x", expand=True)

        btn_edit_path = tk.Button(
            row_path, text="更改目录", font=("Microsoft YaHei UI", 8),
            bg="#ffffff", fg="#2563eb", activebackground="#f1f5f9", activeforeground="#1d4ed8",
            relief="flat", cursor="hand2", bd=0, padx=4,
            command=self._browse_path
        )
        btn_edit_path.pack(side="right")

        # -------------------------------------------------------------
        # 3. 黄金操作区 (Hero CTA & Sub Actions)
        # -------------------------------------------------------------
        # 一键安装超大绿色主按钮
        self.btn_install = tk.Button(
            self.main_box,
            text="一键极速安装 / 更新汉化",
            font=("Microsoft YaHei UI", 11, "bold"),
            bg="#16a34a", fg="#ffffff",
            activebackground="#15803d", activeforeground="#ffffff",
            relief="flat", cursor="hand2", pady=10, bd=0,
            command=self._do_install
        )
        self.btn_install.pack(fill="x", pady=(0, 10))

        # 次级操作并排按钮条
        sub_action_box = tk.Frame(self.main_box, bg="#f8fafc")
        sub_action_box.pack(fill="x", pady=(0, 12))

        self.btn_reload = tk.Button(
            sub_action_box,
            text="🔄 免重启热重载",
            font=("Microsoft YaHei UI", 9),
            bg="#ffffff", fg="#2563eb",
            activebackground="#eff6ff", activeforeground="#1d4ed8",
            relief="solid", bd=1, cursor="hand2",
            padx=12, pady=7,
            command=self._do_reload
        )
        self.btn_reload.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_restore = tk.Button(
            sub_action_box,
            text="↩ 一键还原纯英文",
            font=("Microsoft YaHei UI", 9),
            bg="#ffffff", fg="#64748b",
            activebackground="#f1f5f9", activeforeground="#0f172a",
            relief="solid", bd=1, cursor="hand2",
            padx=12, pady=7,
            command=self._do_restore
        )
        self.btn_restore.pack(side="right", fill="x", expand=True, padx=(6, 0))

        # -------------------------------------------------------------
        # 4. 轻量通知状态条 (Toast / Notification)
        # -------------------------------------------------------------
        self.toast_box = tk.Frame(self.main_box, bg="#ffffff", padx=12, pady=7, highlightbackground="#e2e8f0", highlightthickness=1)
        self.toast_box.pack(fill="x", pady=(0, 10))

        self.lbl_toast = tk.Label(
            self.toast_box,
            text="✓ 就绪 · 支持秒级精准汉化与官方版本自动守护",
            font=("Microsoft YaHei UI", 8),
            bg="#ffffff", fg="#16a34a",
            anchor="w"
        )
        self.lbl_toast.pack(side="left", fill="x", expand=True)

        self.btn_toggle_log = tk.Button(
            self.toast_box, text="高级设置与日志 ▸", font=("Microsoft YaHei UI", 8),
            bg="#ffffff", fg="#64748b", activebackground="#ffffff", activeforeground="#0f172a",
            relief="flat", cursor="hand2", bd=0, padx=4,
            command=self._toggle_advanced
        )
        self.btn_toggle_log.pack(side="right")

        # -------------------------------------------------------------
        # 5. 高级定制与日志折叠抽屉 (默认收起)
        # -------------------------------------------------------------
        self.drawer_container = tk.Frame(self.main_box, bg="#f8fafc")
        # 默认不 pack，点击 toggle 时按需展示

        drawer_card = tk.Frame(self.drawer_container, bg="#ffffff", padx=14, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
        drawer_card.pack(fill="x", pady=(0, 10))

        # 选项配置行
        opts_grid = tk.Frame(drawer_card, bg="#ffffff")
        opts_grid.pack(fill="x", pady=(0, 8))

        tk.Label(opts_grid, text="顶栏定名:", font=("Microsoft YaHei UI", 8), bg="#ffffff", fg="#475569").grid(row=0, column=0, sticky="w", pady=2)
        self.var_title = tk.StringVar(value="谷歌正重力")
        entry_title = tk.Entry(opts_grid, textvariable=self.var_title, font=("Microsoft YaHei UI", 8), relief="solid", bd=1, width=16)
        entry_title.grid(row=0, column=1, sticky="w", padx=(4, 12))

        tk.Label(opts_grid, text="图标方案:", font=("Microsoft YaHei UI", 8), bg="#ffffff", fg="#475569").grid(row=0, column=2, sticky="w", pady=2)
        self.var_icon = tk.StringVar(value="重力模式 (趴地破损A 萌态)")
        self.icon_combo = ttk.Combobox(opts_grid, textvariable=self.var_icon, state="readonly", width=22)
        self.icon_combo['values'] = ("重力模式 (趴地破损A 萌态)", "奔跑小人 (蓝色经典)", "自定义本地 PNG...")
        self.icon_combo.grid(row=0, column=3, sticky="w", padx=(4, 0))
        self.icon_combo.bind("<<ComboboxSelected>>", self._on_icon_select)

        # 特性开关行与词典快捷编辑
        features_frame = tk.Frame(drawer_card, bg="#ffffff")
        features_frame.pack(fill="x", pady=(0, 8))

        self.var_enable_humor = tk.BooleanVar(value=True)
        self.chk_humor = tk.Checkbutton(
            features_frame, text="启用状态条趣味幽默金句轮播 (100条极客打工金句)",
            variable=self.var_enable_humor, font=("Microsoft YaHei UI", 8),
            bg="#ffffff", activebackground="#ffffff", fg="#1e293b",
            selectcolor="#ffffff"
        )
        self.chk_humor.pack(anchor="w")

        feat_sub = tk.Frame(features_frame, bg="#ffffff")
        feat_sub.pack(fill="x", pady=(2, 0))

        self.var_enable_token = tk.BooleanVar(value=True)
        self.chk_token = tk.Checkbutton(
            feat_sub, text="启用任务结束 Token / 算力消耗统计徽章",
            variable=self.var_enable_token, font=("Microsoft YaHei UI", 8),
            bg="#ffffff", activebackground="#ffffff", fg="#1e293b",
            selectcolor="#ffffff"
        )
        self.chk_token.pack(side="left")

        btn_edit_dict = tk.Button(
            feat_sub, text="📝 记事本编辑外置词库", font=("Microsoft YaHei UI", 8),
            bg="#f1f5f9", fg="#2563eb", activebackground="#e2e8f0", activeforeground="#1d4ed8",
            relief="flat", cursor="hand2", padx=6, pady=1, bd=1,
            command=self._open_i18n_notepad
        )
        btn_edit_dict.pack(side="right")

        # 紧凑型日志输出框
        self.txt_log = tk.Text(drawer_card, font=("Consolas", 8), bg="#0f172a", fg="#f8fafc", relief="flat", wrap="word", height=5)
        self.txt_log.pack(fill="both", expand=True)

        # -------------------------------------------------------------
        # 6. 优雅底部版权
        # -------------------------------------------------------------
        lbl_footer = tk.Label(self.main_box, text=FOOTER_TEXT, font=("Microsoft YaHei UI", 8), bg="#f8fafc", fg="#94a3b8")
        lbl_footer.pack(side="bottom", pady=(4, 0))

        self._log(f"助手 {APP_VERSION} 就绪 (作者: {APP_AUTHOR})")

    def _open_i18n_notepad(self):
        try:
            target = self.i18n_source
            if not os.path.exists(target):
                target = os.path.expanduser(r"~\.gemini\antigravity\i18n.js")
            if os.path.exists(target):
                os.system(f'start notepad.exe "{target}"')
                self._set_toast("已调起记事本编辑外置词库 i18n.js", "#2563eb")
                self._log(f"调起记事本编辑: {target}")
            else:
                messagebox.showerror("未找到文件", f"未找到可编辑的 i18n.js 文件: {target}")
        except Exception as e:
            messagebox.showerror("出错", str(e))

    def _toggle_advanced(self):
        self.is_advanced_open = not self.is_advanced_open
        if self.is_advanced_open:
            self.btn_toggle_log.config(text="收起详情 ▾")
            self.drawer_container.pack(fill="x", pady=(0, 6))
            self.root.geometry("520x620")
        else:
            self.btn_toggle_log.config(text="详细日志 ▸")
            self.drawer_container.pack_forget()
            self.root.geometry("520x430")

    def _set_toast(self, text: str, color: str = "#16a34a"):
        self.lbl_toast.config(text=text, fg=color)

    def _log(self, text: str):
        self.txt_log.insert("end", f"> {text}\n")
        self.txt_log.see("end")

    def _browse_path(self):
        folder = filedialog.askdirectory(title="选择 Antigravity 安装根目录")
        if folder:
            self.var_path.set(folder)
            self.patcher.install_dir = folder
            self._refresh_status()

    def _on_icon_select(self, event):
        val = self.var_icon.get()
        if val.startswith("自定义"):
            file_path = filedialog.askopenfilename(
                title="选择自定义透明 PNG 图标",
                filetypes=[("PNG 图片", "*.png"), ("所有文件", "*.*")]
            )
            if file_path:
                self.custom_icon_path = file_path
                self._log(f"已选定图标: {os.path.basename(file_path)}")
                self._set_toast(f"已选定图标: {os.path.basename(file_path)}", "#2563eb")
            else:
                self.var_icon.set("重力模式 (趴地破损A 萌态)")

    def _refresh_status(self):
        p = self.var_path.get().strip()
        self.patcher.install_dir = p
        st = self.patcher.get_status()

        code = st.get("state_code")
        label = st.get("state_label")
        version = st.get("version", "")
        install_dir = st.get("install_dir") or "未检测到安装路径"

        # 优雅截断过长路径
        if len(install_dir) > 42:
            display_dir = install_dir[:20] + "..." + install_dir[-18:]
        else:
            display_dir = install_dir
        self.lbl_path_display.config(text=f"位置: {display_dir}")

        self.lbl_version_tag.config(text=f"v{version}" if version else "检测中")

        if code == "HOOKED":
            self.lbl_status_dot.config(text="●", fg="#16a34a")
            self.lbl_status_title.config(text="已完成深度汉化 (运行良好)", fg="#16a34a")
            self.status_card.config(highlightbackground="#bbf7d0")
            self._set_toast("✓ 汉化运行良好，支持免重启热重载词库", "#16a34a")
        elif code == "UPGRADED_NEED_PATCH":
            self.lbl_status_dot.config(text="▲", fg="#ea580c")
            self.lbl_status_title.config(text="检测到官方更新 (点击一键恢复)", fg="#ea580c")
            self.status_card.config(highlightbackground="#fed7aa")
            self._set_toast("▲ 官方后台刚进行了版本升级，点击下方按钮一键注入", "#ea580c")
        elif code == "ORIGINAL":
            self.lbl_status_dot.config(text="○", fg="#2563eb")
            self.lbl_status_title.config(text="官方英文原版 (待注入汉化)", fg="#2563eb")
            self.status_card.config(highlightbackground="#bfdbfe")
            self._set_toast("○ 当前为原版状态，点击下方按钮一键秒级汉化", "#2563eb")
        else:
            self.lbl_status_dot.config(text="✕", fg="#dc2626")
            self.lbl_status_title.config(text="未找到客户端安装文件", fg="#dc2626")
            self.status_card.config(highlightbackground="#fecaca")
            self._set_toast("✕ 请点击右侧【更改目录】指定 Antigravity 路径", "#dc2626")

    def _resolve_chosen_icon(self) -> Optional[str]:
        val = self.var_icon.get()
        if val.startswith("重力模式"):
            return os.path.join(self.assets_dir, "gravity_mode.png")
        elif val.startswith("奔跑小人"):
            return os.path.join(self.assets_dir, "runner_icon.png")
        elif self.custom_icon_path and os.path.exists(self.custom_icon_path):
            return self.custom_icon_path
        return None

    def _do_install(self):
        def _task():
            try:
                self.btn_install.config(state="disabled")
                self._set_toast("⏳ 正在注入汉化补丁与定制图标...", "#2563eb")
                self._log("开始执行汉化注入任务...")

                title_text = self.var_title.get().strip() or "谷歌正重力"
                icon_path = self._resolve_chosen_icon()
                enable_humor = self.var_enable_humor.get()
                enable_token = self.var_enable_token.get()
                
                if os.path.exists(self.i18n_source):
                    self._log(f"应用定制 (标题: {title_text}, 金句: {enable_humor}, Token徽章: {enable_token})...")
                    Customizer.update_i18n_content(
                        self.i18n_source,
                        title_text=title_text,
                        icon_path=icon_path,
                        enable_humor=enable_humor,
                        enable_token_badge=enable_token
                    )

                self.patcher.install_patch(
                    i18n_src=self.i18n_source,
                    callback=self._log
                )
                self._log("全部补丁挂载完成！")
                self._set_toast("🎉 汉化成功完成！打开或刷新客户端即可体验", "#16a34a")
                messagebox.showinfo("成功", f"汉化成功完成！\n已将标题设为：{title_text}\n特性：趣味金句({'开' if enable_humor else '关'}) · 算力徽章({'开' if enable_token else '关'})\n现在打开或刷新客户端即可体验纯正中文。")
            except Exception as e:
                self._log(f"错误: {str(e)}")
                self._set_toast(f"✕ 注入失败: {str(e)}", "#dc2626")
                messagebox.showerror("执行出错", str(e))
            finally:
                self.btn_install.config(state="normal")
                self._refresh_status()

        threading.Thread(target=_task, daemon=True).start()

    def _do_reload(self):
        self._set_toast("⏳ 正在通过 CDP 向客户端推送热重载...", "#2563eb")
        self._log("尝试热重载客户端...")
        ok = self.patcher.hot_reload()
        if ok:
            self._log("热重载指令已成功发送！")
            self._set_toast("✓ 界面已免重启即时刷新！", "#16a34a")
            messagebox.showinfo("热刷新成功", "已成功向正在运行的 Antigravity 推送最新翻译！")
        else:
            self._log("未检测到运行中的客户端。")
            self._set_toast("▲ 未检测到活跃窗口，可直接启动客户端", "#ea580c")
            messagebox.showwarning("提示", "未检测到活跃的客户端窗口，请直接启动客户端。")

    def _do_restore(self):
        if not messagebox.askyesno("确认还原", "确定要还原为官方纯英文原版吗？此操作将完整撤销汉化补丁。"):
            return

        def _task():
            try:
                self.btn_restore.config(state="disabled")
                self._set_toast("⏳ 正在还原官方原版 ASAR...", "#64748b")
                self.patcher.restore_original(callback=self._log)
                self._log("官方原版文件已就位。")
                self._set_toast("✓ 已完全还原为官方纯英文原版", "#2563eb")
                messagebox.showinfo("还原成功", "已成功恢复为官方未汉化英文版本！")
            except Exception as e:
                self._log(f"还原失败: {str(e)}")
                self._set_toast(f"✕ 还原失败: {str(e)}", "#dc2626")
                messagebox.showerror("还原失败", str(e))
            finally:
                self.btn_restore.config(state="normal")
                self._refresh_status()

        threading.Thread(target=_task, daemon=True).start()

def main():
    root = tk.Tk()
    app = AntigravityGuiApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
