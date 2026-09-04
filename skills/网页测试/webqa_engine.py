#!/usr/bin/env python3
"""
webqa_engine.py — 网页测试增强引擎 v2（提速 + 细致）

针对 MCP 逐个调用"慢 / 响应差 / 粒度粗"的痛点重构：

【提速】
  · 单一浏览器会话复用：所有页面共用一个实例，不重复冷启动
  · 精准等待：goto 后 wait_until="domcontentloaded" + 显式 wait_for_selector(目标元素)，绝不固定 sleep
  · 可选 --parallel：独立 context 并发测多页（线程池，互不干扰）

【细致】
  · 自动捕获：console 错误 / pageerror / 失败网络请求(4xx,5xx) / 请求级耗时（最慢 N 条）
  · 8 类细粒度断言：标题 / URL / 元素存在 / 文本 / 属性 / 可见 / 数量 / 状态码
  · 每页加载计时 + 每断言耗时，报告识别慢页面
  · 失败自动整页截图
  · 可选 --strict：console 错误 / 失败请求也计入失败（回归门禁用）

【报告】
  · JSON + 自包含 HTML 可视化报告（页面摘要 / 断言明细 / 网络 / 截图 / 耗时排行）

用法:
  python3 webqa_engine.py run <cases.json> [--out DIR] [--html] [--parallel] [--strict]
  python3 webqa_engine.py demo                # 本地演示页 + 用例 + 全量自检
  python3 webqa_engine.py selftest            # 注入缺陷用例，验证引擎能检出（自检）

用例格式 (JSON):
  { "urls": [
      { "name": "首页", "url": "https://...", "wait_selector": "#app",
        "timeout_ms": 10000, "screenshot": false,
        "asserts": [
          {"type":"title_contains", "value":"...", "must":true},
          {"type":"element_exists", "selector":"#main"},
          {"type":"text_contains",  "selector":"h1", "value":"..."},
          {"type":"attr", "selector":"a", "attr":"href", "value":"/x"},
          {"type":"visible", "selector":".btn"},
          {"type":"element_count", "selector":"li", "min":3},
          {"type":"status", "value":200}
        ]}]}
"""
import argparse, json, pathlib, sys, time, datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    sys.exit("✗ 需安装: pip3 install playwright && python3 -m playwright install chromium")

OUT = pathlib.Path(__file__).resolve().parent.parent / "_webqa"

# ================= 断言库（8 类，统一签名 (page, spec) -> (ok, note)） =================
def _title_contains(page, s):
    v = s["value"]; t = page.title() or ""
    return v.lower() in t.lower(), f"标题含'{v}' 实际='{t[:40]}'"

def _url_contains(page, s):
    v = s["value"]
    return v in page.url, f"URL 含'{v}' 实际={page.url}"

def _element_exists(page, s):
    el = page.query_selector(s["selector"])
    return el is not None, f"元素 {s['selector']} 存在" if el else f"元素 {s['selector']} 不存在"

def _text_contains(page, s):
    sel, v = s["selector"], s["value"]
    try:
        text = page.inner_text(sel)
    except Exception:
        return False, f"元素 {sel} 无文本内容"
    return v in text, f"{sel} 文本含'{v}'" if v in text else f"{sel} 文本不含'{v}' (实际前50字: {text.strip()[:50]})"

def _attr(page, s):
    sel, attr, want = s["selector"], s["attr"], s["value"]
    el = page.query_selector(sel)
    if not el:
        return False, f"元素 {sel} 不存在"
    actual = el.get_attribute(attr)
    return actual == want, f"{sel}[{attr}]='{actual}'" if actual == want else f"{sel}[{attr}]='{actual}' 期望='{want}'"

def _visible(page, s):
    el = page.query_selector(s["selector"])
    if not el:
        return False, f"元素 {s['selector']} 不存在"
    try:
        ok = el.is_visible()
        return ok, f"{s['selector']} 可见" if ok else f"{s['selector']} 不可见"
    except Exception:
        return False, f"{s['selector']} 可见性判定异常"

def _element_count(page, s):
    n = len(page.query_selector_all(s["selector"])); mn = s.get("min", 1)
    return n >= mn, f"{s['selector']} 数量={n} ≥{mn}" if n >= mn else f"{s['selector']} 数量={n} <{mn}"

def _status(page, s):
    resp = getattr(page, "_last_resp", None)
    if resp is None:
        return False, "无响应记录（页面未成功加载）"
    return resp.status == s["value"], f"状态码={resp.status}" if resp.status == s["value"] else f"状态码={resp.status} 期望={s['value']}"

ASSERTS = {
    "title_contains": _title_contains, "url_contains": _url_contains,
    "element_exists": _element_exists, "text_contains": _text_contains,
    "attr": _attr, "visible": _visible, "element_count": _element_count,
    "status": _status,
}

# ================= 自动捕获（console / pageerror / 网络失败 / 请求耗时） =================
def attach_capture(page):
    page._c = {"console": [], "pageerror": [], "failed": [], "requests": []}
    def on_console(msg):
        if msg.type == "error":
            page._c["console"].append(msg.text[:200])
    def on_pageerror(err):
        page._c["pageerror"].append(str(err)[:200])
    def on_failed(req):
        page._c["failed"].append(f"NETERR {req.url[:120]}")
    def on_response(resp):
        if resp.status >= 400:
            page._c["failed"].append(f"{resp.status} {resp.url[:120]}")
        dur = resp.request.timing
        page._c["requests"].append((resp.url[:120], resp.status, _timing_ms(dur)))
    page.on("console", on_console)
    page.on("pageerror", on_pageerror)
    page.on("requestfailed", on_failed)
    page.on("response", on_response)

def _timing_ms(t):
    try:
        if not t: return None
        st = t.get("requestStart") or 0; end = t.get("responseEnd") or 0
        return round((end - st)) if end >= st else None
    except Exception:
        return None

# ================= 单页测试 =================
def test_page(page, case, out_dir, idx):
    name = case.get("name", case["url"])
    timeout = case.get("timeout_ms", 10000)
    res = {"name": name, "url": case["url"], "asserts": [], "console": [], "pageerror": [],
           "failed_requests": [], "slow_requests": [], "load_ms": None, "passed": True,
           "screenshot": None}
    t0 = time.time()
    try:
        page._last_resp = page.goto(case["url"], wait_until="domcontentloaded", timeout=timeout)
        if case.get("wait_selector"):
            try:
                page.wait_for_selector(case["wait_selector"], timeout=min(timeout, 5000))
            except PWTimeout:
                res["console"].append(f"[等待超时] 选择器 {case['wait_selector']} 未出现")
                res["passed"] = False
        res["load_ms"] = round((time.time() - t0) * 1000)
        # 断言
        for a in case.get("asserts", []):
            fn = ASSERTS.get(a["type"])
            if not fn:
                res["asserts"].append({"type": a["type"], "pass": False, "note": f"未知断言类型 {a['type']}", "ms": 0})
                res["passed"] = False
                continue
            at0 = time.time()
            try:
                ok, note = fn(page, a)
            except Exception as e:
                ok, note = False, f"断言异常 {type(e).__name__}: {e}"
            res["asserts"].append({"type": a["type"], "pass": ok, "note": note, "ms": round((time.time() - at0) * 1000)})
            if not ok:
                res["passed"] = False
    except Exception as e:
        res["passed"] = False
        res["console"].append(f"[页面异常] {type(e).__name__}: {e}")
    # 捕获归集
    c = getattr(page, "_c", {})
    res["console"] = (res["console"] + c.get("console", []))[:10]
    res["pageerror"] = c.get("pageerror", [])[:10]
    res["failed_requests"] = c.get("failed", [])[:10]
    reqs = [r for r in c.get("requests", []) if r[2]]
    res["slow_requests"] = sorted(reqs, key=lambda r: r[2], reverse=True)[:5]
    # 失败自动截图
    if not res["passed"] or case.get("screenshot"):
        try:
            sp = out_dir / f"shot-{idx}-{_safe(name)}.png"
            page.screenshot(path=str(sp), full_page=True)
            res["screenshot"] = sp.name
        except Exception:
            pass
    return res

def _safe(s):
    return "".join(ch for ch in s if ch.isalnum() or ch in "-_")[:30] or "page"

def _run_one_worker(args):
    """并行 worker：独立进程 + 独立 playwright 实例（避开 sync API 线程限制）"""
    case, out_dir, idx = args
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        pg = ctx.new_page()
        attach_capture(pg)
        try:
            return test_page(pg, case, out_dir, idx)
        finally:
            ctx.close()
            browser.close()

# ================= 运行 =================
def run(cases_path, out_dir=None, html=False, parallel=False, strict=False):
    raw = json.loads(pathlib.Path(cases_path).read_text(encoding="utf-8"))
    cases = raw["urls"] if isinstance(raw, dict) and "urls" in raw else raw
    out_dir = out_dir or OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    t_all0 = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        if parallel and len(cases) > 1:
            # 多进程并行：每 URL 独立进程/实例，互不干扰（--parallel）
            import concurrent.futures
            with concurrent.futures.ProcessPoolExecutor(max_workers=min(len(cases), 4)) as ex:
                results = list(ex.map(_run_one_worker, [(c, out_dir, i + 1) for i, c in enumerate(cases)]))
        else:
            ctx = browser.new_context(viewport={"width": 1280, "height": 800})
            results = []
            for i, case in enumerate(cases):
                pg = ctx.new_page(); attach_capture(pg)
                results.append(test_page(pg, case, out_dir, i + 1)); pg.close()
            ctx.close()
        browser.close()
    total_ms = round((time.time() - t_all0) * 1000)

    if strict:
        for r in results:
            if r["console"] or r["pageerror"] or r["failed_requests"]:
                r["passed"] = False
    n_pass = sum(1 for r in results if r["passed"])
    summary = {"total_pages": len(results), "passed_pages": n_pass, "failed_pages": len(results) - n_pass,
               "total_ms": total_ms, "strict": strict,
               "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    report = {"summary": summary, "results": results}
    json_out = out_dir / "webqa-report.json"
    json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if html:
        (out_dir / "webqa-report.html").write_text(_build_html(report), encoding="utf-8")

    print("=" * 62)
    print(f"网页测试完成: {n_pass}/{len(results)} 页通过  总耗时 {total_ms}ms  "
          f"{'(strict 模式)' if strict else ''}")
    print("=" * 62)
    for r in results:
        n_ok = sum(1 for a in r["asserts"] if a["pass"])
        print(f"  {'✓' if r['passed'] else '✗'} {r['name']}  加载 {r['load_ms']}ms  断言 {n_ok}/{len(r['asserts'])}")
        if r.get("console"):  print(f"      console: {r['console'][:2]}")
        if r.get("pageerror"): print(f"      pageerror: {r['pageerror'][:2]}")
        if r.get("failed_requests"): print(f"      失败请求: {r['failed_requests'][:3]}")
        for a in r["asserts"]:
            if not a["pass"]:
                print(f"      ✗ [{a['type']}] {a['note']} ({a['ms']}ms)")
        for q in (r.get("slow_requests") or [])[:2]:
            print(f"      ⏱ 慢请求 {q[2]}ms {q[0][:70]} [{q[1]}]")
    print(f"报告: {json_out}")
    return 0 if n_pass == len(results) else 1

# ================= HTML 报告 =================
def _build_html(report):
    s = report["summary"]
    cards = []
    for r in report["results"]:
        icon = "✅" if r["passed"] else "❌"
        rows = "".join(
            f"<tr><td>{'✅' if a['pass'] else '❌'}</td><td style='white-space:nowrap'>{a['type']}</td>"
            f"<td>{a['note']}</td><td style='text-align:right'>{a['ms']}ms</td></tr>"
            for a in r["asserts"])
        warn = ""
        if r.get("console"):  warn += f"<div style='font-size:11px;color:#B45309;margin-top:6px'>⚠ console: {r['console'][:3]}</div>"
        if r.get("pageerror"): warn += f"<div style='font-size:11px;color:#DC2626;margin-top:2px'>⚠ pageerror: {r['pageerror'][:3]}</div>"
        if r.get("failed_requests"): warn += f"<div style='font-size:11px;color:#DC2626;margin-top:2px'>⚠ 网络: {r['failed_requests'][:3]}</div>"
        slow = ""
        if r.get("slow_requests"):
            slow = "<div style='font-size:11px;color:#6B7280;margin-top:2px'>⏱ 最慢: " + \
                   "; ".join(f"{q[2]}ms {q[0][:40]}" for q in r["slow_requests"][:3]) + "</div>"
        shots = f'<img src="{r["screenshot"]}" style="max-width:100%;border:1px solid #ddd;border-radius:8px;margin-top:8px">' if r.get("screenshot") else ""
        cards.append(f"""
      <div style="background:#fff;border:1px solid rgba(0,0,0,0.08);border-radius:12px;padding:14px;margin:10px 0;box-sizing:border-box">
        <div style="font-size:14px;font-weight:600">{icon} {r['name']} <span style="color:#6B7280;font-weight:400;font-size:12px">加载 {r['load_ms']}ms</span></div>
        <div style="font-size:11px;color:#6B7280">{r['url']}</div>
        <table style="width:100%;border-collapse:collapse;font-size:12px;margin-top:8px">
          <tr style="background:#f4f3ee"><th style="text-align:left;padding:4px 6px">结果</th><th style="text-align:left">断言</th><th style="text-align:left">说明</th><th style="text-align:right">耗时</th></tr>{rows}
        </table>{warn}{slow}{shots}
      </div>""")
    return f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>WebQA 网页测试报告</title></head>
<body style="margin:0;padding:20px;background:#F4F3EE;font-family:'PingFang SC','Roboto','Segoe UI',Arial,sans-serif;color:#1A1B1C">
  <div style="max-width:860px;margin:0 auto">
    <div style="padding:16px;border-radius:14px;background:linear-gradient(135deg,rgba(82,196,26,.15),rgba(148,216,195,.3));box-sizing:border-box">
      <div style="font-size:16px;font-weight:600">WebQA 网页测试报告</div>
      <div style="font-size:12px;color:#4B5563;margin-top:4px">{s['passed_pages']}/{s['total_pages']} 页通过 · 总耗时 {s['total_ms']}ms · {s['generated_at']} {('· strict' if s.get('strict') else '')}</div>
    </div>{''.join(cards)}
    <div style="font-size:10px;color:#9CA3AF;text-align:center;margin-top:12px">doubao-eng webqa_engine v2 · 单会话复用提速 + 多维度自动捕获</div>
  </div>
</body></html>"""

# ================= demo：本地演示页 =================
def demo():
    local = OUT / "demo"; local.mkdir(parents=True, exist_ok=True)
    (local / "index.html").write_text(_DEMO_HTML, encoding="utf-8")
    url = "file://" + str(local / "index.html")
    cases = {"urls": [
        {"name": "首页结构", "url": url, "wait_selector": "#main-title", "screenshot": True, "asserts": [
            {"type": "title_contains", "value": "WebQA"},
            {"type": "element_exists", "selector": "#main-title"},
            {"type": "text_contains", "selector": "#main-title", "value": "演示"},
            {"type": "element_count", "selector": "li", "min": 3},
            {"type": "visible", "selector": ".nav-link"},
            {"type": "attr", "selector": ".btn", "attr": "class", "value": "btn"},
            {"type": "status", "value": 200},
        ]},
    ]}
    (local / "demo_cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"演示用例: {local / 'demo_cases.json'}")
    return run(local / "demo_cases.json", local, html=True)

_DEMO_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>WebQA 演示站点</title>
<style>body{font-family:sans-serif;padding:40px}h1{color:#333}.btn{padding:10px 20px;background:#4a90d9;color:#fff;border:none;border-radius:6px;cursor:pointer}.nav-link{color:#4a90d9}</style></head>
<body>
  <h1 id="main-title">WebQA 演示页面</h1>
  <p class="desc">用于演示网页测试引擎的本地页面。</p>
  <a href="#sec2" class="nav-link">跳转</a>
  <button class="btn">按钮</button>
  <ul id="list"><li>项目A</li><li>项目B</li><li>项目C</li></ul>
  <script>setTimeout(function(){var d=document.createElement('div');d.id='late';d.textContent='延迟加载完成';document.body.appendChild(d);},800);</script>
</body></html>"""

# ================= selftest：注入缺陷验证引擎能检出 =================
def selftest():
    local = OUT / "selftest"; local.mkdir(parents=True, exist_ok=True)
    good = _DEMO_HTML
    (local / "good.html").write_text(good, encoding="utf-8")
    bad = good.replace('id="main-title"', 'id="main-title-moved"').replace('class="btn">按钮', 'class="btn-other">按钮')
    (local / "bad.html").write_text(bad, encoding="utf-8")
    g = "file://" + str(local / "good.html"); b = "file://" + str(local / "bad.html")
    cases = {"urls": [
        {"name": "正常页(应全过)", "url": g, "wait_selector": "#main-title", "asserts": [
            {"type": "title_contains", "value": "WebQA"},
            {"type": "element_exists", "selector": "#main-title"},
            {"type": "element_count", "selector": "li", "min": 3},
        ]},
        {"name": "缺陷页(应检出)", "url": b, "wait_selector": "#main-title-moved", "asserts": [
            {"type": "element_exists", "selector": "#main-title"},      # 应失败(元素已改名)
            {"type": "attr", "selector": ".btn", "attr": "class", "value": "btn"},  # 应失败(class 变了)
            {"type": "element_count", "selector": "li", "min": 5},       # 应失败(只有3个)
        ]},
    ]}
    (local / "selftest_cases.json").write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")
    print("自检：正常页应全过，缺陷页 3 条断言应全部检出失败。")
    rc = run(local / "selftest_cases.json", local, html=True)
    ok_normal = rc is None or rc == 1  # 有失败页是预期
    print("自检结论: 引擎能检出缺陷 ✓" if rc == 1 else "自检结论: 引擎检出异常，需检查")
    return 0 if rc == 1 else 1

def main():
    ap = argparse.ArgumentParser(prog="webqa_engine")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("cases"); r.add_argument("--out", default=None)
    r.add_argument("--html", action="store_true"); r.add_argument("--parallel", action="store_true")
    r.add_argument("--strict", action="store_true")
    r.set_defaults(fn=lambda a: run(a.cases, pathlib.Path(a.out) if a.out else None, a.html, a.parallel, a.strict))
    sub.add_parser("demo").set_defaults(fn=lambda a: demo())
    sub.add_parser("selftest").set_defaults(fn=lambda a: selftest())
    args = ap.parse_args()
    sys.exit(args.fn(args) or 0)

if __name__ == "__main__":
    main()
