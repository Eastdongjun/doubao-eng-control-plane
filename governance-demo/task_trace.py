#!/usr/bin/env python3
"""Task Trace: 复杂任务结构化执行追踪（追加写入 .governance/trace.jsonl）"""
import argparse, datetime, json, pathlib, sys

TRACE = pathlib.Path(__file__).resolve().parent.parent / ".governance" / "trace.jsonl"

def load():
    records = {}
    if TRACE.exists():
        for line in TRACE.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
                records[r["task_id"]] = r
            except (json.JSONDecodeError, KeyError):
                continue
    return records

def save(records):
    TRACE.parent.mkdir(parents=True, exist_ok=True)
    with TRACE.open("w", encoding="utf-8") as f:
        for r in records.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def now():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def cmd_start(args):
    recs = load()
    rec = {
        "task_id": args.task, "intent": args.intent,
        "plan": [s.strip() for s in args.plan.split("|") if s.strip()],
        "steps": [], "result": None, "fail_point": None,
        "duration_ms": None, "model": args.model, "created_at": now(),
    }
    recs[args.task] = rec
    save(recs)
    print(f"✓ 任务已开启: {args.task} | 意图: {args.intent[:40]}")

def cmd_step(args):
    recs = load()
    rec = recs.get(args.task)
    if not rec:
        print(f"✗ 任务不存在: {args.task}"); return 1
    rec["steps"].append({
        "tool": args.tool, "desc": args.desc,
        "duration_ms": args.duration_ms, "at": now(),
    })
    save(recs)
    print(f"✓ 步骤记录: {args.tool} — {args.desc[:40]}")

def cmd_end(args):
    recs = load()
    rec = recs.get(args.task)
    if not rec:
        print(f"✗ 任务不存在: {args.task}"); return 1
    rec["result"] = args.result
    rec["duration_ms"] = args.duration_ms
    if args.result == "fail":
        if not args.fail_point:
            print("✗ 失败任务必须提供 --fail_point"); return 1
        rec["fail_point"] = args.fail_point
    save(recs)
    print(f"✓ 任务结束: {args.task} → {args.result} ({args.duration_ms}ms)"
          + (f" | 失败点: {args.fail_point}" if args.fail_point else ""))

def cmd_list(args):
    recs = load()
    items = sorted(recs.values(), key=lambda r: r["created_at"], reverse=True)[: args.last]
    for r in items:
        icon = {"success": "✓", "fail": "✗", "partial": "◐"}.get(r["result"], "·")
        n_steps = len(r["steps"])
        print(f"{icon} {r['task_id']}  [{r['result'] or '进行中'}] {n_steps}步 "
              f"{r['duration_ms'] or '-'}ms  {r['created_at']}")
        print(f"    意图: {r['intent'][:50]}")
        if r.get("fail_point"):
            print(f"    失败点: {r['fail_point']}")
    print(f"（共 {len(recs)} 条 trace）")

def main():
    p = argparse.ArgumentParser(description="Task Trace")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("start"); sp.add_argument("--task", required=True)
    sp.add_argument("--intent", required=True); sp.add_argument("--plan", default="")
    sp.add_argument("--model", default=""); sp.set_defaults(fn=cmd_start)
    sp = sub.add_parser("step"); sp.add_argument("--task", required=True)
    sp.add_argument("--tool", required=True); sp.add_argument("--desc", default="")
    sp.add_argument("--duration_ms", type=int, default=0); sp.set_defaults(fn=cmd_step)
    sp = sub.add_parser("end"); sp.add_argument("--task", required=True)
    sp.add_argument("--result", choices=["success", "fail", "partial"], required=True)
    sp.add_argument("--fail_point", default=""); sp.add_argument("--duration_ms", type=int, default=0)
    sp.set_defaults(fn=cmd_end)
    sp = sub.add_parser("list"); sp.add_argument("--last", type=int, default=10)
    sp.set_defaults(fn=cmd_list)
    a = p.parse_args()
    sys.exit(a.fn(a) or 0)

if __name__ == "__main__":
    main()
