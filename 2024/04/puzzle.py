#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import re
import numpy as np

def open_input(input_f: str = "input") -> list[str]:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str.split("\n")


def occurences_in_str(line: str) -> int:
    xmas = re.findall("XMAS", line)
    samx = re.findall("SAMX", line)

    return len(xmas) + len(samx)


def occurences_diagonally(grid: list[str]) -> int:
    total_occurences = 0
    lines = len(grid)
    columns = len(grid[0])
    np_grid = np.array([list(e) for e in grid])
    diagonals = ["".join(np_grid.diagonal(i)) for i in range(lines-1, -columns, -1)]
    reversed_grid = np.array([list(e[::-1]) for e in grid])
    diagonals.extend(["".join(reversed_grid.diagonal(i)) for i in range(lines-1, -columns, -1)])

    for e in diagonals:
        total_occurences += occurences_in_str(e)
    return total_occurences


def solve_puzzle_1(grid: list[str]) -> int:
    """Solves puzzle 1"""
    total_occurences = 0
    for line in grid:  # lines
        total_occurences += occurences_in_str(line)
    for i in range(len(grid[0])):  # columns
        column = "".join([grid[j][i] for j in range(len(grid))])
        total_occurences += occurences_in_str(column)
    total_occurences += occurences_diagonally(grid)
    return total_occurences

def solve_puzzle_2(grid: list[str]) -> int:
    """Solves puzzle 2"""
    def condition_word_1(x: int, y: int) -> bool:
        return (grid[x][y] == "M" and grid[x+2][y+2] == "S") or \
            (grid[x][y] == "S" and grid[x+2][y+2] == "M")

    def condition_word_2(x: int, y: int) -> bool:
        return (grid[x+2][y] == "M" and grid[x][y+2] == "S") or \
            (grid[x+2][y] == "S" and grid[x][y+2] == "M")

    total_occurences = 0
    for i in range(len(grid)-2):
        for j in range(len(grid[0])-2):
            if grid[i+1][j+1] == "A" and condition_word_1(i, j) and condition_word_2(i, j):
                total_occurences += 1
    return total_occurences

puzzle_input = open_input()
puzzle_input.pop(-1)
print(solve_puzzle_1(puzzle_input))
print(solve_puzzle_2(puzzle_input))

