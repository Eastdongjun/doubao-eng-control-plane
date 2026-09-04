#!/usr/bin/env python3
"""工程化体系运营指标监控（L4 可运营）。

采集并评估当前工程化体系的运行指标，异常项标记 FAIL 并输出告警。
覆盖六类指标：
  ① 技能库健康  ② 注册中心一致  ③ 项目运营  ④ 治理健康  ⑤ CI 状态  ⑥ 资产完整性
用法:
  python3 monitor/eng_metrics.py            # 采集并输出报告 + 写 .governance/eng-metrics.json
  python3 monitor/eng_metrics.py --json     # 仅输出 JSON
"""
import datetime,  json, pathlib, re, subprocess, sys

ROOT = pathlib.Path("/Users/donglai/Doubao/chats/2026-09-03/new-chat-6")
SKILL_DIR = pathlib.Path("/Users/donglai/Library/Application Support/Doubao/Default/.doubao/agent_mode/workspace/.user_skills")
GOV = ROOT / ".governance"
PROJECTS = ROOT / "_projects"

def ts():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

def py_ok(p):
    try:
        compile(p.read_text(encoding="utf-8"), str(p), "exec"); return True
    except Exception:
        return False

def skill_health():
    skills = sorted(d for d in SKILL_DIR.iterdir() if d.is_dir() and not d.name.startswith("."))
    bad_fm = []; broken = []; py_fail = []
    for d in skills:
        fm = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        if "name:" not in fm or "description:" not in fm:
            bad_fm.append(d.name)
        for ref in re.findall(r"\]\(([^)#]+)\)", fm):
            if ref.startswith(("http", "mailto", "#")): continue
            if not (d / ref).exists():
                broken.append(f"{d.name}→{ref}")
    total_py = 0
    for p in SKILL_DIR.rglob("*.py"):
        total_py += 1
        if not py_ok(p): py_fail.append(p.name)
    return {"技能数": len(skills), "frontmatter异常": bad_fm, "引用断裂": broken,
            "py脚本数": total_py, "py语法失败": py_fail}

def registry_health():
    reg = GOV / "capability_registry.json"
    if not reg.exists(): return {"注册表": "缺失"}
    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
    except Exception as e:
        return {"注册表": f"解析失败 {e}"}
    skills = [d.name for d in SKILL_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    entries = data.get("skills", []) if isinstance(data, dict) else []
    keys = [e.get("id") for e in entries if isinstance(e, dict)] if isinstance(entries, list) else list(entries.keys())
    missing = [s for s in skills if s not in keys]
    stale = [k for k in keys if k not in skills]
    stage = sum(1 for e in entries if isinstance(e, dict) and e.get("stage"))
    return {"注册技能数": len(keys), "漏注册": missing, "陈旧": stale, "阶段型": stage}

def projects_health():
    out = {}
    if not PROJECTS.exists(): return out
    for p in sorted(PROJECTS.iterdir()):
        if not p.is_dir(): continue
        stages = sorted(f.name for f in p.glob("阶段*.md"))
        cov = None
        mf = p / "需求追踪矩阵.md"
        if mf.exists():
            rows = [l for l in mf.read_text(encoding="utf-8").splitlines()
                    if l.startswith("| ") and not l.startswith("| REQ") and not l.startswith("|---")]
            full = sum(1 for r in rows if all(c.strip() != "—" for c in [r.split("|")[4], r.split("|")[5], r.split("|")[6], r.split("|")[7]]) if len(r.split("|")) >= 9)
            cov = f"{full}/{len(rows)}"
        out[p.name] = {"阶段产物": len(stages), "最新": stages[-1] if stages else "无", "追踪矩阵": cov or "未生成"}
    return out

def governance_health():
    trace = GOV / "trace.jsonl"
    trace_lines = sum(1 for _ in trace.open(encoding="utf-8")) if trace.exists() else 0
    # 最近一次回滚演练
    backups = ROOT / "backups"
    last_drill = "无"
    if backups.exists():
        dirs = sorted(backups.glob("doubao-eng-*"))
        if dirs:
            last_drill = dirs[-1].name
    return {"trace行数": trace_lines, "最近回滚演练": last_drill}

def ci_health():
    try:
        r = subprocess.run(["gh", "run", "list", "--limit", "1", "--json", "status,conclusion"],
                           capture_output=True, text=True, timeout=15, cwd=ROOT)
        if r.returncode != 0: return "查询失败"
        runs = json.loads(r.stdout)
        if not runs: return "无"
        return f"{runs[0]['status']} {runs[0].get('conclusion') or '-'}"
    except Exception as e:
        return f"查询异常 {e}"

def asset_health():
    checks = {
        "总控技能": SKILL_DIR / "工程化总控/SKILL.md",
        "注册构建器": ROOT / "governance-demo/skill_registry_builder.py",
        "追踪矩阵工具": ROOT / "governance-demo/traceability_matrix.py",
        "回滚演练": ROOT / "governance-demo/backup_restore_drill.py",
        "VSCode-MCP": ROOT / "vscode-mcp/server.py",
        "网页测试引擎": ROOT / "webqa/webqa_engine.py",
    }
    return {k: "存在" if v.exists() else "缺失" for k, v in checks.items()}

def main():
    json_only = "--json" in sys.argv
    m = {
        "时间": ts(),
        "技能库": skill_health(),
        "注册中心": registry_health(),
        "项目运营": projects_health(),
        "治理": governance_health(),
        "CI": ci_health(),
        "资产": asset_health(),
    }
    # 告警判定
    alerts = []
    sk = m["技能库"]
    if sk.get("frontmatter异常"): alerts.append("frontmatter 异常")
    if sk.get("引用断裂"): alerts.append(f"引用断裂 {len(sk['引用断裂'])} 处")
    if sk.get("py语法失败"): alerts.append("py 语法失败")
    rg = m["注册中心"]
    if rg.get("漏注册") or rg.get("陈旧"): alerts.append("注册表不一致")
    if isinstance(rg.get("注册表"), str): alerts.append("注册表缺失")
    m["告警"] = alerts
    m["状态"] = "🔴 有告警" if alerts else "🟢 正常"

    # 写历史指标（持续累积）
    hist = GOV / "eng-metrics-history.jsonl"
    GOV.mkdir(exist_ok=True)
    with hist.open("a", encoding="utf-8") as f:
        f.write(json.dumps(m, ensure_ascii=False) + "\n")

    if json_only:
        print(json.dumps(m, ensure_ascii=False, indent=2)); return 0 if not alerts else 1

    print("=" * 60)
    print(f"豆包工程化体系 · 运营指标监控  {m['时间']}")
    print(f"总体状态: {m['状态']}")
    print("-" * 60)
    print(f"① 技能库: {sk['技能数']} 技能 | py {sk['py脚本数']} 脚本, 语法失败 {len(sk['py语法失败'])} | 引用断裂 {len(sk['引用断裂'])}")
    if isinstance(rg.get("注册表"), str):
        print(f"② 注册中心: {rg['注册表']}")
    else:
        print(f"② 注册中心: {rg['注册技能数']} 注册 | 漏注册 {len(rg['漏注册'])} | 陈旧 {len(rg['陈旧'])} | 阶段型 {rg['阶段型']}")
    print(f"③ 项目运营: {json.dumps(m['项目运营'], ensure_ascii=False)}")
    print(f"④ 治理: trace {m['治理']['trace行数']} 行 | 最近回滚演练 {m['治理']['最近回滚演练']}")
    print(f"⑤ CI: {m['CI']}")
    print(f"⑥ 资产: " + " ".join(f"{k}:{v}" for k, v in m['资产'].items()))
    if alerts:
        print("-" * 60)
        print("⚠ 告警: " + "、".join(alerts)); return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
