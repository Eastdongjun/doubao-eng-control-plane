#!/usr/bin/env python3
"""西安古城景点查询工具：通过 MCP 通道写入并自动运行验证"""
import json
import urllib.request

BASE = "http://127.0.0.1:8848/mcp"
A = "/Users/donglai/Doubao/chats/2026-09-03/new-chat-6/auto-dev-demo"


def parse_body(body):
    body = body.strip()
    if body.startswith("{"):
        return json.loads(body)
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
        return resp.headers.get("mcp-session-id"), parse_body(resp.read().decode())


def tool_result(body):
    result = (body or {}).get("result", {})
    content = result.get("content", [])
    return "\n".join(c.get("text", "") for c in content if c.get("type") == "text")


# 握手
sid, body = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                 "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                            "clientInfo": {"name": "xian-demo", "version": "1.0"}}})
SESSION = sid
rpc({"jsonrpc": "2.0", "method": "notifications/initialized"}, SESSION)

# 1. MCP 写入西安古城查询工具
code = '''#!/usr/bin/env python3
"""西安古城景点查询工具：查询西安知名古迹与景点信息"""

# 内置西安古城景点数据（名称、年代、类型、简介）
SIGHTS = [
    {"name": "钟楼", "era": "明代", "type": "古建筑", "desc": "西安中心地标，明代钟楼，晨钟报时"},
    {"name": "鼓楼", "era": "明代", "type": "古建筑", "desc": "与钟楼相望，鼓楼暮鼓报时"},
    {"name": "西安城墙", "era": "明代", "type": "古城墙", "desc": "中国现存最完整的古代城垣，可骑行游览"},
    {"name": "大雁塔", "era": "唐代", "type": "佛塔", "desc": "玄奘译经之地，唐代著名佛塔"},
    {"name": "小雁塔", "era": "唐代", "type": "佛塔", "desc": "荐福寺内，唐代密檐式砖塔"},
    {"name": "回民街", "era": "清代", "type": "街区", "desc": "西安著名美食街，回坊风情"},
    {"name": "兵马俑", "era": "秦代", "type": "遗址", "desc": "秦始皇陵陪葬坑，世界第八大奇迹"},
    {"name": "华清池", "era": "唐代", "type": "园林", "desc": "唐代皇家温泉行宫，杨贵妃沐浴之地"},
]


def list_all():
    # 列出全部景点
    print(f"西安古城共有 {len(SIGHTS)} 处知名景点：")
    for i, s in enumerate(SIGHTS, 1):
        print(f"{i}. {s['name']}（{s['era']}·{s['type']}）：{s['desc']}")


def search(keyword):
    # 按关键字搜索景点名称或简介
    hits = [s for s in SIGHTS if keyword in s["name"] or keyword in s["desc"]]
    if not hits:
        print(f"未找到与「{keyword}」相关的景点")
        return
    print(f"搜索「{keyword}」共 {len(hits)} 个结果：")
    for s in hits:
        print(f"  - {s['name']}（{s['era']}·{s['type']}）：{s['desc']}")


def main():
    # 用法：python3 xian_guide.py [搜索关键字]
    import sys
    if len(sys.argv) < 2:
        # 无参数时列出全部景点
        list_all()
        return
    # 有参数时按关键字搜索
    search(sys.argv[1])


if __name__ == "__main__":
    main()
'''
_, body = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
               "params": {"name": "dev_write_file",
                          "arguments": {"path": f"{A}/xian_guide.py", "content": code}}}, SESSION)
print("[写入] " + tool_result(body))

# 2. 运行 1：列出全部
def run(cmd):
    _, body = rpc({"jsonrpc": "2.0", "id": 100, "method": "tools/call",
                   "params": {"name": "dev_run_command",
                              "arguments": {"command": cmd, "cwd": A}}}, SESSION)
    return tool_result(body)

print("\n[运行1] 无参数（列出全部）：")
print(run("python3 xian_guide.py"))
print("\n[运行2] 搜索「唐代」：")
print(run("python3 xian_guide.py 唐代"))
print("\n[运行3] 搜索「城墙」：")
print(run("python3 xian_guide.py 城墙"))

# 3. 打开到 VSCode
_, body = rpc({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
               "params": {"name": "dev_open_file",
                          "arguments": {"path": f"{A}/xian_guide.py"}}}, SESSION)
print("\n[打开] " + tool_result(body))
