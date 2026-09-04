#!/usr/bin/env python3
"""需求追踪矩阵自动生成/回填/校验工具。

在 12 阶段工程化流程中使用，保证「业务目标 → 需求 → 设计 → 代码 → 测试 → 版本 → 指标」全链路可追溯。

用法:
  python3 traceability_matrix.py init   <project_dir>   # 从 阶段2_需求规格.md 提取需求生成矩阵
  python3 traceability_matrix.py update <project_dir>   # 扫描阶段产物回填 设计/代码/测试/版本
  python3 traceability_matrix.py check  <project_dir>   # 校验每项需求是否覆盖全链路
  python3 traceability_matrix.py view   <project_dir>   # 打印当前矩阵
"""
import argparse, pathlib, re, sys

COLUMNS = ["REQ", "需求描述", "验收标准", "设计模块", "代码文件", "测试用例", "发布版本", "运行指标", "状态"]
MATRIX_FILE = "需求追踪矩阵.md"

def load_requirements(spec_md: pathlib.Path):
    """从需求规格提取 US-xx 用户故事与 AC-xx 验收标准"""
    text = spec_md.read_text(encoding="utf-8", errors="replace")
    reqs = []
    # 匹配 ### US-01 标题 及其下的 AC-xx
    blocks = re.split(r"(?m)^###\s+(US-\d+)", text)
    # blocks[0]=前言, 之后成对: id, body
    for i in range(1, len(blocks) - 1, 2):
        req_id, body = blocks[i], blocks[i + 1]
        title = body.split("\n")[0].strip() if body.split("\n") else ""
        acs = re.findall(r"(?m)^[-*]\s*(AC-\d+[^\n]*)", body)
        ac_text = "; ".join(acs) if acs else "（未定义验收标准）"
        reqs.append({"id": req_id, "title": title, "ac": ac_text})
    # 兜底：匹配普通编号需求行（如 "1. xxx"）
    if not reqs:
        for m in re.finditer(r"(?m)^\d+\.\s*(.+)$", text):
            reqs.append({"id": f"REQ-{len(reqs)+1:03d}", "title": m.group(1).strip(), "ac": "（未定义验收标准）"})
    return reqs

def matrix_path(project: pathlib.Path):
    return project / MATRIX_FILE

def gen_matrix(project: pathlib.Path, reqs):
    lines = [
        "# 需求追踪矩阵",
        "",
        f"> 由 traceability_matrix.py 自动生成 · 项目: {project.name} · 时间: {__import__('datetime').datetime.now():%Y-%m-%d %H:%M}",
        "> 追踪链: 业务目标 → REQ → 设计模块 → 代码文件 → 测试用例 → 发布版本 → 运行指标。各阶段完成后运行 `update` 自动回填。",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join(["---"] * len(COLUMNS)) + "|",
    ]
    for r in reqs:
        lines.append(f"| {r['id']} | {r['title']} | {r['ac']} | — | — | — | — | — | 🔲 待开发 |")
    lines.append("")
    return "\n".join(lines)

def cmd_init(args):
    project = pathlib.Path(args.project)
    spec = project / "阶段2_需求规格.md"
    if not spec.exists():
        print(f"✗ 未找到 {spec}（先完成阶段2，产物须命名 阶段2_需求规格.md）"); return 1
    reqs = load_requirements(spec)
    if not reqs:
        print("✗ 未从需求规格提取到任何需求/用户故事"); return 1
    (project / MATRIX_FILE).write_text(gen_matrix(project, reqs), encoding="utf-8")
    print(f"✓ 已生成 {project / MATRIX_FILE}（{len(reqs)} 项需求）")
    return 0

def cmd_update(args):
    project = pathlib.Path(args.project)
    mf = matrix_path(project)
    if not mf.exists():
        print(f"✗ 矩阵不存在，先运行 init"); return 1
    text = mf.read_text(encoding="utf-8")
    # 收集各阶段证据（按文件名粗粒度回填到全部行，人工可按行精修）
    design = ", ".join(sorted(p.name for p in project.glob("阶段4_*.md")) + sorted(p.name for p in project.glob("阶段5_*.md")))
    code_files = ", ".join(sorted(p.name for p in project.glob("阶段7_*.md"))) or ", ".join(
        sorted({p.name for p in project.rglob("*.py") if p.parent != project})[:5]) or "（无代码产物）"
    tests = ", ".join(sorted(p.name for p in project.glob("阶段8_*.md"))) or "（无测试产物）"
    # 版本：从上线/发布/阶段9/10 产物提取
    ver_files = sorted(project.glob("阶段9_*.md")) + sorted(project.glob("阶段10_*.md")) + sorted(project.glob("发布*.md"))
    if ver_files:
        version = "; ".join(p.name for p in ver_files)
    else:
        version = "（未发布）"
    # 更新表头下方每行（跳过表头与分隔行）
    lines = text.split("\n")
    out = []
    for line in lines:
        if line.startswith("| REQ") or line.startswith("|---"):
            out.append(line); continue
        if line.startswith("| ") and "| — |" in line:
            cells = line.split("|")
            # cells: ['', ' REQ ', ' 需求 ', ' AC ', ' — ', ' — ', ' — ', ' — ', ' — ', ' 状态 ', '']
            if len(cells) >= 10:
                cells[4] = f" {design or '—'} "
                cells[5] = f" {code_files} "
                cells[6] = f" {tests} "
                cells[7] = f" {version} "
                cells[9] = " 🟡 已回填 " if design or code_files != "（无代码产物）" else " 🔲 待开发 "
                line = "|".join(cells)
        out.append(line)
    mf.write_text("\n".join(out), encoding="utf-8")
    print(f"✓ 已回填矩阵: 设计[{design or '无'}] 代码[{code_files}] 测试[{tests}] 版本[{version}]")
    return 0

def cmd_check(args):
    project = pathlib.Path(args.project)
    mf = matrix_path(project)
    if not mf.exists():
        print(f"✗ 矩阵不存在，先运行 init"); return 1
    rows = []
    for line in mf.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith("| REQ") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 9:
                rows.append({"id": cells[0], "design": cells[3], "code": cells[4],
                             "test": cells[5], "version": cells[6]})
    total = len(rows)
    full = [r for r in rows if r["design"] != "—" and r["code"] != "—" and r["test"] != "—" and r["version"] != "—"]
    print(f"需求总数: {total} | 全链路覆盖: {len(full)} | 覆盖率: {len(full)/total*100:.0f}%" if total else "无需求")
    missing = [r["id"] for r in rows if not (r["design"] != "—" and r["code"] != "—" and r["test"] != "—" and r["version"] != "—")]
    if missing:
        print("未覆盖需求:", "、".join(missing))
        print("结论: 追踪链未闭环（需补充设计/代码/测试/版本）")
        return 1
    print("结论: ✓ 全部需求追踪链闭环")
    return 0

def cmd_view(args):
    project = pathlib.Path(args.project)
    mf = matrix_path(project)
    if not mf.exists():
        print(f"✗ 矩阵不存在，先运行 init"); return 1
    print(mf.read_text(encoding="utf-8"))
    return 0

def main():
    p = argparse.ArgumentParser(description="需求追踪矩阵工具")
    sub = p.add_subparsers(dest="cmd", required=True)
    for c, fn in [("init", cmd_init), ("update", cmd_update), ("check", cmd_check), ("view", cmd_view)]:
        s = sub.add_parser(c); s.add_argument("project"); s.set_defaults(fn=fn)
    a = p.parse_args()
    sys.exit(a.fn(a) or 0)

if __name__ == "__main__":
    main()
