#!/usr/bin/env python3
"""日志统计与清理工具

功能：
  1. 扫描指定目录下的 .log 文件，统计每个文件的行数并降序输出；
  2. 支持按文件修改时间清理超过 N 天的 .log（配合 --delete 才真正删除，否则只预览）；
  3. 目录不存在或参数非法时给出友好中文提示，不抛原始堆栈。

用法：
  python3 logclean.py [目录] [--max-old 天数] [--delete]
  示例：
  python3 logclean.py logs                 # 只统计
  python3 logclean.py logs --max-old 30    # 预览 30 天前的日志（不删除）
  python3 logclean.py logs --max-old 30 --delete   # 真正删除 30 天前的日志
"""
import argparse
import os
import sys
import time


def scan_logs(directory):
    """扫描目录下的 .log 文件，返回完整路径列表。

    边界处理：目录不存在、不是目录、无权限时返回空列表并打印原因，
    避免调用方因 FileNotFoundError / NotADirectoryError 崩溃。
    """
    if not os.path.exists(directory):
        print(f"错误：目录不存在：{directory}", file=sys.stderr)
        return []
    if not os.path.isdir(directory):
        print(f"错误：不是目录：{directory}", file=sys.stderr)
        return []
    try:
        names = os.listdir(directory)
    except PermissionError:
        print(f"错误：没有权限读取目录：{directory}", file=sys.stderr)
        return []
    return [os.path.join(directory, n) for n in names if n.endswith(".log")]


def count_lines(path):
    """统计单个文件的行数（空文件返回 0）。"""
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def list_expired(paths, max_old_days):
    """筛出修改时间早于 max_old_days 天的日志文件。"""
    now = time.time()
    cutoff = now - max_old_days * 86400
    return [p for p in paths if os.path.getmtime(p) < cutoff]


def main():
    # 参数解析：目录 + 可选清理参数
    parser = argparse.ArgumentParser(description="日志统计与清理工具")
    parser.add_argument("directory", nargs="?", default="logs", help="日志目录（默认 logs）")
    parser.add_argument("--max-old", type=int, default=0, help="清理 N 天前的日志")
    parser.add_argument("--delete", action="store_true", help="真正删除（默认仅预览）")
    args = parser.parse_args()

    # 参数合法性校验：天数必须为正整数
    if args.max_old < 0:
        print("错误：--max-old 必须是非负整数", file=sys.stderr)
        sys.exit(2)

    logs = scan_logs(args.directory)

    # 统计部分：行数降序输出
    stats = [(os.path.basename(p), count_lines(p)) for p in logs]
    stats.sort(key=lambda x: x[1], reverse=True)
    total = sum(n for _, n in stats)
    print(f"共 {len(stats)} 个 .log 文件，总行数 {total}")
    for name, n in stats:
        print(f"  {n:>6} 行  {name}")

    # 清理部分：仅当显式给出 --max-old 时才启用
    if args.max_old > 0:
        expired = list_expired(logs, args.max_old)
        if not expired:
            print(f"没有超过 {args.max_old} 天的日志，无需清理")
        else:
            print(f"\n以下 {len(expired)} 个文件超过 {args.max_old} 天：")
            for p in expired:
                action = "删除" if args.delete else "（预览，未删除）"
                print(f"  [{action}] {os.path.basename(p)}")
            if args.delete:
                for p in expired:
                    os.remove(p)
                print(f"已删除 {len(expired)} 个文件")


if __name__ == "__main__":
    main()
