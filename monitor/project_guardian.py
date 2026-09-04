#!/usr/bin/env python3
"""项目守护巡检（自动推进）：扫描 _projects 下所有项目，评估工程化推进状态并给出下一步动作。

区分两类项目：
  A. 工程化流程项目（有 阶段N_*.md 产物）→ 判定当前阶段，给出下一阶段动作清单
  B. 外部存量项目（有代码但无阶段产物）→ 识别为"未纳入流程"，建议纳入

用法:
  python3 monitor/project_guardian.py            # 巡检全部项目，输出推进报告
  python3 monitor/project_guardian.py --project X  # 只巡检指定项目
"""
import datetime, pathlib, re, sys

ROOT = pathlib.Path("/Users/donglai/Doubao/chats/2026-09-03/new-chat-6")
PROJECTS = ROOT / "_projects"

# 与工程化总控一致的 12 阶段路由简表
STAGES = [
    (1, "项目立项", ["阶段1_项目立项.md"], "目标清晰、可进入需求"),
    (2, "需求工程", ["阶段2_需求规格.md"], "每项需求有验收标准、流程无歧义"),
    (3, "产品与交互设计", ["阶段3_产品设计.md", "阶段3_原型.md"], "核心页面可演示、业务确认"),
    (4, "系统架构设计", ["阶段4_系统架构.md"], "架构支撑需求、技术风险已验证"),
    (5, "详细设计", ["阶段5_详细设计.md"], "开发可独立编码、异常有方案"),
    (6, "开发准备", ["阶段6_开发准备.md"], "新成员可启动、提交可自动检查"),
    (7, "编码开发", ["阶段7_编码实现.md"], "已开发/评审/测试/可回滚"),
    (8, "测试与质量", ["阶段8_测试报告.md"], "严重缺陷清零、核心流程通过"),
    (9, "上线准备", ["阶段9_上线方案.md"], "检查通过、回滚已验证"),
    (10, "发布上线", ["阶段10_发布记录.md"], "核心流程/数据/接口验证通过"),
    (11, "运行维护", ["阶段11_运维.md"], "监控告警正常、事故闭环"),
    (12, "迭代与退役", ["阶段12_迭代.md"], "迭代有规划"),
]
# 建议执行的下一阶段技能（与总控路由一致）
STAGE_SKILLS = {
    1: "想法打磨", 2: "需求架构/规格驱动开发", 3: "doubao-ui-design/doubao-visualization",
    4: "权衡分析/架构决策记录", 5: "API接口设计/数据建模", 6: "Git工作树/CI-CD流水线",
    7: "零幻觉编码/测试驱动开发", 8: "质量门禁/性能测试", 9: "上线发布/运维助手",
    10: "功能开关/完成前验证", 11: "可观测性/事故管理", 12: "弃用与迁移",
}
STAGE_GATE = {
    8: "python3 governance-demo/eval_gate.py --project {proj}",
    9: "python3 governance-demo/backup_restore_drill.py",
}

def stage_of(proj: pathlib.Path):
    """按 阶段N_*.md 产物判定当前最高阶段"""
    highest = 0
    for f in proj.glob("阶段*.md"):
        m = re.match(r"阶段(\d+)", f.name)
        if m:
            highest = max(highest, int(m.group(1)))
    return highest

def has_code(proj: pathlib.Path):
    """是否外部存量项目（有代码工程特征）"""
    markers = ["backend", "frontend", "pom.xml", "package.json", "deploy.sh", ".git"]
    return any((proj / m).exists() for m in markers)

def inspect(proj: pathlib.Path):
    name = proj.name
    stage = stage_of(proj)
    artifacts = sorted(f.name for f in proj.glob("阶段*.md"))
    state = proj / "PROJECT_STATE.md"
    state_text = state.read_text(encoding="utf-8")[:300] if state.exists() else None
    trace_cov = None
    mf = proj / "需求追踪矩阵.md"
    if mf.exists():
        rows = [l for l in mf.read_text(encoding="utf-8").splitlines() if l.startswith("| ") and not l.startswith("| REQ") and not l.startswith("|---")]
        full = sum(1 for r in rows if len(r.strip("|").split("|")) >= 9 and all(c.strip() != "—" for c in [r.strip("|").split("|")[3], r.strip("|").split("|")[4], r.strip("|").split("|")[5], r.strip("|").split("|")[6]]))
        trace_cov = f"{full}/{len(rows)}" if rows else "0/0"

    if stage == 0 and has_code(proj):
        return {"类型": "B 外部存量项目", "阶段": "未纳入流程", "建议": "纳入工程化：先跑 工程化总控 init 建 阶段1_项目立项.md，再按 12 阶段推进", "产物": len(artifacts)}
    if stage == 0:
        return {"类型": "待启动", "阶段": "无", "建议": "从阶段1 项目立项开始（技能：想法打磨）", "产物": 0}

    next_stage = stage + 1 if stage < 12 else None
    cur = next((s for s in STAGES if s[0] == stage), None)
    next_s = next((s for s in STAGES if s[0] == next_stage), None) if next_stage else None
    missing_cur = [a for a in (cur[2] if cur else []) if not (proj / a).exists()] if cur else []
    return {
        "类型": "A 工程化流程项目", "阶段": f"{stage}/{12}", "阶段名": cur[1] if cur else "",
        "产物": len(artifacts), "最新产物": artifacts[-1] if artifacts else "无",
        "追踪矩阵": trace_cov or "未生成",
        "本阶段缺口": missing_cur or "无",
        "下一步": f"进入阶段{next_stage} {next_s[1]}（技能：{STAGE_SKILLS.get(next_stage, '-')}）→ 产物 {next_s[2][0]}" if next_s else "12 阶段已完成，进入持续迭代/运维",
        "门禁": STAGE_GATE.get(stage, None),
        "退出条件": cur[3] if cur else "",
    }

def main():
    args = sys.argv[1:]
    only = None
    if "--project" in args:
        only = args[args.index("--project") + 1]
    targets = [PROJECTS / only] if only else sorted(PROJECTS.iterdir())
    targets = [t for t in targets if t.is_dir() and not t.name.startswith(".")]
    print("=" * 66)
    print(f"项目守护巡检 · {datetime.datetime.now():%Y-%m-%d %H:%M} · {len(targets)} 个项目")
    print("=" * 66)
    need_advance = []
    for p in targets:
        info = inspect(p)
        print(f"\n▍{p.name}  [{info['类型']}]")
        for k, v in info.items():
            if k in ("类型",): continue
            print(f"   {k}: {v}")
        if info["类型"] == "A 工程化流程项目" and info.get("下一步", "").startswith("进入阶段"):
            need_advance.append((p.name, info["下一步"]))
    print("\n" + "=" * 66)
    if need_advance:
        print("⚡ 可自动推进的项目：")
        for name, nxt in need_advance:
            print(f"   → {name}: {nxt}")
    else:
        print("⚡ 暂无待推进的工程化项目")
    return 0

if __name__ == "__main__":
    sys.exit(main())
