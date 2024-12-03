#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Parse the input into tuples of ints to multiply"""
    result1: list[tuple[int, int]] = []
    result2: list[tuple[int, int]] = []

    current = ""
    do_the_next_one = True

    # that’s what happen when you’re too lazy to think to better solutions
    for char in puzzle_input:
        if char == "m":
            current = "m"
        elif char == "u" and current == "m":
            current += "u"
        elif char == "l" and current == "mu":
            current += "l"
        elif char == "(" and current == "mul":
            current += "("
        elif char in "1234567890" and current.startswith("mul("):
            current += char
        elif char == "," and current.startswith("mul(") and "," not in current:
            current += char
        elif char == ")" and current.startswith("mul(") and "," in current:
            current = current[4:].split(",")
            try:
                if do_the_next_one:
                    result2.append((
                        int(current[0]), int(current[1])
                    ))
                result1.append((
                    int(current[0]), int(current[1])
                ))
            except Exception:
                pass
            current = ""
        elif char == "d":
            current = "d"
        elif char == "o" and current == "d":
            current += "o"
        elif char == "n" and current == "do":
            current += "n"
        elif char == "'" and current == "don":
            current += "'"
        elif char == "t" and current == "don'":
            current += "t"
        elif char == "(" and current in ["do", "don't"]:
            current += "("
        elif char == ")" and current in ["do(", "don't("]:
            do_the_next_one = current == "do("
            current = ""
        else:
            current = ""

    return result1, result2


def solve_puzzle(memory: list[tuple[int, int]]) -> int:
    """Solves puzzle"""
    return sum(a*b for a, b in memory)


puzzle_input = open_input()
parsed_input1, parsed_input2 = parse(puzzle_input)
print(solve_puzzle(parsed_input1))
print(solve_puzzle(parsed_input2))

