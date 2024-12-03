#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    """Parse the input into tuples of ints to multiply"""
    result1: list[tuple[int, int]] = []
    result2: list[tuple[int, int]] = []

    do_the_next_one = True

    x = re.findall("mul\\([0-9]+,[0-9]+\\)|do\\(\\)|don\'t\\(\\)", puzzle_input)
    for y in x:
        if y == "do()":
            do_the_next_one = True
        elif y == "don't()":
            do_the_next_one = False
        else:
            int1, int2 = tuple(map(int, y[4:][:-1].split(",")))
            if do_the_next_one:
                result2.append((
                    int(int1), int(int2)
                ))
            result1.append((
                int(int1), int(int2)
            ))

    return result1, result2


def solve_puzzle(memory: list[tuple[int, int]]) -> int:
    """Solves puzzle"""
    return sum(a*b for a, b in memory)


puzzle_input = open_input()
parsed_input1, parsed_input2 = parse(puzzle_input)
print(solve_puzzle(parsed_input1))
print(solve_puzzle(parsed_input2))

