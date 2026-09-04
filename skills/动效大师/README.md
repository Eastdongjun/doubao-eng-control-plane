# Motion Grandmaster / 动效大师

[![Validate](https://github.com/qlhouseClub/motion-grandmaster/actions/workflows/validate.yml/badge.svg)](https://github.com/qlhouseClub/motion-grandmaster/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/qlhouseClub/motion-grandmaster?display_name=tag)](https://github.com/qlhouseClub/motion-grandmaster/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个把审美判断、时间构图、物理感、品牌人格、交互动效、动态叙事和生产实现连接起来的动效技能包。它不从动画库或潮流名称出发，而先判断为什么动、如何动、什么必须保持静止，以及这种运动为什么只属于当前项目。

## 最近更新

### [v0.2.0](https://github.com/qlhouseClub/motion-grandmaster/releases/tag/v0.2.0) — 2026-07-30

- 建立开源动效库注册表：Motion、Anime.js、React Spring、AutoAnimate 和 SVG.js 为默认候选，ManimGL 为辅助路线。
- 为 Motion Primitives、Lucide Animated、dotLottie、Rive、Lenis、Three.js / React Three Fiber、Motion Canvas 和 React Native Reanimated 定义条件触发边界。
- 加入最小依赖、单一实现所有者、帧循环协调、版本与许可证核验、资产权利、降级和性能验收规则。
- 默认禁止 Emoji 修饰；图标优先复用批准图标集，新增图标以项目一致的 SVG 语法为主。

### v0.1.0 — 2026-07-28

- 初始版本，建立 Motion Thesis、时间构图、物理材质、交互动效、品牌签名、Motion Token 和生产验证主链路。

## 核心能力

- 客户动态审美发现、参考调研和趋势谱系分析
- Motion Thesis、审美拨盘、动态人格和静止规则
- 节奏、停顿、重音、交叠、错位、密度和时间层级
- 重量、惯性、弹性、阻尼、粘性、光学与空间连续性
- 交互动效、手势、状态反馈、加载、错误与恢复
- 产品 Signature Moment 与品牌动态识别
- 动态排版、镜头、剪辑、声音和触觉
- Motion Token、组件动效模式和治理
- CSS / Web Animations、Motion、Anime.js、React Spring、AutoAnimate、SVG.js 等默认生产路由
- ManimGL 辅助路线，以及 dotLottie、Rive、Lenis、Three.js / React Three Fiber、Motion Canvas、React Native Reanimated 等条件路线
- 开源动效库选型、组合所有权、依赖获取、版本许可与资产权利治理
- reduced motion、前庭安全、性能预算和运行验证

## 审美决策不是附录

动效大师会先建立动态审美命题，再选择技术。高视觉项目需要从具体参考和反例中提取节奏、材质、镜头、字体、声音与情绪机制；完整应用则把注意力当作有限预算，把表达集中在真正定义品牌或帮助理解的时刻。

高要求方向通过十项 Aesthetic Jury 裁决：必要性、特异性、时间构图、物理一致性、连续性、情绪精度、记忆点、克制、系统适配和生产真实性。技术复杂不等于审美优秀。

## 重要默认值

- 静止也是动效决策
- 高频操作默认安静、直接、快速；稀有且重要的时刻才获得更强表达
- 共用 Motion Token、组件行为和全局动效默认只读
- 默认禁止使用 Emoji 进行修饰、标记或充当界面图标；只有用户对当前项目明确提出要求时才放行
- 图标优先复用已批准的图标集；需要新增时以 SVG 为主，并在同一项目中统一来源、网格、描边或填充、线宽、端点、转角、光学尺寸、颜色与动效语言
- Liquid Glass 只是材料假设之一，不是默认风格
- 趋势必须研究其谱系、机制、饱和度和过期风险
- reduced motion 不是简单删除一切，而是保留状态、因果与层级
- 故事板证明构图，Animatic 证明节奏，交互原型证明实时行为，运行分析证明生产可行
- 动效库只负责实现，不负责决定审美；先复用现有技术栈，再为每个行为选择一个主要所有者
- 默认核心库是 Motion、Anime.js、React Spring、AutoAnimate 和 SVG.js，但“默认核心”不等于默认安装

## 内置开源动效库注册表

| 分层 | 选型 | 用途 |
|---|---|---|
| 默认核心 | M1 Motion | 通用组件、布局、手势与滚动关联动效 |
| 默认核心 | M2 Anime.js | 框架无关的 DOM、SVG、对象和时间线编排 |
| 默认核心 | M3 React Spring | React 中连续、可中断、状态趋向型的物理运动 |
| 默认核心 | M4 AutoAnimate | 简单的增删、排序与布局变化 |
| 默认核心 | M11 SVG.js | 自定义 SVG 构造、几何与矢量动效 |
| 辅助 | M16 ManimGL | 数学、数据、系统与算法解释视频 |
| 条件触发 | Motion Primitives、Lucide Animated、dotLottie、Rive、Lenis、Three.js / React Three Fiber、Motion Canvas、React Native Reanimated | 仅在项目技术栈、行为目标和运行约束明确匹配时引入 |

技能不会一次性安装这些库。Agent 必须先检查项目框架、包管理器、锁文件、已有依赖、设计规范和 Motion Token，再验证官方仓库、当前包名、版本兼容性与许可证；每个元素、属性、状态周期和动画帧循环只允许一个主要实现所有者。

完整的选型边界、组合规则与依赖获取协议见 [开源动效库注册表](references/open-source-motion-library-registry.md)。

## 跨平台安装

仓库适配 Codex / ChatGPT、TRAE Work、Hermes、OpenClaw 和扣子。以下命令假设公开仓库地址为 `qlhouseClub/motion-grandmaster`。

### Codex / ChatGPT 桌面端

Windows：

```powershell
$skillDir = "$env:USERPROFILE\.codex\skills\motion-grandmaster"
New-Item -ItemType Directory -Force (Split-Path $skillDir) | Out-Null
git clone https://github.com/qlhouseClub/motion-grandmaster.git $skillDir
```

macOS / Linux：

```bash
skill_dir="$HOME/.codex/skills/motion-grandmaster"
mkdir -p "$(dirname "$skill_dir")"
git clone https://github.com/qlhouseClub/motion-grandmaster.git "$skill_dir"
```

### ChatGPT Work / OpenAI Plugin

```powershell
git clone https://github.com/qlhouseClub/motion-grandmaster.git
Set-Location .\motion-grandmaster
python .\scripts\build_compat.py --platform openai
codex.cmd plugin marketplace add .\dist\openai-marketplace
```

macOS / Linux：

```bash
codex plugin marketplace add ./dist/openai-marketplace
```

### TRAE Work / SOLO / IDE

```powershell
python .\scripts\build_compat.py --platform trae
```

上传 `dist/trae/motion-grandmaster.zip`，或复制完整目录到：

```text
<项目>/.trae/skills/motion-grandmaster/
```

Windows 全局目录通常为 `%USERPROFILE%/.trae-cn/skills/motion-grandmaster/`。导入后确认 `references/` 与 `assets/` 未丢失。

### Hermes Agent

```powershell
git clone https://github.com/qlhouseClub/motion-grandmaster.git "$env:USERPROFILE\.hermes\skills\motion-grandmaster"
```

macOS / Linux：

```bash
git clone https://github.com/qlhouseClub/motion-grandmaster.git "$HOME/.hermes/skills/motion-grandmaster"
```

也可以生成 `dist/portable/motion-grandmaster.zip` 后解压到 `~/.hermes/skills/`。

### OpenClaw

```text
openclaw skills install git:qlhouseClub/motion-grandmaster@main
```

全局安装：

```text
openclaw skills install git:qlhouseClub/motion-grandmaster@main --global
```

### 扣子 / Coze

```powershell
python .\scripts\build_compat.py --platform coze
```

把 `dist/coze/motion-grandmaster/agent-prompt.md` 粘贴到系统提示词，并把 `knowledge/` 中全部 Markdown 上传到知识库。

### 一次生成所有平台包

```powershell
python .\scripts\build_compat.py --platform all
```

平台边界和维护规则见 [COMPATIBILITY.md](COMPATIBILITY.md)。

## 使用示例

- “先研究我们的动态审美，再给品牌网站提出三条真正不同的 Motion Thesis。”
- “为这个高频后台定义克制的交互动效，不要让视觉表现拖慢操作。”
- “研究当前动态排版和玻璃材质趋势，提取机制，不要套一个热门滤镜。”
- “为首次生成成功设计一个 Signature Moment，并同时给出 reduced-motion 版本。”
- “审查这套动效的节奏、物理一致性、Motion Token、性能和中间帧。”
- “把故事板转成可交付的时间、曲线、镜头、资产和运行验收规范。”

## 目录

```text
motion-grandmaster/
├─ SKILL.md
├─ agents/openai.yaml
├─ references/
├─ assets/
├─ platforms/
├─ scripts/build_compat.py
├─ COMPATIBILITY.md
└─ THIRD_PARTY_NOTICES.md
```

专业能力只在 `SKILL.md` 与 `references/` 维护；`dist/` 是可重建产物。

## 许可

- [MIT License](LICENSE)
- [第三方来源与权利边界](THIRD_PARTY_NOTICES.md)
- [贡献指南](CONTRIBUTING.md)
- [安全策略](SECURITY.md)
