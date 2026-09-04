#!/usr/bin/env python3
"""简易命令行计算器：支持加、减、乘、除"""

import sys


def add(a, b):
    # 加法
    return a + b


def sub(a, b):
    # 减法
    return a - b


def mul(a, b):
    # 乘法
    return a * b


def div(a, b):
    # 除法（含除零保护）
    if b == 0:
        return "错误：除数不能为 0"
    return a / b


def main():
    # 用法：python3 calculator.py 10 + 5
    if len(sys.argv) != 4:
        print("用法：python3 calculator.py <数字> <运算符> <数字>")
        return
    a = float(sys.argv[1])
    op = sys.argv[2]
    b = float(sys.argv[3])
    # 根据运算符分发
    ops = {"+": add, "-": sub, "*": mul, "/": div}
    if op in ops:
        print(f"{a} {op} {b} = {ops[op](a, b)}")
    else:
        print(f"不支持的运算符：{op}")


if __name__ == "__main__":
    main()
