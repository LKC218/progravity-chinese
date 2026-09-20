import os
import sys
import shutil
import subprocess

ASAR_PATH = r"F:\ProgramData\antigravity\resources\app.asar"
BACKUP_PATH = r"F:\ProgramData\antigravity\resources\app.asar.original.bak"
I18N_PATH = r"C:\Users\Administrator\.gemini\antigravity\i18n.js"
TEMP_DIR = r"C:\Users\Administrator\.gemini\antigravity\asar_temp"

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

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}\nStderr: {result.stderr}")
        return False
    return True

def install():
    if not os.path.exists(ASAR_PATH):
        print(f"Error: app.asar not found at {ASAR_PATH}")
        return False

    if not os.path.exists(BACKUP_PATH):
        print(f"正在备份原始 app.asar -> {BACKUP_PATH} ...")
        shutil.copy2(ASAR_PATH, BACKUP_PATH)
        print("备份完成！")

    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    print("正在解包 app.asar ...")
    if not run_cmd(f'npx --yes @electron/asar extract "{ASAR_PATH}" "{TEMP_DIR}"'):
        return False

    # 1. 注入 preload.js
    preload_file = os.path.join(TEMP_DIR, "dist", "preload.js")
    with open(preload_file, "r", encoding="utf-8") as f:
        p_content = f.read()

    # 清除旧版 hook
    if "ANTIGRAVITY_I18N_HOOK_V1" in p_content:
        p_content = p_content.split("/* [ANTIGRAVITY_I18N_HOOK_V1] */")[0]

    if HOOK_TAG not in p_content:
        print("注入 preload.js 钩子 (webFrame.executeJavaScript) ...")
        p_content = p_content.strip() + "\n" + PRELOAD_HOOK
        with open(preload_file, "w", encoding="utf-8") as f:
            f.write(p_content)

    # 2. 注入 utils.js (Main Process dom-ready 双重保证)
    utils_file = os.path.join(TEMP_DIR, "dist", "utils.js")
    with open(utils_file, "r", encoding="utf-8") as f:
        u_content = f.read()

    if "_i18nFile" not in u_content and UTILS_HOOK_TARGET in u_content:
        print("注入 utils.js 钩子 (webContents dom-ready) ...")
        u_content = u_content.replace(UTILS_HOOK_TARGET, UTILS_HOOK_REPLACEMENT)
        with open(utils_file, "w", encoding="utf-8") as f:
            f.write(u_content)

    # 3. 重新打包
    print("正在重新打包 app.asar ...")
    packed_file = os.path.join(os.path.dirname(TEMP_DIR), "temp_app.asar")
    if os.path.exists(packed_file):
        os.remove(packed_file)

    if not run_cmd(f'npx --yes @electron/asar pack "{TEMP_DIR}" "{packed_file}"'):
        return False

    shutil.move(packed_file, ASAR_PATH)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

    print("=== 双重保障汉化补丁安装成功！===")
    return True

def uninstall():
    if not os.path.exists(BACKUP_PATH):
        print(f"未找到备份文件: {BACKUP_PATH}")
        return False
    shutil.copy2(BACKUP_PATH, ASAR_PATH)
    print("=== 还原成功！===")
    return True

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "install"
    if action == "install":
        install()
    elif action == "uninstall":
        uninstall()
