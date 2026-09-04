# 豆包工程化控制面（doubao-eng-control-plane）

把豆包在本地构建的工程化能力资产**版本化、可回滚、可备份**，纳入配置管理。

## 仓库内容

| 目录 | 说明 |
|---|---|
| `skills/` | 用户技能基线快照（82 个，全中文化），来自 `~/.doubao/.../.user_skills` |
| `vscode-mcp/` | VSCode 桥接 MCP Server（9 个 dev_* 工具，含打字机模式 dev_typewrite） |
| `governance-demo/` | 可信执行治理实测（L0-L4 分级 / 审计 / 回滚） |
| `auto-dev-demo/` | 自动编码闭环演示（写→跑→查→改→注释→归零） |
| `vscode-demo/` `proj-b-demo/` | 多项目隔离演示 |

## 核心能力清单

- **自动编码循环**：MCP 后台写代码→运行→查错→修复→注释→完善→归零验收，不碰 GUI
- **可信执行治理**：动作风险分级（L0-L4）、改前备份、执行后审计日志、失败回滚
- **工程化总控**：12 阶段路由 + TodoWrite 清单 + 自动推进
- **多项目隔离**：所有操作按项目路径隔离，并行互不干扰

## 恢复 / 同步方法

- **技能**：把 `skills/*` 复制回 `.user_skills/`（恢复基线）；技能有改动时反向复制回仓库提交。
- **MCP Server**：`cd vscode-mcp && ./.venv/bin/python server.py`（需 `pip install "mcp<2"`）。
- **豆包连接器**：HTTP → `http://127.0.0.1:8848/mcp`，工具前缀 `mcp__vscode__`。

## 约束

- 第三方克隆（`_ref_skills/`）、虚拟环境（`.venv/`）、运行产物已 gitignore，不入库。
- 仓库为私有；不含任何密钥/token。
