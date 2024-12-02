#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> list[str]:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str.split("\n")


def parse(puzzle_input: list[str]) -> list[list[int]]:
    """Parse the input into a 2-dimentional array"""
    result: list[list[int]] = []

    for i in puzzle_input:
        if i == "":
            continue

        report = i.split()
        result.append([int(level) for level in report])

    return result


def is_sorted_increasingly(report: list[int]) -> bool:
    """Returns true if the report is sorted increasingly AND any two adjacents
       levels differ by at least one and at most three"""
    for i, level in enumerate(report):
        if i == 0:
            continue

        if level < report[i-1]:
            return False
        if not (1 <= level-report[i-1] <= 3):
            return False
    return True

assert(is_sorted_increasingly([1, 2, 4, 6, 7]))
assert(not is_sorted_increasingly([1, 2, 4, 6, 10]))
assert(not is_sorted_increasingly([1, 2, 4, 6, 5]))


def is_sorted_decreasingly(report: list[int]) -> bool:
    """Returns true if the report is sorted decreasingly AND any two adjacents
       levels differ by at least one and at most three"""
    for i, level in enumerate(report):
        if i == 0:
            continue

        if level > report[i-1]:
            return False
        if not (1 <= report[i-1]-level <= 3):
            return False
    return True


def solve_puzzle_1(reports: list[list[int]]) -> int:
    """Solves puzzle 1"""
    safe_reports = 0

    for report in reports:
        if is_sorted_increasingly(report) or is_sorted_decreasingly(report):
            safe_reports += 1

    return safe_reports

def solve_puzzle_2(reports: list[list[int]]) -> int:
    """Solves puzzle 2"""
    safe_reports = 0

    for report in reports:
        if is_sorted_increasingly(report) or is_sorted_decreasingly(report):
            safe_reports += 1
            continue
        for i in range(len(report)):
            # we just check without one of the elements
            new_report = report[:i] + report[(i+1):]
            if is_sorted_increasingly(new_report) or is_sorted_decreasingly(new_report):
                safe_reports += 1
                break

    return safe_reports

puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle_1(parsed_input))
print(solve_puzzle_2(parsed_input))

