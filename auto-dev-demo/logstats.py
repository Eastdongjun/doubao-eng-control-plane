#!/usr/bin/env python3
"""日志统计工具：统计日志文件行数与关键字出现次数"""

import sys


def count_lines(path):
    # 统计文件行数
    with open(path) as f:
        return len(f.readlines())


def count_keyword(lines, keyword):
    # 统计关键字出现次数
    total = 0
    for line in lines:
        if keyword in line:
            total += 1
    return total


def main():
    # 用法：python3 logstats.py <日志文件> <关键字>
    if len(sys.argv) < 3:
        print("用法：python3 logstats.py <日志文件> <关键字>")
        return
    path = sys.argv[1]
    keyword = sys.argv[2]
    try:
        lines = open(path, encoding="utf-8").readlines()
    except FileNotFoundError:
        # 文件不存在时给出友好提示，避免程序崩溃
        print(f"错误：日志文件不存在：{path}")
        return
    print(f"文件 {path} 共 {count_lines(path)} 行")
    print(f"关键字 '{keyword}' 出现 {count_keyword(lines, keyword)} 次")


if __name__ == "__main__":
    main()
