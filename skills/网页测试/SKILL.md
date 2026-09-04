---
name: 网页测试
description: 网页功能/回归/UI自动化测试与网站质量检查。当用户需要测试网页、网站、Web应用（可访问性、元素、文本、链接、表单、加载性能、控制台报错、网络请求失败、多页面批量检查、页面截图证据）时使用。相比逐个调用浏览器MCP更快速（单会话复用/精准等待/可并行）且更细致（8类断言+自动捕获console/网络/慢请求+失败截图+HTML报告）。触发词：网页测试、网站测试、页面检查、回归测试、验证网页、检查页面。
---

# 网页测试（WebQA 增强引擎）

对网页做**快速、细致、可追溯**的自动化测试。解决逐个调用浏览器 MCP 的三大痛点：慢（重复冷启动/固定等待）、响应差（全量快照拖累）、粒度粗（只有"能不能看到"）。

## 引擎位置

- 引擎脚本：`webqa/webqa_engine.py`（相对当前工程仓库根目录；若在其它工作目录，用绝对路径）
- 演示与自检输出：`_webqa/`（运行产物，不入库）

## 何时使用

1. 用户要求"测一下/检查/验证 这个网页/网站/页面"（功能、回归、UI、性能）。
2. 页面报错、样式异常、加载慢、请求失败，需要**证据**（console 错误 / 网络失败 / 加载耗时 / 截图）。
3. 多页面批量检查（站内多页、多个 URL）。

## 核心提速（引擎已内置，无需手工）

- **单浏览器会话复用**：所有页面共用一个实例，不重复启动浏览器。
- **精准等待**：`goto(wait_until="domcontentloaded")` + 显式 `wait_for_selector`（用例里配 `wait_selector`），绝不固定 sleep。
- **可选 `--parallel`**：多页面多进程并发（每页独立实例，互不干扰），大站点批量测提速明显。

## 核心细致（引擎自动完成）

- 自动捕获：console 错误、pageerror、失败网络请求（4xx/5xx）、最慢请求（响应耗时排行）。
- 8 类细粒度断言：标题/URL/元素存在/文本/属性/可见/数量/状态码。
- 每页加载计时 + 每断言耗时，报告可直接定位"哪页慢、哪个断言耗时"。
- 失败自动整页截图。

## 用例格式（JSON）

```json
{"urls": [
  {"name": "首页", "url": "https://example.com", "wait_selector": "#app",
   "timeout_ms": 10000, "screenshot": false,
   "asserts": [
     {"type": "title_contains", "value": "Example"},
     {"type": "element_exists", "selector": "#main"},
     {"type": "text_contains",  "selector": "h1", "value": "欢迎"},
     {"type": "attr", "selector": "a.cta", "attr": "href", "value": "/start"},
     {"type": "visible", "selector": ".submit-btn"},
     {"type": "element_count", "selector": "li", "min": 3},
     {"type": "status", "value": 200}
   ]},
  {"name": "列表页", "url": "https://example.com/list", "wait_selector": "table"}]
}
```

### 断言类型速查

| type | 参数 | 说明 |
|---|---|---|
| `title_contains` | `value` | 页面标题包含 |
| `url_contains` | `value` | 当前 URL 包含 |
| `element_exists` | `selector` | 元素存在（DOM 有） |
| `text_contains` | `selector`,`value` | 元素文本包含 |
| `attr` | `selector`,`attr`,`value` | 属性值精确匹配 |
| `visible` | `selector` | 元素可见（区分"存在但隐藏"） |
| `element_count` | `selector`,`min` | 匹配数量 ≥ min |
| `status` | `value` | 主文档状态码 |

`wait_selector`：进入页面后精准等待的关键元素（如 `#app`、`#main`），无它则引擎不额外等待。

## 命令

```bash
# 跑用例（输出 JSON 报告，--html 生成可视化报告）
python3 webqa/webqa_engine.py run <cases.json> --html [--parallel] [--strict]

# 演示（本地页，自证引擎可用）
python3 webqa/webqa_engine.py demo

# 自检（注入缺陷用例，验证引擎能检出问题——交付前必跑）
python3 webqa/webqa_engine.py selftest
```

- `--strict`：console 错误 / 失败请求也算失败（回归门禁用）。
- `--parallel`：多页并发（大站点批量）。

## 报告解读

- 每页一行：`✓/✗ 页名 加载 Xms 断言 n/m`。
- `✗ [断言类型] 说明 (耗时)`：失败的断言明细。
- `⚠ console / pageerror / 网络`：自动捕获的问题。
- `⏱ 慢请求 Xms url [状态]`：最慢的 5 个请求——定位"响应慢"。
- 失败页自动截图，HTML 报告内嵌展示。

## 交付前验收（归零）

1. 引擎自身：`python3 webqa/webqa_engine.py selftest` 必须能检出全部注入缺陷（返回码 1 = 缺陷页被检出，属预期）。
2. 用例正确性：目标页的所有正常断言全过；任何真实问题（不可见/缺元素/请求失败）都被如实标红。
3. 不通过时**必须**修复用例（选择器/等待）或如实上报页面问题，禁止静默改判。
