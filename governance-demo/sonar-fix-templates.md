# Sonar 修复模板库（VSCode AI Sonar Guard · 层 7）

> 把常见 SonarQube 问题做成**固定工程套路**的修复模板。AI 修问题时不是"凭感觉拆"，而是按模板的步骤走，保证修复质量一致、可预测。
> 配合 `sonar-rules.md`（规则定义）+ `engineering queue`（优先级队列）+ `engineering impact`（影响面分析）使用。

---

## S3776 认知复杂度过高（方法 > 15）

**固定 5 步拆法**：

1. **找主流程**：通读方法，识别"这个方法最终要产出什么"——把主流程用 3-5 句话写在注释里。
2. **抽取 guard clause**：所有 `if (条件) { return / throw }` 提前到方法开头，去掉 `else` 嵌套。
3. **抽取条件判断方法**：复杂 `if (a && b || c)` 抽成 `private boolean isXxx(...)`，方法名表达判断语义。
4. **抽取数据组装方法**：DTO/Response 构建、列表转换、字段映射抽成 `private XxxResponse buildXxx(...)`。
5. **保持 public 方法只读起来像业务流程**：重构后 public 方法应该是 `validate → query → assemble → return` 这种线性流程，细节全在 private 方法里。

**反模式（禁止）**：
- 把大方法切成两个同样大的方法（假拆分）
- 拆完后 public 方法还是一堆 if/else
- 为降复杂度把逻辑藏在 lambda/stream 里（复杂度转移，没消除）

---

## S1192 重复字符串（≥3 次）

**固定 4 步**：

1. **分类**：先判断重复字符串属于哪类——业务状态值（"PAID"/"CANCELLED"）、校验消息（"手机号不能为空"）、配置 key（"shopjoy.storage.type"）、日志模板、测试数据。
2. **提常量**：业务状态值/校验消息/配置 key → `private static final String XXX = "..."`，常量名表达业务含义（`MSG_PHONE_EMPTY`、`STATUS_PAID`）。
3. **全处替换**：用 IDE/`rg` 确认所有出现处都替换，不留漏网。
4. **测试数据保持字面量**：测试文件里的编号（"ORD001"）、金额（"500.00"）、商品名（"测试商品"）**不提常量**——提了反而降低测试可读性，直接豁免。

**反模式**：
- 常量名叫 `CONSTANT_1` / `STR_2`（无语义）
- 把 map key / 注解元数据 / 标准值也提常量（这些不该报，报了是引擎误报，应修引擎而非提常量）

---

## S8688 now() 无时区

**固定 3 步**：

1. **统一时区常量**：文件顶部加 `private static final ZoneId ZONE = ZoneId.of("Asia/Shanghai");`（项目级可提到 common 常量类）。
2. **替换所有无参 now()**：`LocalDate.now()` → `LocalDate.now(ZONE)`；`LocalDateTime.now()` → `LocalDateTime.now(ZONE)`；`LocalTime.now()` → `LocalTime.now(ZONE)`。
3. **补 import**：`import java.time.ZoneId;`（如果文件还没有）。

**注意**：
- 测试类里如果用固定时间做断言，优先用 `Clock.fixed(...)` 注入，而不是写死 `LocalDate.of(2026,1,1)`。
- Python：`datetime.now()` → `datetime.now(timezone.utc)` 或 `datetime.now(ZoneInfo("Asia/Shanghai"))`。

---

## S1168 返回 null 集合/Map

**固定 2 步**：

1. **找到所有 `return null`**：在返回类型是 `List/Map/Set/Collection` 的方法里，把 `return null` 改成 `return Collections.emptyList()` / `emptyMap()` / `emptySet()`。
2. **检查调用方**：`rg "xxx()"` 查调用方是否有 `if (list == null)` 判空——如果有，改成 `if (list.isEmpty())`（空集合语义更清晰）。

**Python**：`return None` → `return []` / `return {}`；调用方 `if x is None` → `if not x`。

---

## S1172 未使用参数

**固定决策树**：

1. **方法是 private 吗？** → 是：直接删参数，改所有调用处。
2. **方法是 public/接口实现吗？** → 查调用链：
   - 所有调用方都不传这个参数 → 删参数（接口签名一起改）。
   - 有调用方传但方法体不用 → 可能是接口契约要求保留 → 加 `@SuppressWarnings("unused")` + 注释说明"接口签名约束，预留扩展"，并写豁免文件。
3. **是重写方法（@Override）吗？** → 不能删（父类签名约束），加注释 + 豁免。

**反模式**：为消警告在方法体里加 `// noinspection` 或 `// NOSONAR` 而不说明原因。

---

## S6204 Collectors.toList()（Java 16+）

**固定 3 步**：

1. **确认 JDK 版本**：`java -version` 或 pom.xml `<maven.compiler.source>` ≥ 16。
2. **替换**：`.collect(Collectors.toList())` → `.toList()`（返回不可变 List）。
3. **检查调用方是否依赖可变性**：如果后续对返回的 list 做 `add/remove/set` → 不能直接替换，改成 `.collect(Collectors.toCollection(ArrayList::new))` 或在调用方 `new ArrayList<>(stream.toList())`。
4. **清理 import**：替换后如果文件里不再用 `Collectors`，删 `import java.util.stream.Collectors;`。

---

## S3358 嵌套三元

**固定 2 步**：

1. **识别真假嵌套三元**：TS 里 `key?: string` 是可选属性，**不是三元**（引擎已排除）。真嵌套三元是 `a ? b : c ? d : e`。
2. **拆法**：
   - 两层：拆成 `if/else` 赋值中间变量。
   - 多层：用策略模式/Map 查表/switch 表达式（Java 14+）替代。

**示例**：
```java
// 坏
String r = a ? "A" : b ? "B" : c ? "C" : "D";
// 好
String r;
if (a) r = "A";
else if (b) r = "B";
else if (c) r = "C";
else r = "D";
```

---

## S107 参数过多（>7）

**固定 3 步**：

1. **判断参数是否相关**：
   - 相关（都是查询条件/都是请求字段）→ 封装成 DTO/Query 对象（`OrderQuery`、`CreateOrderRequest`）。
   - 不相关（方法做了多件事）→ 拆方法，每个方法只做一件事。
2. **对外服务接口**：改签名影响全部调用方 → 属独立重构专项，先豁免 + 列技术债，排期后统一改。
3. **Builder 模式**：参数可选且多 → 用 Builder 替代长参数列表。

---

## S1128 未使用 import

**固定 2 步**：

1. **全仓确认**：`rg "import xxx"` 确认该 import 在文件里确实没被使用（注意静态 import、注解里的全限定名）。
2. **删除**：直接删行。Python 用 `pyflakes`/IDE 辅助。

**注意**：删除后跑一次编译/导入测试，确认没有"删除后其他文件引用本文件时缺依赖"的情况（import 是文件级的，一般不影响其他文件，但 re-export 模式除外）。

---

## 通用修复原则（所有规则适用）

1. **最小修复**：只改被报问题的代码，不顺手重构无关部分。
2. **改完即检**：每改一个文件，立即跑 `engineering problems <root> --file <file>` 确认该文件归零。
3. **影响面分析**：改方法签名/返回值/常量/时间逻辑后，必须跑 `engineering impact <root>` 查调用方。
4. **编译验证**：Java 改动必须 `mvn compile` 通过；Python 必须 `py_compile` 通过。
5. **禁止 NOSONAR**：默认禁止新增 `// NOSONAR`；确需豁免走 `exemptions.json` + reason。
