# Interaction Design Expert / 交互设计专家

[![Validate](https://github.com/qlhouseClub/interaction-design-expert/actions/workflows/validate.yml/badge.svg)](https://github.com/qlhouseClub/interaction-design-expert/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/qlhouseClub/interaction-design-expert?display_name=tag)](https://github.com/qlhouseClub/interaction-design-expert/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个把产品目标转化为完整行为系统的交互设计技能包。它覆盖用户心智、信息架构、任务流、状态机、交互规则、跨端模式、无障碍、认知与情绪、原型验证、交付和 Design QA，而不止生成一排快乐路径界面。

## 最近更新

### [v0.2.0](https://github.com/qlhouseClub/interaction-design-expert/releases/tag/v0.2.0) — 2026-07-30

- 引入服务于掌握感、自主性和有意义选择的游戏思维，避免把游戏化简化成积分、徽章与连续签到。
- 加强布局推演、阅读习惯、第一感、显性与隐性视觉引导，以及用户、业务、风险、时机和频率之间的信息权重判断。
- 扩展分层渐进、挑战反馈、恢复机制、业务强调和注意力架构的交互设计方法。
- 默认禁止 Emoji 修饰；图标优先复用批准图标集，新增图标以项目一致的 SVG 语法为主。

### v0.1.0 — 2026-07-28

- 初始版本，建立任务流、状态机、交互契约、跨端模式、无障碍、原型验证和设计 QA 主链路。

## 核心能力

- 从目标、对象和规则出发，而不是从控件出发
- 用户心智模型、任务分析、信息架构和对象模型
- 主路径、分支、取消、中断、异常与恢复
- 完整状态矩阵和可实现的行为契约
- 表单、搜索、导航、选择、命令、手势与微交互
- 认知负荷、信任、情绪体验和伦理边界
- 游戏思维、目标与反馈循环、进度、选择、掌握感和体验增强
- 布局推演、阅读与视觉习惯、显性与隐性引导、信息权重和业务强调
- 键盘、焦点、语义、读屏、缩放与 reduced motion
- 风险匹配的原型、可用性研究、指标和证据门槛
- 既有设计系统、交互模式和 Design Token 的持续遵循
- 工程交付、验收示例、设计走查和偏差治理

## 重要默认值

- 快乐路径不是完整交互
- 高频操作优先效率与克制，低频高风险操作优先解释与恢复
- 手势、悬停、颜色和动效不能成为唯一的信息或操作渠道
- 共用 Design Token、组件和全局行为默认只读
- 默认禁止使用 Emoji 进行修饰、标记或充当界面图标；只有用户对当前项目明确提出要求时才放行
- 图标优先复用已批准的图标集；需要新增时以 SVG 为主，并在同一项目中统一来源、网格、描边或填充、线宽、端点、转角、光学尺寸、颜色与动效语言
- 研究深度由风险、频率、可逆性和决策成本决定
- 静态界面不能替代延迟、权限、并发、失败和中断的行为说明
- 游戏思维默认服务掌握感、自主性和有意义的选择，不等于积分、徽章、连续签到或排行榜
- 信息权重分别考虑用户、业务、决策、风险、时机和频率，不能用一个平均分掩盖冲突

## 跨平台安装

仓库同时适配 Codex / ChatGPT、TRAE Work、Hermes、OpenClaw 和扣子。以下命令假设公开仓库地址为 `qlhouseClub/interaction-design-expert`。

### Codex / ChatGPT 桌面端

Windows：

```powershell
$skillDir = "$env:USERPROFILE\.codex\skills\interaction-design-expert"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/interaction-design-expert.git $skillDir
```

macOS / Linux：

```bash
skill_dir="$HOME/.codex/skills/interaction-design-expert"
mkdir -p "$(dirname "$skill_dir")"
git clone https://github.com/qlhouseClub/interaction-design-expert.git "$skill_dir"
```

### ChatGPT Work / OpenAI Plugin

```powershell
git clone https://github.com/qlhouseClub/interaction-design-expert.git
Set-Location .\interaction-design-expert
python .\scripts\build_compat.py --platform openai
codex.cmd plugin marketplace add .\dist\openai-marketplace
```

macOS / Linux 将最后一行改为：

```bash
codex plugin marketplace add ./dist/openai-marketplace
```

### TRAE Work / SOLO / IDE

```powershell
python .\scripts\build_compat.py --platform trae
```

上传 `dist/trae/interaction-design-expert.zip`，或把完整目录复制到：

```text
<项目>/.trae/skills/interaction-design-expert/
```

Windows 全局目录通常为 `%USERPROFILE%/.trae-cn/skills/interaction-design-expert/`。导入 ZIP 后应确认 `references/` 和 `assets/` 未丢失。

### Hermes Agent

```powershell
git clone https://github.com/qlhouseClub/interaction-design-expert.git "$env:USERPROFILE\.hermes\skills\interaction-design-expert"
```

macOS / Linux：

```bash
git clone https://github.com/qlhouseClub/interaction-design-expert.git "$HOME/.hermes/skills/interaction-design-expert"
```

也可以生成 `dist/portable/interaction-design-expert.zip` 后解压到 `~/.hermes/skills/`。

### OpenClaw

```text
openclaw skills install git:qlhouseClub/interaction-design-expert@main
```

安装为全局共享技能：

```text
openclaw skills install git:qlhouseClub/interaction-design-expert@main --global
```

### 扣子 / Coze

```powershell
python .\scripts\build_compat.py --platform coze
```

然后把 `dist/coze/interaction-design-expert/agent-prompt.md` 粘贴到智能体系统提示词，并把 `knowledge/` 中全部 Markdown 上传至知识库。

### 一次生成所有平台包

```powershell
python .\scripts\build_compat.py --platform all
```

更完整的平台边界和维护规则见 [COMPATIBILITY.md](COMPATIBILITY.md)。

## 使用示例

- “把审批功能拆成完整交互流，覆盖权限、撤回、驳回、超时和并发修改。”
- “审查这个表单为什么用户总在最后一步放弃，不要只改视觉。”
- “在不改变现有 Design Token 和组件的前提下，设计批量操作。”
- “为移动端拖拽排序定义手势、键盘替代、反馈、取消和撤销。”
- “把这组静态界面补成工程可实现的状态矩阵和交互契约。”

## 目录

```text
interaction-design-expert/
├─ SKILL.md
├─ agents/openai.yaml
├─ references/
├─ assets/
├─ platforms/
├─ scripts/build_compat.py
├─ COMPATIBILITY.md
└─ THIRD_PARTY_NOTICES.md
```

专业能力只在 `SKILL.md` 与 `references/` 维护；`dist/` 是可重建产物，不手工编辑或提交。

## 许可

- [MIT License](LICENSE)
- [第三方来源与权利边界](THIRD_PARTY_NOTICES.md)
- [贡献指南](CONTRIBUTING.md)
- [安全策略](SECURITY.md)
