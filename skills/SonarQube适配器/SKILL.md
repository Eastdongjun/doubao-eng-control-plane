---
name: SonarQube适配器
description: 把 SonarQube 规则固化为 AI 写代码的硬门禁闭环（VSCode AI Sonar Guard：写前预检→写前约束→写后自动检查→自动优化循环→提交阻断→修复手册）。当 AI 新增/修改任何代码文件、写完代码准备宣称完成、或准备 git 提交时，必须按本技能执行 SonarQube 门禁；涉及 S1192/S3776/S8688/S1172/S1168/S6204/S3358/S107 等规则问题时使用本技能修复。也用于"归零/无报错/无问题"验收（SonarQube 视角）。
---

# SonarQube 硬门禁（VSCode AI Sonar Guard 六层闭环）

SonarQube 不是"提示词说一下"，而是**写码流程里的硬门禁**。AI 写任何代码都要走完六层，缺一层都不算完成。

**规则手册**：`governance-demo/sonar-rules.md`（主仓库）与项目根 `SONAR-RULES.md`——所有 agent 写代码前必读，按规则号固化修复 adapter。

## 第 0 层：写前预检（先看雷区再动手）

修改目标文件前，先跑：

```
MCP:  engineering_sonar_plan  <项目根> <目标文件>
CLI:  python3 governance-demo/engineering.py sonar-plan <项目根> <目标文件>
```

输出：目标文件**现有问题**（按规则汇总）+ **本次写代码必须避免新增的模式**（无参 now()/return null 集合/嵌套三元/重复字符串/Collectors.toList/复杂度膨胀）+ 对应修复 adapter 指引。AI 还没写，就知道这个文件的雷区。

## 第 1 层：写前约束（固定规则，先读再写）

新增/修改代码时必须优先满足以下规则，**写完再修的成本永远高于写时守规**：

| 规则 | 要求 |
|---|---|
| 不留未使用 import/变量/参数 | 写完自查：import 全被使用；函数参数全部用上（S1128/S1172） |
| 不复制魔法字符串 | 同一字符串出现 ≥3 次 → 提 `private static final String` 常量（S1192） |
| 方法复杂度超限就拆小方法 | 圈复杂度 > 15 → 拆分为多个小方法，减少 if/else 嵌套（S3776） |
| now() 必须传 Clock 或 ZoneId | `LocalDate.now()` / `datetime.now()` 必须显式传时区，禁止默认时区（S8688） |
| 不返回 null 集合/Map | 空集合返回 `Collections.emptyList()`/`emptyMap()`/`[]`，禁止 return null（S1168） |
| 不用嵌套三元 | 三元里套三元 → 拆成 if/elif 或局部变量（S3358） |
| 泛型转换要收口 | 避免 unchecked cast；必须转换时用类型安全方式并集中收口 |
| 不用 NOSONAR 逃避 | 除非有明确误报说明并写入豁免文件，否则禁止 NOSONAR 注释 |

## 第 2 层：写入约束（VSCode 写入桥，写完即检）

写代码**必须**走 VSCode-MCP 写入通道（`dev_write_file` / `dev_edit_file` / `dev_typewrite`）——写入动作本身带 Sonar 闭环：

- 写入工具返回内容**自动附带该文件 Sonar 检查结果**（`🟢 0 problems` 或 `🔴 N 个问题` 清单）。
- 写完立刻看到文件状态，不需要等全仓扫描。
- 若返回 `🔴`，按问题清单当场修，直到该文件 `🟢`。

## 第 3 层：写后自动检查（Problems ≠ 0 就不能说完成）

**每次写完文件，立即运行**（优先 MCP 工具，次选 CLI）：

```
MCP:  engineering_problems  <项目根>
CLI:  python3 governance-demo/engineering.py problems <项目根>
```

- 返回 problems 列表（SonarQube 风格：`S8688[ERROR]: ... (src/X.java:9)`）。
- **只要 problems 非 0（尤其 ERROR>0 或未豁免 WARNING>0），就不能宣称"完成/可提交"**。

## 第 4 层：自动优化循环（improve → 读 state → 修 → 重跑 → PASS）

Problems 非 0 时进入优化循环：

```
MCP:  engineering_improve  <项目根>
CLI:  python3 governance-demo/engineering.py improve <项目根>
```

- 工具把剩余问题写入 `<项目根>/.ai/evidence/improve-state.json`。
- **AI 必须读取该文件**，按 `diagnostics` 数组逐条修复（每条含 rule/severity/message/file/line/suggestion/**adapter**——adapter 是 sonar-rules.md 固化的修复指引）。
- 修完**重跑 engineering_problems**，直到 0 problems（status=PASS）。
- 循环上限：同批问题最多 10 轮；超限如实上报剩余问题与原因，不得伪造 PASS。

## 第 5 层：提交前阻断（git hook）

`engineering install-hook <仓库>` 安装 pre-commit hook 后，git 提交被硬性拦截：

- SonarQube **Error > 0** → 禁止 commit（exit 1）
- **未豁免 Warning > 0** → 禁止 commit（exit 1）
- **AI Gate（VSCode-MCP :8848）不在线** → 禁止 commit（提示启动命令）
- **桥不可用**（engineering.py 缺失）/ **采集失败** → 禁止 commit
- 确需绕过的场景：`SKIP_SONAR_GATE=1 git commit ...`（仅限例外，正常流程禁用）

豁免：对确实合理的问题，写 `<项目根>/.ai/evidence/exemptions.json`：

```json
[{"rule": "S1172", "file": "src/X.java", "line": 12, "reason": "接口签名必须保留，调用链约定传入"}]
```

豁免必须写明原因（人工评审可追溯），不允许无理由批量豁免。

## 第 6 层：修复手册（常见规则 → adapter 指南）

> 完整版见 `governance-demo/sonar-rules.md`；**固定工程套路**见 `governance-demo/sonar-fix-templates.md`（S3776 五步拆法 / S1192 四步提常量 等）；`engineering improve` 的 diagnostics 已内联 adapter 字段。

| 规则 | 问题 | 修法 | 示例 |
|---|---|---|---|
| **S1192** | 重复字符串字面量 | 提 `private static final String` 常量 | `private static final String LOADING = "正在加载";` 全处替换 |
| **S3776** | 圈复杂度超限（>15） | 拆方法，减少 if/else 嵌套；每方法只做一件事 | `if(a){if(b){if(c){...}}}` → `if(a && b && c){ doX(); }` 或拆分 helper |
| **S8688** | `LocalDate.now()` 无时区 | 传 Clock/ZoneId | `LocalDate.now(ZoneId.of("Asia/Shanghai"))`；`datetime.now(timezone.utc)` |
| **S1172** | 未使用参数 | 移除；接口签名必须保留时加注释说明或调整调用链 | 删参数 → 改调用处；或 `@SuppressWarnings`+豁免文件 |
| **S1168** | 集合/Map 返回 null | 空集合返回 empty 容器 | `Collections.emptyList()` / `emptyMap()` / `[]` / `{}` |
| **S6204** | `Collectors.toList()` | Java 16+ 用 `stream.toList()` | `.collect(Collectors.toList())` → `.toList()` |
| **S3358** | 嵌套三元 | 拆 if/elif 或局部变量 | `a ? b : (c ? d : e)` → `if a: r=b elif c: r=d else: r=e` |
| **S107** | 参数 > 7 个 | 封装参数对象 / 拆职责 | `f(a,b,c,d,e,f,g,h)` → `f(OrderQuery(a,b,c,d,e,f,g,h))` |
| **S1128** | 未使用 import | 删除 | `import os`（未用）→ 移除 |
| **S9998** | NOSONAR 滥用 | 移除，改用豁免文件 | `// NOSONAR` → 删除 + 写 `exemptions.json` 带 reason |

## 完整工作流（诊断队列 → 最小修复 → 复查归零 → 证据交付）

AI 每次修 Sonar 问题必须按此顺序走，**不能跳步、不能挑简单的刷数量**：

```
1. engineering snapshot <root>     记录基线（修复前 problems 数）
2. engineering queue <root>        看 P0-P4 优先级队列 + 分批计划
3. engineering sonar-plan <root> <file>  看目标文件雷区 + 角色预算
4. 写代码（MCP 写后即检）           按队列优先级修，先 P0 再 P1...
5. engineering diff <root>         新增诊断门禁：新增>0 必须修复或回滚
6. engineering impact <root>       改动影响面：方法签名/返回值/常量/时间
7. engineering report <root>       AI 自检报告（修复前后/新增/编译/NOSONAR/文件）
8. git commit                      hook 自动阻断（Error/Warning/Gate离线）
```

**分阶段交付规则**（不能一口气修 95 个）：
- 第一批：所有 P0（Java Error / 编译错误）
- 第二批：当前打开文件的所有问题
- 第三批：P1/P2 高风险（时区/null 集合/复杂度）
- 第四批：P3 低风险风格（重复字符串/未用 import）
- 每批都要：写入 → diff 对比 → compile/test → evidence

**Stale Diagnostic 识别**：VSCode 报 Java Error 但 Maven 编译过了 → 跑 `engineering verify-stale <root> <file>`，自动 mvn compile 验证，标记 suspected_stale 并提示刷新 Language Server。

**文件级质量预算**（AI 写代码前先知道文件角色）：
- Controller：复杂度<=8，不允许复杂业务逻辑
- Service：复杂度<=15，必须显式时区
- Mapper：不允许拼接 SQL 风险
- DTO：不允许业务计算
- Task/Schedule：必须显式时区、必须幂等

**禁止 NOSONAR 滥用**：默认禁止新增 `// NOSONAR` / `// noinspection`。允许条件：Sonar 明确误报 + 有业务原因 + 注释说明 + 单独记录到 evidence。否则 S9998 会报。

## 与既有技能配合

- 完整项目流程 → `工程化总控`（本技能负责其中的"编码开发/质量门禁"环节）
- 自动写码闭环 → `自动编码循环`（写码→运行→修复→归零，本技能提供 SonarQube 视角的归零）
- 疑难 bug 根因 → `系统化调试`
- 测试优先 → `测试驱动开发`

## 硬性规则

- 运行输出是唯一验收证据：problems 结果 0 才是 PASS，没跑过就是没跑过。
- 报错先读完整信息再改，不靠猜。
- 不伪造结果、不用 NOSONAR 逃避、不批量豁免。
- 豁免必须可追溯（rule+file+line+reason）。
- 交付汇报：逐文件列出 problems 检查结果（修复前后数量、剩余 0 才可交付）。
