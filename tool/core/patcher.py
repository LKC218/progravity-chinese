import os
import sys
import shutil
import tempfile
import urllib.request
import json
import asyncio
from typing import Optional, Dict, Any

from .asar import AsarArchive

HOOK_TAG = "/* [ANTIGRAVITY_I18N_HOOK_V2] */"

PRELOAD_HOOK = f"""
{HOOK_TAG}
try {{
    const _fs = require('fs');
    const _path = require('path');
    const _electron = require('electron');
    const _i18nFile = _path.join(process.env.USERPROFILE || 'C:\\\\Users\\\\Administrator', '.gemini', 'antigravity', 'i18n.js');
    const _runI18n = () => {{
        try {{
            if (_fs.existsSync(_i18nFile)) {{
                const _code = _fs.readFileSync(_i18nFile, 'utf8');
                if (_electron.webFrame && _electron.webFrame.executeJavaScript) {{
                    _electron.webFrame.executeJavaScript(_code);
                }}
            }}
        }} catch (_err) {{
            console.error('[i18n] Injection error:', _err);
        }}
    }};
    if (document.readyState === 'loading') {{
        window.addEventListener('DOMContentLoaded', _runI18n);
    }} else {{
        _runI18n();
    }}
}} catch (_err) {{
    console.error('[i18n] Hook error:', _err);
}}
"""

UTILS_HOOK_TARGET = "void applyStoredZoomLevel();\n        });"
UTILS_HOOK_REPLACEMENT = """void applyStoredZoomLevel();
        });
        win.webContents.on('dom-ready', () => {
            try {
                const _i18nFile = path_1.default.join(process.env.USERPROFILE || 'C:\\\\Users\\\\Administrator', '.gemini', 'antigravity', 'i18n.js');
                if (fs.existsSync(_i18nFile)) {
                    const _code = fs.readFileSync(_i18nFile, 'utf8');
                    void win.webContents.executeJavaScript(_code);
                }
            } catch (_e) {}
        });"""

COMMON_PATHS = [
    r"F:\ProgramData\antigravity",
    r"C:\ProgramData\antigravity",
    r"D:\ProgramData\antigravity",
    r"E:\ProgramData\antigravity",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\antigravity"),
    os.path.expandvars(r"%PROGRAMFILES%\antigravity"),
    os.path.expandvars(r"%PROGRAMFILES(X86)%\antigravity")
]

class AntigravityPatcher:
    def __init__(self, install_dir: Optional[str] = None):
        self.install_dir = install_dir or self.auto_detect_path()

    @staticmethod
    def auto_detect_path() -> Optional[str]:
        """智能多维度自动探测 Antigravity 安装目录"""
        # 1. 尝试从当前正在运行的进程探测
        try:
            import subprocess
            out = subprocess.check_output(
                'wmic process where "name=\'Antigravity.exe\'" get ExecutablePath',
                shell=True, stderr=subprocess.DEVNULL
            ).decode('gbk', errors='ignore')
            for line in out.splitlines():
                line = line.strip()
                if line and os.path.isfile(line) and 'antigravity.exe' in line.lower():
                    cand = os.path.dirname(line)
                    if os.path.isfile(os.path.join(cand, "resources", "app.asar")):
                        return cand
        except Exception:
            pass

        # 2. 从桌面快捷方式探测
        try:
            desktop = os.path.expanduser(r"~\Desktop")
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            for lnk in [os.path.join(desktop, "Antigravity.lnk"), os.path.join(desktop, "谷歌正重力.lnk")]:
                if os.path.exists(lnk):
                    sc = shell.CreateShortcut(lnk)
                    if sc.WorkingDirectory and os.path.isfile(os.path.join(sc.WorkingDirectory, "resources", "app.asar")):
                        return sc.WorkingDirectory
                    if sc.TargetPath and os.path.isfile(sc.TargetPath):
                        cand = os.path.dirname(sc.TargetPath)
                        if os.path.isfile(os.path.join(cand, "resources", "app.asar")):
                            return cand
        except Exception:
            pass

        # 3. 扫描常见安装路径
        for p in COMMON_PATHS:
            if os.path.isfile(os.path.join(p, "resources", "app.asar")):
                return p

        return None

    def get_paths(self) -> Dict[str, str]:
        base = self.install_dir or ""
        return {
            "exe": os.path.join(base, "Antigravity.exe"),
            "asar": os.path.join(base, "resources", "app.asar"),
            "backup": os.path.join(base, "resources", "app.asar.original.bak"),
            "update_yml": os.path.join(base, "resources", "app-update.yml"),
            "user_i18n": os.path.expanduser(r"~\.gemini\antigravity\i18n.js")
        }

    def get_status(self) -> Dict[str, Any]:
        """获取当前客户端的汉化状态诊断"""
        paths = self.get_paths()
        if not self.install_dir or not os.path.exists(paths["asar"]):
            return {
                "installed": False,
                "is_hooked": False,
                "has_backup": False,
                "version": "未检测到",
                "state_code": "NOT_FOUND",
                "state_label": "未检测到客户端安装路径"
            }

        # 读版本
        version = "2.x (最新)"
        if os.path.exists(paths["update_yml"]):
            try:
                with open(paths["update_yml"], "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("version:"):
                            version = line.split(":", 1)[1].strip()
                            break
            except Exception:
                pass

        has_backup = os.path.exists(paths["backup"])
        is_hooked = False
        try:
            with open(paths["asar"], "rb") as f:
                content = f.read()
                is_hooked = b"ANTIGRAVITY_I18N_HOOK_V2" in content
        except Exception:
            pass

        if is_hooked:
            state_code = "HOOKED"
            state_label = "已完成深度汉化 (运行良好)"
        elif has_backup and not is_hooked:
            state_code = "UPGRADED_NEED_PATCH"
            state_label = "检测到官方版本更新 (需补桩)"
        else:
            state_code = "ORIGINAL"
            state_label = "官方纯英文原版 (未汉化)"

        return {
            "installed": True,
            "install_dir": self.install_dir,
            "is_hooked": is_hooked,
            "has_backup": has_backup,
            "version": version,
            "state_code": state_code,
            "state_label": state_label
        }

    def install_patch(self, i18n_src: Optional[str] = None, callback=None) -> bool:
        """一键安装/更新汉化补丁"""
        paths = self.get_paths()
        if not os.path.exists(paths["asar"]):
            raise FileNotFoundError(f"未找到核心文件: {paths['asar']}")

        if callback: callback("正在创建官方原版安全备份...")
        if not os.path.exists(paths["backup"]):
            shutil.copy2(paths["asar"], paths["backup"])

        temp_dir = tempfile.mkdtemp(prefix="antigravity_patch_")
        try:
            if callback: callback("正在解包核心 ASAR 模块 (原生加速引擎)...")
            AsarArchive.extract(paths["asar"], temp_dir)

            # 1. 注入 preload.js
            preload_path = os.path.join(temp_dir, "dist", "preload.js")
            if os.path.exists(preload_path):
                if callback: callback("正在挂载渲染层注入钩子 (preload)...")
                with open(preload_path, "r", encoding="utf-8") as f:
                    p_content = f.read()
                # 清除旧版标记
                if "ANTIGRAVITY_I18N_HOOK" in p_content:
                    p_content = p_content.split("/* [ANTIGRAVITY_I18N_HOOK")[0]
                p_content = p_content.strip() + "\n" + PRELOAD_HOOK
                with open(preload_path, "w", encoding="utf-8") as f:
                    f.write(p_content)

            # 2. 注入 utils.js (主进程 dom-ready 双重保障)
            utils_path = os.path.join(temp_dir, "dist", "utils.js")
            if os.path.exists(utils_path):
                if callback: callback("正在挂载主进程双重保障钩子 (dom-ready)...")
                with open(utils_path, "r", encoding="utf-8") as f:
                    u_content = f.read()
                if "_i18nFile" not in u_content and UTILS_HOOK_TARGET in u_content:
                    u_content = u_content.replace(UTILS_HOOK_TARGET, UTILS_HOOK_REPLACEMENT)
                    with open(utils_path, "w", encoding="utf-8") as f:
                        f.write(u_content)

            if callback: callback("正在打包封装 ASAR 归档文件...")
            AsarArchive.pack(temp_dir, paths["asar"])

            # 3. 复制/同步 i18n.js
            if i18n_src and os.path.exists(i18n_src):
                if callback: callback("正在同步最新汉化词典与引擎...")
                os.makedirs(os.path.dirname(paths["user_i18n"]), exist_ok=True)
                shutil.copy2(i18n_src, paths["user_i18n"])

            # 4. 尝试热加载
            self.hot_reload()

            if callback: callback("汉化补丁安装成功！")
            return True
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def restore_original(self, callback=None) -> bool:
        """一键还原为官方纯英文原版"""
        paths = self.get_paths()
        if not os.path.exists(paths["backup"]):
            raise FileNotFoundError("未找到原始官方备份文件 (app.asar.original.bak)，无法执行一键还原。")

        if callback: callback("正在还原官方原始文件...")
        shutil.copy2(paths["backup"], paths["asar"])
        if callback: callback("已成功恢复为官方纯英文原版！重启客户端即可完全生效。")
        return True

    def hot_reload(self) -> bool:
        """如果客户端正在运行，热加载当前翻译"""
        try:
            port_file = os.path.expanduser(r"~\AppData\Roaming\Antigravity\DevToolsActivePort")
            if not os.path.exists(port_file):
                return False
            with open(port_file, "r") as f:
                port = f.readline().strip()

            with urllib.request.urlopen(f"http://127.0.0.1:{port}/json") as resp:
                targets = json.loads(resp.read().decode())
            if not targets:
                return False

            import websockets
            paths = self.get_paths()
            i18n_path = paths["user_i18n"]
            if not os.path.exists(i18n_path):
                return False

            with open(i18n_path, "r", encoding="utf-8") as f:
                code = f.read()

            async def _do():
                ws_url = targets[0]["webSocketDebuggerUrl"]
                async with websockets.connect(ws_url) as ws:
                    await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": "window.__antigravity_i18n_loaded = false;"}}))
                    await ws.recv()
                    await ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": code}}))
                    await ws.recv()

            asyncio.run(_do())
            return True
        except Exception:
            return False
