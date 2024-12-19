#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import functools


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[str], list[str]]:
    """Returns the list of available towels and the list of wanted patterns"""
    input_list = puzzle_input.splitlines()

    towels = input_list[0].split(", ")
    patterns: list[str] = []
    for line in input_list[1:]:
        if line == "": continue
        patterns.append(line)

    return towels, patterns


def is_possible(towels: list[str], pattern: str) -> bool:
    if pattern in towels: return True
    if pattern == "": return False

    for i in range(len(pattern)):
        if pattern[:i] not in towels: continue
        if not is_possible(towels, pattern[i:]): continue
        return True

    return False


def solve_puzzle1(towels: list[str], patterns: list[str]) -> int:
    """Solves puzzle 1"""
    doable = 0
    for pattern in patterns:
        doable += is_possible(towels, pattern)
    return doable


puzzle_input = open_input()
towels, patterns = parse(puzzle_input)


@functools.cache
def all_possibilities(pattern: str) -> int:
    if pattern == "": return 0

    result: int = 0
    if pattern in towels:
        result += 1
    for t in towels:
        if pattern.startswith(t):
            result += all_possibilities(pattern[len(t):])

    return result


def solve_puzzle2(patterns: list[str]) -> int:
    """Solves puzzle 2"""
    total = 0
    for pattern in patterns:
        possibilities = all_possibilities(pattern)
        total += possibilities
    return total


print(solve_puzzle1(towels, patterns))
print(solve_puzzle2(patterns))

