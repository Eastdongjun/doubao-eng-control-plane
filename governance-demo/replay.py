#!/usr/bin/env python3
"""任务执行回放：基于 trace.jsonl 重建复杂任务的执行时间线
用法: replay.py list                       # 任务列表
      replay.py <task_id>                  # 终端时间线回放
      replay.py <task_id> --html           # 生成 HTML 回放页（可打开）
"""
import argparse, datetime, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRACE = ROOT / ".governance" / "trace.jsonl"

def load():
    if not TRACE.exists():
        print("✗ 无 trace 记录，先运行 task_trace.py"); return {}
    recs = {}
    for line in TRACE.read_text(encoding="utf-8").splitlines():
        if not line.strip(): continue
        try:
            r = json.loads(line); recs[r["task_id"]] = r
        except (json.JSONDecodeError, KeyError):
            continue
    return recs

def fmt_dur(ms):
    return f"{ms}ms" if ms is not None else "-"

def fmt_at(at):
    try:
        return datetime.datetime.fromisoformat(at).strftime("%H:%M:%S")
    except (ValueError, TypeError):
        return at or "-"

def terminal(rec):
    icon = {"success": "✓", "fail": "✗", "partial": "◐"}.get(rec.get("result"), "·")
    print("=" * 58)
    print(f"{icon} 任务 {rec['task_id']}  [{rec.get('result') or '进行中'}]  "
          f"总耗时 {fmt_dur(rec.get('duration_ms'))}")
    print(f"  意图  : {rec.get('intent')}")
    if rec.get("plan"):
        print(f"  计划  : {' → '.join(rec['plan'])}")
    if rec.get("fail_point"):
        print(f"  失败点: {rec['fail_point']}")
    print("-" * 58)
    steps = rec.get("steps", [])
    if not steps:
        print("  （无步骤记录）")
    for idx, s in enumerate(steps, start=1):
        bar = "│" * 0
        print(f"  {idx:>2}. [{fmt_at(s.get('at'))}] {s.get('tool'):<22} {fmt_dur(s.get('duration_ms')):>10}  {s.get('desc','')}")
    print("=" * 58)

def html(rec):
    icon = {"success": "✅", "fail": "❌", "partial": "⚠️"}.get(rec.get("result"), "⏳")
    steps_html = []
    for idx, s in enumerate(rec.get("steps", []), start=1):
        steps_html.append(f"""
      <div style="position:relative;padding:10px 14px;margin:6px 0 6px 22px;background:#fff;border:1px solid rgba(0,0,0,0.08);border-radius:10px;box-sizing:border-box;">
        <div style="position:absolute;left:-16px;top:14px;width:10px;height:10px;border-radius:50%;background:#9EACEA;border:2px solid #fff;"></div>
        <div style="font-size:12px;font-weight:600;">{idx}. {s.get('tool','')} <span style="color:#6B7280;font-weight:400;">({fmt_dur(s.get('duration_ms'))})</span></div>
        <div style="font-size:11px;color:#6B7280;margin-top:2px;">{s.get('desc','')}</div>
        <div style="font-size:10px;color:#9CA3AF;margin-top:2px;">{fmt_at(s.get('at'))}</div>
      </div>""")
    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>任务回放 {rec['task_id']}</title></head>
<body style="margin:0;padding:20px;background:#F4F3EE;font-family:'PingFang SC','Roboto','Segoe UI',Arial,sans-serif;color:#1A1B1C;">
  <div style="max-width:720px;margin:0 auto;">
    <div style="padding:18px;border-radius:14px;background:linear-gradient(135deg,rgba(158,172,234,0.25),rgba(148,216,195,0.35));box-sizing:border-box;">
      <div style="font-size:18px;font-weight:600;">{icon} 任务回放 · {rec['task_id']}</div>
      <div style="font-size:12px;color:#4B5563;margin-top:6px;">{rec.get('intent','')}</div>
      <div style="font-size:11px;color:#6B7280;margin-top:4px;">结果: {rec.get('result') or '进行中'} ｜ 总耗时 {fmt_dur(rec.get('duration_ms'))} ｜ 创建 {rec.get('created_at','')}</div>
      {('<div style="font-size:11px;color:#B45309;margin-top:6px;">⚠ 失败点: '+rec['fail_point']+'</div>') if rec.get('fail_point') else ''}
    </div>
    <div style="margin-top:14px;">
      {(''.join(steps_html)) if steps_html else '<div style="color:#6B7280;font-size:12px;">（无步骤记录）</div>'}
    </div>
    <div style="font-size:10px;color:#9CA3AF;margin-top:16px;text-align:center;">由 doubao-eng Task Trace 生成 · 只读回放</div>
  </div>
</body></html>"""
    out = ROOT / "_replay" / f"{rec['task_id']}.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"✓ HTML 回放页已生成: {out}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task", nargs="?", default=None)
    ap.add_argument("--html", action="store_true")
    args = ap.parse_args()
    recs = load()
    if args.task is None or args.task == "list":
        items = sorted(recs.values(), key=lambda r: r.get("created_at", ""), reverse=True)
        print("任务回放清单:")
        for r in items:
            icon = {"success": "✓", "fail": "✗", "partial": "◐"}.get(r.get("result"), "·")
            print(f"  {icon} {r['task_id']}  [{r.get('result') or '进行中'}]  {len(r.get('steps', []))}步  {fmt_dur(r.get('duration_ms'))}  {r.get('created_at','')}")
            print(f"      {r.get('intent','')[:48]}")
        return 0
    rec = recs.get(args.task)
    if not rec:
        print(f"✗ 任务不存在: {args.task}"); return 1
    if args.html:
        html(rec)
    else:
        terminal(rec)
    return 0

if __name__ == "__main__":
    sys.exit(main())
