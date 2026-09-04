#!/usr/bin/env python3
"""Capability Registry: 工具/技能统一元数据注册中心
登记 9 个 MCP 工具 + 核心工程化技能，含成本/失败模式/可回滚性。
支持: build(生成 registry) / check(校验 schema) / query(按类查询)
"""
import argparse, datetime, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / ".governance" / "capability_registry.json"

SCHEMA = {
    "type": "object",
    "required": ["id", "type", "name", "description", "destructive", "failure_mode", "cost", "status"],
    "properties": {
        "id": {"type": "string"},
        "type": {"enum": ["tool", "skill"]},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "destructive": {"type": "boolean"},   # true=需谨慎/需回滚预案
        "failure_mode": {"type": "string"},
        "cost": {"enum": ["L", "M", "H"]},    # 相对成本
        "status": {"enum": ["active", "deprecated"]},
        "alias": {"type": "string"},
    },
}

TOOLS = [
    {"id": "dev_open_project", "name": "打开项目", "description": "在 VSCode 打开指定项目目录",
     "destructive": False, "failure_mode": "路径不存在", "cost": "L"},
    {"id": "dev_open_file", "name": "打开文件", "description": "在 VSCode 打开/聚焦指定文件",
     "destructive": False, "failure_mode": "文件不存在", "cost": "L"},
    {"id": "dev_list_dir", "name": "列目录", "description": "列出目录内容", "destructive": False,
     "failure_mode": "目录不存在/无权限", "cost": "L"},
    {"id": "dev_read_file", "name": "读文件", "description": "读取文件内容", "destructive": False,
     "failure_mode": "文件不存在/编码异常", "cost": "L"},
    {"id": "dev_write_file", "name": "写文件", "description": "写入/覆盖文件", "destructive": True,
     "failure_mode": "覆盖未备份内容", "cost": "L"},
    {"id": "dev_edit_file", "name": "改文件", "description": "精准编辑文件片段", "destructive": True,
     "failure_mode": "匹配串不唯一", "cost": "L"},
    {"id": "dev_search", "name": "搜索", "description": "在项目中搜索内容", "destructive": False,
     "failure_mode": "无结果/超时", "cost": "M"},
    {"id": "dev_typewrite", "name": "打字机写入", "description": "逐行追加写入（视觉打字机模式）",
     "destructive": True, "failure_mode": "追加到错误位置", "cost": "M"},
    {"id": "dev_run_command", "name": "运行命令", "description": "在项目内执行 shell 命令",
     "destructive": True, "failure_mode": "命令失败/超时/副作用", "cost": "H"},
]

SKILLS = [
    {"id": "自动编码循环", "name": "自动编码循环", "description": "写→跑→查→改→注释→完善→归零闭环",
     "destructive": True, "failure_mode": "运行失败需自动修复", "cost": "H"},
    {"id": "可信执行治理", "name": "可信执行治理", "description": "L0-L4 动作分级+备份+审计+回滚",
     "destructive": False, "failure_mode": "回滚后需验证", "cost": "M"},
    {"id": "工程化总控", "name": "工程化总控", "description": "12 阶段路由 + TodoWrite 自动推进",
     "destructive": False, "failure_mode": "阶段卡住", "cost": "M"},
    {"id": "任务追踪", "name": "任务追踪", "description": "复杂任务结构化 trace 记录",
     "destructive": False, "failure_mode": "日志膨胀", "cost": "L"},
    {"id": "编写计划", "name": "编写计划", "description": "TDD 微任务拆分", "destructive": False,
     "failure_mode": "拆分粒度不当", "cost": "L"},
    {"id": "执行计划", "name": "执行计划", "description": "分批执行带检查点", "destructive": False,
     "failure_mode": "检查点遗漏", "cost": "M"},
    {"id": "cicd流水线", "name": "CICD流水线", "description": "GitHub Actions 流水线设计",
     "destructive": False, "failure_mode": "环境差异", "cost": "M"},
    {"id": "api接口设计", "name": "API接口设计", "description": "REST/OpenAPI 契约设计",
     "destructive": False, "failure_mode": "契约漂移", "cost": "M"},
    {"id": "owasp安全", "name": "OWASP安全", "description": "OWASP Top10 安全审查",
     "destructive": False, "failure_mode": "误报", "cost": "M"},
    {"id": "mcp服务构建", "name": "MCP服务构建", "description": "FastMCP/TS MCP Server 构建",
     "destructive": False, "failure_mode": "SDK 版本差异", "cost": "H"},
    {"id": "系统化调试", "name": "系统化调试", "description": "系统性根因定位",
     "destructive": False, "failure_mode": "环境因素", "cost": "M"},
    {"id": "测试驱动开发", "name": "测试驱动开发", "description": "红-绿-重构 TDD",
     "destructive": False, "failure_mode": "测试脆弱", "cost": "M"},
]

def cmd_build(args):
    reg = {
        "_meta": {
            "version": "1.0", "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "schema": "见本文件 properties 定义",
        },
        "tools": [dict(t, type="tool", status="active") for t in TOOLS],
        "skills": [dict(s, type="skill", status="active") for s in SKILLS],
    }
    REG.parent.mkdir(parents=True, exist_ok=True)
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ 已生成 {REG.relative_to(ROOT)}")
    print(f"  工具 {len(TOOLS)} 个 / 技能 {len(SKILLS)} 个")

def cmd_check(args):
    if not REG.exists():
        print("✗ registry 不存在，先 build"); return 1
    data = json.loads(REG.read_text(encoding="utf-8"))
    errors = []
    for group in ("tools", "skills"):
        for item in data.get(group, []):
            for field in SCHEMA["required"]:
                if field not in item:
                    errors.append(f"{item.get('id')} 缺 {field}")
            if item.get("type") not in ("tool", "skill"):
                errors.append(f"{item.get('id')} type 非法")
            if item.get("cost") not in ("L", "M", "H"):
                errors.append(f"{item.get('id')} cost 非法")
    if errors:
        print("✗ schema 校验失败:"); [print("  " + e) for e in errors]; return 1
    print("✓ schema 校验通过（全部字段合法）")
    print(f"  工具 {len(data['tools'])} / 技能 {len(data['skills'])}")

def cmd_query(args):
    if not REG.exists():
        print("✗ registry 不存在，先 build"); return 1
    data = json.loads(REG.read_text(encoding="utf-8"))
    items = data.get(args.kind, []) if args.kind else data["tools"] + data["skills"]
    for it in items:
        flag = "🔴" if it["destructive"] else "🟢"
        print(f"{flag} [{it['type']}] {it['name']}  cost={it['cost']}  {it['description']}")
        print(f"      失败模式: {it['failure_mode']}")

def main():
    p = argparse.ArgumentParser(description="Capability Registry")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    sub.add_parser("check").set_defaults(fn=cmd_check)
    q = sub.add_parser("query"); q.add_argument("--kind", choices=["tools", "skills"], default=None)
    q.set_defaults(fn=cmd_query)
    a = p.parse_args()
    sys.exit(a.fn(a) or 0)

if __name__ == "__main__":
    main()
