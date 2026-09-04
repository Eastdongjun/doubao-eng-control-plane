# Design Grandmaster

[![Validate](https://github.com/qlhouseClub/design-grandmaster/actions/workflows/validate.yml/badge.svg)](https://github.com/qlhouseClub/design-grandmaster/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/qlhouseClub/design-grandmaster?display_name=tag)](https://github.com/qlhouseClub/design-grandmaster/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

面向高要求产品与视觉项目的设计宗师技能包。它同时处理业务目标、用户体验、设计规范、Design Token、品牌表达、审美判断、历史与当代视觉研究、交互、情绪体验、无障碍和工程交付。

它不会把“好看”简化成流行风格，也不会为了视觉表现破坏已有设计系统。

## 最近更新

### v2.0.0 — 2026-08-28

- 将本轮 P0、P1、P2 能力合并为首个 v2 正式版本，不再以内部迭代批次充当公开版本号。
- 新增通用环境与依赖授权协议：缺少运行时、浏览器、Python/Node 包、系统库、可执行文件或权限时，工具输出结构化 `authorization_required`；Agent 必须说明用途、范围、命令、影响、替代方案和复验计划，再向用户请求授权。
- 边界几何审查覆盖 Node.js、Playwright、浏览器内核和系统库缺失；截图回归缺少 Pillow、YAML 输入缺少 PyYAML 时也使用同一授权契约，不再只报错或静默降级。未经授权不会安装依赖，用户拒绝或暂缓后才允许使用明确标记 `unproven` 的降级方案。
- Playwright 授权闭环已经真实验证：缺失检测、用户授权、技能本地安装、模块解析、现有 Chrome 启动和多视口几何审查均可执行，不伪造通过结果。
- 完成混排与空间秩序 fixture、布局指纹与灰阶剪影检查、渐进加载清单、视觉定位图完整性、浏览器边界审查、跨行业回归目录、截图差异信号、趋势证据校验和内容寻址研究缓存。
- 新增 `REGRESSION_CATALOG`、`TREND_EVIDENCE`、`LOADING_MANIFEST`、`DEPENDENCY_AUTHORIZATION` 等模板，并将模板、脚本和契约纳入 Codex/ChatGPT、TRAE、扣子、Hermes 与 OpenClaw 兼容包。
- 新增可执行的任务能力路由：根据任务模式、业务风险、视觉 stakes、规范权威和交付形态生成必需能力、条件能力、最小产物与阻断门禁，解决过度加载和能力漏载。
- 新增审美决策记录与业务加权评估：候选方向必须记录证据、不可补偿门、拒绝理由、置信度和复审条件，避免用流行标签代替业务适配。
- 新增调研覆盖校验、设计权威快照、代码视觉值审计、SVG 资产 lint 和模式化交付门禁；没有证据的方向只能标记为 `unproven`。
- 新增执行契约、任务/权威/审美/来源/资产模板；设计宗师本体不内置主题、示例页面或任何 Emoji 图形。
- 发布前通过 14 项执行契约测试、Ruff、Python/Node 语法检查、元数据与四平台归档验证；代码语言治理为 0 错误/0 警告，代码工艺治理无错误。

### v1.6.0 — 2026-08-13

- 新增中英文字、数字、标点与 SVG 图标的混排基线治理：先识别实际字体回退、字面度量、数字样式、标点和可见边界，再允许有归属的光学校正，禁止散落偏移修补。
- 新增文字编排、图文混排和创意构图方法：将蒙版、裁切、定位、重叠和伪元素划分为语义、交互、结构、装饰四类图层，并要求碰撞边界、移动端转化、无障碍顺序和降级方案。
- 用“结构 → 排版与节奏 → 表达与光学 QA”三轮收敛替代无边界调试；同类问题重复出现时回到责任层，超过四轮必须输出根因记录。
- 新增批次化视觉定位图：页面区块使用稳定语义锚点，交付时生成 `VLM-{批次}-{页面}-{区块}-{序号}` 修改点索引，支持局部修改引用和变更日志。
- 新增渐进式加载判定文档：分别治理技能知识按需加载，以及页面代码、数据、媒体和交互状态的渐进加载，输出优先级、稳定占位、无障碍、失败恢复与降级裁决。

### v1.5.0 — 2026-08-04

- 新增外部主题接入与适配流程：主题必须由用户提供、明确选择、批准为参考，或经调研完成适配裁决，不会成为设计宗师的新默认审美。
- 设计宗师不再内置主题、主题资产或示例页面；主题作为独立依赖维护，技能只负责来源、版本、权利、适配性、Token 映射和验证治理。
- [`DawnVision Editorial`](https://github.com/qlhouseClub/dawnvision-editorial) 已拆分为独立主题项目，设计宗师通过外部主题协议使用它，不再随技能及跨平台兼容包分发。

### v1.4.0 — 2026-08-03

- 新增非装饰性贴边治理：文字、信息图像、功能图标、控件、焦点、数据与状态提示必须落在明确的视口、区块、组件和滚动安全区内。
- 新增可执行的浏览器几何审查：检测文档横向溢出、区域内边界、半截文字/图标裁切、横向滚动首尾、粘性区域和滚动轴串扰，并输出可复核的 JSON 证据。
- 建立双端边界安全门：桌面、断点两侧、目标移动端与 320px 窄屏按实际 Token 或保守基线审查；背景、分隔线和纯装饰出血与有效内容分开裁决。
- 将本次简历实战的修复逻辑抽象为通用流程：定位责任容器、恢复授权内边距、重组滚动区域、隔离滚动轴、重新测量和视觉复核。

### [v1.3.0](https://github.com/qlhouseClub/design-grandmaster/releases/tag/v1.3.0) — 2026-08-03

- 新增审美权威状态：没有既有规范、用户参考或可信调研时，自动发起与项目风险相称的同类、邻近领域和反参考调研，不再让 Agent 的惯用审美接管项目。
- 新增版式语法与新鲜度治理：从画布、网格、视觉体量、阅读顺序、密度、信息单元、边界和移动端重构分析布局，不把“近期流行”写成固定模板。
- 新增灰阶剪影竞争和版式指纹：最终配色与表面处理前先比较结构真正不同的方案，并检查左右分栏首屏、数据条、卡片矩阵、深浅区块交替等复合模板收敛。
- 增强移动端重新编排、普通状态证明和跨行业回归场景；深色荧光技术风、玻璃、超大留白等均不得在无证据时成为默认答案。

### [v1.2.0](https://github.com/qlhouseClub/design-grandmaster/releases/tag/v1.2.0) — 2026-07-30

- 新增视觉语言承袭流程：建立规范快照、寻找高频共性、划分表达值权重，并审计改版中的设计漂移。
- 加强品牌、UI、UX 三视角的文字排版与布局，包括字号层级、混排、对齐、块间距、行间距、字间距和视觉舒适度。
- 加强代码视觉值审计；共享 Design Token 默认只读，未经授权不得创建近似值、替代规范或新的全局设计语言。
- 默认禁止 Emoji 修饰；图标优先复用批准图标集，新增图标以项目一致的 SVG 语法为主。

### [v1.1.0](https://github.com/qlhouseClub/design-grandmaster/releases/tag/v1.1.0) — 2026-07-23

- 完善审美发现、历史与潮流研究、视觉工艺、真实资产、方向证明、跨平台安装和运行验证。

## 核心能力

- 既有设计规范与组件库的严格遵循
- Design Token 治理、映射和一致性审计
- 改版中的视觉语言承袭、样式共性提取、表达权重与代码视觉值审计
- 品牌、UI、UX 三视角的文字排版、混排、对齐、间距与布局控制
- 中英数字标点及 SVG 混排基线、真实字体回退与空间节奏治理
- 文字编排、图文混排、蒙版、定位、裁切、伪元素和响应式创意构图
- 批次化视觉定位图、稳定页面区块语义锚点与局部修改日志
- 技能知识与界面资源的渐进式加载判定
- 双端安全区、非装饰性贴边、横向溢出、滚动裁切与粘性区域审查
- 客户审美发现、参考与反参考分析
- 无规范场景下的自动同类调研、版式语法、灰阶剪影竞争与反收敛指纹
- 高级审美判断、视觉命题与设计裁决
- 历史、文化、材料和视觉潮流的研究与数字化转译
- 真实品牌资产、方向可视证明、决策留痕与运行验证
- 配色拓扑、留白与焦点几何、动效连续性和表达性交互
- 原子化设计、品牌、字体、色彩、排版、图像与动效
- 信息架构、用户流程、状态、交互和认知负荷
- 情绪体验、心理机制与用户自主性
- 响应式、国际化、无障碍与包容性设计
- 原型验证、设计批评、交付标注和实现 QA
- 外部主题接入、主题适配裁决与跨项目语义映射
- 混排与空间秩序回归 fixture、布局指纹和灰阶剪影验证
- 渐进式加载清单、视觉定位图完整性与浏览器边界审查接线
- 跨行业视觉回归目录、截图差异信号、趋势证据和研究缓存

## 核心原则

1. 用具体视觉证据了解客户审美，而不是依赖“高级、现代、有质感”等形容词。
2. 对历史、文化、陌生风格和当前潮流先研究再转译。
3. 先明确受众、任务、情绪和品牌意义，再选择视觉语言。
4. 完整应用优先解决业务、信息、流程、状态和可用性；纯视觉项目允许投入更深的审美研究。
5. 已批准的设计规范具有约束力，共享 Design Token 未经明确授权不得更改。
6. 原子化设计是组合模型，不是机械的文件夹分类法。
7. 趋势是一种视觉谱系，不是可以直接套用的皮肤。
8. 情绪设计必须服务于理解、信任和用户自主性。
9. 重要视觉决策必须用代表性成品证明，不能只让客户从文字风格标签中选择。
10. 灵感来源必须转成可解释、可测试的机制，而不是复制某位设计师或某张作品。
11. 改版授权不等于新建设计系统；必须先区分批准规则、稳定共性、局部表达和既有漂移。
12. 代码中的色彩、字体、间距、表面、图标和动效值必须映射到批准角色或已记录例外。
13. 没有视觉权威时先调研再定稿；重要版式必须先通过灰阶剪影、版式指纹和移动端重构验证。
14. 有效信息和操作必须处于明确安全区；只有经设计意图确认的装饰层或结构层可以贴边、裁切或出血。
15. 外部主题是可选视觉语法，不是默认皮肤；技能不捆绑主题或样例，主题必须服从项目已有规范，并用签名场景与普通状态共同证明。
16. 混排先治理真实字体、字面度量、数字和图标角色，再进行有边界的光学校正；不允许用散落偏移掩盖系统问题。
17. 创意排版必须保留语义顺序和交互可用性；蒙版、定位和伪元素只能在明确图层、责任容器、碰撞边界和响应式规则下使用。
18. 可运行页面交付必须具备可引用的语义区块和当前任务批次视觉定位图；局部修改仍须遵守组件和 Token 权威。

## 规范遵循

当项目已有设计系统时，技能默认采用：

```text
复用现有组件
→ 组合现有能力
→ 使用被允许的局部变体
→ 提出系统扩展建议
→ 获得授权后才修改共享规则
```

间距、字号、色彩、圆角、阴影和动效等数值必须解析到获准的 Token 或明确记录的技术例外。若间距体系提供 `12 / 16 / 20 / 24`，则 `15 / 21 / 23` 不会被视为“微调”，而是规范违例。

## 自适应工作路径

- **完整产品或应用：** 业务与体验优先，只在品牌关键节点进行必要的视觉研究。
- **品牌、文化、编辑、展览或旗舰视觉项目：** 深入进行客户审美发现、视觉语料研究和设计方向竞争。
- **既有设计系统项目：** 首先锁定规范版本、权威来源和 Token，不允许无授权漂移。
- **趋势项目：** 研究趋势的来源、机制、当前状态和过期风险，再决定是否以及如何使用。
- **可运行视觉产物：** 先做最小但真实的方向证明，再逐步扩展，并在目标运行环境中检查渲染、交互、响应式和异常状态。
- **多端、粘性或横向滚动界面：** 运行边界几何审查，并用截图复核非装饰内容的视口、区块、组件和裁切安全区。
- **无规范、无参考的视觉任务：** 自动建立同类、邻近领域和反参考证据场；完成结构不同的灰阶剪影和版式指纹后才进入最终视觉。
- **用户指定外部主题：** 核验主题来源、版本、权利和入口，确认适配性与权威层级，将语义角色映射到项目 Token，并记录保留、调整和拒绝的机制。
- **混排、编辑或创意构图：** 读取混排与创意构图规范，以真实内容完成结构、排版节奏、表达和光学审查三轮收敛。
- **可运行页面交付或后续局部修改：** 为主要视觉区块建立稳定语义锚点，生成当前任务批次的视觉定位图并随产物交付。
- **渐进式加载任务：** 先区分技能知识加载与产品资源/数据加载，再输出与当前任务相称的判定记录。

## 目录结构

```text
design-grandmaster/
├── SKILL.md                         # 主入口、路径选择与质量门槛
├── agents/openai.yaml               # Codex 界面元数据
├── .github/workflows/               # 自动验证与版本发布
├── references/
│   ├── design-system-conformance.md
│   ├── aesthetic-discovery-research.md
│   ├── aesthetic-governor.md
│   ├── visual-trend-atlas.md
│   ├── visual-craft-grammar.md
│   ├── layout-intelligence-and-freshness.md
│   ├── mixed-script-typography-and-creative-composition.md
│   ├── visual-location-and-revision-map.md
│   ├── progressive-loading-routing.md
│   ├── experience-strategy.md
│   ├── brand-and-visual-language.md
│   ├── atomic-design-system.md
│   ├── interaction-cognition-emotion.md
│   ├── accessibility-content-inclusion.md
│   ├── responsive-motion-data.md
│   ├── layout-boundary-safety.md
│   ├── artifact-production-validation.md
│   ├── critique-prototype-handoff.md
│   ├── artifact-templates.md
│   ├── canonical-sources.md
│   └── external-theme-translation.md
├── platforms/                       # 跨平台元数据与扣子桥接提示词
├── scripts/
│   ├── build_compat.py              # 生成 TRAE、OpenAI Plugin、扣子和便携包
│   └── audit_layout_boundaries.mjs  # 浏览器几何边界与安全区审查
├── COMPATIBILITY.md                 # 跨平台安装、限制与维护规则
├── CONTRIBUTING.md                  # 贡献规则
├── SECURITY.md                      # 私密安全报告
└── LICENSE                          # MIT 许可证
```

## 跨平台安装

仓库同时适配 Codex、ChatGPT、TRAE Work、Hermes、OpenClaw 和扣子。请选择实际使用的平台；不需要把所有版本都安装一遍。

不想在本地构建时，可以直接从 [GitHub Releases](https://github.com/qlhouseClub/design-grandmaster/releases) 下载 TRAE、OpenAI Plugin、扣子或便携 ZIP。

| 平台 | 推荐安装方式 | 安装后形态 |
|---|---|---|
| Codex / ChatGPT 桌面端 | 克隆到个人技能目录 | 原生 Agent Skill |
| ChatGPT Work / 团队 | 生成并安装 Plugin | OpenAI Plugin |
| TRAE Work / SOLO / IDE | 克隆到技能目录，或上传生成的 ZIP | 原生 Skill |
| Hermes Agent | 克隆到 Hermes 技能目录 | 原生 Skill |
| OpenClaw | 使用 Git 安装命令 | 原生 Agent Skill |
| 扣子 / Coze | 生成提示词与知识库包 | 提示词 + RAG 知识库 |

### Codex / ChatGPT 桌面端

Windows PowerShell：

```powershell
$skillDir = "$env:USERPROFILE\.codex\skills\design-grandmaster"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/design-grandmaster.git $skillDir
```

macOS / Linux：

```bash
skill_dir="$HOME/.codex/skills/design-grandmaster"
mkdir -p "$(dirname "$skill_dir")"
git clone https://github.com/qlhouseClub/design-grandmaster.git "$skill_dir"
```

若希望与其他兼容 Agent 共用技能，也可以把目标根目录改为 `~/.agents/skills/`。重启或刷新客户端后，即可通过“使用设计宗师……”等自然语言触发。

### ChatGPT Work / 团队 Plugin

先克隆仓库并生成 OpenAI Plugin：

```powershell
git clone https://github.com/qlhouseClub/design-grandmaster.git
Set-Location .\design-grandmaster
python .\scripts\build_compat.py --platform openai
codex.cmd plugin marketplace add .\dist\openai-marketplace
```

macOS / Linux 最后一条命令使用：

```bash
codex plugin marketplace add ./dist/openai-marketplace
```

重启 ChatGPT 桌面端，在 Plugins 中安装“设计宗师”。需要团队使用时，可从插件详情页分享到 ChatGPT 工作区。独立插件包为 `dist/openai/design-grandmaster-plugin.zip`。

### TRAE Work / SOLO / IDE

国内版全局安装：

```powershell
$skillDir = "$env:USERPROFILE\.trae-cn\skills\design-grandmaster"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/design-grandmaster.git $skillDir
```

国际版把 `.trae-cn` 改为 `.trae`。项目级安装则克隆或复制到：

```text
<项目>/.trae/skills/design-grandmaster/
```

也可以下载 Release 中的 `design-grandmaster.zip`，在 TRAE 的“设置 → 技能与命令/规则和技能 → 创建或上传技能”中导入。自行构建命令为：

```powershell
python .\scripts\build_compat.py --platform trae
```

### Hermes Agent

将完整仓库安装到 Hermes 个人技能目录，确保 `references/` 等引用文件一并保留：

```powershell
$skillDir = "$env:USERPROFILE\.hermes\skills\design-grandmaster"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/design-grandmaster.git $skillDir
```

macOS / Linux：

```bash
skill_dir="$HOME/.hermes/skills/design-grandmaster"
mkdir -p "$(dirname "$skill_dir")"
git clone https://github.com/qlhouseClub/design-grandmaster.git "$skill_dir"
```

安装后新建会话；若希望当前会话立即刷新，可在 Hermes 中执行 `/reset`。

### OpenClaw

安装到当前工作区：

```text
openclaw skills install git:qlhouseClub/design-grandmaster@main
```

安装为所有本地 Agent 共用的全局技能：

```text
openclaw skills install git:qlhouseClub/design-grandmaster@main --global
```

从已克隆的仓库根目录安装：

```text
openclaw skills install . --as design-grandmaster
```

### 扣子 / Coze

扣子不直接读取 Agent Skill 目录。可以下载 Release 中的 `design-grandmaster-coze.zip`，或自行生成：

```powershell
git clone https://github.com/qlhouseClub/design-grandmaster.git
Set-Location .\design-grandmaster
python .\scripts\build_compat.py --platform coze
```

然后在扣子中完成以下设置：

1. 将 `dist/coze/design-grandmaster/agent-prompt.md` 粘贴到智能体系统提示词。
2. 新建知识库，上传 `dist/coze/design-grandmaster/knowledge/` 中的全部 Markdown 文件。
3. 将知识库绑定到智能体并启用检索。
4. 按需要配置联网、Figma、代码库等插件或工作流。

### 生成全部平台包

已经克隆仓库时，可以一次生成所有适配产物：

```powershell
python .\scripts\build_compat.py --platform all
```

完整的平台边界、目录说明、维护规则和官方依据见 [COMPATIBILITY.md](COMPATIBILITY.md)。

## 使用示例

- “在不改变现有 Design Token 的前提下，为这个后台增加一个审批模块。”
- “先了解我的审美，再为品牌网站提出三条不同的视觉方向。”
- “研究唐代岩彩、矿物颜料和当代数字视觉，转译成一个可读的网站系统。”
- “判断液态玻璃是否适合这个金融应用，不要为了潮流牺牲可用性。”
- “审查这套界面里的间距、字体、组件和交互是否违反设计规范。”
- “把这个视觉方案提升到具有明确作者性和品牌辨识度的水平。”
- “从这些灵感中提取配色、版式、动效和交互机制，再做一套不照搬原作的项目语法。”
- “这个版式看起来陈旧，先调研当前同类并用相同内容提出三个结构真正不同的灰阶剪影，检查是否又用了惯常模板。”
- “检查这个中英数字混排页面的基线、行距、块间距和图文关系，用三轮收敛完成，不要继续堆偏移补丁。”
- “为这次页面交付生成视觉定位图，我后面要直接引用区块编号做局部修改。”
- “判断首屏、图片、数据和交互应该如何渐进加载，并输出稳定占位、失败恢复和降级文档。”

### v2.0 执行入口

先复制 `templates/DESIGN_TASK.example.yaml` 并填写任务事实：

```powershell
python scripts/capability_router.py DESIGN_TASK.yaml --output ROUTE.json
```

按路由加载最小参考集，再使用 `references/execution-contracts.md` 中的命令完成调研覆盖、审美评估、视觉值审计、SVG 检查和交付门禁。没有代表性渲染或运行证据时，交付状态必须保持 `unproven`，不能写成“已完成”。

任何当前执行路径需要的环境或依赖缺失时，工具会写出退出码 `3` 和结构化授权请求。Agent 必须把缺失项、阻断能力、安装范围、准确命令、环境变化、风险、替代方案和安装后的复验计划展示给用户，并在得到明确授权后才执行安装。详见 [`references/dependency-authorization.md`](references/dependency-authorization.md)。

## Token 与研究策略

技能采用有判定记录的渐进式加载。普通产品设计不会自动加载完整的审美研究、趋势图谱、高级视觉裁决、创意构图或交付定位模块；只有视觉雄心、文化风险、混排/构图问题、界面加载决策或交付方式需要时才进入对应深度。完整判定见 [`references/progressive-loading-routing.md`](references/progressive-loading-routing.md)。

视觉调研以“新证据不再改变视觉语法、风险或方向空间”为停止条件，避免把无上限收集参考误认为专业。

产品交互研究优先查看真实上线流程，实验性网站与视觉作品用于拓展表达边界；两类证据不会混为一谈。高视觉方向先用代表性页面、幻灯片或关键帧证明，再进入批量生产。

## 本轮吸收与来源

本版本对 [Huashu Design](https://github.com/alchaincyf/huashu-design) 的真实资产、视觉方向证明、阶段决策与运行验证方法进行了重新设计，并保留其 [MIT 许可](https://github.com/alchaincyf/huashu-design/blob/master/LICENSE)来源说明。未吸收随机风格轮盘、模仿特定设计师、所有任务强制三稿、资产覆盖已批准规范等做法。

视觉工艺模块还基于 [Dreameryanyan 在 X 的公开策展内容](https://x.com/yanliudreamer)建立了二次研究路径，并核验了其引用的真实产品流程库 [Mobbin](https://mobbin.com/)、网页案例库 [Lapa Ninja](https://www.lapa.ninja/)、创意开发案例 [Codrops](https://tympanus.net/codrops/hub/author/the_bugged_dev/) 与开源编辑设计实验 [GC Minimal Zine Poster](https://github.com/LiamGvchi/gc-minimal-zine-poster)。技能吸收的是可迁移机制，不复制具体作品或个人风格。

## 重要默认值

- 规范优先于个人审美
- 共用 Design Token 默认只读
- 默认禁止使用 Emoji 进行修饰、标记或充当界面图标；只有用户对当前项目明确提出要求时才放行
- 图标优先复用已批准的图标集；需要新增时以 SVG 为主，并在同一项目中统一来源、网格、描边或填充、线宽、端点、转角、光学尺寸、颜色与动效语言
- 研究结论区分来源事实、直接观察、推断和设计转译
- 无障碍不是最终检查项
- 潮流不等于方向，效果不等于品味
- 高视觉要求必须形成可识别的设计命题，而不只是干净和精致
- 没有既有规范、用户方向或项目调研时，审美权威处于未解决状态，不能直接使用 Agent 的惯用配色和版式
- 最终版式需要通过结构竞争、版式指纹和移动端重新编排，配色、图片与动效不能掩盖模板化构图
- 真实品牌资产必须核验来源、版本与权利，但不能凌驾于已批准的规范
- 重要方向用同内容、同资产、同场景的可视证明进行比较
- 可运行产物必须在实际运行环境中打开、检查和验证，不能只读源文件
- 缺少必需环境或依赖时必须先发起可审计的安装或启用授权；不得自动安装、只报错结束或悄悄降级
- 混排、图文和创意版式以三轮责任分明的收敛替代无限微调；超过四轮先记录根因
- 可运行页面的主要区块使用稳定语义名称，并随批次交付视觉定位图，方便后续直接引用修改点

## 状态

- YAML 元数据校验通过
- 本地引用链接校验通过
- 已验证既有 Token 约束在跨页面输出中的持续遵循
- 已验证历史文化视觉研究与当代数字转译流程
- 已加入真实资产清单、风险分级方向 Gate、视觉工艺语法与运行验证链路
- 已生成并校验 TRAE、OpenAI Plugin、扣子和便携适配产物

## 许可、贡献与安全

- 使用条款：[MIT License](LICENSE)
- 第三方研究与许可边界：[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- 贡献方式：[CONTRIBUTING.md](CONTRIBUTING.md)
- 私密报告安全问题：[SECURITY.md](SECURITY.md)
