#!/usr/bin/env python3
"""西安古城景点查询工具：查询西安知名古迹与景点信息"""

# 内置西安古城景点数据（名称、年代、类型、简介）
SIGHTS = [
    {"name": "钟楼", "era": "明代", "type": "古建筑", "desc": "西安中心地标，明代钟楼，晨钟报时"},
    {"name": "鼓楼", "era": "明代", "type": "古建筑", "desc": "与钟楼相望，鼓楼暮鼓报时"},
    {"name": "西安城墙", "era": "明代", "type": "古城墙", "desc": "中国现存最完整的古代城垣，可骑行游览"},
    {"name": "大雁塔", "era": "唐代", "type": "佛塔", "desc": "玄奘译经之地，唐代著名佛塔"},
    {"name": "小雁塔", "era": "唐代", "type": "佛塔", "desc": "荐福寺内，唐代密檐式砖塔"},
    {"name": "回民街", "era": "清代", "type": "街区", "desc": "西安著名美食街，回坊风情"},
    {"name": "兵马俑", "era": "秦代", "type": "遗址", "desc": "秦始皇陵陪葬坑，世界第八大奇迹"},
    {"name": "华清池", "era": "唐代", "type": "园林", "desc": "唐代皇家温泉行宫，杨贵妃沐浴之地"},
]


def list_all():
    # 列出全部景点
    print(f"西安古城共有 {len(SIGHTS)} 处知名景点：")
    for i, s in enumerate(SIGHTS, 1):
        print(f"{i}. {s['name']}（{s['era']}·{s['type']}）：{s['desc']}")


def search(keyword):
    # 按关键字搜索景点名称或简介
    hits = [s for s in SIGHTS if keyword in s["name"] or keyword in s["desc"]]
    if not hits:
        print(f"未找到与「{keyword}」相关的景点")
        return
    print(f"搜索「{keyword}」共 {len(hits)} 个结果：")
    for s in hits:
        print(f"  - {s['name']}（{s['era']}·{s['type']}）：{s['desc']}")


def main():
    # 用法：python3 xian_guide.py [搜索关键字]
    import sys
    if len(sys.argv) < 2:
        # 无参数时列出全部景点
        list_all()
        return
    # 有参数时按关键字搜索
    search(sys.argv[1])


if __name__ == "__main__":
    main()
