# 谷歌正重力 (Antigravity 2.0) 客户端深度汉化项目

> **作者**: @LKC218  
> **当前版本**: v2.1.1 (体验优化版)  
> **演进基线**: v2.0 起点统一演进  
> **适用平台**: Windows (Google Antigravity 2.x)

本项目为 Google Antigravity 2.0 桌面客户端的**轻量级、零依赖、一键注入、热更新、升级自动守护**的深度中文化（汉化）工程。
已集成 **思考过程汉化**、**100条趣味金句轮播池**、**Token/算力额度消耗徽章**、**8秒呼吸记忆锁** 及 **一键逃生急停开关**。

---

## 📁 规范化目录结构

```text
G:\项目\反重力汉化\
├── .gitignore                         # 标准 Git 过滤规范 (忽略编译产物与临时文件)
├── CHANGELOG.md                       # 版本演进与变更规范 (以 v2.0 为基线)
├── CONTEXT.md                         # 跨会话无缝接续与架构说明文档
├── README.md                          # 项目总览与使用指南
├── i18n.js                            # 核心动态汉化引擎与外置词库 (热更新源)
│
├── assets/                            # 品牌与图标素材库
│   ├── gravity_mode.png               # 标准图标 (128x128)
│   ├── runner_icon.png                # 托盘图标
│   └── source/                        # 高清设计原画与矢量源文件
│       └── gravity_mode_hd.png        # 原画素材 (1254x1254)
│
├── data/                              # 词典提取与分析数据集
│   ├── current_ui_texts.json          # 客户端抓取全量 UI 文本
│   ├── extracted_settings.json        # 设置中心 120+ 项配置提取集
│   └── high_value_ui_terms.json       # 高价值界面术语词汇表
│
├── docs/                              # 实施与交付文档中心
│   ├── 实施方案.md                     # 深度汉化技术实施方案
│   ├── 交付与使用指南.md               # 交付验收与使用手册
│   └── archive/                       # 历史会话与过程数据归档
│       ├── 完整会话记录.md             # 历史开发会话完整 Markdown 记录
│       └── logs/                      # 原始会话 transcript 追踪日志
│
├── scripts/                           # 独立运维、底层注入与快捷启动脚本
│   ├── Antigravity-Proxy.cmd          # 代理与自动守护启动脚本
│   ├── Launch_Antigravity.vbs         # 静默启动器脚本
│   ├── ensure_i18n.py                 # 官方升级毫秒级自动感知与守护脚本
│   └── patch_i18n.py                  # CLI 底层 ASAR 补丁安装/卸载工具
│
├── tool/                              # 独立 GUI 汉化助手源码工程
│   ├── app.ico                        # 窗口与程序图标
│   ├── version_info.txt               # Windows PE 文件版本信息
│   ├── build_exe.py                   # 一键独立打包脚本
│   ├── main.py                        # 程序入口 (支持 GUI / CLI 双模)
│   ├── core/                          # 核心业务逻辑 (ASAR编解码、智能补丁、标题定制)
│   └── gui/                           # Tkinter 现代化图形交互界面
│
└── release/                           # ⭐ 开箱即用绿色独立分发包 (可直接打包发给他人)
    └── 谷歌正重力_汉化分发包/
        ├── 谷歌正重力汉化助手.exe       # 独立单文件 GUI 程序 (零环境依赖，双击即用)
        ├── i18n.js                    # 外置核心汉化词库 (任何人可用记事本自由扩充)
        ├── CHANGELOG.md               # 版本规范与变更记录 (以 v2.0 为起点)
        ├── assets/                    # 高清品牌图标素材库
        └── 使用说明.txt                # 小白专属极简使用指南
```

---

## 🚀 两种使用方式

### 方式 A：使用独立 GUI 汉化助手（推荐小白用户或对外分发）
1. 将 `release/谷歌正重力_汉化分发包` 文件夹压缩打包（如 `谷歌正重力汉化包.zip`）直接发送给任何用户；
2. 对方电脑**无需安装 Node.js、npm 或 Python**，解压后直接双击运行 `谷歌正重力汉化助手.exe`；
3. 程序自动检测客户端安装目录与当前状态：
   - 点击 **【🚀 一键安装 / 更新汉化】** 即可秒级完成汉化；
   - 点击 **【🔄 热重载界面】** 即可无需重启客户端即时刷新中文；
   - 点击 **【↩ 一键还原官方英文】** 即可无损还原官方原版。
4. 协同扩充词库：任何人只需使用记事本打开同目录下的 `i18n.js` 添加词条，保存后点击助手上的“热重载”即可立刻体验！

### 方式 B：开发者代码模式
1. 开发者直接在本工程目录下运行：
   ```powershell
   python tool/main.py
   ```
2. 或通过命令行脚本直接注入：
   ```powershell
   python scripts/patch_i18n.py install
   ```
3. 若修改了工具源码需重新打包发布包：
   ```powershell
   python tool/build_exe.py
   ```

