#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import copy


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[dict[str, int], list[tuple[str, str, str, str]]]:
    """Returns the puzzle under the form of a dict str: int (initial values) and
    a list of tuples var, op, var, dest"""
    symbol_table: dict[str, int] = {}
    operations: list[tuple[str, str, str, str]] = []

    for line in puzzle_input.splitlines():
        if line == "": continue
        line_splitted = line.split()
        if len(line_splitted) == 2:
            symbol_table[line_splitted[0][:-1]] = int(line_splitted[1])
            continue
        operations.append(
            (line_splitted[0], line_splitted[1], line_splitted[2],
             line_splitted[4])
        )
    return symbol_table, operations



def solve_puzzle1(initial_symbol_table: dict[str, int], initial_operations: list[tuple[str, str, str, str]]) -> int:
    """Solves puzzle 1"""
    symbol_table = copy.deepcopy(initial_symbol_table)
    operations = copy.deepcopy(initial_operations)
    while len(operations) != 0:
        new_operations: list[tuple[str, str, str, str]] = []
        for src1, op, src2, dst in operations:
            if src1 not in symbol_table or src2 not in symbol_table:
                new_operations.append((src1, op, src2, dst))
                continue
            bit1 = symbol_table[src1]
            bit2 = symbol_table[src2]
            assert op in ["AND", "OR", "XOR"]
            if op == "AND":
                symbol_table[dst] = int(bit1 and bit2)
            elif op == "OR":
                symbol_table[dst] = int(bit1 or bit2)
            elif op == "XOR":
                symbol_table[dst] = bit1^bit2
        operations = new_operations

    result = 0
    for i in range(100):
        if i < 10:
            var = f"z0{i}"
        else:
            var = f"z{i}"
        if var not in symbol_table:
            continue
        result += symbol_table[var]*(2**i)

    return result


def to_mermaid(initial_operations: list[tuple[str, str, str, str]]) -> str:
    res = "flowchart TD\n"

    i = 0
    for src1, op, src2, dst in initial_operations:
        res += f"    {src1} --> op{i}" + "{" + op + "}\n"
        res += f"    {src2} --> op{i}\n"
        res += f"    op{i} --> {dst}\n"
        i += 1
    return res



puzzle_input = open_input()
global_symbol_table, global_operations = parse(puzzle_input)

print(solve_puzzle1(global_symbol_table, global_operations))
print(to_mermaid(global_operations))

