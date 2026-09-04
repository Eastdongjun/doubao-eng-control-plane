#!/usr/bin/env python3
"""engineering — SonarQube 硬门禁适配器 CLI。

把 SonarQube 规则固化为可执行的确定性检查，让 AI 写代码按"写前约束 → 写后检查 →
自动优化 → 提交阻断"闭环工作。不依赖 SonarQube Server，输出 SonarQube 风格问题码。

子命令:
  engineering problems <root>            # 全量检查，输出 Problems（非 0 即不能算完成）
  engineering problems <root> --json     # JSON 输出
  engineering improve  <root>            # 写 .ai/evidence/improve-state.json（AI 读取逐条修复）
  engineering hook     <root>            # git pre-commit 用：Error>0 或未豁免 Warning>0 → exit 1
  engineering install-hook <repo>        # 安装 pre-commit hook 到仓库

支持语言: Python(ast 精确) / Java / JS / TS / 通用文本
豁免: <root>/.ai/evidence/exemptions.json  → [{"rule":"S1172","file":"src/X.java","line":12,"reason":"接口签名必须保留"}]
状态: <root>/.ai/evidence/improve-state.json → diagnostics 列表 + status(NEEDS_WORK/PASS)
"""
import argparse, ast, datetime, json, pathlib, re, subprocess, sys

SEV_ERROR, SEV_WARNING = "ERROR", "WARNING"
DEFAULT_COMPLEXITY = 15
DEFAULT_PARAMS = 7
DEFAULT_DUP = 3
# 规则修复适配器（sonar-rules.md 固化，供 sonar-plan / improve 输出给 AI）
ADAPTERS = {
    "S1192": "提 private static final String 常量（业务含义命名，如 MSG_PHONE_EMPTY）；map key/注解元数据/标准值/测试数据不在此列",
    "S3776": "拆小方法：条件分支、循环体、校验逻辑、组装逻辑各拆一个职责方法，命名表达职责",
    "S8688": "now() 必须传时区：LocalDate.now(ZoneId.of(\"Asia/Shanghai\"))；Python datetime.now(timezone.utc)；禁止无参",
    "S1168": "List→Collections.emptyList() / Map→emptyMap() / Set→emptySet()；Python 返回 []/{} 而非 None",
    "S1172": "私有方法直接删参数；公共接口查调用链，不能删时加注释说明，不破坏接口契约",
    "S6204": "stream.collect(Collectors.toList())→stream.toList()（JDK16+，确认调用方不依赖可变性），清理 Collectors import",
    "S3358": "拆 if/else 或中间变量；TS 的 key?: 可选属性不是三元，勿误改",
    "S107": "封装参数对象（request/query DTO）或拆职责；对外服务签名属独立重构专项可豁免+列技术债",
    "S1128": "删除未使用 import；删除前全仓搜索确认无引用",
    "S9999": "修复语法错误（Python py_compile / JS node --check / 编译构建）",
}
# 标准参数值/协议词：重复出现不视为魔法字符串（编码、模式、HTTP 动词、常用格式名等）
STD_LITERALS = {
    "utf-8", "utf8", "ascii", "latin-1", "gbk", "utf-16", "__main__",
    "r", "w", "a", "rb", "wb", "ab", "x", "w+", "r+",
    "strict", "ignore", "replace", "errors", "encoding", "decode", "encode",
    "json", "txt", "csv", "xml", "html", "yaml", "yml", "toml", "ini", "log", "md",
    "http", "https", "ftp", "GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS",
    "true", "false", "null", "none", "True", "False", "None",
    "zh-CN", "en-US", "zh", "en", "cn", "us",
    "Asia/Shanghai", "UTC", "GMT", "GMT+8", "UTC+8", "Asia/Beijing",
    "dev", "test", "prod", "production", "staging", "local", "remote",
    "main", "master", "develop", "release", "feature", "hotfix", "bugfix",
    "error", "warning", "info", "debug", "critical", "fatal",
    "success", "failed", "fail", "pass", "pending", "skipped", "unknown",
    "default", "custom", "manual", "auto", "all", "none",
}
evidence_dir = lambda root: pathlib.Path(root) / ".ai" / "evidence"

class Problem:
    def __init__(self, rule, severity, message, file, line, suggestion=""):
        self.rule, self.severity, self.message = rule, severity, message
        self.file, self.line, self.suggestion = file, line, suggestion
    def to_dict(self):
        return {"rule": self.rule, "severity": self.severity, "message": self.message,
                "file": self.file, "line": self.line, "suggestion": self.suggestion}
    def __str__(self):
        return f"{self.rule}[{self.severity}]: {self.message} ({self.file}:{self.line})"

def load_exemptions(root):
    f = evidence_dir(root) / "exemptions.json"
    if not f.exists(): return []
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return []

def is_exempt(exemptions, rule, file, line):
    for e in exemptions:
        if e.get("rule") != rule: continue
        if e.get("file") == file:
            # 文件级豁免：省略 line 或 line=0 → 该文件该规则全部豁免
            if not e.get("line") or e["line"] == 0:
                return True
            if e["line"] == line:
                return True
    return False

def rel(path, root):
    try:
        return str(pathlib.Path(path).resolve().relative_to(pathlib.Path(root).resolve()))
    except Exception:
        return str(path)

# ==================== Python 检查器（ast 精确） ====================

class PyChecker:
    def __init__(self, root):
        self.root, self.problems, self.exemptions = root, [], load_exemptions(root)
        self.dup_counter = {}  # literal -> [(file,line)]
    def check(self, path, code):
        f = rel(path, self.root)
        try:
            tree = ast.parse(code, filename=str(f))
        except SyntaxError as e:
            self._add("S9999", SEV_ERROR, f"语法错误: {e.msg}", f, e.lineno or 0, "修复语法错误")
            return
        self._scan_dup_literals(tree, f)
        self._scan_complexity(tree, f)
        self._scan_now_without_tz(tree, f)
        self._scan_unused_params(tree, f)
        self._scan_null_collection(tree, f)
        self._scan_nested_ternary(tree, f)
        self._scan_too_many_params(tree, f)
        self._scan_unused_imports(tree, f)
        self._scan_nosonar(code, f)
    def _scan_nosonar(self, code, f):
        # 禁止新增 NOSONAR/noinspection 逃避（S9998）；只匹配行尾真正的抑制注释（// NOSONAR 或 // NOSONAR java:S1234）
        # 代码注释里提到"NOSONAR 统计/检测"等不算逃避
        for m in re.finditer(r"(?://|#)\s*(?:NOSONAR|noinspection)(?:\s+[-\w:.]+)?\s*$", code, re.MULTILINE):
            self._add("S9998", SEV_WARNING, f"禁止使用 NOSONAR 逃避问题；确需豁免请写 exemptions.json + reason。",
                      f, code[:m.start()].count("\n") + 1, "移除 NOSONAR，改用 exemptions.json 带 reason 豁免。")
    def _add(self, rule, sev, msg, f, line, sug=""):
        if not is_exempt(self.exemptions, rule, f, line):
            self.problems.append(Problem(rule, sev, msg, f, line, sug))
    def _scan_dup_literals(self, tree, f):
        # 字典/对象键不是魔法字符串，先收集并排除
        dict_keys = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                for k in node.keys:
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        dict_keys.add(k.value)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                v = node.value.strip()
                if len(v) < 3 or len(v) > 80 or v.isdigit() or v in dict_keys: continue
                if v in STD_LITERALS: continue          # 标准参数值/协议词
                if v.startswith(("/", ".", "\\")): continue  # 路径/相对路径片段
                if re.fullmatch(r"[\w.\-]+\.(py|js|ts|java|json|md|txt|csv|xml|html|yml|yaml|log|sh|bat|jar|war|class|png|jpg|svg|css|scss|tsx|jsx)", v): continue
                key = v
                self.dup_counter.setdefault(key, []).append((f, node.lineno))
    def _dup_report(self):
        for v, locs in self.dup_counter.items():
            if len(locs) >= DEFAULT_DUP:
                f, line = locs[0]
                self._add("S1192", SEV_WARNING, f'Define a constant instead of duplicating this literal "{v[:40]}" {len(locs)} times.',
                          f, line, '提取为模块级常量（如 LOADING_TEXT），替换全部出现处。')
    def _scan_complexity(self, tree, f):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                c = self._complexity(node)
                if c > DEFAULT_COMPLEXITY:
                    self._add("S3776", SEV_WARNING,
                              f"Refactor this function to reduce its Cognitive Complexity from {c} to {DEFAULT_COMPLEXITY} allowed.",
                              f, node.lineno, "拆分为多个小函数，减少 if/else/for 嵌套。")
    def _complexity(self, node):
        c = 0
        for n in ast.walk(node):
            if isinstance(n, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.ExceptHandler, ast.With, ast.AsyncWith)):
                c += 1
            elif isinstance(n, ast.BoolOp):
                c += len(n.values) - 1
            elif isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                c += 1
        return c
    def _scan_now_without_tz(self, tree, f):
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
               and node.func.attr in ("now", "today"):
                base = node.func.value
                if isinstance(base, ast.Name):
                    base_id = base.id
                elif isinstance(base, ast.Attribute):
                    base_id = base.attr
                else:
                    base_id = ""
                if base_id in ("datetime", "date", "LocalDate", "LocalDateTime") \
                   and not node.args \
                   and not any(k.arg in ("tz", "tzinfo", "zone", "clock") for k in node.keywords if k.arg):
                    self._add("S8688", SEV_ERROR, f"{base_id}.{node.func.attr}() 必须显式传时区/Clock/ZoneId，禁止默认时区。",
                              f, node.lineno, '传入 Clock 或 ZoneId：如 LocalDate.now(ZoneId.of("Asia/Shanghai")) 或 datetime.now(timezone.utc)。')
    def _scan_unused_params(self, tree, f):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a.arg for a in node.args.args]
                if not args: continue
                names = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
                for a in args:
                    if a in ("self", "cls") or a.startswith("_"): continue
                    if a not in names:
                        self._add("S1172", SEV_WARNING, f'Unused method parameter "{a}".', f, node.lineno,
                                  "移除未使用参数；若为接口签名必须保留，加注释说明并计入豁免文件。")
    def _scan_null_collection(self, tree, f):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                ret = node.returns
                hint = ""
                if ret is not None:
                    hint = ast.unparse(ret).lower()
                coll = any(k in hint for k in ("list", "set", "dict", "tuple", "map")) if hint else False
                has_return_none = any(isinstance(n, ast.Return) and (n.value is None or
                    (isinstance(n.value, ast.Constant) and n.value.value is None)) for n in ast.walk(node))
                if coll and has_return_none:
                    self._add("S1168", SEV_ERROR, "函数声明返回集合/Map 却返回 None，调用方无法安全迭代。",
                              f, node.lineno, "空集合返回 [] / {} / set() / ()，空 Map 返回 {}，禁止返回 None。")
    def _scan_nested_ternary(self, tree, f):
        for node in ast.walk(tree):
            if isinstance(node, ast.IfExp):
                if isinstance(node.body, ast.IfExp) or isinstance(node.orelse, ast.IfExp):
                    self._add("S3358", SEV_ERROR, "嵌套三元表达式不可读，拆分为 if/elif 或局部变量。",
                              f, node.lineno, "改为 if/elif/else 语句或先赋值中间变量。")
    def _scan_too_many_params(self, tree, f):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a for a in node.args.args if a.arg not in ("self", "cls")]
                if len(args) > DEFAULT_PARAMS:
                    self._add("S107", SEV_WARNING, f"Function has {len(args)} parameters, which is greater than {DEFAULT_PARAMS} authorized.",
                              f, node.lineno, "封装参数对象（dataclass/POJO）或拆分职责。")
    def _scan_unused_imports(self, tree, f):
        imported = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    imported[a.asname or a.name.split(".")[0]] = node.lineno
            elif isinstance(node, ast.ImportFrom):
                for a in node.names:
                    imported[a.asname or a.name] = node.lineno
        used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        used |= {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
        for name, line in imported.items():
            if name not in used and name != "*":
                self._add("S1128", SEV_WARNING, f'Remove this unused import "{name}".', f, line, "删除未使用 import。")

# ==================== Java / JS / TS 检查器（文本+正则，务实） ====================

class TextChecker:
    def __init__(self, root, lang):
        self.root, self.lang, self.problems, self.exemptions = root, lang, [], load_exemptions(root)
        self.dup_counter = {}
    def check(self, path, code):
        f = rel(path, self.root)
        self._dup(code, f)
        self._complexity(code, f)
        self._now_no_zone(code, f)
        self._null_collection(code, f)
        self._nested_ternary(code, f)
        self._params(code, f)
        if self.lang == "java":
            self._collectors_to_list(code, f)
        # 语法级：node --check 用于 JS/TS
        if self.lang in ("js", "ts") and path.suffix in (".js", ".mjs", ".cjs"):
            r = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
            if r.returncode != 0:
                self._add("S9999", SEV_ERROR, f"语法错误: {r.stderr.strip()[:120]}", f, 0, "修复语法错误")
        self._nosonar(code, f)
    def _nosonar(self, code, f):
        for m in re.finditer(r"(?://|#)\s*(?:NOSONAR|noinspection)(?:\s+[-\w:.]+)?\s*$", code, re.MULTILINE):
            self._add("S9998", SEV_WARNING, f"禁止使用 NOSONAR 逃避问题；确需豁免请写 exemptions.json + reason。",
                      f, code[:m.start()].count("\n") + 1, "移除 NOSONAR，改用 exemptions.json 带 reason 豁免。")
    def _add(self, rule, sev, msg, f, line, sug=""):
        if not is_exempt(self.exemptions, rule, f, line):
            self.problems.append(Problem(rule, sev, msg, f, line, sug))
    def _dup(self, code, f):
        if self.lang == "java":
            pat = re.compile(r'"((?:[^"\\]|\\.){3,80})"')
        else:
            pat = re.compile(r"['\"]((?:[^'\"\\]|\\.){3,80})['\"]")
        for m in pat.finditer(code):
            v = m.group(1)
            if "\n" in v or "\r" in v: continue  # 跨行字符串/文本块不视为魔法字符串
            if v.isdigit() or v.startswith(("http", "/", ".")): continue
            if v in STD_LITERALS: continue
            # 跳过 map/get 调用 key 上下文：xxx("key") 或 xxx("key", ...) —— 字典键不视为魔法字符串
            if re.search(r"\b(?:get|put|set|remove|containsKey|getOrDefault|computeIfAbsent|getProperty|setProperty|setAttribute|getAttribute)\s*\(\s*['\"]?$", code[max(0, m.start() - 60):m.start()]):
                continue
            # 跳过注解属性/参数上下文：@Xxx(value = "v")、@Xxx(name = "v", defaultValue = "v")、@SuppressWarnings("unchecked") —— 注解元数据不视为魔法字符串
            if re.search(r"@\w+[^\n]*?\b(?:value|name|defaultValue|pattern|message|required|header|path|param)\s*=\s*['\"]$", code[max(0, m.start() - 120):m.start()]):
                continue
            if re.search(r"@SuppressWarnings\(\s*['\"]$", code[max(0, m.start() - 60):m.start()]):
                continue
            # 跳过全限定名（含两个点，如 com.shopjoy.common / java.util.List）
            if v.count(".") >= 2:
                continue
            self.dup_counter.setdefault(v, []).append((f, code[:m.start()].count("\n") + 1))
    def _dup_report(self):
        for v, locs in self.dup_counter.items():
            if len(locs) >= DEFAULT_DUP:
                # 报在第一个未豁免出现位置：全部位置均豁免才跳过（避免"首次位置碰巧豁免"导致漏报）
                for f, ln in locs:
                    if not is_exempt(self.exemptions, "S1192", f, ln):
                        self._add("S1192", SEV_WARNING, f'Define a constant instead of duplicating this literal "{v[:40]}" {len(locs)} times.',
                                  f, ln, "提取为 private static final String 常量，替换全部出现处。")
                        break
    def _complexity(self, code, f):
        for m in re.finditer(r"\b(public|private|protected)\s+[\w<>,\.\[\] ]+\s+(\w+)\s*\([^)]*\)\s*\{", code):
            body = code[m.end():]
            depth = 0; c = 0; i = 0
            while i < len(body) and depth >= 0:
                ch = body[i]
                if ch == "{": depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth < 0: break
                i += 1
            seg = body[:i]
            c = sum(len(re.findall(r"\b(if|for|while|catch|case)\b", seg.split(";")[k])) for k in range(len(seg.split(";")))) if seg else 0
            if c > DEFAULT_COMPLEXITY:
                self._add("S3776", SEV_WARNING, f"Refactor this method to reduce its Cognitive Complexity from {c} to {DEFAULT_COMPLEXITY} allowed.",
                          f, code[:m.start()].count("\n") + 1, "拆分为小方法，减少 if/else 嵌套。")
    def _now_no_zone(self, code, f):
        pat = re.compile(r"\b(LocalDate|LocalDateTime)\.(now|today)\(\s*\)")
        for m in pat.finditer(code):
            self._add("S8688", SEV_ERROR, f"{m.group(1)}.{m.group(2)}() 必须显式传 Clock/ZoneId，禁止默认时区。",
                      f, code[:m.start()].count("\n") + 1, 'LocalDate.now(ZoneId.of("Asia/Shanghai"))。')
    def _null_collection(self, code, f):
        if self.lang != "java": return
        for m in re.finditer(r"\breturn\s+null\s*;", code):
            before = code[:m.start()]
            sigs = list(re.finditer(r"\b(?:public|private|protected)\s+([\w<>,\.\[\] ]+)\s+\w+\s*\([^)]*\)\s*\{", before))
            if not sigs:
                continue
            ret_type = sigs[-1].group(1)
            if re.search(r"\b(List|Set|Map|Collection|Iterable)\b", ret_type):
                self._add("S1168", SEV_ERROR, f"方法返回集合/Map（{ret_type.strip()}）却 return null，调用方无法安全迭代。",
                          f, code[:m.start()].count("\n") + 1, "空集合返回 Collections.emptyList()/emptyMap()/emptySet()。")
    def _nested_ternary(self, code, f):
        # \?(?!:) 排除 TS 可选属性/参数（key?: string）误报；Java/Python 无此语法，同样适用
        pat = re.compile(r"[^;{}()]*\?(?!:)[^;{}()]*:[^;{}()]*\?(?!:)")
        for m in pat.finditer(code):
            self._add("S3358", SEV_ERROR, "嵌套三元表达式不可读，拆分为 if/elif 或局部变量。",
                      f, code[:m.start()].count("\n") + 1, "改为 if/else 语句或先赋值中间变量。")
    def _params(self, code, f):
        if self.lang == "java":
            pat = re.compile(r"\b(?:public|private|protected)\s+[\w<>,\.\[\] ]+\s+\w+\s*\(([^)]*)\)\s*\{")
            def split(a):
                return [x.strip() for x in a.split(",") if x.strip()]
        else:
            pat = re.compile(r"\bfunction\s+\w+\s*\(([^)]*)\)|=>\s*\(([^)]*)\)\s*=>")
            def split(a):
                return [x.strip() for x in a.split(",") if x.strip()]
        for m in pat.finditer(code):
            g = m.group(1)
            if g is None:
                g = m.group(2)
            args = split(g or "")
            if len(args) > DEFAULT_PARAMS:
                self._add("S107", SEV_WARNING, f"Method has {len(args)} parameters, which is greater than {DEFAULT_PARAMS} authorized.",
                          f, code[:m.start()].count("\n") + 1, "封装参数对象或拆分职责。")
    def _collectors_to_list(self, code, f):
        for m in re.finditer(r"\.collect\(\s*Collectors\.toList\(\)\s*\)", code):
            self._add("S6204", SEV_WARNING, "使用 stream.toList() 替代 Collectors.toList()（Java 16+）。",
                      f, code[:m.start()].count("\n") + 1, "改为 .toList()。")

# ==================== 主流程 ====================

def collect_files(root):
    root = pathlib.Path(root)
    files = []
    skip_dirs = {".git", ".venv", "node_modules", "target", "build", "dist", "__pycache__", ".ai", "backups", "_drill",
                 "_ref_skills", "_projects", "_eval_samples", "vscode-demo"}
    for p in root.rglob("*"):
        if p.is_file() and p.suffix in (".py", ".java", ".js", ".ts", ".mjs", ".cjs"):
            # 仅按相对 root 的子目录判断 skip：root 自身为 _projects 下的项目时不受影响
            try:
                rel = p.relative_to(root)
            except ValueError:
                continue
            if any(part in skip_dirs for part in rel.parts):
                continue
            files.append(p)
    return files

def run_checks(root, only=None):
    root = pathlib.Path(root)
    problems = []
    py = PyChecker(root)
    text_checks = {}
    files = collect_files(root) if only is None else only
    for f in files:
        code = f.read_text(encoding="utf-8", errors="replace")
        if f.suffix == ".py":
            py.check(f, code)
        else:
            lang = {".java": "java", ".js": "js", ".mjs": "js", ".cjs": "js", ".ts": "ts"}.get(f.suffix)
            tc = text_checks.setdefault(lang, TextChecker(root, lang))
            tc.check(f, code)
    problems += py.problems
    py._dup_report()
    problems += py.problems
    for tc in text_checks.values():
        tc._dup_report()
        problems += tc.problems
    # 去重（同一 file:line:rule）
    seen, uniq = set(), []
    for p in sorted(problems, key=lambda x: (x.file, x.line, x.rule)):
        k = (p.file, p.line, p.rule)
        if k not in seen:
            seen.add(k); uniq.append(p)
    return uniq

def count_by_sev(problems):
    return {"ERROR": sum(1 for p in problems if p.severity == SEV_ERROR),
            "WARNING": sum(1 for p in problems if p.severity == SEV_WARNING)}

def cmd_problems(args):
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    problems = run_checks(root)
    if args.file:
        # 单文件快速检查：仅报告目标文件（供 MCP 写后即时反馈 / 写前预检）
        target = str((root / args.file).resolve()) if not pathlib.Path(args.file).is_absolute() else args.file
        problems = [p for p in problems if p.file == args.file or str((root / p.file).resolve()) == target]
    if args.json:
        print(json.dumps({"problems_count": len(problems), "problems": [p.to_dict() for p in problems]},
                         ensure_ascii=False, indent=2))
        return 0 if not problems else 1
    c = count_by_sev(problems)
    print(f"SonarQube 硬门禁检查 · {root.name} · {len(problems)} problems "
          f"(ERROR={c['ERROR']}, WARNING={c['WARNING']})")
    for p in problems:
        print(f"  {p}")
    if not problems:
        print("✓ 全部通过（0 problems）")
        return 0
    print(f"\n结论: {'✗ 存在 ERROR，禁止提交/宣称完成' if c['ERROR'] else ''}"
          f"{'✗ 存在未豁免 WARNING，禁止提交' if c['WARNING'] else ''}")
    return 1

def cmd_sonar_plan(args):
    """写前预检：列出目标文件的现有 Sonar 问题 + 本次写代码禁止新增的模式 + 修复指引。
    用法: engineering sonar-plan <项目根> <目标文件>"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    target = pathlib.Path(args.file)
    target_abs = target.resolve() if target.is_absolute() else (root / target).resolve()
    try:
        rel = target_abs.relative_to(root.resolve())
    except ValueError:
        print(f"✗ 目标文件不在项目根内: {target}"); return 2
    if not target_abs.is_file():
        print(f"✗ 目标文件不存在: {target_abs}"); return 2
    problems = run_checks(root)
    mine = [p for p in problems if str((root / p.file).resolve()) == str(target_abs)]
    lang = target_abs.suffix.lstrip(".")
    budget = file_budget(str(rel))
    c = count_by_sev(mine)
    print(f"📍 Sonar 写前预检 · {rel}")
    print(f"  文件角色: {budget['role']} | 复杂度预算: <= {budget['max_complexity']}")
    print(f"  角色约束: {' / '.join(budget['rules'])}")
    print(f"  当前文件已有问题: {len(mine)} 个 (ERROR={c['ERROR']}, WARNING={c['WARNING']})")
    if not mine:
        print("  ✓ 该文件当前 0 problems")
    for r in sorted({p.rule for p in mine}):
        locs = [p.line for p in mine if p.rule == r]
        print(f"    - {r}: {len(locs)} 个 (行 {locs[:8]}{'…' if len(locs)>8 else ''})")
    print(f"  本次写代码必须避免新增:")
    if lang in ("java",):
        forb = ["无参 now()（S8688）", "return null 集合/Map（S1168）", "嵌套三元（S3358）", "重复字符串 ≥3 次（S1192）",
                "Collectors.toList()（S6204）", "方法继续膨胀超 15 复杂度（S3776）", "未使用 import（S1128）"]
    elif lang in ("py", "python"):
        forb = ["datetime.now() 无参（S8688）", "return None 代替空集合（S1168）", "嵌套三元（S3358）",
                "重复字符串 ≥3 次（S1192）", "方法继续膨胀超 15 复杂度（S3776）", "未使用 import（S1128）"]
    else:
        forb = ["无参 now()（S8688）", "重复字符串 ≥3 次（S1192）", "嵌套三元（S3358）", "方法继续膨胀超 15 复杂度（S3776）"]
    for f in forb:
        print(f"    ✗ {f}")
    if mine:
        print(f"  修复指引（对应 adapter，详见 sonar-rules.md）:")
        seen = set()
        for p in mine:
            if p.rule in seen: continue
            seen.add(p.rule)
            print(f"    - {p.rule}: {ADAPTERS.get(p.rule, '按规则修复')}")
    return 0

def cmd_improve(args):
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    problems = run_checks(root)
    ev = evidence_dir(root)
    ev.mkdir(parents=True, exist_ok=True)
    state = {
        "generated_at": __import__("datetime").datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "project": str(root),
        "problems_count": len(problems),
        "status": "PASS" if not problems else "NEEDS_WORK",
        "diagnostics": [{**p.to_dict(), "adapter": ADAPTERS.get(p.rule, "按规则修复，详见 sonar-rules.md")} for p in problems],
        "next_action": "修复全部 diagnostics 后重新运行 problems，直到 0 problems。" if problems else "已达标，可进入提交。",
    }
    out = ev / "improve-state.json"
    out.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    c = count_by_sev(problems)
    print(f"✓ improve-state.json 已写入 {out}")
    print(f"  状态: {state['status']} | {len(problems)} problems (ERROR={c['ERROR']}, WARNING={c['WARNING']})")
    print("  AI 请读取该文件，按 diagnostics 逐条修复（rule/message/suggestion），修完重跑 problems 直到 0。")
    return 0 if not problems else 1

def cmd_hook(args):
    """git pre-commit：Error>0 或 未豁免 Warning>0 → 阻断 commit。--staged 仅检查暂存文件（增量）。"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print("BLOCKED: 项目根不存在，禁止提交"); return 1
    if args.staged:
        r = subprocess.run(["git", "-C", str(root), "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("🔴 BLOCKED: 无法读取 git 暂存区（非 git 仓库？），禁止提交。"); return 1
        wanted = {".py", ".java", ".js", ".ts", ".mjs", ".cjs"}
        only = [root / x for x in r.stdout.splitlines() if pathlib.Path(x).suffix in wanted]
        only = [p for p in only if p.exists()]
        if not only:
            print("🟢 SONARQUBE GATE PASS — 本次无代码文件变更，允许提交")
            return 0
        problems = run_checks(root, only=only)
    else:
        problems = run_checks(root)
    c = count_by_sev(problems)
    blocked = []
    if c["ERROR"] > 0:
        blocked.append(f"{c['ERROR']} 个 ERROR（SonarQube Error>0 禁止 commit）")
    if c["WARNING"] > 0:
        blocked.append(f"{c['WARNING']} 个未豁免 WARNING（禁止 commit）")
    if blocked:
        print("🔴 SONARQUBE GATE BLOCKED")
        for b in blocked: print(f"  - {b}")
        for p in problems[:10]: print(f"  {p}")
        print("请运行: engineering improve <root> 读取 improve-state.json 逐条修复，或对合理项写豁免文件。")
        return 1
    print("🟢 SONARQUBE GATE PASS — 允许提交")
    return 0

def cmd_install_hook(args):
    repo = pathlib.Path(args.repo)
    hooks = repo / ".git" / "hooks"
    hooks.mkdir(parents=True, exist_ok=True)
    hook = hooks / "pre-commit"
    script = f"""#!/bin/sh
# SonarQube 硬门禁 pre-commit hook（由 engineering install-hook 生成）
# 阻断规则: Error>0 / 未豁免 Warning>0 / AI Gate 离线 / 采集失败 → 禁止 commit
# 逃生开关: SKIP_SONAR_GATE=1 git commit ...（仅限确需绕过的场景）
[ -n "$SKIP_SONAR_GATE" ] && exit 0
ENG="{pathlib.Path(__file__).resolve()}"
ROOT="{repo.resolve()}"
GATE_URL="http://127.0.0.1:8848/mcp"
if [ ! -f "$ENG" ]; then
  echo "🔴 BLOCKED: engineering 桥不可用（$ENG 缺失），禁止提交。请先恢复工程化工具链。"
  exit 1
fi
if ! curl -s -m 2 -o /dev/null "$GATE_URL" 2>/dev/null; then
  echo "🔴 BLOCKED: AI Gate（VSCode-MCP :8848）不在线，禁止提交。"
  echo "  请启动: cd $(dirname "$ENG")/../vscode-mcp && .venv/bin/python server.py"
  echo "  或确需绕过时: SKIP_SONAR_GATE=1 git commit ..."
  exit 1
fi
"${{PYTHON:-python3}}" "$ENG" hook "$ROOT" --staged || exit 1
exit 0
"""
    hook.write_text(script, encoding="utf-8")
    hook.chmod(0o755)
    print(f"✓ pre-commit hook 已安装: {hook}")
    return 0

# ==================== 层 8-15：新增诊断门禁 / 队列 / 影响面 / 报告 ====================

# 文件级质量预算（层 9）：按路径角色识别，不同文件不同阈值
FILE_BUDGETS = {
    "controller": {"role": "Controller", "max_complexity": 8, "rules": ["不允许复杂业务逻辑", "只做参数校验+转发+响应组装"]},
    "service": {"role": "Service", "max_complexity": 15, "rules": ["业务逻辑在此", "方法复杂度<=15", "必须显式时区"]},
    "mapper": {"role": "Mapper", "max_complexity": 10, "rules": ["不允许拼接 SQL 风险", "只做数据访问"]},
    "dto": {"role": "DTO", "max_complexity": 3, "rules": ["不允许业务计算", "纯数据载体"]},
    "schedule": {"role": "Task/Schedule", "max_complexity": 12, "rules": ["必须显式时区", "定时任务必须幂等"]},
    "task": {"role": "Task/Schedule", "max_complexity": 12, "rules": ["必须显式时区", "定时任务必须幂等"]},
    "config": {"role": "Config", "max_complexity": 5, "rules": ["只做配置装配", "不允许业务逻辑"]},
    "util": {"role": "Util", "max_complexity": 10, "rules": ["工具类必须无状态", "方法必须纯函数"]},
    "test": {"role": "Test", "max_complexity": 20, "rules": ["测试数据保持字面量", "不强制提常量"]},
}

def file_budget(rel_path):
    """根据文件相对路径识别角色与质量预算。"""
    p = rel_path.lower()
    for key, budget in FILE_BUDGETS.items():
        if f"/{key}/" in p or p.endswith(f"{key}.java") or f"/{key}" in p.split("/")[-1].lower():
            return budget
    return {"role": "Default", "max_complexity": 15, "rules": ["默认复杂度<=15", "遵循通用 Sonar 规则"]}

# 优先级队列（层 10）：P0-P4
PRIORITY_MAP = {
    "S9999": ("P0", "编译/语法错误"),
    "S8688": ("P1", "时区缺失（生产风险）"),
    "S1168": ("P1", "返回 null 集合（NPE 风险）"),
    "S3358": ("P2", "嵌套三元（可读性）"),
    "S3776": ("P2", "认知复杂度（可维护性）"),
    "S107": ("P2", "参数过多（可维护性）"),
    "S1172": ("P3", "未使用参数（代码质量）"),
    "S1128": ("P3", "未使用 import（代码质量）"),
    "S6204": ("P3", "Collectors.toList（风格）"),
    "S1192": ("P3", "重复字符串（风格）"),
    "S9998": ("P1", "NOSONAR 滥用（质量逃避）"),
}

def priority_of(rule):
    return PRIORITY_MAP.get(rule, ("P3", "其他"))

def cmd_snapshot(args):
    """记录当前 problems 快照（层 8 新增诊断门禁的基线）。"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    problems = run_checks(root)
    ev = evidence_dir(root)
    ev.mkdir(parents=True, exist_ok=True)
    snap = {
        "snapshot_at": __import__("datetime").datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "project": str(root),
        "problems_count": len(problems),
        "problems": [p.to_dict() for p in problems],
    }
    out = ev / "sonar-snapshot.json"
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    c = count_by_sev(problems)
    print(f"✓ 快照已写入 {out}")
    print(f"  基线: {len(problems)} problems (ERROR={c['ERROR']}, WARNING={c['WARNING']})")
    return 0

def cmd_diff(args):
    """对比快照 vs 当前，输出新增/修复/总数（层 8 新增诊断门禁）。"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    snap_file = evidence_dir(root) / "sonar-snapshot.json"
    if not snap_file.exists():
        print("✗ 无快照，请先运行: engineering snapshot <root>"); return 2
    snap = json.loads(snap_file.read_text(encoding="utf-8"))
    current = run_checks(root)
    snap_keys = {(p["rule"], p["file"], p["line"]) for p in snap["problems"]}
    cur_keys = {(p.rule, p.file, p.line) for p in current}
    fixed = snap_keys - cur_keys
    added = cur_keys - snap_keys
    print(f"📊 Sonar 诊断对比（基线 {snap['problems_count']} → 当前 {len(current)}）")
    print(f"  ✅ 已修复: {len(fixed)} 个")
    for r, f, l in sorted(fixed)[:10]:
        print(f"    - {r} {f}:{l}")
    if len(fixed) > 10: print(f"    … 共 {len(fixed)} 个")
    print(f"  🔴 新增问题: {len(added)} 个")
    for r, f, l in sorted(added):
        print(f"    + {r} {f}:{l}")
    if added:
        print(f"\n⚠ 新增诊断门禁触发：新增 {len(added)} 个问题，必须修复或回滚本次写入，不允许带着新增问题继续。")
        return 1
    print("\n🟢 无新增问题，允许继续。")
    return 0

def cmd_queue(args):
    """Sonar Fix Queue：按 P0-P4 优先级输出修复队列 + 分批计划（层 10/14）。"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    problems = run_checks(root)
    if not problems:
        print("🟢 0 problems，无需修复队列。"); return 0
    by_prio = {}
    for p in problems:
        prio, desc = priority_of(p.rule)
        by_prio.setdefault(prio, []).append((p, desc))
    print(f"📋 Sonar Fix Queue（共 {len(problems)} 个问题）")
    batch_plan = [
        ("第一批", "P0", "所有 Java Error / 编译错误", "必须先清零，不允许进入下一批"),
        ("第二批", "P1", "时区缺失 / null 集合 / NOSONAR 滥用", "生产风险，清零后再继续"),
        ("第三批", "P2", "复杂度 / 嵌套三元 / 参数过多", "高风险可维护性问题"),
        ("第四批", "P3", "重复字符串 / 未用 import / 风格", "低风险风格问题，最后处理"),
    ]
    for batch_name, prio, desc, rule in batch_plan:
        items = by_prio.get(prio, [])
        print(f"\n  {batch_name}（{prio}）{desc} — {len(items)} 个")
        print(f"    规则: {rule}")
        for p, d in items[:8]:
            print(f"    [{p.rule}] {p.file}:{p.line} — {d}")
        if len(items) > 8: print(f"    … 共 {len(items)} 个")
    # 写队列到 evidence
    ev = evidence_dir(root)
    ev.mkdir(parents=True, exist_ok=True)
    queue_data = {
        "generated_at": __import__("datetime").datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "total": len(problems),
        "batches": {prio: [{"rule": p.rule, "file": p.file, "line": p.line, "message": p.message} for p, _ in items]
                    for prio, items in by_prio.items()},
    }
    out = ev / "fix-queue.json"
    out.write_text(json.dumps(queue_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ 队列已写入 {out}")
    return 0

def _impact_checks(code):
    """检测文件改动类型，返回风险检查列表。"""
    checks = []
    if re.search(r"(public|private|protected)\s+[\w<>,\.\[\]\s]+\s+\w+\s*\([^)]*\)", code):
        checks.append("方法签名变更 → 查调用方")
    if re.search(r"return\s+null", code):
        checks.append("返回 null → 查调用方是否依赖 null")
    if re.search(r"private\s+static\s+final\s+String", code):
        checks.append("常量变更 → 查是否参与协议/数据库枚举")
    if re.search(r"(LocalDate|LocalDateTime|LocalTime|Instant|Date|Calendar)\s*\.", code):
        checks.append("时间逻辑 → 查测试和时区")
    return checks

def _find_callers(root, method, exclude_rel):
    """rg 搜索方法调用方，排除自身文件。"""
    rr = subprocess.run(["rg", "-l", method, str(root), "--glob", "*.java", "--glob", "*.py"],
                         capture_output=True, text=True)
    return [x for x in rr.stdout.splitlines() if x and not x.endswith(exclude_rel)]

def _print_impact_findings(root, findings):
    """输出影响面分析结果（含调用方搜索）。"""
    for rel, role, checks, code in findings:
        print(f"\n  📄 {rel}（角色: {role}）")
        for c in checks:
            print(f"    ⚠ {c}")
            if "方法签名" in c:
                methods = re.findall(r"(?:public|private|protected)\s+[\w<>,\.\[\]\s]+?\s+(\w+)\s*\(", code)
                for m in methods[:3]:
                    callers = _find_callers(root, m, rel)
                    if callers:
                        print(f"      调用方 ({m}): {len(callers)} 个文件")
                        for c2 in callers[:3]: print(f"        - {c2}")

def cmd_impact(args):
    """改动后影响面分析（层 13）：查方法签名/返回值/常量/时间逻辑的调用方。"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    r = subprocess.run(["git", "-C", str(root), "diff", "--name-only", "HEAD"], capture_output=True, text=True)
    changed = [x for x in r.stdout.splitlines() if x.endswith((".java", ".py", ".js", ".ts"))]
    if not changed:
        print("ℹ 无代码文件改动（git diff HEAD 为空），影响面分析跳过。")
        return 0
    print(f"🔍 改动影响面分析（{len(changed)} 个文件）")
    findings = []
    for f in changed:
        full = root / f
        if not full.exists(): continue
        try:
            code = full.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(full.relative_to(root))
        checks = _impact_checks(code)
        if checks:
            findings.append((rel, file_budget(rel)["role"], checks, code))
    if not findings:
        print("  ℹ 未检测到高风险改动类型。")
    _print_impact_findings(root, findings)
    ev = evidence_dir(root)
    ev.mkdir(parents=True, exist_ok=True)
    out = ev / "impact-analysis.json"
    out.write_text(json.dumps({"changed_files": changed, "findings": [
        {"file": r, "role": role, "checks": checks} for r, role, checks, _ in findings
    ]}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ 影响面报告已写入 {out}")
    return 0

def cmd_report(args):
    """AI 自检报告（层 15）：对比快照，生成完整交付报告。没有报告不允许提交。"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    snap_file = evidence_dir(root) / "sonar-snapshot.json"
    snap_count = None
    if snap_file.exists():
        snap = json.loads(snap_file.read_text(encoding="utf-8"))
        snap_count = snap["problems_count"]
    current = run_checks(root)
    c = count_by_sev(current)
    # 编译状态（Java 项目尝试 mvn compile）
    compile_status = "未跑（非 Java 项目或无 pom.xml）"
    pom = root / "pom.xml"
    if pom.exists() or (root / "backend" / "pom.xml").exists():
        compile_status = "需手动运行 mvn compile 验证"
    # 统计 NOSONAR 滥用数量
    nosonar_count = sum(1 for p in current if p.rule == "S9998")
    # 改动文件
    r = subprocess.run(["git", "-C", str(root), "diff", "--name-only", "HEAD"], capture_output=True, text=True)
    changed = [x for x in r.stdout.splitlines() if x.strip()]
    report = {
        "generated_at": __import__("datetime").datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "project": str(root),
        "修复前_problems": snap_count,
        "修复后_problems": len(current),
        "新增_problems": max(0, len(current) - (snap_count or 0)),
        "ERROR": c["ERROR"],
        "WARNING": c["WARNING"],
        "编译": compile_status,
        "NOSONAR_使用": nosonar_count,
        "修改文件数": len(changed),
        "修改文件": changed[:30],
        "结论": "PASS" if c["ERROR"] == 0 and c["WARNING"] == 0 else "FAIL（仍有未清零问题）",
    }
    ev = evidence_dir(root)
    ev.mkdir(parents=True, exist_ok=True)
    out = ev / "self-check-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("📋 AI 自检报告")
    for k, v in report.items():
        if k == "修改文件": continue
        print(f"  {k}: {v}")
    if report["结论"] == "PASS":
        print("\n🟢 自检通过，允许提交。")
    else:
        print(f"\n🔴 自检未通过：仍有 {len(current)} 个问题，不允许提交。")
    return 0 if report["结论"] == "PASS" else 1

def cmd_verify_stale(args):
    """Stale Diagnostic 识别（层 11）：VSCode 报 Java Error 但 Maven 编译过了。"""
    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"✗ 项目根不存在: {root}"); return 2
    target = pathlib.Path(args.file)
    target_abs = target.resolve() if target.is_absolute() else (root / target).resolve()
    if not target_abs.is_file():
        print(f"✗ 文件不存在: {target_abs}"); return 2
    # 1. 读源码对应行
    code = target_abs.read_text(encoding="utf-8")
    lines = code.split("\n")
    print(f"🔍 Stale Diagnostic 验证 · {target_abs.name}")
    print(f"  文件行数: {len(lines)}")
    # 2. 跑 mvn compile（如果是 Java 项目）
    pom = root / "pom.xml"
    backend_pom = root / "backend" / "pom.xml"
    if pom.exists() or backend_pom.exists():
        mvn_dir = str(pom.parent) if pom.exists() else str(backend_pom.parent)
        print(f"  运行 mvn compile（{mvn_dir}）…")
        rr = subprocess.run(["mvn", "-q", "compile", "-DskipTests"], cwd=mvn_dir,
                            capture_output=True, text=True, timeout=300)
        if rr.returncode == 0:
            print("  ✅ Maven 编译通过")
            print("  ⚠ 标记为 suspected_stale：VSCode 报 Error 但编译通过，可能是 Language Server 缓存")
            print("  建议：触发 Java Language Server refresh（VSCode 命令: Java: Clean Java Language Server Workspace）")
            return 0
        else:
            print(f"  🔴 Maven 编译失败（exit {rr.returncode}）")
            print("  这是真实错误，不是 stale diagnostic，必须修复。")
            print(rr.stderr[-500:] if rr.stderr else rr.stdout[-500:])
            return 1
    else:
        print("  ℹ 非 Maven 项目，跳过编译验证。")
        return 0

def main():
    p = argparse.ArgumentParser(description="SonarQube 硬门禁适配器")
    sub = p.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("problems"); s1.add_argument("root"); s1.add_argument("--json", action="store_true"); s1.add_argument("--file", help="仅报告指定文件（相对 root）"); s1.set_defaults(fn=cmd_problems)
    s2 = sub.add_parser("improve"); s2.add_argument("root"); s2.set_defaults(fn=cmd_improve)
    s3 = sub.add_parser("hook"); s3.add_argument("root"); s3.add_argument("--staged", action="store_true"); s3.set_defaults(fn=cmd_hook)
    s4 = sub.add_parser("install-hook"); s4.add_argument("repo"); s4.set_defaults(fn=cmd_install_hook)
    s5 = sub.add_parser("sonar-plan"); s5.add_argument("root"); s5.add_argument("file"); s5.set_defaults(fn=cmd_sonar_plan)
    s6 = sub.add_parser("snapshot"); s6.add_argument("root"); s6.set_defaults(fn=cmd_snapshot)
    s7 = sub.add_parser("diff"); s7.add_argument("root"); s7.set_defaults(fn=cmd_diff)
    s8 = sub.add_parser("queue"); s8.add_argument("root"); s8.set_defaults(fn=cmd_queue)
    s9 = sub.add_parser("impact"); s9.add_argument("root"); s9.set_defaults(fn=cmd_impact)
    s10 = sub.add_parser("report"); s10.add_argument("root"); s10.set_defaults(fn=cmd_report)
    s11 = sub.add_parser("verify-stale"); s11.add_argument("root"); s11.add_argument("file"); s11.set_defaults(fn=cmd_verify_stale)
    a = p.parse_args()
    sys.exit(a.fn(a) or 0)

if __name__ == "__main__":
    main()
