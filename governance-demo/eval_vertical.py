#!/usr/bin/env python3
"""垂直场景 eval：评估代码可执行率 + 输出结构正确性
维度：① 语法可编译率 ② 运行成功率 ③ 输出断言通过率（结构正确性）
被测资产：auto-dev-demo 下的工程化产物
"""
import ast, json, pathlib, subprocess, sys, datetime

ROOT = pathlib.Path("/Users/donglai/Doubao/chats/2026-09-03/new-chat-6")
TARGETS = ROOT / "auto-dev-demo"
CASES = [
    # (文件, 运行参数, 预期输出包含, 描述)
    ("calculator.py", ["3", "+", "4"], "7", "加法"),
    ("calculator.py", ["10", "/", "0"], "不能", "除零保护"),
    ("calculator.py", ["5", "^", "2"], "不支持", "非法运算符"),
    ("logstats.py", ["auto-dev-demo/app.log", "error"], "error", "关键词统计"),
    ("xian_guide.py", ["钟楼"], "钟楼", "景点查询"),
    ("logclean.py", ["--help"], "[-h]", "CLI帮助"),
]
EXTRA_SYNTAX = ["governance-demo/task_trace.py", "governance-demo/backup_restore_drill.py"]

def syntax_check(py):
    try:
        ast.parse(py.read_text(encoding="utf-8"))
        return True, ""
    except SyntaxError as e:
        return False, f"L{e.lineno}: {e.msg}"

def run_case(py, args, expect):
    try:
        r = subprocess.run([sys.executable, str(py), *args],
                           capture_output=True, text=True, timeout=20)
        if r.returncode != 0:
            return False, f"exit={r.returncode} stderr={r.stderr[:80]}"
        ok = expect in (r.stdout + r.stderr)
        return ok, ("输出包含期望" if ok else f"输出不含'{expect}': {r.stdout[:80]}")
    except subprocess.TimeoutExpired:
        return False, "超时"

def main():
    results = {"syntax_total": 0, "syntax_pass": 0, "run_total": 0, "run_pass": 0,
               "assert_total": 0, "assert_pass": 0, "details": []}
    print("=" * 66)
    print("垂直场景 eval · 代码可执行率与输出结构")
    print("=" * 66)

    # ① 语法可编译率（全部 python 产物）
    py_files = sorted(TARGETS.glob("*.py")) + \
               [ROOT / p for p in EXTRA_SYNTAX if (ROOT / p).exists()]
    for py in py_files:
        ok, msg = syntax_check(py)
        results["syntax_total"] += 1
        results["syntax_pass"] += 1 if ok else 0
        print(f"  {'✓' if ok else '✗'} 语法  {py.relative_to(ROOT)}  {msg}")
        results["details"].append({"file": py.name, "dim": "syntax", "pass": ok, "note": msg})

    # ② 运行成功率 + ③ 输出断言
    for name, args, expect, desc in CASES:
        py = TARGETS / name
        if not py.exists():
            continue
        ok, note = run_case(py, args, expect)
        results["run_total"] += 1
        results["run_pass"] += 1 if ok else 0
        results["assert_total"] += 1
        results["assert_pass"] += 1 if ok else 0
        print(f"  {'✓' if ok else '✗'} 运行  {name} {args} → {desc}  {note}")
        results["details"].append({"file": name, "dim": "run", "pass": ok, "note": note})

    # 汇总指标
    st = results["syntax_total"]
    rt = results["run_total"]
    at = results["assert_total"]
    syntax_rate = round(100 * results["syntax_pass"] / st, 1) if st else 0
    run_rate = round(100 * results["run_pass"] / rt, 1) if rt else 0
    assert_rate = round(100 * results["assert_pass"] / at, 1) if at else 0
    results["summary"] = {
        "语法可编译率": f"{results['syntax_pass']}/{st} ({syntax_rate}%)",
        "运行成功率": f"{results['run_pass']}/{rt} ({run_rate}%)",
        "输出断言通过率": f"{results['assert_pass']}/{at} ({assert_rate}%)",
        "评估时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    print("-" * 66)
    print(f"  语法可编译率 : {results['summary']['语法可编译率']}")
    print(f"  运行成功率   : {results['summary']['运行成功率']}")
    print(f"  输出断言通过率: {results['summary']['输出断言通过率']}")

    # 输出报告
    report = ROOT / ".governance" / "eval-vertical.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  报告已写: {report.relative_to(ROOT)}")

    # 通过率阈值（质量门禁）：三率均 ≥ 100%（归零要求）
    gate = syntax_rate >= 100 and run_rate >= 100 and assert_rate >= 100
    print("-" * 66)
    print("质量门禁:", "✓ 通过（三率 100%，归零）" if gate else "✗ 未达归零要求")
    return 0 if gate else 1

if __name__ == "__main__":
    sys.exit(main())
