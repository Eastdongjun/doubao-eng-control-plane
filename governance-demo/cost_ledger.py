#!/usr/bin/env python3
"""成本观测：从 trace 自动派生执行成本台账，输出成本报表与趋势。

价值：可观测「哪些阶段/项目最重、每次执行消耗多少」，支撑模型路由与成本治理。
口径：估算成本 = 执行耗时(分钟) × 单价(元/分钟) + 产物规模(KB) × 单价(元/KB)。
      单价可配置（默认按本地执行成本粗估），输出明确标注「估算」。

用法:
  python3 governance-demo/cost_ledger.py report [--project X]   # 成本报表 + 趋势
  python3 governance-demo/cost_ledger.py record --project X --stage N --skill S --note "..."   # 手动追加
"""
import argparse, datetime, json, pathlib, sys

ROOT = pathlib.Path("/Users/donglai/Doubao/chats/2026-09-03/new-chat-6")
TRACE = ROOT / ".governance/trace.jsonl"
LEDGER = ROOT / ".governance/cost-ledger.jsonl"
RATE_MIN = 0.05   # 元/分钟（本地执行粗估，可调）
RATE_KB = 0.001   # 元/KB 产物规模

def load_trace():
    rows = []
    if TRACE.exists():
        for line in TRACE.open(encoding="utf-8"):
            line = line.strip()
            if not line: continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows

def est_duration(row):
    """估算耗时秒：优先 duration_ms；工程化格式行按产物规模粗估"""
    if "duration_ms" in row and row.get("duration_ms"):
        return row["duration_ms"] / 1000
    art = str(row.get("artifact", ""))
    # 按产物大小粗估：每个产物文件 0.5KB → 5 秒
    size = 0
    for part in art.split("+"):
        p = (ROOT / part.strip())
        if p.exists():
            size += p.stat().st_size / 1024
    return min(600, max(10, size * 10))  # 10s ~ 600s

def est_cost(dur_sec, size_kb):
    return dur_sec / 60 * RATE_MIN + size_kb * RATE_KB

def artifact_size(row):
    art = str(row.get("artifact", ""))
    size = 0
    for part in art.split("+"):
        p = (ROOT / part.strip())
        if p.exists():
            size += p.stat().st_size / 1024
    return size

def normalize(row):
    """统一为 (project, stage/skill, 耗时, 成本)"""
    if "stage" in row and "project" in row:
        project = row.get("project", "?")
        label = f"阶段{row.get('stage')}·{row.get('skill', '')}"
    else:
        project = "（旧任务）"
        label = row.get("intent", "?")[:30]
    dur = est_duration(row)
    cost = est_cost(dur, artifact_size(row))
    return {"project": project, "label": label, "dur_s": round(dur, 1),
            "cost": round(cost, 4), "at": row.get("created_at", ""), "result": row.get("result", "")}

def cmd_report(args):
    rows = [normalize(r) for r in load_trace()]
    if args.project:
        rows = [r for r in rows if r["project"] == args.project]
    if not rows:
        print("无成本记录（trace 为空）"); return 0
    total_dur = sum(r["dur_s"] for r in rows) / 60
    total_cost = sum(r["cost"] for r in rows)
    print("=" * 64)
    print(f"成本观测报表 · {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} · 估算口径(元/分钟={RATE_MIN}, 元/KB={RATE_KB})")
    print("=" * 64)
    # 按项目
    by_proj = {}
    for r in rows:
        by_proj.setdefault(r["project"], []).append(r)
    print(f"{'项目':<16}{'执行':<6}{'总耗时(min)':<14}{'估算成本(元)':<14}")
    print("-" * 64)
    for proj, rs in sorted(by_proj.items()):
        print(f"{proj:<16}{len(rs):<6}{sum(r['dur_s'] for r in rs)/60:<14.1f}{sum(r['cost'] for r in rs):<14.3f}")
    print("-" * 64)
    print(f"{'合计':<16}{len(rows):<6}{total_dur:<14.1f}{total_cost:<14.3f}")
    print(f"\n明细（最近 {min(8, len(rows))} 条）：")
    for r in rows[-8:]:
        print(f"  [{r['at'][:10]}] {r['project']} | {r['label']} | {r['dur_s']:.0f}s | {r['cost']:.4f}元 | {r['result']}")
    print(f"\n⚠ 以上为估算值（本地执行成本），非真实计费；用于相对对比与趋势观测。")
    return 0

def cmd_record(args):
    rec = {"project": args.project, "stage": args.stage, "skill": args.skill,
           "note": args.note, "at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"✓ 已记录成本行: {rec}")
    return 0

def main():
    p = argparse.ArgumentParser(description="成本观测")
    sub = p.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("report"); s1.add_argument("--project", default=None); s1.set_defaults(fn=cmd_report)
    s2 = sub.add_parser("record")
    for a in ["--project", "--stage", "--skill", "--note"]:
        s2.add_argument(a, default=""); s2.set_defaults(fn=cmd_record)
    a = p.parse_args()
    sys.exit(a.fn(a) or 0)

if __name__ == "__main__":
    main()
