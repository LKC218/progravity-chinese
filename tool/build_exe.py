import os
import sys
import shutil
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

tool_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(tool_dir)
release_dir = os.path.join(project_dir, "release", "谷歌正重力_汉化分发包")

def build():
    print("========================================")
    print("开始编译 谷歌正重力汉化助手 (单文件独立 EXE)...")
    print("========================================")

    ico_path = os.path.join(tool_dir, "app.ico")
    ver_path = os.path.join(tool_dir, "version_info.txt")
    main_script = os.path.join(tool_dir, "main.py")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--clean",
        f"--icon={ico_path}",
        f"--version-file={ver_path}",
        "--name=AntigravityPatcher",
        f"--paths={tool_dir}",
        "--distpath", os.path.join(tool_dir, "dist"),
        "--workpath", os.path.join(tool_dir, "build"),
        "--specpath", tool_dir,
        main_script
    ]

    print("执行命令:", " ".join(cmd))
    res = subprocess.run(cmd, cwd=tool_dir)
    if res.returncode != 0:
        print("[ERROR] 编译失败！")
        return False

    print("[OK] PyInstaller 编译成功！")

    # 构建分发包
    print("\n正在生成发布目录:", release_dir)
    os.makedirs(release_dir, exist_ok=True)

    # 1. 拷贝生成的独立 EXE
    exe_src = os.path.join(tool_dir, "dist", "AntigravityPatcher.exe")
    exe_dst = os.path.join(release_dir, "谷歌正重力汉化助手.exe")
    shutil.copy2(exe_src, exe_dst)
    print(f"已复制主程序 -> {exe_dst} (大小: {os.path.getsize(exe_dst) // 1024 // 1024} MB)")

    # 2. 拷贝核心 i18n.js 词库 (外置，供任何人自由扩充)
    i18n_src = os.path.join(project_dir, "i18n.js")
    i18n_dst = os.path.join(release_dir, "i18n.js")
    shutil.copy2(i18n_src, i18n_dst)
    print(f"已复制外置词典 -> {i18n_dst}")

    # 3. 拷贝变更日志与版本规范 (CHANGELOG.md)
    changelog_src = os.path.join(project_dir, "CHANGELOG.md")
    changelog_dst = os.path.join(release_dir, "CHANGELOG.md")
    if os.path.exists(changelog_src):
        shutil.copy2(changelog_src, changelog_dst)
        print(f"已复制版本规范 -> {changelog_dst}")

    # 4. 拷贝素材库 (排除 source 设计原稿)
    assets_src = os.path.join(project_dir, "assets")
    assets_dst = os.path.join(release_dir, "assets")
    if os.path.exists(assets_src):
        if os.path.exists(assets_dst):
            shutil.rmtree(assets_dst)
        shutil.copytree(assets_src, assets_dst, ignore=shutil.ignore_patterns("source", "*.psd", "*.ai"))
        print(f"已复制图标素材库 -> {assets_dst}")

    # 5. 生成小白使用说明 (含作者与版本规范)
    readme_content = """============================================================
谷歌正重力 · Google Antigravity 2.x 客户端一键深度汉化工具
============================================================
【项目作者】：@LKC218
【当前版本】：v2.1.1 (体验优化版)
【发布日期】：2026-09-21
【演进基线】：v2.0 起点统一演进

【核心特点与优势】
1. 真正零门槛：无需安装 Node.js、npm、Python 等任何开发环境，双击即可直接使用！
2. 零侵入安全：内置智能探测与全自动原版备份机制，随时支持一键无损还原官方纯英文。
3. 外置词库协同：核心汉化词库完全外置为 i18n.js，在工具中点击“记事本编辑”即可自由扩充词条与金句。
4. 深度高阶体验：
   - 思考过程地道汉化：Explored / Ran / Searched / Thought for 等动态正则插值自然重组；
   - 趣味幽默金句轮播：100 条极客与打工趣味金句，搭配 8 秒呼吸记忆锁与极光流光，随用随销零残留；
   - 算力/Token 徽章：生成彻底结束时单次结算，优雅展示 ✧ 算力消耗；
   - 紧急逃生开关：内置快捷键 Ctrl + Shift + Alt + F12 一键秒级停用并复原。

------------------------------------------------------------
【使用说明】
1. 双击运行当前目录下的【谷歌正重力汉化助手.exe】；
2. 软件会自动检测您的客户端安装路径；
3. （可选）展开【高级设置与日志】，勾选/取消趣味金句或算力徽章，或自定义顶栏标题与图标；
4. 点击绿色超大按钮【一键安装 / 更新汉化】即可秒级完成汉化！
5. 启动 Antigravity 客户端，尽享专业优雅的中文体验。

------------------------------------------------------------
【其他便捷功能】
- 免重启热重载：客户端已打开时，修改了 i18n.js 后点击【免重启热重载】即可免重启实时生效。
- 一键还原纯英文：若需还原官方原版，点击【一键还原官方英文】即可无损撤销所有补丁。
- 记事本一键编辑：在高级设置中点击【📝 记事本编辑外置词库】，轻松修改词典与金句池。
"""
    with open(os.path.join(release_dir, "使用说明.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("已生成 使用说明.txt")

    print("\n[SUCCESS] 绿色分发包构建完成！目录位置:")
    print(release_dir)
    return True

if __name__ == "__main__":
    build()

