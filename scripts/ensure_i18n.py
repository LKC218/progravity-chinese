import os
import sys
import time
import subprocess
import urllib.request
import json
import asyncio

LOG_FILE = r"C:\Users\Administrator\.gemini\antigravity\guard.log"

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass

# Ensure safe stdio under pythonw
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

ASAR_PATH = r"F:\ProgramData\antigravity\resources\app.asar"
HOOK_TAG = b"ANTIGRAVITY_I18N_HOOK_V2"
PATCHER = r"C:\Users\Administrator\.gemini\antigravity\patch_i18n.py"
I18N_FILE = r"C:\Users\Administrator\.gemini\antigravity\i18n.js"
DEVTOOLS_PORT_FILE = os.path.expanduser(r"~\AppData\Roaming\Antigravity\DevToolsActivePort")

py_dir = os.path.dirname(sys.executable)
PYTHON_EXE = os.path.join(py_dir, "python.exe") if os.path.exists(os.path.join(py_dir, "python.exe")) else sys.executable

def is_hooked():
    if not os.path.exists(ASAR_PATH):
        return False
    try:
        with open(ASAR_PATH, "rb") as f:
            content = f.read()
            return HOOK_TAG in content
    except Exception:
        return False

def hot_reload_i18n():
    """If Antigravity is running with CDP, hot-reload i18n.js immediately without restarting"""
    try:
        if not os.path.exists(DEVTOOLS_PORT_FILE):
            return
        with open(DEVTOOLS_PORT_FILE, "r") as f:
            port = f.readline().strip()
        
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json") as resp:
            targets = json.loads(resp.read().decode())
        
        if not targets:
            return

        import websockets

        async def _inject():
            ws_url = targets[0]["webSocketDebuggerUrl"]
            async with websockets.connect(ws_url) as ws:
                with open(I18N_FILE, "r", encoding="utf-8") as f:
                    code = f.read()
                await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": "window.__antigravity_i18n_loaded = false;"}}))
                await ws.recv()
                await ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": code}}))
                await ws.recv()

        asyncio.run(_inject())
        log("Hot-reloaded i18n into running client successfully.")
    except Exception as e:
        log(f"Hot-reload notice: {e}")

def check_and_ensure():
    if not is_hooked():
        log("Detected unhooked app.asar! Installing patch...")
        res = subprocess.run([PYTHON_EXE, PATCHER, "install"], capture_output=True, text=True)
        log(f"Patch result: returncode={res.returncode}, stdout={res.stdout[:100]}")
        hot_reload_i18n()
        return True
    return False

def watch_loop():
    """Background daemon loop: checks every 30s"""
    log("Started ensure_i18n background watcher daemon.")
    last_mtime = 0
    while True:
        try:
            if os.path.exists(ASAR_PATH):
                mtime = os.path.getmtime(ASAR_PATH)
                if mtime != last_mtime:
                    last_mtime = mtime
                    check_and_ensure()
                elif not is_hooked():
                    check_and_ensure()
        except Exception as e:
            log(f"Error in watch_loop: {e}")
        time.sleep(30)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--watch":
        watch_loop()
    else:
        check_and_ensure()
