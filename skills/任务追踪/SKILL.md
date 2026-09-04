---
name: 任务追踪
description: 复杂任务的结构化执行追踪（Task Trace）。当豆包执行多步骤复杂任务（自动编码、工程化推进、跨工具任务）时，记录「意图→计划→工具调用→耗时→失败点」的可回看轨迹，服务于调试、复盘、评测与质量追溯。触发场景：开始复杂任务前、任务失败后复盘、用户要求"刚才怎么做的/回看执行过程"。
---

# 任务追踪（Task Trace）

## 何时记录

每次**多步骤复杂任务**（≥3 个工具调用、涉及写文件/运行/多阶段）都应记录 trace；单轮问答、简单查询不记录。

## 记录位置

追加写入 `.governance/trace.jsonl`（只追加，不覆盖）。每任务一行 JSON。

## 记录格式

| 字段 | 说明 |
|---|---|
| task_id | 短唯一标识，如 `task-20260904-001` |
| intent | 用户原始意图（一句话） |
| plan | 计划步骤数组 |
| steps | 已执行步骤数组（每步含 tool/desc/duration_ms/status） |
| result | `success` / `fail` / `partial` |
| fail_point | 失败点描述（失败时必填） |
| duration_ms | 总耗时 |
| model | 模型/方案版本（用于复盘比对） |
| created_at | ISO 时间 |

## 使用脚本

```bash
# 开始任务
python3 governance-demo/task_trace.py start --task task-xxx --intent "用户意图" --plan "步骤1|步骤2|步骤3"

# 记录每步（工具调用后）
python3 governance-demo/task_trace.py step --task task-xxx --tool "dev_write_file" --desc "写入 server.py" --duration_ms 320

# 成功结束
python3 governance-demo/task_trace.py end --task task-xxx --result success --duration_ms 45000

# 失败结束（必须带 fail_point）
python3 governance-demo/task_trace.py end --task task-xxx --result fail --fail_point "第3步构建失败" --duration_ms 12000

# 回看最近 trace
python3 governance-demo/task_trace.py list [--last N]
```

## 约束

- 日志只追加不覆盖；失败任务必须留 fail_point。
- 不记录密钥/token/敏感内容到 trace。
- 复盘时：先 `list` 找出 task_id，再读该任务完整轨迹。
