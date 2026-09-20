Set WshShell = CreateObject("WScript.Shell")
Set WshEnv = WshShell.Environment("PROCESS")
WshEnv("HTTP_PROXY") = "http://127.0.0.1:7897"
WshEnv("HTTPS_PROXY") = "http://127.0.0.1:7897"
WshEnv("ALL_PROXY") = "http://127.0.0.1:7897"
WshEnv("NO_PROXY") = "localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,git.vicfun,.vicfun"
WshEnv("http_proxy") = "http://127.0.0.1:7897"
WshEnv("https_proxy") = "http://127.0.0.1:7897"
WshEnv("no_proxy") = "localhost,127.0.0.1,::1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,git.vicfun,.vicfun"

' 1. Check and patch asar if needed (hidden window, wait 15ms)
WshShell.Run """C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"" ""C:\Users\Administrator\.gemini\antigravity\ensure_i18n.py""", 0, True

' 2. Launch Antigravity
WshShell.Run """F:\ProgramData\antigravity\Antigravity.exe""", 1, False
