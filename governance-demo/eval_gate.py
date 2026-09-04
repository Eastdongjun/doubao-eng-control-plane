#!/usr/bin/env python3
"""质量门禁评测闭环（阶段 8 测试 / 阶段 10 发布前自动执行）。

确定性硬门禁检查，每项 PASS/FAIL，全部 PASS 才允许进入下一阶段/发布。
结果带时间戳追加到 .governance/eval-gate-history.jsonl，形成持续评测历史（可观测趋势）。

用法:
  python3 governance-demo/eval_gate.py              # 跑门禁，输出报告
  python3 governance-demo/eval_gate.py --project X  # 对指定项目跑（含其追踪矩阵覆盖率）
退出码: 0=全PASS  1=有FAIL
"""
import datetime, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path("/Users/donglai/Doubao/chats/2026-09-03/new-chat-6")
SKILL_DIR = pathlib.Path("/Users/donglai/Library/Application Support/Doubao/Default/.doubao/agent_mode/workspace/.user_skills")
GOV = ROOT / ".governance"
HIST = GOV / "eval-gate-history.jsonl"

def ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def py_ok(p):
    try:
        compile(p.read_text(encoding="utf-8"), str(p), "exec"); return True
    except Exception:
        return False

def check_skills():
    """引用零断裂 + py 语法全通过"""
    broken = []; py_fail = []
    for d in SKILL_DIR.iterdir():
        if not d.is_dir() or d.name.startswith("."): continue
        fm = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        for ref in re.findall(r"\]\(([^)#]+)\)", fm):
            if ref.startswith(("http", "mailto", "#")): continue
            if not (d / ref).exists(): broken.append(f"{d.name}→{ref}")
    for p in SKILL_DIR.rglob("*.py"):
        if not py_ok(p): py_fail.append(p.name)
    return {"引用零断裂": len(broken) == 0, "py语法全通过": len(py_fail) == 0,
            "断裂明细": broken[:5], "失败明细": py_fail[:5]}

def check_registry():
    reg = GOV / "capability_registry.json"
    if not reg.exists(): return {"注册表一致": False}
    try:
        data = json.loads(reg.read_text(encoding="utf-8"))
    except Exception:
        return {"注册表一致": False}
    entries = data.get("skills", []) if isinstance(data, dict) else []
    keys = [e.get("id") for e in entries if isinstance(e, dict)]
    skills = [d.name for d in SKILL_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")]
    ok = len(set(keys) ^ set(skills)) == 0
    return {"注册表一致": ok, "差异": sorted(set(keys) ^ set(skills))[:5]}

def check_traceability(project_name):
    """指定项目追踪矩阵覆盖率"""
    p = ROOT / "_projects" / project_name
    mf = p / "需求追踪矩阵.md"
    if not mf.exists(): return {"覆盖100%": False, "原因": "矩阵未生成(未 init)"}
    rows = [l for l in mf.read_text(encoding="utf-8").splitlines()
            if l.startswith("| ") and not l.startswith("| REQ") and not l.startswith("|---")]
    full = 0; total = 0
    for r in rows:
        cells = [c.strip() for c in r.strip("|").split("|")]
        if len(cells) < 9: continue
        total += 1
        if cells[3] != "—" and cells[4] != "—" and cells[5] != "—" and cells[6] != "—":
            full += 1
    return {"覆盖100%": total > 0 and full == total, "覆盖率": f"{full}/{total}"}

def check_drill():
    """最近回滚演练存在且 manifest 可读"""
    backups = ROOT / "backups"
    if not backups.exists(): return {"回滚演练就绪": False, "原因": "无备份目录"}
    dirs = sorted(backups.glob("doubao-eng-*"))
    if not dirs: return {"回滚演练就绪": False, "原因": "无演练记录"}
    manifest = dirs[-1] / "manifest.json"
    try:
        n = len(json.loads(manifest.read_text(encoding="utf-8")))
        return {"回滚演练就绪": True, "最新": dirs[-1].name, "条目": n}
    except Exception as e:
        return {"回滚演练就绪": False, "原因": f"manifest 异常 {e}"}

def check_ci():
    try:
        r = subprocess.run(["gh", "run", "list", "--limit", "1", "--json", "conclusion"],
                           capture_output=True, text=True, timeout=15, cwd=ROOT)
        runs = json.loads(r.stdout)
        if not runs: return {"CI最近成功": False, "原因": "无 CI 记录"}
        ok = runs[0].get("conclusion") == "success"
        return {"CI最近成功": ok, "结论": runs[0].get("conclusion")}
    except Exception as e:
        return {"CI最近成功": False, "原因": str(e)}

def main():
    args = [a for a in sys.argv[1:]]
    project = None
    if "--project" in args:
        i = args.index("--project")
        project = args[i + 1]
    results = {}
    results.update(check_skills())
    results.update(check_registry())
    results.update(check_ci())
    if project:
        results.update(check_traceability(project))
    else:
        results["追踪矩阵"] = "未指定项目(加 --project X)"
    results.update(check_drill())
    # 门禁项（必须是布尔真）
    gates = [k for k in results if isinstance(results[k], bool)]
    passed = [k for k in gates if results[k]]
    failed = [k for k in gates if not results[k]]

    record = {"时间": ts(), "项目": project, "门禁": {k: results[k] for k in gates},
              "通过": len(passed), "失败": len(failed), "结论": "PASS" if not failed else "FAIL"}
    GOV.mkdir(exist_ok=True)
    with HIST.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("=" * 60)
    print(f"质量门禁评测  {record['时间']}  项目={project or '全局'}")
    print("-" * 60)
    for k, v in results.items():
        mark = "✓" if v is True else ("✗" if v is False else "·")
        print(f"  {mark} {k}: {v if not isinstance(v, bool) else 'PASS' if v else 'FAIL'}")
    print("-" * 60)
    print(f"结论: {'🟢 全部 PASS，可进入下一阶段/发布' if not failed else '🔴 有 FAIL，禁止放行'}")
    print(f"历史: {HIST} (共 {sum(1 for _ in HIST.open(encoding='utf-8')) if HIST.exists() else 0} 条)")
    return 0 if not failed else 1

if __name__ == "__main__":
    sys.exit(main())
