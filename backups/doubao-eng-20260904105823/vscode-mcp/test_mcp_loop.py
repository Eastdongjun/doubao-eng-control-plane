#!/usr/bin/env python3
"""
MCP 通道完整闭环测试
走真实的 MCP HTTP/JSON-RPC 协议调用 vscode-bridge 的 dev_* 工具，
验证：写代码→运行→查错→修复→完善→回归，以及多项目互不干扰。
"""
import json
import urllib.request

BASE = "http://127.0.0.1:8848/mcp"
A = "/Users/donglai/Doubao/chats/2026-09-03/new-chat-6/auto-dev-demo"
B = "/Users/donglai/Doubao/chats/2026-09-03/new-chat-6/proj-b-demo"


def parse_body(body: str):
    """streamable-http 可能返回 JSON 或 SSE，统一解析为 dict"""
    body = body.strip()
    if body.startswith("{"):
        return json.loads(body)
    # SSE: 多行 event: message / data: {...}
    last = None
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("data:"):
            try:
                last = json.loads(line[5:].strip())
            except Exception:
                pass
    return last


def rpc(payload, session=None):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(BASE, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json, text/event-stream")
    if session:
        req.add_header("Mcp-Session-Id", session)
    with urllib.request.urlopen(req, timeout=90) as resp:
        sid = resp.headers.get("mcp-session-id")
        return sid, parse_body(resp.read().decode())


def tool_result(body):
    """提取 tools/call 返回的文本结果"""
    if not body:
        return "(空响应)"
    result = body.get("result", {})
    content = result.get("content", [])
    texts = [c.get("text", "") for c in content if c.get("type") == "text"]
    return "\n".join(texts) if texts else json.dumps(result, ensure_ascii=False)


def run_command(command, cwd):
    sid, body = rpc({
        "jsonrpc": "2.0", "id": 100, "method": "tools/call",
        "params": {"name": "dev_run_command", "arguments": {"command": command, "cwd": cwd}}
    }, SESSION)
    text = tool_result(body)
    try:
        d = json.loads(text)
        return d.get("exit_code"), d.get("stdout", "").strip(), d.get("stderr", "").strip()
    except Exception:
        return None, text, ""


# 1. 握手
sid, body = rpc({
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
               "clientInfo": {"name": "mcp-loop-test", "version": "1.0"}}
})
print(f"[1] MCP 握手: serverInfo={body.get('result', {}).get('serverInfo')}")
SESSION = sid
rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, SESSION)

# 2. 写入第一版 logstats.py（故意带缺陷：文件不存在会崩溃）
logstats_v1 = '''#!/usr/bin/env python3
"""日志统计工具：统计日志文件行数与关键字出现次数"""

import sys


def count_lines(path):
    # 统计文件行数
    with open(path) as f:
        return len(f.readlines())


def count_keyword(lines, keyword):
    # 统计关键字出现次数
    total = 0
    for line in lines:
        if keyword in line:
            total += 1
    return total


def main():
    # 用法：python3 logstats.py <日志文件> <关键字>
    if len(sys.argv) < 3:
        print("用法：python3 logstats.py <日志文件> <关键字>")
        return
    path = sys.argv[1]
    keyword = sys.argv[2]
    lines = open(path).readlines()
    print(f"文件 {path} 共 {count_lines(path)} 行")
    print(f"关键字 '{keyword}' 出现 {count_keyword(lines, keyword)} 次")


if __name__ == "__main__":
    main()
'''
_, body = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
               "params": {"name": "dev_write_file",
                          "arguments": {"path": f"{A}/logstats.py", "content": logstats_v1}}}, SESSION)
print(f"[2] 写入第一版: {tool_result(body)}")

# 3. 造一个测试日志
demo_log = """[2026-09-04 10:00:00] INFO 服务启动成功
[2026-09-04 10:00:01] INFO 用户登录 userId=1001
[2026-09-04 10:00:02] ERROR 数据库连接超时
[2026-09-04 10:00:03] INFO 重试成功
[2026-09-04 10:00:04] ERROR 接口 /api/order 500
"""
_, body = rpc({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
               "params": {"name": "dev_write_file",
                          "arguments": {"path": f"{A}/app.log", "content": demo_log}}}, SESSION)
print(f"[3] 造测试日志: {tool_result(body)}")

# 4. 运行（成功路径）
code, out, err = run_command("python3 logstats.py app.log INFO", A)
print(f"[4] 运行成功路径 → exit={code}\n    stdout: {out or err}")

# 5. 运行缺陷路径（文件不存在 → 预期崩溃）
code, out, err = run_command("python3 logstats.py missing.log INFO", A)
print(f"[5] 运行缺陷路径（文件不存在）→ exit={code}\n    stderr 前 160 字:\n    {err[:160]}")

# 6. 自动修复：try/except FileNotFoundError + utf-8 编码
_, body = rpc({"jsonrpc": "2.0", "id": 6, "method": "tools/call",
               "params": {"name": "dev_edit_file",
                          "arguments": {
                              "path": f"{A}/logstats.py",
                              "old_string": "    lines = open(path).readlines()",
                              "new_string": "    try:\n"
                                            "        lines = open(path, encoding=\"utf-8\").readlines()\n"
                                            "    except FileNotFoundError:\n"
                                            "        # 文件不存在时给出友好提示，避免程序崩溃\n"
                                            "        print(f\"错误：日志文件不存在：{path}\")\n"
                                            "        return"
                          }}}, SESSION)
print(f"[6] 自动修复: {tool_result(body)}")

# 7. 回归：成功路径
code, out, err = run_command("python3 logstats.py app.log INFO", A)
print(f"[7] 回归·成功路径 → exit={code}\n    stdout: {out or err}")

# 8. 回归：缺陷路径（现在应友好提示）
code, out, err = run_command("python3 logstats.py missing.log INFO", A)
print(f"[8] 回归·缺陷路径 → exit={code}\n    stdout: {out or err}")

# 9. 多项目隔离：读取项目B内容，确认零污染
_, body = rpc({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
               "params": {"name": "dev_list_dir", "arguments": {"path": B}}}, SESSION)
print(f"[9] 项目B目录（应只有 task.md，无 logstats/app.log）:\n{tool_result(body)}")

# 10. 最终代码回读确认注释完善
_, body = rpc({"jsonrpc": "2.0", "id": 10, "method": "tools/call",
               "params": {"name": "dev_read_file", "arguments": {"path": f"{A}/logstats.py"}}}, SESSION)
print("[10] 最终 logstats.py（MCP 回读验证）:\n" + tool_result(body))

print("\n===== MCP 闭环测试完成 =====")
