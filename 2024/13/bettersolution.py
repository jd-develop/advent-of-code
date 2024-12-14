#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# this solution is not the one I used to submit my answers – just a better
# rewrite


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[tuple[(int, int, int, int, int, int)]]:  # A(x), A(y), B(x), B(y), P(x), P(y)
    """parses the input"""
    res: list[tuple[(int, int, int, int, int, int)]] = []
    for machine in puzzle_input.split("\n\n"):
        machine = machine.split("\n")

        a = machine[0].split(", ")
        a_x = int(a[0][12:])
        a_y = int(a[1][2:])

        b = machine[1].split(", ")
        b_x = int(b[0][12:])
        b_y = int(b[1][2:])

        p = machine[2].split(", ")
        p_x = int(p[0][9:])
        p_y = int(p[1][2:])

        res.append((a_x, a_y, b_x, b_y, p_x, p_y))
    return res


def solve_puzzle1(machines: list[tuple[(int, int, int, int, int, int)]], part2: bool = False) -> int:
    """Solves puzzle 1."""
    total = 0
    for ax, ay, bx, by, px, py in machines:
        if part2:
            px += 10000000000000
            py += 10000000000000
        det = ax*by - bx*ay
        assert det != 0
        det_x = px*by-bx*py
        det_y = ax*py-px*ay

        # we only want integer solutions
        if (det_x%det != 0): continue
        if (det_y%det != 0): continue

        times_a = det_x//det
        times_b = det_y//det

        total += 3*times_a + times_b

    return total


puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle1(parsed_input))
print(solve_puzzle1(parsed_input, True))

