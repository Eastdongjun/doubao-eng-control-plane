# doubao-eng-control-plane · 豆包工程化控制面

> 把豆包（Doubao）Agent 从「会回答问题」打造成「可信地替你完成任务」的**工程化能力开源套件**。
> 覆盖：自动编码闭环 · 可信执行治理 · CI/CD · 监控告警 · 任务追踪 · 执行回放 · 多模态评测 · 能力注册。

[![CI](https://github.com/Eastdongjun/doubao-eng-control-plane/actions/workflows/ci.yml/badge.svg)](https://github.com/Eastdongjun/doubao-eng-control-plane/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 这是什么

一个 AI 助手（豆包）在**用户桌面环境**上的完整工程化能力资产仓库。它回答了一个核心问题：

> 当 AI 从「聊天问答」进入「替你写代码、改文件、跑命令」时，如何保证**可控、可验证、可回滚、可追溯**？

本仓库把答案落成了一套可复用的能力：

- **9 个 MCP 工具**：通过本地 MCP Server 让 AI 在真实项目里写代码/跑命令/逐行"打字机"写入，且不碰你的键盘与窗口焦点。
- **87 个中文化技能**：从 12 阶段工程化总控、TDD、CI/CD，到产品/交互/视觉/动效设计专家。
- **6 项治理机制**：权限分级、备份恢复、审计日志、任务追踪、执行回放、多模态评测。
- **CI + 监控**：GitHub Actions 质量门禁 + 本机 launchd 健康监控告警。

## 能力地图

```
┌─────────────────────────────────────────────────────────────┐
│ 执行层   自动编码循环(写→跑→查→改→注释→完善) · 多项目隔离 · 归零验收│
├─────────────────────────────────────────────────────────────┤
│ 治理层   可信执行治理(L0-L4/备份/审计/回滚) · Task Trace · 执行回放│
├─────────────────────────────────────────────────────────────┤
│ 质量层   垂直评测(语法/运行/断言) · 多模态五维评测 · CI 质量门禁   │
├─────────────────────────────────────────────────────────────┤
│ 运维层   监控告警(launchd) · 配置管理(git 纳管) · 备份恢复演练     │
├─────────────────────────────────────────────────────────────┤
│ 能力治理  Capability Registry(工具/技能元数据: 成本/失败模式/可回滚)│
└─────────────────────────────────────────────────────────────┘
```

## 目录结构

| 目录/文件 | 说明 |
|---|---|
| `skills/` | **87 个用户技能基线快照**（全中文化） |
| `vscode-mcp/` | VSCode 桥接 MCP Server（9 个 `dev_*` 工具，含打字机模式 `dev_typewrite`） |
| `governance-demo/` | 治理机制落地脚本：备份演练 / Task Trace / 垂直评测 / 多模态评测 / 执行回放 / 能力注册 |
| `monitor/` | MCP 健康检查脚本 + launchd 定时监控（每 5 分钟 + 异常告警） |
| `auto-dev-demo/` | 自动编码闭环演示产物 |
| `.github/workflows/ci.yml` | GitHub Actions 流水线（Python 语法 / 技能 frontmatter / 一致性校验） |
| `.governance/` | 运行期治理数据（审计、trace、评测报告、能力注册表） |

## 核心能力详解

### 1. 自动编码闭环（`vscode-mcp/`）
通过本地 MCP Server（`127.0.0.1:8848/mcp`），AI 在真实项目里完成
**写代码 → 运行 → 查错 → 修复 → 注释 → 完善 → 归零验收**，全程后台写入、不抢焦点、多项目按路径天然隔离。

```bash
# 启动 MCP Server
cd vscode-mcp
./.venv/bin/python server.py     # 依赖: pip install "mcp<2"
```

豆包侧配置：技能·连接器·伙伴 → 新建自定义连接器 → HTTP → `http://127.0.0.1:8848/mcp`，工具前缀 `mcp__vscode__dev_*`。

### 2. 可信执行治理（`governance-demo/`）
任何外部写操作按风险分级：

| 等级 | 范围 | 机制 |
|---|---|---|
| L0 | 只读查询 | 直接执行 |
| L1 | 创建草稿 | 审计日志 |
| L2 | 修改文件 | **改前备份** + 审计 |
| L3 | 删除/覆盖 | 进回收站 + 备份 + 审计 |
| L4 | 高风险（外部发送/交易） | 明确确认 + 回滚预案 |

审计日志只追加不覆盖，失败自动回滚并验证。

### 3. 任务追踪 + 执行回放
复杂任务全程记录结构化 trace（意图→计划→工具→耗时→失败点），可随时回放：

```bash
python3 governance-demo/task_trace.py start --task xxx --intent "..." --plan "a|b|c"
python3 governance-demo/task_trace.py step --task xxx --tool dev_run_command --desc "..." --duration_ms 100
python3 governance-demo/task_trace.py end --task xxx --result success --duration_ms 5000
python3 governance-demo/replay.py xxx                 # 终端时间线
python3 governance-demo/replay.py xxx --html          # HTML 回放页
```

### 4. 多模态专项评测（`eval_multimodal.py`）
五维垂直评测 + 质量门禁：代码可执行率 / Excel 公式准确性 / PPT 结构 / 网页可运行性 / 报告引用可靠性。

```bash
python3 governance-demo/eval_multimodal.py            # 标准样本，五维 100% 归零
python3 governance-demo/eval_multimodal.py --selftest # 注入缺陷，验证评测器能检出
```

### 5. CI 流水线
push 到 `main` / 任何 PR 自动触发：全仓 Python 语法检查 → 技能 frontmatter 校验 → 治理一致性（无敏感/无虚拟环境混入）。

### 6. 监控告警（`monitor/`）
`health_check.sh` 检查：MCP 端口 / 进程 / 关键资产 / 技能目录 / GitHub 远端。异常时 macOS 通知 + 退出码 1。已注册 launchd 每 300 秒运行 + 开机自启。

## 快速开始

1. **恢复技能基线**：把 `skills/*` 复制到你的 `~/.doubao/.../workspace/.user_skills/`。
2. **启动 MCP**：`cd vscode-mcp && ./.venv/bin/python server.py`。
3. **接入豆包**：连接器 → HTTP → `http://127.0.0.1:8848/mcp`。
4. **跑通治理闭环**：执行 `governance-demo/` 下的 `backup_restore_drill.py` / `eval_multimodal.py` / `replay.py list` 验证环境。

## 技能体系（87 个）

- **工程化总控**：12 阶段路由（立项→需求→设计→架构→详设→开发→测试→上线→运维→迭代）+ TodoWrite 清单 + 自动推进。
- **自动编码循环 / 编写计划 / 执行计划**：TDD 微任务、分批执行、归零验收。
- **可信执行治理 / 任务追踪**：安全与可追溯。
- **ci-cd流水线 / 上线发布 / 发布管理 / 可观测性 / 事故管理**：交付与运维。
- **产品专家 / 设计宗师 / 交互设计专家 / 动效大师**：产品-交互-视觉-动效专家链（来自 [qlhouseClub](https://github.com/qlhouseClub) 的 MIT 开源技能，已按豆包规范中文化安装）。
- 另有 tdd / 测试策略 / owasp安全 / api接口设计 / 数据建模 / 微服务 / 容器化 等。

## 设计理念

本套件的三个核心原则：

1. **归零**：交付给用户的每个文件必须通过语法/运行/Lint 三档验收，绝不留问题文件。
2. **可回滚**：一切写操作先备份，失败自动回滚并验证；配置管理纳管全部工程资产。
3. **可解释**：每个复杂任务都有 trace，随时可回放"AI 当时做了什么、哪步失败、花了多久"。

## License

[MIT](LICENSE) © Eastdongjun
