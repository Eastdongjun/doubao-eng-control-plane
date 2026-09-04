#!/usr/bin/env python3
"""
VSCode 桥接 MCP Server（vscode_bridge_mcp）
============================================
让豆包通过 MCP 协议与本地 VSCode 开发环境交互：
写代码 → 运行 → 查错 → 修改 → 注释 → 完善，形成自动开发闭环。

工具一览（参数全部扁平，便于 Agent 直接调用）：
  dev_open_project(path)    在 VSCode 中打开/聚焦项目目录
  dev_open_file(path)       在 VSCode 中打开指定文件
  dev_list_dir(path)        列出目录内容
  dev_read_file(path)       读取文件（UTF-8，带行号）
  dev_write_file(path, content)  写入文件（新建/覆盖）
  dev_edit_file(path, old_string, new_string)  精确替换（diff 式编辑）
  dev_search(pattern, path) 在项目中搜索文本
  dev_run_command(command, cwd)  执行命令，返回退出码与输出

安全边界：
  - 仅监听 127.0.0.1:8848，不对外网开放
  - 所有文件操作限制在允许根目录（VSCODE_MCP_ROOTS 环境变量，默认 ~）
"""
import asyncio
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vscode_bridge_mcp", host="127.0.0.1", port=8848)

# 允许操作的文件根目录（逗号分隔，默认用户主目录）
_DEFAULT_ROOT = str(Path.home())
ALLOWED_ROOTS = [os.path.abspath(p) for p in os.environ.get("VSCODE_MCP_ROOTS", _DEFAULT_ROOT).split(",") if p.strip()]

CODE_CLI = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"


# ---------------------------------------------------------------------------
# 共享工具函数
# ---------------------------------------------------------------------------

def _resolve(path: str) -> Path:
    """解析为绝对路径，并校验必须在允许根目录内。"""
    p = Path(path).expanduser().resolve()
    for root in ALLOWED_ROOTS:
        if p == Path(root) or p.is_relative_to(root):
            return p
    raise PermissionError(f"路径不在允许根目录内（允许: {ALLOWED_ROOTS}）：{p}")


def _fmt_err(e: Exception) -> str:
    """统一错误格式，给 Agent 可执行的下一步提示。"""
    return f"错误: {type(e).__name__}: {e}"


def _find_git_root(path: Path) -> Optional[Path]:
    """从文件所在目录向上找第一个含 .git 的项目根（Sonar 检查的项目边界）。"""
    cur = path.parent if path.is_file() else path
    for d in [cur, *cur.parents]:
        if (d / ".git").exists():
            return d
    return None


def _sonar_check(path: Path) -> str:
    """写后即时 Sonar 单文件检查：返回目标文件问题状态（0 problems 或问题清单）。
    基于 engineering problems <root> --json --file <rel>，全仓规则口径（含跨文件 S1192）。"""
    try:
        root = _find_git_root(path)
        if root is None:
            return ""
        rel = path.relative_to(root)
        eng = Path(__file__).resolve().parent.parent / "governance-demo" / "engineering.py"
        if not eng.exists():
            return "\n⚠ Sonar 检查跳过（engineering.py 不存在）"
        r = subprocess.run([sys.executable, str(eng), "problems", str(root), "--json", "--file", str(rel)],
                           capture_output=True, text=True, timeout=30)
        if r.returncode not in (0, 1):
            return f"\n⚠ Sonar 检查失败: {r.stderr.strip()[:120]}"
        d = json.loads(r.stdout)
        n = d["problems_count"]
        if n == 0:
            return "\n🟢 Sonar 单文件检查: 0 problems ✓"
        lines = [f"\n🔴 Sonar 检查 {n} 个问题（本文件）:"]
        for p in d["problems"][:8]:
            lines.append(f"  {p['rule']} L{p['line']} {p['message'][:60]}")
        if n > 8:
            lines.append(f"  … 共 {n} 个（运行 engineering improve 查看全部）")
        return "\n".join(lines)
    except Exception as e:
        return f"\n⚠ Sonar 检查异常: {e}"


# ---------------------------------------------------------------------------
# 工具实现（展开参数，schema 扁平）
# ---------------------------------------------------------------------------

@mcp.tool(
    name="dev_open_project",
    annotations={"title": "在 VSCode 打开项目", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
)
async def dev_open_project(path: str) -> str:
    '''在 VSCode 中打开/聚焦指定项目目录。

    当用户要求"在 VSCode 里看项目"、或代码写好后需要展示时调用。
    Args:
        path: 项目目录绝对路径（例如 /Users/donglai/myapp）
    Returns: 打开结果提示
    '''
    try:
        p = _resolve(path)
        if not p.is_dir():
            return f"错误: 目录不存在: {p}"
        proc = await asyncio.create_subprocess_exec(
            CODE_CLI, "-r", str(p),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.communicate()
        return f"已在 VSCode 中打开项目: {p}"
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_open_file",
    annotations={"title": "在 VSCode 打开文件", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
)
async def dev_open_file(path: str) -> str:
    '''在 VSCode 中打开指定文件（聚焦所在窗口）。写代码/改代码后调用展示。'''
    try:
        p = _resolve(path)
        if not p.is_file():
            return f"错误: 文件不存在: {p}"
        proc = await asyncio.create_subprocess_exec(
            CODE_CLI, "-r", str(p),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        await proc.communicate()
        return f"已在 VSCode 中打开文件: {p}"
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_list_dir",
    annotations={"title": "列出目录内容", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
)
async def dev_list_dir(path: str = ".", show_hidden: bool = False) -> str:
    '''列出目录下的条目（名称+类型+大小），帮助了解项目结构。
    Args:
        path: 目录绝对路径（默认当前项目目录）
        show_hidden: 是否显示隐藏文件
    '''
    try:
        p = _resolve(path)
        if not p.is_dir():
            return f"错误: 目录不存在: {p}"
        entries = []
        for child in sorted(p.iterdir()):
            if child.name.startswith(".") and not show_hidden:
                continue
            kind = "dir" if child.is_dir() else "file"
            size = child.stat().st_size if child.is_file() else ""
            entries.append({"name": child.name, "type": kind, "size": size})
        return json.dumps({"path": str(p), "count": len(entries), "entries": entries}, ensure_ascii=False, indent=2)
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_read_file",
    annotations={"title": "读取文件", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
)
async def dev_read_file(path: str, offset: Optional[int] = None, limit: Optional[int] = None) -> str:
    '''读取文件内容（UTF-8），带行号返回，便于定位代码。
    Args:
        path: 文件绝对路径
        offset: 起始行号（1 起）
        limit: 返回最大行数
    '''
    try:
        p = _resolve(path)
        if not p.is_file():
            return f"错误: 文件不存在: {p}"
        text = p.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        start = (offset - 1) if offset else 0
        end = start + limit if limit else len(lines)
        selected = lines[start:end]
        numbered = [f"{i+1:>5} | {ln}" for i, ln in enumerate(selected, start=start)]
        return f"文件: {p}  共 {len(lines)} 行  显示 {len(selected)} 行\n" + "\n".join(numbered)
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_write_file",
    annotations={"title": "写入文件", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": True, "openWorldHint": False}
)
async def dev_write_file(path: str, content: str) -> str:
    '''写入/覆盖文件（UTF-8），父目录不存在自动创建。自动编码循环的主写入工具，写完 VSCode 实时可见。
    Args:
        path: 文件绝对路径
        content: 完整文件内容（含中文注释）
    '''
    try:
        p = _resolve(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"已写入 {p}（{len(content.encode('utf-8'))} 字节）{_sonar_check(p)}"
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_edit_file",
    annotations={"title": "精确编辑文件", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": False}
)
async def dev_edit_file(path: str, old_string: str, new_string: str, replace_all: bool = False) -> str:
    '''在文件中做精确文本替换（类似编辑器查找替换）。修复 bug、补注释、完善逻辑时使用。
    Args:
        path: 文件绝对路径
        old_string: 要替换的原文（必须与文件内容完全匹配且唯一，除非 replace_all=True）
        new_string: 替换后的新文本
        replace_all: 是否替换所有匹配项
    '''
    try:
        p = _resolve(path)
        if not p.is_file():
            return f"错误: 文件不存在: {p}"
        text = p.read_text(encoding="utf-8")
        count = text.count(old_string)
        if count == 0:
            return f"错误: 未找到匹配文本: {old_string[:80]}"
        if count > 1 and not replace_all:
            return f"错误: 匹配到 {count} 处，old_string 不唯一，请加更多上下文或设 replace_all=True"
        p.write_text(text.replace(old_string, new_string), encoding="utf-8")
        return f"已替换 {count} 处 → {p}{_sonar_check(p)}"
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_search",
    annotations={"title": "搜索代码", "readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
)
async def dev_search(pattern: str, path: str = ".", glob: Optional[str] = None, max_results: int = 50) -> str:
    '''在目录中按正则/文本搜索，返回 文件:行号:内容。定位代码、找引用时使用。
    Args:
        pattern: 正则表达式或普通文本
        path: 搜索起点目录
        glob: 文件过滤（如 *.py、*.{js,ts}）
        max_results: 最多返回匹配行数
    '''
    try:
        root = _resolve(path)
        if not root.is_dir():
            return f"错误: 目录不存在: {root}"
        import fnmatch
        rx = re.compile(pattern)
        results = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith((".git", "node_modules", ".venv", "__pycache__", "venv"))]
            for fn in filenames:
                if glob and not fnmatch.fnmatch(fn, glob):
                    continue
                fp = Path(dirpath) / fn
                try:
                    for i, line in enumerate(fp.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                        if rx.search(line):
                            rel = fp.relative_to(root)
                            results.append(f"{rel}:{i}: {line.strip()[:160]}")
                            if len(results) >= max_results:
                                return json.dumps({"count": len(results), "results": results}, ensure_ascii=False, indent=2)
                except (OSError, UnicodeDecodeError):
                    continue
        return json.dumps({"count": len(results), "results": results}, ensure_ascii=False, indent=2)
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_typewrite",
    annotations={"title": "打字机模式逐行写入", "readOnlyHint": False, "destructiveHint": True, "idempotentHint": False, "openWorldHint": False}
)
async def dev_typewrite(path: str, content: str, interval_ms: int = 200) -> str:
    '''打字机模式：把完整内容按行逐行追加写入文件，每行之间间隔 interval_ms 毫秒。
    配合 dev_open_file 使用：先打开（空）文件，再调用本工具，VSCode 里会看到代码
    一行一行"长"出来，像真人逐行打字——但全程是后台文件写入，不碰键盘、不抢焦点。
    Args:
        path: 文件绝对路径
        content: 完整文件内容（含中文注释），会清空后逐行写入
        interval_ms: 每行间隔毫秒数（默认 200，范围 0-2000）
    '''
    try:
        p = _resolve(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        iv = max(0, min(2000, interval_ms))
        p.write_text("", encoding="utf-8")  # 清空，从头写
        lines = content.split("\n")
        total = len(lines)
        for i, ln in enumerate(lines):
            with p.open("a", encoding="utf-8") as f:
                f.write(ln)
                if i < total - 1:
                    f.write("\n")
                f.flush()
                os.fsync(f.fileno())
            if i < total - 1 and iv > 0:
                await asyncio.sleep(iv / 1000.0)
        return f"打字机模式完成：{p}（{total} 行，间隔 {iv}ms，共约 {total * iv / 1000:.1f}s）{_sonar_check(p)}"
    except Exception as e:
        return _fmt_err(e)


@mcp.tool(
    name="dev_run_command",
    annotations={"title": "执行开发命令", "readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": False}
)
async def dev_run_command(command: str, cwd: str = ".", timeout: int = 60) -> str:
    '''在项目目录执行命令（如 python3 main.py / npm test / go build），返回退出码、标准输出、标准错误。
    自动编码循环的运行/查错环节：运行失败时根据 stderr 定位问题再修改。
    Args:
        command: 要执行的命令
        cwd: 工作目录（项目目录绝对路径）
        timeout: 超时秒数（默认 60）
    Returns: {exit_code, cwd, command, stdout, stderr}
    '''
    try:
        cwd_p = _resolve(cwd)
        if not cwd_p.is_dir():
            return f"错误: 工作目录不存在: {cwd_p}"
        import shlex
        argv = shlex.split(command)
        proc = await asyncio.create_subprocess_exec(
            *argv,
            cwd=str(cwd_p),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            proc.kill()
            return json.dumps({"exit_code": -1, "stdout": "", "stderr": f"命令超时（>{timeout}s），已终止"}, ensure_ascii=False)
        out = stdout.decode("utf-8", errors="replace")
        err = stderr.decode("utf-8", errors="replace")
        return json.dumps({
            "exit_code": proc.returncode,
            "cwd": str(cwd_p),
            "command": command,
            "stdout": out[-8000:],
            "stderr": err[-4000:],
        }, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return f"错误: 命令不存在: {command}"
    except Exception as e:
        return _fmt_err(e)


# ---------- SonarQube 硬门禁（engineering 桥） ----------
_ENGINEERING = str(Path(__file__).resolve().parent.parent / "governance-demo" / "engineering.py")


async def _run_engineering(args: list, cwd: str) -> str:
    """运行 engineering CLI 并返回结构化结果"""
    proc = await asyncio.create_subprocess_exec(
        sys.executable, _ENGINEERING, *args,
        cwd=cwd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
    except asyncio.TimeoutError:
        proc.kill()
        return json.dumps({"exit_code": -1, "stdout": "", "stderr": "engineering 超时（>120s）"}, ensure_ascii=False)
    return json.dumps({
        "exit_code": proc.returncode,
        "stdout": stdout.decode("utf-8", errors="replace")[-6000:],
        "stderr": stderr.decode("utf-8", errors="replace")[-2000:],
    }, ensure_ascii=False, indent=2)


@mcp.tool(
    name="engineering_problems",
    description="SonarQube 硬门禁检查：对项目根目录跑规则检查（S1192重复串/S3776复杂度/S8688时区/S1172未用参数/S1168 null集合/S6204 toList/S3358嵌套三元/S107参数过多 等），返回 problems 列表。AI 写完代码后必须立即调用本工具；只要 problems 非 0 就不能宣称完成。",
)
async def engineering_problems(path: str) -> str:
    cwd_p = _resolve(path)
    if not cwd_p.is_dir():
        return json.dumps({"exit_code": 2, "stdout": "", "stderr": f"项目根不存在: {path}"}, ensure_ascii=False)
    return await _run_engineering(["problems", str(cwd_p), "--json"], cwd=str(cwd_p.parent))


@mcp.tool(
    name="engineering_improve",
    description="SonarQube 自动优化循环：对项目根跑检查并把剩余问题写入 <root>/.ai/evidence/improve-state.json（含 rule/message/suggestion）。AI 必须读取该文件按 diagnostics 逐条修复，修完重跑 engineering_problems 直到 0 problems（PASS）。",
)
async def engineering_improve(path: str) -> str:
    cwd_p = _resolve(path)
    if not cwd_p.is_dir():
        return json.dumps({"exit_code": 2, "stdout": "", "stderr": f"项目根不存在: {path}"}, ensure_ascii=False)
    return await _run_engineering(["improve", str(cwd_p)], cwd=str(cwd_p.parent))


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
