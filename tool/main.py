import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from core.patcher import AntigravityPatcher
from core.customizer import Customizer
from core.version import APP_NAME, APP_VERSION, APP_AUTHOR

def cli_main():
    # 如果通过命令行带参数调用，尝试挂载调用者的父控制台输出
    args = sys.argv[1:]
    if args:
        try:
            import ctypes
            if ctypes.windll.kernel32.AttachConsole(-1):
                sys.stdout = open("CONOUT$", "w", encoding="utf-8")
                sys.stderr = open("CONOUT$", "w", encoding="utf-8")
        except Exception:
            pass

    patcher = AntigravityPatcher()
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(current_dir)

    if "--status" in args:
        st = patcher.get_status()
        print("=" * 45)
        print(f"{APP_NAME} {APP_VERSION} (作者: {APP_AUTHOR})")
        print("=" * 45)
        print(f"安装路径: {st.get('install_dir')}")
        print(f"检测状态: {st.get('state_label')}")
        print(f"当前版本: {st.get('version')}")
        print("=" * 45)
        return

    if "--install" in args:
        print("正在执行一键汉化注入...")
        i18n_path = os.path.join(base_dir, "i18n.js")
        patcher.install_patch(i18n_src=i18n_path, callback=print)
        print("汉化注入完成！")
        return

    if "--restore" in args:
        print("正在执行一键还原官方原版...")
        patcher.restore_original(callback=print)
        print("已恢复为官方纯英文原版！")
        return

    # 默认无参数或双击运行时启动 GUI 交互界面
    try:
        import tkinter as tk
        from gui.app import AntigravityGuiApp
        root = tk.Tk()
        app = AntigravityGuiApp(root)
        root.mainloop()
    except Exception as e:
        print(f"启动图形界面失败: {e}")
        print("转入命令行运行模式:")
        st = patcher.get_status()
        print(f"状态: {st.get('state_label')}")
        input("按回车键退出...")

if __name__ == "__main__":
    cli_main()
