# 精英职业教练 Elite Career Coach

一个可移植、可审计、可直接安装的职业教练智能体，基于 Dexter 的 `elite-life-coach` 综合系统重构，面向职业方向、转型、晋升、求职与 Offer 决策、领导力、工作倦怠、高绩效行为改变和长期职业资本建设。

它保留原系统的五位教练方法论、七个核心模型、五阶段会谈、表达 DNA、行动问责和安全边界，同时加入职业决策、事实核验与可逆实验。它不靠鸡血，也不会只用问题把决定重新推给你。

**官网与一键安装：** [life-coach-agent.dexter797.chatgpt.site](https://life-coach-agent.dexter797.chatgpt.site)

## 复制一句话，交给智能体安装

打开官网，复制首页的安装指令；也可以直接复制这一句到 **Codex / ChatGPT 桌面端**：

```text
阅读 https://life-coach-agent.dexter797.chatgpt.site/install.txt，帮我安装 Life Coach 插件，并创建一个新的职业教练任务。
```

智能体会读取机器可读安装协议，添加 `dexter-coaching` marketplace、安装 `life-coach` 插件、验证 `career-coach` Skill，并在新任务里开始第一次教练对话。

仓库同时保留一个跨平台安装协议，供 WorkBuddy 等智能体使用：

把下面这条链接直接发给 **Codex 或 WorkBuddy**。链接本身是一份机器可读的安装说明，接收它的智能体会识别当前平台、安装并验证：

```text
https://raw.githubusercontent.com/dexterqiu-collab/life-coach/main/INSTALL.md
```

如果对方没有把“只有一个链接”理解成安装请求，就在链接前加一句：`安装这个职业教练智能体：`。

## 各平台入口

| 平台 | 推荐入口 | 部署结果 |
|---|---|---|
| Codex / ChatGPT 桌面端 | [官网一键安装](https://life-coach-agent.dexter797.chatgpt.site) | `life-coach` 插件，内含可自动触发或用 `$career-coach` 调用的 Skill |
| Codex Skill 兼容模式 | [直接导入 Skill](https://github.com/dexterqiu-collab/life-coach/tree/main/skills/career-coach) | 用户级 `career-coach` Skill |
| WorkBuddy | 将上面的 `INSTALL.md` 链接发给 WorkBuddy；也可下载 Release 中的 `career-coach-workbuddy-skill.zip` | 用户级 Skill |
| WorkBuddy / CodeBuddy 独立智能体 | 下载 Release 中的 `career-coach-workbuddy-agent.zip` | 可在 Agent/专家列表中选择的职业教练角色，同时携带 Skill |
| 豆包 | 打开 [豆包系统提示词](https://raw.githubusercontent.com/dexterqiu-collab/life-coach/main/platforms/doubao/SYSTEM_PROMPT.md)，全选复制到“创建智能体 → 设定描述” | 独立“精英职业教练”智能体 |
| 其他支持 Agent Skills 的工具 | 导入 [`skills/career-coach`](skills/career-coach) | 标准 `SKILL.md` 能力包 |

> 豆包目前没有通用的 GitHub `SKILL.md` 链接安装协议，因此无法诚实地承诺“粘贴 URL 后自动创建另一个智能体”。仓库已经把豆包版压成单文件系统提示词，实际操作只需创建智能体并粘贴一次。

## 手动安装

macOS / Linux：

```bash
git clone --depth 1 https://github.com/dexterqiu-collab/life-coach.git
cd life-coach
bash scripts/install.sh auto
```

Windows PowerShell：

```powershell
git clone --depth 1 https://github.com/dexterqiu-collab/life-coach.git
cd life-coach
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 -Target auto
```

可选目标为 `codex`、`workbuddy`、`codebuddy` 或 `all`。安装器默认不会覆盖已有版本；显式传入 `--force` 或 `-Force` 时，会先保留带时间戳的备份。

## 能做什么

- 澄清职业方向，识别真正的约束、优势和机会成本
- 比较 Offer、岗位、公司、城市或创业选项
- 设计低成本职业实验，减少“大赌注式转型”
- 制定晋升、求职、转型和 30/60/90 天计划
- 处理管理挑战、沟通冲突、绩效困境和工作倦怠
- 建立每周复盘与问责机制，让行动持续发生
- 当薪酬、行业或公司事实会改变建议时，先研究再判断

## 方法论系统

系统综合了马歇尔·戈德史密斯、布兰登·伯查德、比尔·坎贝尔、托尼·罗宾斯、罗宾·夏玛的方法论，以及 ICF 风格的伦理、倾听、觉察、行动与问责原则。运行时按场景选择最相关的模型：

1. 前馈式成长
2. 状态—行动闭环
3. 信任—坦诚—人文三角
4. 专注时间护城河
5. 信念—证据区分
6. 五阶段转化流程
7. 刻意练习与问责

这些是经过整理的实用视角，不代表 ICF 认证、任何人物背书或普遍科学定律。智能体会明确方法局限，不把真实约束粗暴归因于“心态”。

## 试用提示词

```text
我工作 6 年，收入还可以，但越来越没有成长感。请不要只问我问题，先帮我判断这是应该换团队、换公司还是换赛道。
```

```text
我有两个 Offer，请帮我做决策。先告诉我还缺哪些关键信息，然后给出明确倾向和两周内可验证的动作。
```

```text
我想在 6 个月内完成晋升。请根据我提供的背景，做一份有证据指标的晋升计划和每周复盘模板。
```

## 仓库结构

```text
life-coach/
├── .agents/plugins/marketplace.json   # Codex marketplace 入口
├── INSTALL.md                         # 发给智能体的机器可读安装入口
├── plugins/life-coach/                # 可由 Codex 安装的正式插件
│   ├── .codex-plugin/plugin.json
│   └── skills/career-coach/
├── skills/career-coach/               # Codex / Agent Skills 标准包
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/
├── agents/career-coach.md             # WorkBuddy / CodeBuddy 独立 Agent
├── .codebuddy-plugin/plugin.json      # WorkBuddy / CodeBuddy 插件清单
├── platforms/doubao/SYSTEM_PROMPT.md  # 豆包单文件系统提示词
├── scripts/                            # 安装、打包与校验
└── tests/                              # 结构与分发包测试
```

## 设计原则

- **建议与提问并重**：用户要判断时给判断，不把所有责任伪装成“教练式提问”。
- **原系统完整迁移**：保留七个模型、五阶段流程、直接而温暖的表达与行动问责。
- **事实与假设分离**：对时效信息优先研究；无法研究时明确标出假设。
- **小实验优先**：高不确定且可逆的职业问题，优先用真实行动获取信息。
- **渐进式加载**：核心 Skill 保持精简，只按场景读取相关框架与模板。
- **安全边界清晰**：不冒充持证心理、医疗、法律或财务专业人士。

## 开发与发布

```bash
python3 scripts/validate.py
python3 scripts/build_packages.py
python3 -m unittest discover -s tests -v
```

提升 `SKILL.md` 中的语义化版本并推送到 `main` 后，GitHub Actions 会在该版本首次出现时自动打标签，构建 Codex 插件、Codex Skill、WorkBuddy Skill、WorkBuddy Agent 和豆包五类发布产物，并生成 SHA-256 校验文件。

## License

[MIT](LICENSE) © Dexter
