#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[tuple[int, list[int]]]:
    """Parses the input"""
    parsed: list[tuple[int, list[int]]] = []
    for line in puzzle_input.split("\n"):
        if line == "": continue

        line = line.split(": ")
        aim = int(line[0])
        available_numbers = list(map(int, line[1].split()))
        parsed.append((aim, available_numbers))
    return parsed


def solve_puzzle(parsed_input: list[tuple[int, list[int]]], concatenation: bool = False) -> int:
    """Solves puzzle. Set concatenation to True to solve puzzle 2"""
    result = 0
    for aim, available_numbers in parsed_input:
        possible_results: list[int] = []
        for num in available_numbers:
            if len(possible_results) == 0:
                possible_results.append(num)
                continue
            new_possible_results: list[int] = \
                [e + num for e in possible_results] + \
                [e * num for e in possible_results]
            if concatenation:
                new_possible_results.extend(
                    [int(str(e)+str(num)) for e in possible_results]
                )
            possible_results = new_possible_results
        if aim in possible_results:
            result += aim
    return result


puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle(parsed_input))
print(solve_puzzle(parsed_input, True))

