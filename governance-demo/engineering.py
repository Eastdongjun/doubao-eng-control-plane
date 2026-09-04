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
import argparse, ast, json, pathlib, re, subprocess, sys

SEV_ERROR, SEV_WARNING = "ERROR", "WARNING"
DEFAULT_COMPLEXITY = 15
DEFAULT_PARAMS = 7
DEFAULT_DUP = 3
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
        "diagnostics": [p.to_dict() for p in problems],
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
# 阻断规则: Error>0 / 未豁免 Warning>0 / 桥不可用 → 禁止 commit（仅检查本次暂存代码，增量）
ENG="{pathlib.Path(__file__).resolve()}"
ROOT="{repo.resolve()}"
if [ ! -f "$ENG" ]; then
  echo "🔴 BLOCKED: engineering 桥不可用（$ENG 缺失），禁止提交。请先恢复工程化工具链。"
  exit 1
fi
"${{PYTHON:-python3}}" "$ENG" hook "$ROOT" --staged || exit 1
exit 0
"""
    hook.write_text(script, encoding="utf-8")
    hook.chmod(0o755)
    print(f"✓ pre-commit hook 已安装: {hook}")
    return 0

def main():
    p = argparse.ArgumentParser(description="SonarQube 硬门禁适配器")
    sub = p.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("problems"); s1.add_argument("root"); s1.add_argument("--json", action="store_true"); s1.set_defaults(fn=cmd_problems)
    s2 = sub.add_parser("improve"); s2.add_argument("root"); s2.set_defaults(fn=cmd_improve)
    s3 = sub.add_parser("hook"); s3.add_argument("root"); s3.add_argument("--staged", action="store_true"); s3.set_defaults(fn=cmd_hook)
    s4 = sub.add_parser("install-hook"); s4.add_argument("repo"); s4.set_defaults(fn=cmd_install_hook)
    a = p.parse_args()
    sys.exit(a.fn(a) or 0)

if __name__ == "__main__":
    main()
