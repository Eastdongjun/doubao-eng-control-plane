# Sonar 修复规范手册（VSCode AI Sonar Guard · 规则知识层）

> 给所有 AI 编码代理（豆包 / Claude / Codex / Copilot）的 SonarQube 修复规范。
> 每次修改 Java / Python / JS / TS 文件前，必须先读本手册对应规则；写完必须闭环到 Problems = 0。
> 配套命令：`engineering problems <root>`（检查）、`engineering sonar-plan <root> <file>`（写前雷区）、`engineering improve <root>`（生成修复清单）、pre-commit hook（提交阻断）。

## 一、写前铁律（所有语言）

1. 禁止无参 `now()`：Java 必须传 `ZoneId`/`Clock`（`LocalDate.now(ZoneId.of("Asia/Shanghai"))`）；Python 用 `datetime.now(timezone.utc)` 或传 tz。
2. 不返回 null 集合/Map：List → `Collections.emptyList()`，Map → `Collections.emptyMap()`，Set → `Collections.emptySet()`；Python 返回 `[]`/`{}` 而非 `None`。
3. 不复制魔法字符串：重复 ≥3 次提 `private static final String` 常量，常量名表达业务含义；不为了消警告乱抽象。
4. 不写嵌套三元：拆 if/elif 或中间变量。
5. 不用 NOSONAR / noinspection 逃避：除非有明确误报说明并写豁免文件。
6. 不留未使用 import / 变量 / 参数：私有方法直接删；公共接口先查调用链。
7. 方法复杂度：认知复杂度超 15 必须拆小方法（拆条件分支、循环体、校验逻辑、组装逻辑）。
8. 泛型转换要收口，避免 unchecked cast；Java 16+ 用 `stream.toList()` 替代 `Collectors.toList()`。

## 二、规则适配器（按规则号）

### S1192 重复字符串
- 优先提 `private static final String` 常量；常量名表达业务含义（如 `MSG_PHONE_EMPTY`）。
- 排除项：字典/Map key（`map.get("key")`）、注解元数据（`@Xxx(value = "v")`）、标准值（编码/时区/HTTP 动词）、全限定名/包名、测试数据字面量。
- 业务校验消息、日志模板、feign 服务名属于合理常量，纳入常量治理专项即可豁免。

### S3776 认知复杂度
- 方法复杂度 > 15 必须拆小方法；优先拆：条件分支、循环体、校验逻辑、组装逻辑。
- 拆出的私有方法命名表达职责（如 `buildResponse`、`validateParam`）。
- 禁止用 NOSONAR 逃避；确实需要豁免时写豁免文件 + reason。

### S8688 now() 时区
- 禁止无参 `now()`：`LocalDate.now(ZoneId.of("Asia/Shanghai"))`、`LocalDateTime.now(ZoneId.of("Asia/Shanghai"))`、`LocalTime.now(ZoneId.of("Asia/Shanghai"))`。
- 优先用统一时区常量（如 `ZoneId.of("Asia/Shanghai")`），必要处用 `Clock` 便于测试注入。
- Python：`datetime.now(timezone.utc)` / `datetime.now(ZoneId...)`，禁止 `datetime.now()` 无参。

### S1168 返回 null 集合/Map
- List → `Collections.emptyList()`；Map → `Collections.emptyMap()`；Set → `Collections.emptySet()`。
- Python：返回 `[]` / `{}` 而非 `None`；调用方按空集合处理。
- 语义上"无结果"与"错误"区分：无结果返回空集合，错误抛异常/返回错误码。

### S1172 未使用参数
- 私有方法：直接删参数，改调用处。
- 公共接口/实现方法：不能乱删时——查调用链确认约束；接口签名不允许改时加 `@SuppressWarnings("unused")` 并注释原因，或调整调用链。
- 不要为消警告而破坏接口契约。

### S6204 Java 16+ toList
- `stream.collect(Collectors.toList())` → `stream.toList()`（返回不可变 List，确认调用方不依赖可变性）。
- 替换后删除不再使用的 `import java.util.stream.Collectors;`。

### S3358 嵌套三元
- 拆成 if/else 或先赋值中间变量；禁止 `a ? b : c ? d : e` 式链。
- 排除：TS 可选属性/参数 `key?: string`（不是三元）。

### S107 参数过多（>7）
- 封装参数对象（request/query DTO），或拆职责。
- 对外服务/搜索接口签名改动影响全部调用方，属独立重构专项，可豁免 + 列技术债。

### S1128 未使用 import
- 删除未使用 import；全仓搜索确认无引用后再删。
- Python 用 `pyflakes`/IDE 提示辅助识别。

## 三、五层闭环（AI 每次写代码必须走完）

1. **写前预检**：`engineering sonar-plan <项目根> <目标文件>` → 知道目标文件现有问题 + 本次禁止新增的模式。
2. **写入约束**：通过 VSCode 写入桥写文件（写完自动返回该文件 Sonar 状态）。
3. **写后检查**：`engineering problems <项目根>`；非 0 则 `engineering improve <项目根>`。
4. **强制消费**：读取 `<项目根>/.ai/evidence/improve-state.json`，按 diagnostics（rule/message/suggestion/adapter）逐条修复，修完重跑 problems，直到 0。
5. **提交阻断**：pre-commit hook 拦截——Error > 0 禁、未豁免 Warning > 0 禁、AI Gate 离线禁、采集失败禁。豁免必须带 reason 写入 `<root>/.ai/evidence/exemptions.json`。

## 四、完成标准

- `engineering problems <root>` = 0 problems（ERROR=0, WARNING=0）。
- 有豁免时：每条豁免带 rule/file/reason，且真实业务硬伤（S8688/S3358/S1168/S9999）不允许豁免。
- Maven/Gradle/脚本编译通过（Java 改动必须 `mvn compile` 或等价构建验证）。
