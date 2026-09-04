# Product Expert

[![Validate](https://github.com/qlhouseClub/product-expert/actions/workflows/validate.yml/badge.svg)](https://github.com/qlhouseClub/product-expert/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/qlhouseClub/product-expert?display_name=tag)](https://github.com/qlhouseClub/product-expert/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

面向真实业务决策的端到端产品专家技能包。它从第一性原理出发，把业务、用户、需求、体验、数据、系统、商业化、组织协同和持续学习连接成一条可追溯的决策链，而不是只生成一份看似完整的 PRD。

## 最近更新

### [v1.1.0](https://github.com/qlhouseClub/product-expert/releases/tag/v1.1.0) — 2026-07-30

- 新增与风险匹配的需求对抗审查：冻结待审方案、构造最强反例、核验关键证据、记录裁决与剩余风险。
- 增强对指标博弈、滥用路径、边界条件、替代方案和不可逆决策的压力测试。
- 默认禁止 Emoji 修饰；界面图标优先复用批准图标集，新增图标以项目一致的 SVG 语法为主。

### [v1.0.0](https://github.com/qlhouseClub/product-expert/releases/tag/v1.0.0) — 2026-07-23

- 首个公开稳定版本，提供产品发现、业务分析、需求拆解、规划、数据、技术方案和跨平台适配。

## 核心能力

- 第一性原理与业务建模
- 市场、商业模式、定价、包装、GTM 与增长
- 用户研究、JTBD、机会识别与需求拆解
- 需求对抗审查、反例压力测试、滥用与指标博弈审查
- 产品规划、优先级、路线图、原型和验证
- 指标契约、实验设计、留存与 SaaS 分析
- 领域模型、数据库、API、事件与埋点设计
- 产品运营、决策权、干系人协同与发布治理
- AI 产品、RAG、上下文工程与 Agent 工作流
- 预测校准、决策复盘与产品知识连续性

## 设计原则

1. 从需要做出的决策开始，而不是从用户提出的功能开始。
2. 区分事实、观察、推断和假设。
3. 保持从业务目标到发布决策的完整追溯关系。
4. 根据风险和可逆性决定研究与验证深度。
5. 一个任务选择一个主模式，只加载真正影响决策的支持模块。
6. 不把行业基准、框架默认值或统计阈值当作普遍真理。
7. 默认禁止使用 Emoji 进行修饰、标记或充当界面图标；只有用户对当前项目明确提出要求时才放行。
8. 图标优先复用已批准的图标集；需要新增时以 SVG 为主，并在同一项目中统一来源、网格、描边或填充、线宽、端点、转角、光学尺寸、颜色与动效语言。
9. 重要需求必须经过与风险匹配的独立对抗审查，保留冻结版本、最强反例、处置结果和剩余风险。

## 工作模式

技能会根据任务自动选择诊断、战略、商业化、发现、定义、需求对抗审查、规划、验证、分析、产品运营、产品判断、系统设计、AI 系统、审计或完整产品蓝图模式。

简单问题不会被强制扩展为完整产品方案；跨领域问题则会共享同一套证据、指标、实体和决策记录，避免模块之间互相矛盾。

## 目录结构

```text
product-expert/
├── SKILL.md                  # 主入口、模式路由和质量门槛
├── agents/openai.yaml        # Codex 界面元数据
├── .github/workflows/        # 自动验证与版本发布
├── references/               # 按任务需要加载的专业模块
│   ├── first-principles-and-business.md
│   ├── commercialization-and-growth.md
│   ├── discovery-and-requirements.md
│   ├── planning-and-validation.md
│   ├── product-analytics-and-experiments.md
│   ├── data-and-architecture.md
│   ├── organization-and-product-ops.md
│   ├── delivery-and-governance.md
│   ├── product-judgment-and-continuity.md
│   ├── ai-product-extension.md
│   ├── ai-context-and-agents.md
│   └── artifact-templates.md
├── platforms/                # 跨平台元数据与扣子桥接提示词
├── scripts/build_compat.py   # 生成 TRAE、OpenAI Plugin、扣子和便携包
├── COMPATIBILITY.md          # 跨平台安装、限制与维护规则
├── CONTRIBUTING.md           # 贡献规则
├── SECURITY.md               # 私密安全报告
└── LICENSE                   # MIT 许可证
```

## 跨平台安装

仓库同时适配 Codex、ChatGPT、TRAE Work、Hermes、OpenClaw 和扣子。请选择实际使用的平台；不需要把所有版本都安装一遍。

不想在本地构建时，可以直接从 [GitHub Releases](https://github.com/qlhouseClub/product-expert/releases) 下载 TRAE、OpenAI Plugin、扣子或便携 ZIP。

| 平台 | 推荐安装方式 | 安装后形态 |
|---|---|---|
| Codex / ChatGPT 桌面端 | 克隆到个人技能目录 | 原生 Agent Skill |
| ChatGPT Work / 团队 | 生成并安装 Plugin | OpenAI Plugin |
| TRAE Work / SOLO / IDE | 克隆到技能目录，或上传 Release ZIP | 原生 Skill |
| Hermes Agent | 克隆到 Hermes 技能目录 | 原生 Skill |
| OpenClaw | 使用 Git 安装命令 | 原生 Agent Skill |
| 扣子 / Coze | 导入提示词与知识库包 | 提示词 + RAG 知识库 |

### Codex / ChatGPT 桌面端

Windows PowerShell：

```powershell
$skillDir = "$env:USERPROFILE\.codex\skills\product-expert"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/product-expert.git $skillDir
```

macOS / Linux：

```bash
skill_dir="$HOME/.codex/skills/product-expert"
mkdir -p "$(dirname "$skill_dir")"
git clone https://github.com/qlhouseClub/product-expert.git "$skill_dir"
```

若希望与其他兼容 Agent 共用技能，也可以把目标根目录改为 `~/.agents/skills/`。重启或刷新客户端后，即可通过“使用产品专家……”等自然语言触发。

### ChatGPT Work / 团队 Plugin

先克隆仓库并生成 OpenAI Plugin：

```powershell
git clone https://github.com/qlhouseClub/product-expert.git
Set-Location .\product-expert
python .\scripts\build_compat.py --platform openai
codex.cmd plugin marketplace add .\dist\openai-marketplace
```

macOS / Linux 最后一条命令使用：

```bash
codex plugin marketplace add ./dist/openai-marketplace
```

重启 ChatGPT 桌面端，在 Plugins 中安装“产品专家”。需要团队使用时，可从插件详情页分享到 ChatGPT 工作区。独立插件包为 `dist/openai/product-expert-plugin.zip`。

### TRAE Work / SOLO / IDE

Windows 国内版全局安装：

```powershell
$skillDir = "$env:USERPROFILE\.trae-cn\skills\product-expert"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/product-expert.git $skillDir
```

国际版把 `.trae-cn` 改为 `.trae`。项目级安装则克隆或复制到：

```text
<项目>/.trae/skills/product-expert/
```

也可以下载 Release 中的 `product-expert.zip`，在 TRAE 的“设置 → 技能与命令/规则和技能 → 创建或上传技能”中导入。自行构建命令为：

```powershell
python .\scripts\build_compat.py --platform trae
```

### Hermes Agent

将完整仓库安装到 Hermes 个人技能目录，确保 `references/` 等引用文件一并保留。

Windows PowerShell：

```powershell
$skillDir = "$env:USERPROFILE\.hermes\skills\product-expert"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/product-expert.git $skillDir
```

macOS / Linux：

```bash
skill_dir="$HOME/.hermes/skills/product-expert"
mkdir -p "$(dirname "$skill_dir")"
git clone https://github.com/qlhouseClub/product-expert.git "$skill_dir"
```

安装后新建会话；若希望当前会话立即刷新，可在 Hermes 中执行 `/reset`。

### OpenClaw

安装到当前工作区：

```text
openclaw skills install git:qlhouseClub/product-expert@main
```

安装为所有本地 Agent 共用的全局技能：

```text
openclaw skills install git:qlhouseClub/product-expert@main --global
```

从已克隆的仓库根目录安装：

```text
openclaw skills install . --as product-expert
```

### 扣子 / Coze

扣子不直接读取 Agent Skill 目录。可以下载 Release 中的 `product-expert-coze.zip`，或自行生成：

```powershell
git clone https://github.com/qlhouseClub/product-expert.git
Set-Location .\product-expert
python .\scripts\build_compat.py --platform coze
```

然后：

1. 将 `dist/coze/product-expert/agent-prompt.md` 粘贴到智能体系统提示词。
2. 新建知识库，上传 `dist/coze/product-expert/knowledge/` 中的全部 Markdown 文件。
3. 将知识库绑定到智能体并启用检索。
4. 按需要配置联网、数据库或其他外部插件与工作流。

### 生成全部平台包

```powershell
python .\scripts\build_compat.py --platform all
```

完整的平台边界、目录说明、维护规则和官方依据见 [COMPATIBILITY.md](COMPATIBILITY.md)。

## 使用示例

- “帮我判断这个需求背后真正的业务问题，并决定是否应该做。”
- “为这个 B2B SaaS 设计定价、套餐和进入市场策略。”
- “把这份访谈材料转成机会地图和可验证的产品需求。”
- “诊断留存下降，但先不要写完整 PRD。”
- “为这个功能设计领域模型、数据库、API 和埋点。”
- “设计一个带 RAG 和人工审核机制的 AI 客服产品。”
- “审查这份产品方案，找出证据、指标和交付链路中的断点。”

## Token 与上下文策略

`SKILL.md` 只保留共同原则、路由和质量门槛。商业化、分析、数据、组织和 AI 等专业知识放在独立引用模块中，按需加载。知识库总量不会在每次任务中全部进入上下文。

## 研究来源

部分能力经过 [PM Brain](https://github.com/andreaskelm/pm-brain)、[18F Guides](https://github.com/18F/guides)、[GrowthBook](https://github.com/growthbook/growthbook)、[OpenFeature](https://github.com/open-feature/spec) 和 [Open Data Contract Standard](https://github.com/bitol-io/open-data-contract-standard) 的交叉研究。技能只吸收通用思想，并保留对许可、版本和适用边界的判断。

## 状态

- YAML 元数据校验通过
- 本地引用链接校验通过
- 已进行跨商业化、AI、数据和组织协同的前向测试
- 已生成并校验 TRAE、OpenAI Plugin、扣子和便携适配产物

## 许可、贡献与安全

- 使用条款：[MIT License](LICENSE)
- 第三方研究与许可边界：[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- 贡献方式：[CONTRIBUTING.md](CONTRIBUTING.md)
- 私密报告安全问题：[SECURITY.md](SECURITY.md)
