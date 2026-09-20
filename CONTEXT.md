# 项目上下文与接续指南 (Project Context & Handover)

> 本文档用于在新的 Antigravity 会话中**一秒无缝承接所有背景、架构与任务进展**。在新项目中开启会话后，直接让智能体阅读本文档即可。

---

## 一、 项目背景与定名
* **项目名称**：**谷歌正重力 (Antigravity 2.0 桌面端深度汉化工程)**
* **项目根目录**：`G:\项目\反重力汉化`
* **应用类型**：Electron 桌面端 (Node.js + Chromium + React SPA + Go Language Server)
* **核心原则**：
  1. **专业化 (信·达·雅)**：杜绝机械生硬机翻，符合国内一线资深研发人员习惯（如 `Artifact` 译为“交付产物/产物文档”，`Agent` 译为“智能体”，`Tool Execution Policy` 译为“工具运行鉴权策略”）。
  2. **高可用零侵入**：字典与引擎完全外置解耦，支持热更新（修改即生效无需重装），且具备更新自动守护。
  3. **代码与输入隔离**：严格排除了 `<pre>`, `<code>`, `.monaco-editor`, `.prism-code` 及用户聊天输入框，保证代码展示与输入体验绝对安全。

---

## 二、 关键架构与核心文件分布

| 文件/目录 | 作用说明 | 运行时/工程位置 |
| :--- | :--- | :--- |
| **`i18n.js`** | 核心汉化字典与 DOM 动态翻译引擎 (包含精准词典、动态正则、Scope 上下文监听) | `C:\Users\Administrator\.gemini\antigravity\i18n.js`<br>*(本工程根目录下保持同步)* |
| **`scripts/patch_i18n.py`** | 客户端底层 ASAR 补丁工具 (已升级为 V2 主进程 dom-ready + preload 双重保障) | `C:\Users\Administrator\.gemini\antigravity\patch_i18n.py`<br>`scripts/patch_i18n.py` |
| **`scripts/ensure_i18n.py`** | 官方更新自动感知守护脚本 (启动时 10ms 检测，被覆盖则后台 1 秒静默补齐) | `C:\Users\Administrator\.gemini\antigravity\ensure_i18n.py`<br>`scripts/ensure_i18n.py` |
| **`scripts/Antigravity-Proxy.cmd`** | 桌面端代理与守护启动器 (整合守护调用与本地代理环境变量配置) | 桌面及 `scripts/Antigravity-Proxy.cmd` |
| **`tool/`** | 纯 Python 零依赖 GUI 汉化助手源代码工程 (纯原生 ASAR 解析打包) | `tool/` 目录 (可直接 `python tool/main.py`) |
| **`release/`** | 开箱即用绿色独立免安装分发包 | `release/谷歌正重力_汉化分发包/` |
| **`docs/`** | 实施规划、方案原则、详细验收指南及历史归档 | `docs/实施方案.md`<br>`docs/交付与使用指南.md`<br>`docs/archive/完整会话记录.md` |
| **`data/`** | 提取的全部设置项、前端高频 UI 词条及扫描数据 (供扩展) | `data/extracted_settings.json`<br>`data/high_value_ui_terms.json`<br>`data/current_ui_texts.json` |

---

## 三、 当前汉化与系统状态 (100% 达成状态)

1. **顶栏与品牌标识**：
   * 左上角与窗口标题：正式定名为 **`谷歌重力反`**；
   * 一级菜单：**`文件`**、**`视图`**、**`窗口`**；
   * 文件下拉子菜单：`新建会话`、`创建项目`、`命令面板`、`打开会话历史` 等已全量汉化。
2. **侧边栏与主工作区**：
   * `新建会话`、`计划任务`、`项目管理`、`系统设置`、`会话列表`、`全部会话`、`独立会话` 等 100% 汉化。
3. **设置中心 (Settings)**：
   * 通用、应用设置、外观、模型、规则、网络、沙箱等全部分类页面及 120+ 项说明文案 100% 深度中文覆盖。
4. **动态状态与悬停操作 (Tooltips / Aria-labels)**：
   * `思考了 X 秒`、`工作了 X 分钟`、`执行了 X 条系统命令`；
   * 缩放、切换侧边栏、滚动到底部、添加上下文、录音、终止执行等操作 100% 汉化。
5. **升级守护**：
   * 即使官方版本自动更新，启动时也会通过守护脚本在 1 秒内无感补丁，永久保持中文。

---

## 四、 在新会话中开启对话的推荐提示词 (复制即用)

在新会话窗口中，您可以直接发送以下指令唤醒智能体：

```text
你好！我们正在进行“反重力汉化”项目。请先阅读项目根目录下的 CONTEXT.md、README.md 以及完整会话记录.md，了解当前项目的整体架构、已落地的核心文件和当前的汉化进展，然后等待我的下一步指示。
```
