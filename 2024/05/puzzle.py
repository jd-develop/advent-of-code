#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> list[str]:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str.split("\n")


def parse(puzzle_input: list[str]) -> tuple[dict[int, list[int]], list[list[int]]]:
    rules: dict[int, list[int]] = {}
    updates: list[list[int]] = []

    currently = "rules"
    for i in puzzle_input:
        if i == "":
            currently = "updates"
            continue

        if currently == "rules":
            rule = i.split("|")
            a, b = tuple(map(int, rule))
            if a not in rules:
                rules[a] = []
            rules[a].append(b)
        else:
            update = i.split(",")
            updates.append(list(map(int, update)))

    return rules, updates


def is_line_valid(line: list[int], rules: dict[int, list[int]]) -> bool:
    for i, n in enumerate(line):
        for j in range(i+1, len(line)):
            if line[j] not in rules:
                continue
            if n in rules[line[j]]:  # i should be after j
                return False
    return True


def solve_puzzle_1(rules: dict[int, list[int]], updates: list[list[int]]) -> int:
    """Solves puzzle 1"""
    total = 0
    for line in updates:
        if not is_line_valid(line, rules):
            continue
        total += line[len(line)//2]
    return total


def sort_line(line: list[int], rules: dict[int, list[int]]) -> list[int]:
    result: list[int] = []
    # I guess there’s a better alogorithm – but it’s 6:30 AM…
    for n in line:
        n_should_be_printed_before = rules[n] if n in rules else []
        n_should_be_printed_after = [j for j in rules.keys() if n in rules[j]]
        i = 0
        for r in result:
            if r in n_should_be_printed_before:
                break
            elif r in n_should_be_printed_after:
                i += 1
        result.insert(i, n)

    return result


def solve_puzzle_2(rules: dict[int, list[int]], updates: list[list[int]]) -> int:
    """Solves puzzle 2"""
    total = 0
    for line in updates:
        if is_line_valid(line, rules):
            continue
        sorted_line = sort_line(line, rules)
        total += sorted_line[len(sorted_line)//2]
    return total

puzzle_input = open_input()
rules, updates = parse(puzzle_input)
print(solve_puzzle_1(rules, updates))
print(solve_puzzle_2(rules, updates))

