# 清醒职业教练 Career Coach

一个可移植、可审计、可直接安装的职业教练智能体，面向职业方向、转型、晋升、求职与 Offer 决策、领导力、工作倦怠和长期职业资本建设。

它不靠鸡血，也不会只用问题把决定重新推给你。它会区分事实、判断和未知信息，在需要时给出明确建议，再把大决定缩小成可验证、可回退的下一步。

## 复制一个链接，交给智能体安装

把下面这条链接直接发给 **Codex 或 WorkBuddy**。链接本身是一份机器可读的安装说明，接收它的智能体会识别当前平台、安装并验证：

```text
https://raw.githubusercontent.com/dexterqiu-collab/life-coach/main/INSTALL.md
```

如果对方没有把“只有一个链接”理解成安装请求，就在链接前加一句：`安装这个职业教练智能体：`。

## 各平台入口

| 平台 | 推荐入口 | 部署结果 |
|---|---|---|
| Codex | [直接安装 Skill](https://github.com/dexterqiu-collab/life-coach/tree/main/skills/career-coach) | 用户级 `career-coach` Skill，可自动触发或用 `$career-coach` 调用 |
| WorkBuddy | 将上面的 `INSTALL.md` 链接发给 WorkBuddy；也可下载 Release 中的 `career-coach-workbuddy-skill.zip` | 用户级 Skill |
| WorkBuddy / CodeBuddy 独立智能体 | 下载 Release 中的 `career-coach-workbuddy-agent.zip` | 可在 Agent/专家列表中选择的职业教练角色，同时携带 Skill |
| 豆包 | 打开 [豆包系统提示词](https://raw.githubusercontent.com/dexterqiu-collab/life-coach/main/platforms/doubao/SYSTEM_PROMPT.md)，全选复制到“创建智能体 → 设定描述” | 独立职业教练智能体 |
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
├── INSTALL.md                         # 发给智能体的机器可读安装入口
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

创建 `v*` 标签后，GitHub Actions 会构建 Codex、WorkBuddy Skill、WorkBuddy Agent 和豆包四种发布产物，并生成 SHA-256 校验文件。

## License

[MIT](LICENSE) © Dexter
