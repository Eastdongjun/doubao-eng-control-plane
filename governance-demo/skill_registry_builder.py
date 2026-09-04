#!/usr/bin/env python3
"""技能协同注册构建器：全量扫描 .user_skills，为每个技能生成注册条目。
含能力分组(conflict 消解)、12 阶段映射(routing)、风险分级(destructive/cost)。
用法:
  python3 skill_registry_builder.py build     # 全量重建 registry
  python3 skill_registry_builder.py check     # schema 校验
  python3 skill_registry_builder.py query     # 列出全部
  python3 skill_registry_builder.py chain     # 打印一条 12 阶段协同链路示例
"""
import argparse, datetime, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
USER_SKILLS = pathlib.Path("/Users/donglai/Library/Application Support/Doubao/Default/.doubao/agent_mode/workspace/.user_skills")
REG = ROOT / ".governance" / "capability_registry.json"

# ---------- 阶段映射（技能名关键词 → 阶段号）----------
STAGE_KEYWORDS = {
    1:  ["想法打磨", "需求盘问", "史诗设计", "头脑风暴"],
    2:  ["需求", "规格驱动", "功能分析", "需求盘问", "文档盘问"],
    3:  ["ui设计", "交互设计", "原型", "设计工程", "设计专家", "苹果设计"],
    4:  ["架构师", "架构评审", "架构绘图", "权衡分析", "集成设计", "微服务", "技术栈评估",
         "迁移架构", "rag架构", "事件驱动", "aws", "azure", "gcp", "架构决策", "企业架构"],
    5:  ["api", "sql", "数据库", "数据建模", "错误处理", "领域建模", "严格api", "契约"],
    6:  ["git工作树", "cicd", "流水线", "测试策略", "脚手架", "测试驱动开发", "数据库优化"],
    7:  ["后端", "前端", "全栈", "零幻觉", "代码库", "代码导览", "单仓", "合并冲突", "react",
         "rn移动", "swift", "编码", "开发", "自动编码", "规格驱动"],
    8:  ["qa", "playwright", "browserstack", "testrail", "性能", "质量门禁", "测试用例追踪",
         "网页测试", "测试台", "技能测试", "集成测试", "回归"],
    9:  ["上线发布", "发布管理", "发布门禁", "就绪", "运维手册", "回滚", "备份", "功能开关", "运维助手"],
    10: ["发布门禁", "功能开关", "完成前验证", "变更日志", "发布"],
    11: ["可观测", "slo", "事故", "监控", "运维助手", "容量", "云成本", "告警", "数据库优化"],
    12: ["弃用", "迁移", "技术债", "退役", "路线图", "迭代"],
}
DESTRUCTIVE_KW = ["执行", "写入", "删除", "部署", "发布", "回滚", "修改", "编辑", "运行", "操作", "提交", "合并", "推送", "替换", "覆盖", "爬"]
COST_KW = {
    "H": ["架构", "渗透", "红队", "部署", "发布", "全栈", "完整", "企业", "平台", "系统", "深度"],
}
PHASE_NAMES = {1:"立项",2:"需求",3:"设计",4:"架构",5:"详细设计",6:"开发准备",7:"编码",8:"测试",9:"上线准备",10:"发布",11:"运维",12:"迭代退役"}

# 冲突消解分组：同组技能按描述区分触发对象，避免 AI 选错
CONFLICT_GROUPS = {
    "代码审查族": ["代码审查", "pr审查专家", "具名角色对抗审查", "对抗审查", "api设计审查", "依赖审计", "pr审查专家"],
    "测试族": ["网页测试", "Playwright专业", "性能测试", "测试驱动开发", "测试用例追踪", "智能体测试台"],
    "安全族": ["AI安全", "云安全", "渗透测试", "红队", "威胁检测", "owasp安全", "安全测试", "安全设计"],
    "架构族": ["高级架构师", "架构评审引导", "权衡分析", "技术栈评估", "架构绘图"],
    "数据库族": ["数据库设计", "数据库表结构设计", "SQL数据库助手", "数据库优化", "数据建模", "数据质量审计"],
}
# 每个分组的"场景路由提示"
GROUP_ROUTING = {
    "代码审查族": "本地改动→代码审查；PR/diff→pr审查专家；方案多视角→具名角色对抗审查；接口→api设计审查；依赖→依赖审计",
    "测试族": "网页端→网页测试；端到端浏览器→Playwright专业；性能→性能测试；TDD→测试驱动开发；测试资产管理→测试用例追踪",
    "安全族": "AI应用→AI安全；云设施→云安全；主动攻击模拟→渗透测试/红队；持续监测→威胁检测；Web→owasp安全",
    "架构族": "整体方案→高级架构师；评审已有→架构评审引导；选型取舍→权衡分析；技术盘点→技术栈评估",
    "数据库族": "结构设计→数据库设计；物理表→数据库表结构设计；调优→数据库优化；质量→数据质量审计",
}

# 权威映射覆盖：关键词映射漏网的技能（未映射补齐 / 贯穿型标记）
OVERRIDE = {
    # 贯穿型（不属单一阶段，全程参与）
    "工程化总控": "贯穿", "任务追踪": "贯穿", "可信执行治理": "贯穿", "任务分解": "贯穿",
    "执行计划": "贯穿", "编写计划": "贯穿", "工作流构建": "贯穿", "技能医生": "贯穿",
    "技能安全审计": "贯穿", "自评": "贯穿", "评审反馈处理": "贯穿", "协作证明": "贯穿",
    "文档与决策记录": "贯穿", "任务交接": "贯穿", "上下文工程": "贯穿", "提示词治理": "贯穿",
    "大模型成本优化": "贯穿", "记忆工程": "贯穿", "环境密钥管理": "贯穿", "密钥保险库": "贯穿",
    "算法艺术": "贯穿",
    # 安全族
    "ai安全": [4, 8], "owasp安全": [4, 8], "安全测试": [8], "安全设计": [4],
    "认证与授权": [4, 5], "威胁检测": [8, 11], "云安全": [4, 11], "渗透测试": [8],
    "红队": [8, 11], "默认漏洞检测": [8], "无障碍审计": [8], "合规与隐私": [4],
    # 部署/运维
    "k8s专家": [9, 10], "容器化": [9], "基础设施即代码": [9, 10], "高级devops": [9, 10, 11],
    "高级安全": [8, 11], "高级安全运营": [8, 11],
    # 编码/审查
    "代码审查": [7, 8], "pr审查专家": [7, 8], "对抗审查": [4, 7], "具名角色对抗审查": [4, 7],
    "差异审查": [7], "依赖审计": [5, 8], "数据质量审计": [5], "分支收尾": [7],
    "增量实现": [7], "遗留系统改造": [7, 12], "适应度函数": [7], "测试实现": [7, 8],
    "系统化调试": [7, 11], "危险边缘识别": [4, 7],
    # 设计/前端
    "design-grandmaster": [3], "interaction-design-expert": [3], "motion-grandmaster": [3],
    "product-expert": [2, 3, 4], "sonner提示库": [3], "网页设计规范": [3],
    "动画构建": [3], "动画构建expo": [3], "动画词汇表": [3], "动效改进": [3],
    "动效审查": [3], "寻找动画机会": [3], "面试系统设计": [4, 7],
    # AI/Agent
    "智能体设计": [4, 7], "智能体工作流设计": [4, 7], "智能体记忆": [4, 7], "大模型知识库": [4, 7],
    "高级提示词工程": [2, 7], "缓存与搜索": [5, 7],
    # 数据/算法
    "高级数据工程师": [5, 8], "高级数据科学家": [5, 8], "高级机器学习": [4, 5],
    "高级计算机视觉": [4, 5], "统计分析": [8],
    # 工具/接口
    "mcp服务构建": [5, 7], "stripe集成专家": [9, 10], "通用爬虫架构": [4, 7],
    "嵌入式物联网顾问": [4, 7], "浏览器自动化": [8], "整页截图": [8], "演示视频": [8],
    "混沌工程": [8, 11], "交互向导": [9, 10], "人工闸门": [9, 10], "变更影响分析": [2, 12],
    "架构沟通": [4], "架构风险评估": [4], "敏捷v生命周期": [12], "方案拷问": [2, 4],
    "书籍转技能": [7], "邮件模板": [2], "智能体测试台": [8], "技能测试": [8],
    "技术文档": [5, 12],
}

def scan_skills():
    """扫描 .user_skills，返回技能条目列表"""
    items = []
    if not USER_SKILLS.is_dir():
        print(f"✗ 技能目录不存在: {USER_SKILLS}"); sys.exit(1)
    for d in sorted(p for p in USER_SKILLS.iterdir() if p.is_dir() and not p.name.startswith(".")):
        fm = d / "SKILL.md"
        if not fm.exists(): continue
        t = fm.read_text(encoding="utf-8", errors="replace")
        name = d.name
        m = re.search(r"(?m)^description:\s*(.+)$", t)
        desc = (m.group(1).strip().strip('"') if m else "")
        # 阶段映射（先查权威覆盖表，再按技能名关键词）
        stages = []
        if name in OVERRIDE:
            ov = OVERRIDE[name]
            stages = [] if ov == "贯穿" else ov
        else:
            for s, kws in STAGE_KEYWORDS.items():
                if any(kw.lower() in name.lower() for kw in kws):
                    stages.append(s)
        stages = sorted(set(stages))
        # 风险分级
        destructive = any(kw in name for kw in DESTRUCTIVE_KW)
        cost = "M"
        for lv, kws in COST_KW.items():
            if any(kw in name for kw in kws): cost = lv
        # 冲突分组
        group = None
        for g, members in CONFLICT_GROUPS.items():
            if name in members:
                group = g; break
        items.append({
            "id": name, "type": "skill", "name": name,
            "description": desc,
            "destructive": destructive, "failure_mode": "执行失败需检查产物",
            "cost": cost, "status": "active",
            "stage": stages, "stage_label": ",".join(PHASE_NAMES[s] for s in stages),
            "group": group,
            "routing": GROUP_ROUTING.get(group, ""),
        })
    return items

def build():
    tools = []  # MCP 工具由 capability_registry.py 的 TOOLS 维护，这里不重复
    skills = scan_skills()
    reg = {
        "_meta": {
            "version": "2.0", "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
            "schema": "skill/工具统一注册：id/type/name/description/destructive/failure_mode/cost/status/stage/group/routing",
            "source": str(USER_SKILLS),
            "total": len(skills),
        },
        "tools": tools,
        "skills": skills,
        "conflict_groups": {g: {"members": ms, "routing": GROUP_ROUTING.get(g)} for g, ms in CONFLICT_GROUPS.items()},
    }
    REG.parent.mkdir(parents=True, exist_ok=True)
    REG.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    grp = {}
    for s in skills:
        if s["group"]: grp[s["group"]] = grp.get(s["group"], 0) + 1
    print(f"✓ 已注册 {len(skills)} 个技能 → {REG.relative_to(ROOT)}")
    print(f"  冲突分组: {json.dumps(grp, ensure_ascii=False)}")
    print(f"  阶段覆盖: " + " | ".join(f"{PHASE_NAMES[s]}:{sum(1 for x in skills if s in x['stage'])}" for s in range(1,13)))

def check():
    if not REG.exists(): print("✗ 先 build"); return 1
    data = json.loads(REG.read_text(encoding="utf-8"))
    errs = []
    for it in data["skills"]:
        for f in ("id","type","name","description","destructive","failure_mode","cost","status","stage"):
            if f not in it: errs.append(f"{it.get('id')} 缺 {f}")
        if it["cost"] not in ("L","M","H"): errs.append(f"{it['id']} cost 非法")
    print(f"✓ schema 校验通过，{len(data['skills'])} 个技能全部合法" if not errs else f"✗ {len(errs)} 处错误")
    [print("  "+e) for e in errs[:20]]
    return 0 if not errs else 1

def query():
    data = json.loads(REG.read_text(encoding="utf-8"))
    grp = {}
    for s in data["skills"]:
        g = s["group"] or "未分组"
        grp.setdefault(g, []).append(s["name"])
    for g, lst in sorted(grp.items(), key=lambda x: -len(x[1])):
        print(f"[{g}] ({len(lst)})")
        print("   " + "、".join(lst))
    print(f"\n技能总数: {len(data['skills'])}")

def chain():
    """打印一条 12 阶段协同链路示例（证明编排闭环）"""
    data = json.loads(REG.read_text(encoding="utf-8"))
    by_stage = {}
    for s in data["skills"]:
        for st in s["stage"]:
            by_stage.setdefault(st, []).append(s["name"])
    print("=== 12 阶段协同链路（技能→产物→下一阶段输入）===")
    links = {
        1: ("项目立项", "项目概念/目标/风险清单", "需求输入"),
        2: ("需求工程", "需求规格/验收标准", "功能/原型输入"),
        3: ("产品交互", "原型/UI稿/状态图", "页面结构输入"),
        4: ("架构设计", "架构图/选型/ADR", "技术边界"),
        5: ("详细设计", "API文档/数据模型/错误码", "接口契约"),
        6: ("开发准备", "脚手架/CI/测试基线", "工程基线"),
        7: ("编码开发", "功能代码/单测/脚本", "可运行产物"),
        8: ("测试质量", "测试报告/缺陷清单", "质量证据"),
        9: ("上线准备", "上线方案/回滚/检查表", "发布审批"),
        10:("发布上线", "发布记录/验证记录", "线上版本"),
        11:("运行维护", "监控/事故复盘/SLA", "运行指标"),
        12:("迭代退役", "路线图/技术债/退役方案", "新需求回流"),
    }
    for st in range(1, 13):
        name, out, to_next = links[st]
        sk = by_stage.get(st, [])
        shown = "、".join(sk[:5]) + ("…" if len(sk) > 5 else "")
        print(f" 阶段{st:>2} {name:<5} ← 技能: {shown or '（默认编排）'}")
        print(f"       → 产物: {out}  |  交接: {to_next}")
    print("\n贯穿技能: 工程化总控(编排) + 任务追踪(trace) + 可信执行治理(分级/审计/回滚) + 需求追踪矩阵(追踪链)")

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for c, fn in [("build", build), ("check", check), ("query", query), ("chain", chain)]:
        s = sub.add_parser(c); s.set_defaults(fn=fn)
    a = p.parse_args()
    sys.exit(a.fn() or 0)

if __name__ == "__main__":
    main()
