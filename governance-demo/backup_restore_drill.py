#!/usr/bin/env python3
"""备份/恢复演练：备份关键工程化资产 → 模拟丢失 → 从备份恢复 → 校验一致性"""
import datetime, hashlib, pathlib, shutil, json, sys

ROOT = pathlib.Path("/Users/donglai/Doubao/chats/2026-09-03/new-chat-6")
SRC = [
    ("vscode-mcp/server.py", "MCP Server 主程序"),
    ("vscode-mcp/test_mcp_loop.py", "MCP 闭环测试"),
    ("governance-demo", "可信执行治理实测"),
    ("skills/自动编码循环/SKILL.md", "自动编码循环技能"),
    ("skills/可信执行治理/SKILL.md", "可信执行治理技能"),
    ("skills/工程化总控/SKILL.md", "工程化总控技能"),
]
DRY_RUN = len(sys.argv) > 1 and sys.argv[1] == "--simulate-ok"

def md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()

def main():
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_dir = ROOT / f"backups/doubao-eng-{ts}"
    work_dir = ROOT / f"_drill/{ts}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 62)
    print("【阶段1·备份】关键工程化资产 → " + backup_dir.relative_to(ROOT).as_posix())
    manifest = []
    for rel, label in SRC:
        src = ROOT / rel
        if not src.exists():
            print(f"  ✗ 缺失: {rel}")
            continue
        dst = backup_dir / rel
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
            files = [p for p in dst.rglob("*") if p.is_file()]
            total = sum(len(p.read_bytes()) for p in files)
            print(f"  ✓ {label}: 目录 {len(files)} 文件, {total} 字节")
            for f in files:
                relf = f.relative_to(dst)
                manifest.append({"rel": f"{rel}/{relf}", "md5": md5(f)})
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  ✓ {label}: {md5(src)[:8]}… {src.stat().st_size} 字节")
            manifest.append({"rel": rel, "md5": md5(src)})
    (backup_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → manifest.json {len(manifest)} 条校验记录")

    # 模拟恢复目标：drill 工作区（不碰真实源）
    print("\n【阶段2·模拟】把资产「复制」到演练区，然后模拟丢失/损坏")
    for rel, label in SRC:
        src = ROOT / rel
        if not src.exists():
            continue
        dst = work_dir / rel
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    print("  → 已复制到演练区:", work_dir.relative_to(ROOT).as_posix())

    # 模拟事故：删除 + 篡改演练区多个关键文件（覆盖"文件丢失"与"内容损坏"两类）
    victims = [
        ("vscode-mcp/server.py", "删除"),
        ("skills/工程化总控/SKILL.md", "删除"),
        ("governance-demo/capability_registry.py", "篡改"),
    ]
    for rel, kind in victims:
        v = work_dir / rel
        if v.exists():
            if kind == "删除":
                v.unlink()
                print(f"  ✗ 模拟事故[{kind}]: {rel}")
            else:
                v.write_text("# 被恶意篡改的内容\n", encoding="utf-8")
                print(f"  ✗ 模拟事故[{kind}]: {rel}")
        else:
            print(f"  ⚠ 演练区无 {rel}（备份时该资产缺失）")

    print("\n【阶段3·恢复】从备份恢复全部 manifest 条目到演练区")
    manifest = json.loads((backup_dir / "manifest.json").read_text(encoding="utf-8"))
    restored = 0
    for entry in manifest:
        dst = work_dir / entry["rel"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup_dir / entry["rel"], dst)
        restored += 1
    print(f"  → 已恢复 {restored} 个文件")

    print("\n【阶段4·校验】全量 manifest md5 一致性")
    ok_count = 0
    fail = []
    for entry in manifest:
        f = work_dir / entry["rel"]
        if not f.exists():
            fail.append((entry["rel"], "缺失"))
            continue
        cur = md5(f)
        if cur == entry["md5"]:
            ok_count += 1
        else:
            fail.append((entry["rel"], "md5 不一致"))
    total = len(manifest)
    print(f"  校验 {ok_count}/{total} 一致")
    for rel, why in fail[:8]:
        print(f"  ✗ {rel}: {why}")
    ok = ok_count == total
    print("  结果:", "✓ 全量备份可完整恢复，回滚端到端演练通过" if ok else f"✗ {len(fail)} 项恢复失败")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
