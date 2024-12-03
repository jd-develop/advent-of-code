#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> list[str]:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str.split("\n")


def parse(puzzle_input: list[str]) -> tuple[list[int], list[int]]:
    """Parse the input into two lists : the left one and the right one"""
    first_list: list[int] = []
    second_list: list[int] = []

    for i in puzzle_input:
        if i == "":
            continue

        numbers = i.split()
        first_list.append(int(numbers[0]))
        second_list.append(int(numbers[-1]))

    return first_list, second_list


def solve_puzzle_1(list1: list[int], list2: list[int]) -> int:
    """Solves puzzle 1"""
    diff_list: list[int] = []
    list1.sort()
    list2.sort()

    while len(list1) != 0:
        diff_list.append(
            abs(list1.pop(0)-list2.pop(0))
        )

    return sum(diff_list)

def solve_puzzle_2(list1: list[int], list2: list[int]) -> int:
    """Solves puzzle 2"""
    occurences: dict[int, int] = {e: 0 for e in list1+list2}
    for e in list2:
        occurences[e] += 1

    return sum(e*occurences[e] for e in list1)

puzzle_input = open_input()
print(solve_puzzle_1(*parse(puzzle_input)))
print(solve_puzzle_2(*parse(puzzle_input)))

