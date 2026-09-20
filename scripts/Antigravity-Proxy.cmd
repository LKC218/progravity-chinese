@echo off
rem ============================================================
rem  Antigravity 2.x proxy launcher
rem
rem  ROOT CAUSE OF BLACK SCREEN:
rem    language_server.exe is a Go binary. Go's http.ProxyFromEnvironment
rem    reads ONLY the HTTP_PROXY / HTTPS_PROXY environment variables and
rem    IGNORES the Windows system proxy (WinINET registry settings).
rem    On this machine googleapis.com is unreachable directly (blocked),
rem    so the language server hangs during init, its local HTTP/HTTPS
rem    endpoints accept TCP but never answer, and the Electron window's
rem    loadURL("https://127.0.0.1:<random port>/") fails with ERR_TIMED_OUT
rem    -> the window stays completely black.
rem
rem  FIX: hand the language server the Clash proxy via env vars.
rem ============================================================

rem  INSTALL LOCATION: F:\ProgramData\antigravity
rem ============================================================

set "HTTP_PROXY=http://127.0.0.1:7897"
set "HTTPS_PROXY=http://127.0.0.1:7897"
set "ALL_PROXY=http://127.0.0.1:7897"
set "NO_PROXY=localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,git.vicfun,.vicfun"
set "no_proxy=%NO_PROXY%"
set "http_proxy=%HTTP_PROXY%"
set "https_proxy=%HTTPS_PROXY%"

rem Ensure i18n hook is active
python "C:\Users\Administrator\.gemini\antigravity\ensure_i18n.py" >nul 2>&1

start "" "F:\ProgramData\antigravity\Antigravity.exe"
exit /b 0
