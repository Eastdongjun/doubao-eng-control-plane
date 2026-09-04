#!/usr/bin/env python3
"""可信执行治理实测：备份→修改→审计→失败→回滚→验证，全链路走一遍"""
import json, shutil, datetime, pathlib

ROOT = pathlib.Path("/Users/donglai/Doubao/chats/2026-09-03/new-chat-6/governance-demo")
GOV = ROOT / ".governance"
BACKUPS = GOV / "backups"
AUDIT = GOV / "audit.jsonl"
TARGET = ROOT / "task.txt"

def now():
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat()

def audit(task, risk, action, target, command="", backup="", result="ok", note=""):
    rec = {"ts": now(), "task": task, "risk": risk, "action": action,
           "target": str(target), "command": command, "backup": str(backup),
           "result": result, "note": note}
    BACKUPS.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec

def backup(path):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S%f")
    dst = BACKUPS / ts / path.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, dst)
    return dst

def read(path):
    return path.read_text(encoding="utf-8").strip()

print("=" * 60)
print("【L1·写入草稿】创建 task.txt v1")
TARGET.write_text("v1: 登录模块需求", encoding="utf-8")
audit("governance-demo", "L1", "create", TARGET, note="首次写入")
print(f"  → {TARGET.name} = {read(TARGET)!r}")

print("【L2·修改前备份】")
bak1 = backup(TARGET)
print(f"  → 备份到 {bak1.relative_to(ROOT)}")

print("【L2·执行修改】v1 → v2")
TARGET.write_text("v2: 登录模块 + 验证码", encoding="utf-8")
audit("governance-demo", "L2", "modify", TARGET, backup=bak1, note="加入验证码")
print(f"  → {TARGET.name} = {read(TARGET)!r}")

print("【L2·第二次修改（将失败）】v2 → v3")
bak2 = backup(TARGET)
audit("governance-demo", "L2", "modify", TARGET, backup=bak2, note="尝试改为 v3（模拟中途异常）")
print("  → 模拟写入中途抛异常...")
try:
    raise RuntimeError("磁盘写入失败（模拟）")
except RuntimeError as e:
    print(f"  → 异常: {e}")

print("【失败回滚】从备份恢复 v2")
shutil.copy2(bak2, TARGET)
restored = read(TARGET)
# 更新该条审计记录为 rolled_back（追加一条回滚记录，保持追加不覆盖）
audit("governance-demo", "L2", "rollback", TARGET, backup=bak2, result="rolled_back", note=f"失败后回滚，恢复内容={restored!r}")
print(f"  → 恢复后 {TARGET.name} = {restored!r}")

print("【验证】内容 == v2 ?", "✓ 通过" if restored == "v2: 登录模块 + 验证码" else "✗ 失败")

print("=" * 60)
print("审计日志（.governance/audit.jsonl）：")
for line in AUDIT.read_text(encoding="utf-8").splitlines():
    d = json.loads(line)
    print(f"  [{d['risk']}] {d['action']:9s} result={d['result']:10s} note={d['note']}")
print("=" * 60)
print("文件树：")
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and ".governance" not in p.parts or p == AUDIT or p == BACKUPS.parent:
        pass
for p in sorted(ROOT.rglob("*")):
    if p.is_file():
        print(" ", p.relative_to(ROOT))
