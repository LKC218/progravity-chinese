/**
 * 谷歌正重力 · Google Antigravity 2.x 客户端深度中文化引擎与词库
 * 作者: @LKC218
 * 起点版本: v2.0
 * 更新时间: 2026-09-20
 * 规范: 语义驱动精准匹配 + 动态 DOM 监听 + 外置词库免编译扩展
 */
(function () {
    window.__ANTIGRAVITY_I18N_META__ = {
        name: "谷歌正重力",
        author: "@LKC218",
        version: "v2.0"
    };
    window.__ENABLE_CHINESE__ = true;
    if (window.__antigravity_i18n_loaded) return;
    window.__antigravity_i18n_loaded = true;

    // ========================
    // 顶栏品牌图标注入
    // ========================
    const LOGO_ICON_BASE64 = "data:image/png;base64,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";

    function ensureTitleIcon() {
        const btn = document.querySelector('[data-testid="title-menu-bar-item"]');
        if (btn && !btn.querySelector('.agy-title-icon')) {
            const img = document.createElement('img');
            img.className = 'agy-title-icon';
            img.src = LOGO_ICON_BASE64;
            img.style.width = '18px';
            img.style.height = '18px';
            img.style.objectFit = 'contain';
            img.style.display = 'inline-block';
            img.style.flexShrink = '0';
            img.style.verticalAlign = 'middle';
            img.style.marginRight = '4px';
            btn.prepend(img);
        }
    }
    ensureTitleIcon();


    // 1. 精确匹配词典 (UI 按钮、菜单、分类、标题、标签与设置说明)
    const EXACT_DICT = {
        "Conversation Log": "会话运行记录",
        "Working": "正在执行处理",
        "Walkthrough": "交付成果指引 (Walkthrough)",
        "Review": "审查方案 (Review)",
        "Overview": "全局概览",
        "Actions": "快捷操作",
        "Action required": "需人工介入处理",
        "Working Tree": "工作区工作树",
        "Staged Changes": "已暂存的更改",
        "Changes": "文件变更",
        "All Changes": "所有变更",
        "Ask anything, @ to mention, / for actions": "输入任何编程问题，输入 @ 引用上下文，输入 / 触发快捷操作",
        "Enter project name...": "输入项目名称...",
        "Search across files...": "在项目中全局搜索文件...",
        "Search projects...": "搜索项目名称...",
        "Enter a prompt for the agent to run...": "输入要让智能体执行的指令或提示词...",
        "Enter file or directory path...": "输入文件或目录的绝对/相对路径...",
        "Enter tool name or server...": "输入工具名称或服务地址...",
        "Select category to search...": "选择检索分类...",
        "Select or enter a workspace URI": "选择或输入工作区路径 URI",
        "Sidebar": "侧边栏",
        "Toggle Sidebar": "切换侧边栏展开/折叠",
        "Toggle Auxiliary Pane": "切换右侧辅助面板",
        "Toggle Terminal": "切换终端控制台",
        "Toggle Editor": "切换代码编辑器",
        "Toggle Fullscreen": "切换全屏显示",
        "Toggle Model Selector": "切换模型选择器",
        "Toggle Project Selector": "切换项目选择面板",
        "Toggle File Viewer": "切换文件查看器",
        "Toggle Thumbnails": "切换缩略图视图",
        "Toggle Voice Recording": "切换语音输入录制",
        "Scroll to Bottom": "滚动至最新底部",
        "Add context": "添加文件或上下文 (@)",
        "Record voice memo": "录制语音备忘",
        "Cancel (Ctrl+D)": "取消执行 (Ctrl+D)",
        "Overview tab": "概览标签页",
        "Review tab": "审查标签页",
        "Terminal tab": "终端控制台标签页",
        "Artifact Viewer": "产物文档查看器",
        "Artifact Viewer header": "产物查看器标题栏",
        "Add inline comment": "添加行内批注",
        "Go Back": "后退",
        "Go Forward": "前进",
        "Maximize Pane": "最大化当前面板",
        "Typeahead menu": "智能补全菜单",
        "Stop execution": "停止当前执行",
        "Open Settings": "打开系统设置",
        "Close Settings": "关闭设置面板",
        "Open Command Palette": "打开命令面板",
        "Open Keyboard Shortcuts": "查看快捷键列表",
        "Open Launchpad": "打开启动面板",
        "Open Preferences": "打开偏好设置",
        "Open Preview": "打开预览视图",
        "Open Search": "打开全局搜索",
        "Open URL": "打开外部链接",
        "Open Workspace": "打开工作区",
        "Open Workspace Selector": "打开工作区选择器",
        "Open in Code Search": "在代码检索中打开",
        "Open in Notebook View": "在 Notebook 视图中打开",
        "Open in Preview Pane": "在预览面板中打开",
        "Open in new tab": "在新标签页中打开",
        "Open project settings": "打开项目配置",
        "Open side-by-side view": "打开并排对比视图",
        "Open with External Browser": "使用系统默认浏览器打开",
        "Open File Search": "打开文件搜索",
        "Open Folder": "打开本地文件夹",
        "New Project": "新建项目",
        "New Workspace": "新建工作区",
        "New Worktree": "新建 Git Worktree",
        "New Editor Window": "新建编辑器窗口",
        "New Group": "新建分组",
        "New Terminal Tab": "新建终端标签页",
        "Close Tab": "关闭标签页",
        "Close Terminal Tab": "关闭终端标签页",
        "Collapse All Folders": "折叠所有文件夹",
        "Expand All Folders": "展开所有文件夹",
        "Clear Search": "清空搜索输入",
        "Clear search (Esc)": "清空搜索 (Esc)",
        "Copy Content": "复制文件内容",
        "Copy File Name": "复制文件名",
        "Copy File Path": "复制文件绝对路径",
        "Copy Image": "复制图片",
        "Copy Path": "复制路径",
        "Copy config file path": "复制配置文件路径",
        "Copy conversation markdown": "复制会话 Markdown 全文",
        "Copy debug info": "复制调试诊断信息",
        "Copy description": "复制描述内容",
        "Copy error to clipboard": "复制错误堆栈到剪贴板",
        "Copy full URL to clipboard": "复制完整 URL 链接",
        "Copy output": "复制标准输出",
        "Copy thinking": "复制思考推理链",
        "Copy raw string value": "复制原始字符串值",
        "Click to copy full command": "点击复制完整命令",
        "Click to copy URL": "点击复制链接",
        "Delete Conversation": "删除此会话",
        "Delete Permanently": "永久删除 (不可恢复)",
        "Delete Task": "删除任务",
        "Delete Skill": "删除技能扩展",
        "Delete MCP Server": "删除 MCP 服务配置",
        "Delete Hook": "删除钩子",
        "Delete Handler": "删除处理器",
        "Delete comment": "删除批注",
        "Delete workspace": "删除工作区",
        "Failed to delete conversation": "删除会话失败",
        "Failed to save project": "保存项目配置失败",
        "Failed to stop agent": "终止智能体运行失败",
        "Cancel All Tasks": "取消所有正在运行的任务",
        "Stop All Subagents": "终止所有子智能体",
        "Stop Subagent": "终止此子智能体",
        "Custom Agents": "自定义智能体",
        "Customize Global Skills": "配置全局技能库",
        "Manage Skills": "管理技能扩展",
        "Manage Hooks": "管理执行钩子",
        "Installed Skills": "已加载技能列表",
        "Installed MCP Servers": "已连接 MCP 服务列表",
        "MCP Tools": "MCP 扩展工具",
        "MCP tool": "MCP 工具",
        "Refresh skills paths": "刷新技能检索路径",
        "Refresh quota and credits data": "刷新配额与额度数据",
        "Select Model": "切换推理模型",
        "Select Model to Send Message": "选择发送消息的目标模型",
        "Select another model": "选择其他可用模型",
        "No Model Selected": "尚未选择任何模型",
        "No Models Available": "当前暂无可用模型",
        "Model Quota": "模型调用配额",
        "Model quota reached": "当前模型配额已达上限",
        "Insufficient AI Credits": "AI 额度不足",
        "Check for Updates": "检查客户端更新",
        "Update Available": "检测到新版本客户端可用",
        "Dark Theme": "深色暗调主题",
        "Light Theme": "清爽浅色主题",
        "About": "关于客户端",

// ========================
        // 任务/会话右键菜单与上下文选项
        // ========================
        "Rename": "重命名",
        "Mark Unread": "标记为未读",
        "Mark Read": "标记为已读",
        "Mark as Read": "标记为已读",
        "Mark as Unread": "标记为未读",
        "Split": "分屏",
        "Split Right": "向右分屏",
        "Split Down": "向下分屏",
        "Split Left": "向左分屏",
        "Split Up": "向上分屏",
        "Replace With New": "替换为新会话",
        "Split Editor": "拆分编辑器",
        "Split Editor Right": "向右拆分编辑器",
        "Split Editor Down": "向下拆分编辑器",
        "Split View": "分屏视图",
        "Conversation Name": "会话名称",
        "Conversation ID": "会话 ID",
        "Project Name": "项目名称",
        "Copy Link": "复制链接",
        "Copy Conversation Name": "复制会话名称",
        "Copy Conversation ID": "复制会话 ID",
        "Copy Project Name": "复制项目名称",
        "Archive conversation": "归档会话",
        "Unarchive conversation": "取消归档会话",
        "Pinned Conversations": "已置顶会话",
        "Pinned": "已置顶",
        "Unpinned": "已取消置顶",
        "Pin conversation": "置顶会话",
        "Unpin conversation": "取消置顶",
        "Group By": "分组方式",
        "Sort Conversations": "会话排序方式",
        "Last Updated": "最近更新时间",
        "Last Prompt": "最近提示词时间",
        "Alphabetical (A-Z)": "按名称首字母 (A-Z)",
        "Date Added": "创建添加时间",
        "Subtitles": "副标题显示",
        "Worktree": "Git Worktree",
        "No Subtitle": "不显示副标题",
        "Filter": "筛选过滤",
        "Duplicate": "创建副本",
        "Fork": "派生会话 (Fork)",
        "Share": "分享",
        "Close Others": "关闭其他",
        "Close to the Right": "关闭右侧所有",
        "Close All": "全部关闭",

        // ========================
        // 输入框“+”添加菜单与二级子项
        // ========================
        "Add Context": "添加上下文",
        "Media": "媒体文件",
        "Mentions": "@ 引用与提及",
        "recently opened": "最近打开",
        "file results": "文件检索结果",
        "Rules": "规则",
        "Conversation": "会话",
        "At mention code block": "@ 引用此代码块",
        "Copy code": "复制代码",
        "Media actions": "媒体操作",
        "Upload Media": "上传媒体文件",
        "Take Screenshot": "截取屏幕",
        "Upload from Computer": "从电脑上传",
        "Paste from Clipboard": "从剪贴板粘贴",
        "Files & Folders": "文件与文件夹",
        "Git Commits": "Git 提交记录",
        "Problems & Diagnostics": "代码问题与诊断",
        "Terminal Sessions": "终端会话",
        "Docs & Knowledge": "文档与知识库",
        "Past Conversations": "历史会话",
        "Rules & Workflows": "规则与工作流",

        // ========================
        // 顶栏与应用标题 (用户定制)
        // ========================
        "Antigravity": "谷歌正重力",
        "谷歌重力反": "谷歌正重力",
        "File": "文件",
        "View": "视图",
        "Window": "窗口",
        "Help": "帮助",
        "Create Project": "创建项目",
        "Command Palette": "命令面板",
        "Close Window": "关闭窗口",
        "Reload": "重新加载",
        "Force Reload": "强制重新加载",
        "Toggle Developer Tools": "切换开发者工具",
        "Actual Size": "实际大小",
        "Zoom In": "放大",
        "Zoom Out": "缩小",
        "Reset Zoom": "重置缩放",
        "Toggle Full Screen": "切换全屏",
        "Minimize": "最小化",
        "Zoom": "最大化",

        // ========================
        // 设置面板 (图 1 深度汉化补充)
        // ========================
        "Application": "应用设置",
        "Shortcuts": "快捷键",
        "Provide Feedback": "意见反馈",
        "Not in Project": "非项目会话",
        "Configure agent execution, queued message delivery, and permissions.": "配置智能体执行机制、队列消息分发策略与安全权限。",
        "Execution": "执行与消息机制",
        "Queued Messages": "队列消息",
        "Configure when follow-up messages are sent.": "配置后续追加消息的发送与处理时机。",
        "Keyboard shortcuts": "键盘快捷键",
        "Queue": "入队排队",
        "Send Immediately": "立即发送",
        "Global Permissions": "全局权限管理",
        "Security Preset": "安全预设模式",
        "Controls the actions the agent can take.": "控制智能体允许自主执行的操作范围。",
        "Learn more about Turbo mode": "了解关于 Turbo 极速模式的详情",
        "Turbo Mode": "Turbo 极速模式",
        "Tool Permissions": "工具调用权限",
        "Modify permissions for file, terminal, and MCP tools.": "配置代码文件、终端命令及 MCP 扩展工具的访问授权。",
        "Open": "打开配置",
        "Agent Behavior": "智能体行为偏好",
        "Artifact Review Policy": "交付产物审查策略",
        "Whether the agent asks you to review its documents.": "设置智能体在生成交付文档时是否主动向您申请审查确认。",
        "Network Permissions": "网络访问权限",
        "Network Access Rules": "网络访问白名单规则",

        // ========================
        // 侧边栏、主导航与全局面板
        // ========================
        "New Conversation": "新建会话",
        "Conversation History": "会话历史",
        "Open Conversation History": "打开会话历史",
        "Select Next Conversation": "选择下一会话",
        "Select Previous Conversation": "选择上一会话",
        "Projects": "项目管理",
        "Scheduled Tasks": "计划任务",
        "Skills & Customizations": "技能与定制",
        "Settings": "系统设置",
        "Feedback": "意见反馈",
        "Standalone": "独立会话",
        "Install IDE": "安装 IDE",
        "All Conversations": "全部会话",
        "Conversations": "会话列表",
        "No conversations yet": "暂无会话记录",
        "Display Options": "界面显示选项",
        "Create New Project": "创建新项目",
        "Project options": "项目选项",
        "New Conversation in Project": "在项目中新建会话",
        "More options": "更多选项",
        "More actions": "更多操作",
        "Pin conversation": "置顶会话",
        "Stop execution": "停止执行",
        "Archive conversation": "归档会话",
        "Load older messages": "加载更早的历史消息",
        "No more older messages": "没有更早的历史消息了",

        // ========================
        // 顶部操作栏与辅助工作区
        // ========================
        "Files Changed": "文件变更",
        "Changes Overview": "变更总览",
        "Background Tasks": "后台任务",
        "Subagents": "子智能体",
        "Artifacts": "产物文档",
        "Terminal": "终端控制台",
        "Terminals": "终端列表",
        "Agent": "智能体",
        "Planning": "架构规划模式",
        "Planning Mode": "规划决策模式",
        "Fast": "快速模式",
        "Inherit": "继承模型配置",
        "Model Selection": "模型选择",
        "Good response": "回答满意",
        "Bad response": "回答不满意",
        "Undo changes up to this point": "撤销更改至此处",
        "View full transcript": "查看完整推理记录",
        "Show Plan": "展开方案",
        "Hide Plan": "折叠方案",
        "Running command": "正在执行系统命令",
        "Command execution": "命令执行",
        "Directory analysis": "目录结构分析",
        "File edit": "编辑代码文件",
        "Viewing file": "读取文件内容",
        "Web search": "联网检索信息",

        // ========================
        // 规划模式与人机审查 (Review)
        // ========================
        "Implementation Plan": "架构实施方案 (Implementation Plan)",
        "User Review Required": "待人工审查事项 (User Review Required)",
        "Open Questions": "待确认疑问 (Open Questions)",
        "Proposed Changes": "拟定技术改动方案 (Proposed Changes)",
        "Verification Plan": "验收与验证方案 (Verification Plan)",
        "Automated Tests": "自动化测试清单",
        "Manual Verification": "人工验证指引",
        "Approve": "批准执行",
        "Approve Plan": "批准实施方案",
        "Proceed": "继续执行",
        "Request Changes": "提出修改要求",
        "Reject": "驳回",

        // ========================
        // 交互按钮与通用表单
        // ========================
        "Cancel": "取消",
        "Save": "保存",
        "Close": "关闭",
        "Delete": "删除",
        "Edit": "编辑",
        "Copy": "复制",
        "Copied": "已复制到剪贴板",
        "Retry": "重试",
        "Allow": "允许",
        "Deny": "拒绝",
        "Always Allow": "始终允许",
        "Always Deny": "始终拒绝",
        "Ask": "询问",
        "Approve": "批准",
        "Skip": "跳过",
        "Submit": "提交",
        "Confirm": "确认",
        "Back": "返回",
        "Next": "下一步",
        "Done": "完成",
        "Clear": "清空",
        "Reset": "重置",
        "Apply": "应用",
        "Discard Changes": "放弃更改",
        "Revert File": "还原此文件",

        // ========================
        // 子智能体与后台任务监视
        // ========================
        "Running": "正在运行",
        "Idle": "空闲待命",
        "Completed": "已完成",
        "Failed": "执行失败",
        "Cancelled": "已取消",
        "Kill Task": "终止任务",
        "Kill All": "终止全部任务",
        "Send Input": "发送标准输入",
        "View Logs": "查看执行日志",
        "Active tasks": "运行中任务",
        "No tasks running": "暂无正在运行的任务",

        // ========================
        // 设置中心: 分类与屏幕 (Screens)
        // ========================
        "General": "通用偏好",
        "Appearance": "外观与主题",
        "Models": "模型与推理",
        "Notifications": "通知提醒",
        "Account": "账号与身份",
        "Customizations": "规则与技能扩展",
        "App": "客户端设置",
        "Developer": "开发者高级选项",
        "Browser": "浏览器集成与测试",
        "Editor": "代码编辑器",
        "Tab": "智能补全 (Tab)",
        "Labs": "实验性功能实验室",
        "Global Settings": "全局统一设置",
        "Project-Level Settings": "当前项目特定设置",

        // ========================
        // 设置中心: 配置项标签与说明
        // ========================
        "Tool Execution Policy": "工具运行鉴权策略",
        "Specifies when the agent requires confirmation before executing terminal commands.": "指定智能体在执行终端命令前是否需要用户人工审核确认。",
        
        "always-proceed": "自动放行 (免确认)",
        "request-review": "逐项询问 (人工确认)",
        "proceed-in-sandbox": "沙箱隔离安全执行",
        "strict": "严格封锁模式",
        "allow": "始终允许",
        "ask": "每次询问",
        "deny": "彻底禁止",
        "agent-decides": "由智能体自主决策",
        "asks-for-review": "主动发起人工审查",

        "Always Proceed": "自动放行 (免审批)",
        "Agent never asks for review. This maximizes the autonomy of the Agent, but also has the highest risk of the Agent operating over unsafe or injected Artifact content.": "智能体永远不主动申请人工确认。这能最大化自主执行效率，但在面对不可信或包含提示词注入风险的内容时具有最高安全风险。",

        "Always Ask": "逐项询问 (人工确认)",
        "Agent always asks for review.": "智能体在执行关键变动前始终主动请求人工审查确认。",

        "Allow List Terminal Commands": "终端命令白名单",
        "The agent auto-executes commands matched by an allow list entry.": "匹配白名单规则的终端命令将被自动直接执行，无需人工二次审批。",

        "Deny List Terminal Commands": "终端命令黑名单",
        "The agent asks for permission before executing commands matched by a deny list entry.": "匹配黑名单规则的终端命令在执行前必须强制向用户申请明确授权。",

        "Agent Auto-Fix Lints": "代码检查 (Lint) 自动修复",
        "Give the agent awareness of lint errors created by its edits so it can fix them without explicit prompting.": "使智能体能够自动捕获其代码修改产生的 Lint 语法与规范检查错误，并在无需用户明确提醒的情况下主动修复。",

        "Strict Mode": "安全严格模式",
        "Enforce settings that prevent the agent from autonomously running targeted exploits and require human review for all agent actions. Visit antigravity.google/docs/strict-mode for details.": "开启严格安全基线，禁止智能体自主执行任何未授权的高风险操作，所有行为均须人工逐一审批。详情访问 antigravity.google/docs/strict-mode。",

        "Agent Non-Workspace File Access": "跨工作区外文件读写权限",
        "Allow the agent to automatically view and edit files outside the current workspace. Use with caution: this gives the agent access to additional potentially-relevant information, but also allows the agent to access credential files, secrets, and other files outside of the workspace that could be targeted in prompt injection attacks or other exploits by malicious actors.": "允许智能体自动读取和编辑当前工作区以外的文件。请谨慎开启：这能为智能体提供更多系统级上下文，但也意味着智能体可以访问工作区之外的敏感凭证、密钥文件，存在被恶意提示词注入利用的安全风险。",

        "Enable Terminal Sandbox": "启用终端安全沙箱",
        "Run terminal commands with sandbox restrictions.": "在具有系统资源限制的安全沙箱中隔离运行终端命令。",

        "Sandbox Allow Network": "允许沙箱网络外联",
        "Allow sandboxed commands to make network requests.": "允许沙箱隔离环境中的命令访问外部网络（如下载依赖、调用接口等）。",

        "Enable Shell Integration": "启用终端 Shell 集成",
        "Use the IDE's shell integration to detect and report terminal command execution. When disabled, the agent uses its own shell. Restart the application for this to take effect.": "利用 IDE 的终端集成层来追踪并上报命令执行状态。关闭后智能体将使用独立子进程 Shell。修改后需重启生效。",

        "Review Policy": "交付产物审查策略",
        "Specifies the agent's behavior when asking for review on artifacts, which are documents it creates to enable a richer conversation experience.": "指定智能体在创建交付文档（如实施方案、架构图表等产物）时的人机审查确认行为。",

        "Enable Sounds for Agent": "任务生成提示音",
        "Play a sound when the agent finishes generating a response.": "当智能体完成推理与代码生成时播放提示音。",

        "Enable Notifications for Agent": "桌面系统通知提醒",
        "Show browser notifications when your action is needed or execution finishes.": "当需要人工交互确认或后台任务执行完毕时弹出系统通知。",

        "Auto-Expand Changes Overview": "自动展开文件变更概览",
        "Automatically expand the Changes Overview toolbar when the agent finishes generating a response.": "当智能体完成响应生成后，自动展开文件变更概览工具栏。",

        "Conversation History": "参考历史会话知识",
        "Let the agent access past conversations to inform its responses.": "允许智能体读取以往的历史会话内容来辅助当下的分析与决策。",

        "Knowledge": "智能知识库",
        "Let the agent access its knowledge base to inform its responses and automatically generate knowledge items in the background. Turning this off prevents the agent from accessing existing knowledge items, but doesn't delete them.": "允许智能体读取知识库并在后台自动沉淀提炼经验条目。关闭此项仅阻止智能体调用知识库，不会删除已保存的条目。",

        "Auto-Open Edited Files": "自动打开编辑过的文件",
        "Open files in the background if the agent creates or edits them": "当智能体创建或修改了代码文件时，自动在编辑器后台标签页中打开它们。",

        "Open Agent on Reload": "重启保持面板开启",
        "Open the agent panel on window reload": "窗口重载或刷新时自动保持展开智能体侧边面板。",

        "Verbose Agent Chat": "完整思维链展示 (Verbose)",
        "Display and preserve intermediate thinking steps.": "展示并完整保留智能体在执行任务过程中的全部中间思考推演步骤。",

        "Conversation Width": "会话阅读宽度限制",
        "Configure the maximum width of the conversation panel.": "配置主聊天视图区域的最大水平宽度。",

        "Markdown Artifact Width": "Markdown 产物渲染宽度",
        "Configure the default width of markdown artifacts.": "配置 Markdown 交付物在画布上的默认显示宽度。",

        "Table Width": "数据表格渲染宽度",
        "Configure the default width of tables.": "配置数据表格在会话中的默认渲染宽度。",

        "Suggestions in Editor": "编辑器实时代码补全",
        "Show suggestions when typing in the editor": "在代码编辑器中敲击键盘时实时展示 AI 代码补全建议。",

        "Tab to Jump": "按 Tab 快速跳转编辑点",
        "Predict the location of your next edit and navigate you there with a tab keypress.": "预测下一处可能修改的代码位置，只需敲击一次 Tab 键即可智能对齐光标。",

        "Tab to Import": "按 Tab 自动补齐 Import",
        "Quickly add and update imports with a tab keypress.": "按 Tab 键自动在文件头部补齐或更新缺失的依赖库导入语句。",

        "Tab Speed": "补全生成速率",
        "Set the speed of tab suggestions": "设置 Tab 代码补全建议的生成与展示响应延迟。",

        "Highlight After Accept": "采纳补全后高亮标记",
        "Highlight newly inserted text after accepting a Tab completion.": "采纳 Tab 代码补全后，短暂高亮展示刚刚插入的代码内容。",

        "Tab Gitignore Access": "补全允许访问 .gitignore 文件",
        "Allow Tab to view and edit the files in .gitignore. Use with caution if your .gitignore lists files containing credentials, secrets, or other sensitive information.": "允许代码补全引擎检索 .gitignore 中的忽略文件。若其中包含账号密钥等敏感信息，请谨慎开启。",

        "Enable Browser Tools": "启用浏览器自动化工具",
        "Let the agent use browser tools to open URLs, read web pages, and interact with browser content. This gives the agent access to important (and often critical) knowledge and methods of validation, but any browser integration does increase exposure to external malicious parties for security exploits.": "允许智能体使用浏览器工具访问网址、阅读公网文档或验证网页交互。这赋予了智能体关键的验证能力，但也会相应增加网络安全暴露面。",

        "Browser Javascript Execution Policy": "浏览器脚本执行权限",
        "Controls whether the agent can run custom JavaScript to automate complex browser actions.": "控制智能体在浏览器自动化操作中是否允许执行自定义 JavaScript 脚本。",

        "Chrome Binary Path": "Chrome/Chromium 核心路径",
        "Path to the Chrome/Chromium executable. Leave empty for auto-detection.": "指定 Chrome 或 Chromium 的二进制执行文件绝对路径。留空则系统自动探测。",

        "Browser User Profile Path": "浏览器用户缓存配置路径",
        "Custom path for the browser user profile directory. Leave empty for default (~/.gemini/antigravity-browser-profile).": "自定义浏览器的数据缓存目录。留空使用默认路径 (~/.gemini/antigravity-browser-profile)。",

        "Browser CDP Port": "浏览器调试端口 (CDP)",
        "Port number for Chrome DevTools Protocol remote debugging. Leave empty for default (9222).": "用于 Chrome DevTools 协议远程通信的端口。留空默认使用 9222。",

        "Include Jetski Default Customizations": "加载内置技能库",
        "Include default customizations, such as default skills.": "自动加载官方预设的默认技能扩展与规约规则。",

        "Prevent Sleep": "防休眠保持常驻",
        "Prevent the computer from sleeping while the app is running.": "当智能体正在运行或客户端开启时，阻止操作系统自动进入休眠状态。",

        "Keep In Menu Bar": "托盘后台驻留",
        "Keep the app accessible from the menu bar and running in the background when all windows are closed.": "在关闭所有窗口后，保持在系统任务栏/托盘中常驻运行。",

        "Automatic Check for Updates": "自动检查软件版本更新",
        "Automatically prompt you to restart the app when a new update is available. When disabled, you can check for updates manually from the app menu.": "当有新版本客户端发布时自动提示重启更新。关闭后可从菜单手动检查更新。",

        "Workspaces": "受信任工作区列表",
        "Folders the automation agents can access.": "允许自动化智能体进行读写与代码操作的项目目录列表。",

        "Access grants": "特殊权限授权列表",
        "Command and file access granted to the automation agents.": "显式授予自动化智能体的特定高危命令与受限系统资源清单。",

        "Inline Actions": "跨会话浮动交互卡片",
        "Show a floating notification card when background conversations need your input. Answer questions, approve commands, and grant permissions without leaving your current conversation. Share feedback at go/inline-actions-feedback.": "当后台运行的会话需要人工输入或审批时显示浮动卡片，无需切换当前会话即可直接答复问题或授权命令。",

        // 外观与主题
        "Theme": "界面主题",
        "Theme Mode": "主题模式",
        "Wide": "宽屏",
        "Normal": "标准",
        "Dark": "深色暗调",
        "Light": "清爽浅色",
        "System": "跟随系统"
    };

    // 2. 占位符匹配
    const PLACEHOLDERS = {
        "Ask anything, @ to mention, / for workflows": "输入任何编程问题，输入 @ 引用上下文，输入 / 触发专属工作流",
        "Search...": "全域搜索...",
        "Search conversations...": "搜索历史会话...",
        "Search tasks...": "搜索任务...",
        "Filter files...": "过滤文件...",
        "Type a command...": "键入控制命令..."
    };

    // 3. 正则动态语序重组与变量插值 (重构为自然中文语序)
    const PATTERNS = [
        { regex: /^Select model, current:\s*(.+)$/i, replace: (m, p1) => `切换推理模型 (当前: ${p1})` },

        { regex: /^Thought for (\d+)s$/, replace: (m, p1) => `思考了 ${p1} 秒` },
        { regex: /^Thought for (\d+)m$/, replace: (m, p1) => `思考了 ${p1} 分钟` },
        { regex: /^Thought for (\d+)m\s+(\d+)s$/, replace: (m, p1, p2) => `思考了 ${p1} 分 ${p2} 秒` },
        { regex: /^Worked for (\d+)s$/, replace: (m, p1) => `工作了 ${p1} 秒` },
        { regex: /^Worked for (\d+)m$/, replace: (m, p1) => `工作了 ${p1} 分钟` },
        { regex: /^Worked for (\d+)m\s+(\d+)s$/, replace: (m, p1, p2) => `工作了 ${p1} 分 ${p2} 秒` },
        { regex: /^Worked for (\d+)h$/, replace: (m, p1) => `工作了 ${p1} 小时` },
        { regex: /^Ran\s+(\d+)\s+commands?$/i, replace: (m, p1) => `执行了 ${p1} 条系统命令` },
        { regex: /^Running\s+(\d+)\s+commands?$/i, replace: (m, p1) => `正在执行 ${p1} 条系统命令` },
        { regex: /^(\d+)\s+files? changed$/i, replace: (m, p1) => `${p1} 个文件已修改` },
        { regex: /^(\d+)\s+subagents?$/i, replace: (m, p1) => `${p1} 个子智能体` },
        { regex: /^Load older messages, showing (\d+) of (\d+)$/i, replace: (m, p1, p2) => `加载更早消息 (当前显示 ${p2} 条中的 ${p1} 条)` },
        { regex: /^Showing (\d+) of (\d+) messages?$/i, replace: (m, p1, p2) => `显示全部 ${p2} 条中的 ${p1} 条消息` }
    ];

    // 4. 防误伤机制 (严格保护代码、编辑器及输入区域)
    const IGNORE_TAGS = new Set(["SCRIPT", "STYLE", "PRE", "CODE", "TEXTAREA"]);

    function shouldIgnore(node) {
        if (!window.__ENABLE_CHINESE__) return true;
        let el = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
        while (el) {
            if (IGNORE_TAGS.has(el.tagName)) return true;
            if (el.classList && (
                el.classList.contains("monaco-editor") ||
                el.classList.contains("prism-code") ||
                el.classList.contains("code-block") ||
                el.classList.contains("cm-editor") ||
                el.getAttribute("data-lexical-editor") !== null
            )) {
                return true;
            }
            if (el.tagName === "DIV" && el.classList && el.classList.contains("markdown-body")) {
                let p = node.parentElement;
                if (p && (p.tagName === "PRE" || p.tagName === "CODE")) return true;
            }
            el = el.parentElement;
        }
        return false;
    }

    function translateText(text) {
        if (!text) return null;
        const trimmed = text.trim();
        if (!trimmed) return null;

        // 1. 精准词典匹配
        if (EXACT_DICT[trimmed]) {
            return text.replace(trimmed, EXACT_DICT[trimmed]);
        }

        // 2. 正则复合模板匹配
        for (const p of PATTERNS) {
            if (p.regex.test(trimmed)) {
                const replaced = trimmed.replace(p.regex, p.replace);
                return text.replace(trimmed, replaced);
            }
        }

        return null;
    }

    function translateTextNode(node) {
        if (shouldIgnore(node)) return;
        const raw = node.nodeValue;
        const translated = translateText(raw);
        if (translated && translated !== raw) {
            node.nodeValue = translated;
        }
    }

    function translateElement(el) {
        if (shouldIgnore(el)) return;

        if (el.placeholder && PLACEHOLDERS[el.placeholder]) {
            el.placeholder = PLACEHOLDERS[el.placeholder];
        }

        const title = el.getAttribute("title");
        if (title) {
            const tr = translateText(title);
            if (tr) el.setAttribute("title", tr);
        }

        const ariaLabel = el.getAttribute("aria-label");
        if (ariaLabel) {
            const tr = translateText(ariaLabel);
            if (tr) el.setAttribute("aria-label", tr);
        }
    }

    function walk(root) {
        if (!root || shouldIgnore(root)) return;
        const walker = document.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT,
            {
                acceptNode: function (node) {
                    if (shouldIgnore(node)) return NodeFilter.FILTER_REJECT;
                    return NodeFilter.FILTER_ACCEPT;
                }
            }
        );

        let current;
        while ((current = walker.nextNode())) {
            if (current.nodeType === Node.TEXT_NODE) {
                translateTextNode(current);
            } else if (current.nodeType === Node.ELEMENT_NODE) {
                translateElement(current);
            }
        }
        ensureTitleIcon();
    }

    // 初次遍历
    if (document.body) {
        walk(document.body);
    } else {
        window.addEventListener("DOMContentLoaded", () => walk(document.body));
    }

    // 动态 DOM 变动监听
    const observer = new MutationObserver((mutations) => {
        if (!window.__ENABLE_CHINESE__) return;
        for (const mutation of mutations) {
            if (mutation.type === "childList") {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === Node.TEXT_NODE) {
                        translateTextNode(node);
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        walk(node);
                    }
                });
            } else if (mutation.type === "characterData") {
                translateTextNode(mutation.target);
            }
        }
    });

    observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
        characterData: true
    });

    

    
    // 监听与动态替换窗口标题
    function updateTitle() {
        if (document.title && document.title.includes("Antigravity")) {
            document.title = document.title.replace(/Antigravity|谷歌重力反/g, "谷歌正重力");
        }
    }
    updateTitle();
    const titleObserver = new MutationObserver(updateTitle);
    const titleEl = document.querySelector('title');
    if (titleEl) {
        titleObserver.observe(titleEl, { childList: true, characterData: true });
    }

    console.log("[Antigravity i18n] 深度专业汉化引擎已激活运行。");
})();
