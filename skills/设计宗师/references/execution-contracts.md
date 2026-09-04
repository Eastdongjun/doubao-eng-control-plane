# v2.0 执行契约

这些契约把设计原则转换成可检查的中间产物。它们不是新的视觉规范，不会覆盖用户项目的 Token 或组件库。

## 任务路由

先复制 `templates/DESIGN_TASK.example.yaml`，填写事实后运行：

```powershell
python scripts/capability_router.py DESIGN_TASK.yaml --output ROUTE.json
```

`ROUTE.json` 给出模式、权威状态、必需能力、条件能力、最小交付物和阻断门禁。路由结果是建议与约束的组合：必须能力不可省略，条件能力需要记录不加载的理由。

## 调研与审美

使用 `SOURCE_LEDGER.example.yaml` 和 `AESTHETIC_DECISION_RECORD.example.yaml`。先运行：

```powershell
python scripts/research_coverage.py SOURCE_LEDGER.yaml
python scripts/evaluate_aesthetic.py AESTHETIC_DECISION_RECORD.yaml
```

研究覆盖通过不等于方向获批；审美评分也不能用高差异化抵消业务、层级或无障碍失败。

## 规范与资产

把批准的规范复制为项目自己的 `DESIGN_AUTHORITY.yaml`，然后运行：

```powershell
python scripts/design_value_audit.py . --authority DESIGN_AUTHORITY.yaml
python scripts/svg_lint.py .
```

扫描发现的是待调查值。内在尺寸、第三方组件和获批例外要进入偏差清单，不得直接把扫描结果改写成新的共享 Token。

扫描结果为 `clean` 才表示没有发现项；`needs_review` 表示发现了待解释的原始值或风格风险，`blocked` 表示存在不可接受的输入或结构错误。

## 交付门禁

完成最小产物后运行：

```powershell
python scripts/design_gate.py DESIGN_TASK.yaml --artifacts .
```

只有 `evidenced`、`approved` 或 `shipped` 状态且具备对应产物与决策负责人，才允许进入交付阶段。渲染、浏览器或外部网络不可用时，先按依赖授权契约请求用户决策；用户拒绝或暂缓后，状态必须保持 `unproven` 或 `blocked`。

## P1/P2 回归

P1 使用 `TYPE_LAYOUT_FIXTURE.example.json`、`LAYOUT_FINGERPRINT.example.json` 和 `LOADING_MANIFEST.example.json`，分别运行：

```powershell
python scripts/typography_layout_audit.py TYPE_LAYOUT_FIXTURE.json
python scripts/layout_fingerprint.py LAYOUT_FINGERPRINT.json
python scripts/loading_manifest.py LOADING_MANIFEST.json
python scripts/visual_location_audit.py VISUAL-LOCATION-MAP.md
python scripts/run_boundary_audit.py index.html --output BOUNDARY-REPORT.json --viewport 1280x800 --viewport 390x844
```

P2 使用 `REGRESSION_CATALOG.example.json`、`TREND_EVIDENCE.example.json` 和截图基线：

```powershell
python scripts/regression_catalog.py REGRESSION_CATALOG.json
python scripts/trend_evidence.py TREND_EVIDENCE.json
python scripts/visual_regression.py baseline.png candidate.png --output VISUAL-DIFF.json
python scripts/research_cache.py .research-cache/index.json --url https://example.com/reference --content notes.md --lane category --source-date 2026-08-28
```

截图差异只表示实现变化，不自动表示设计变好；必须与审美决策、业务目标、普通状态和无障碍证据一起判断。

## 环境与依赖授权

运行当前路径所需的 Node、Playwright、浏览器内核、系统库、PyYAML、Pillow 或其他环境能力缺失时，工具必须输出 `status: authorization_required` 和退出码 `3`，不能只抛异常或悄悄降级。完整字段与 Agent 行为见 `dependency-authorization.md`，示例见 `templates/DEPENDENCY_AUTHORIZATION.example.json`。

Agent 需要向用户说明：缺少什么、阻断哪项能力、安装到哪里、准确命令、会改变什么、风险与磁盘/网络影响、拒绝后的证据损失，以及安装后要重跑哪项验证。未经明确授权不得安装；用户拒绝或暂缓后，才可在明确标记 `unproven` 的前提下执行其接受的降级方案。

`visual_regression.py` 默认不会在 Pillow 缺失时退化成二进制比较。只有用户明确接受证据损失后，才可使用 `--allow-binary-fallback`。

## 状态语义

`not_started`、`in_progress`、`unproven`、`evidenced`、`approved`、`shipped`、`blocked` 是证据状态，不是视觉质量分数。没有证据的“看起来完成”不属于 `approved`。
