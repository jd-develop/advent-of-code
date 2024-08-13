#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# from pprint import pprint

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()

if input_list[-1] == "\n":
    input_list = input_list[:-1]

input_list = [list(r[:-1]) if r.endswith("\n") else list(r) for r in input_list]


def step(only_terrain: list[list[str]], previous_step: list[list[str]]):
    """Perform one step"""
    output = [[t for t in r] for r in only_terrain]
    for i, line in enumerate(previous_step):
        for j, char in enumerate(line):
            if char in "OS":
                for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    try:
                        if previous_step[i+x][j+y] not in "OS#":
                            output[i+x][j+y] = "O"
                    except IndexError:
                        pass
    return output


def steps(puzzle_input: list[list[str]], steps: int):
    """Perform `steps` steps"""
    only_terrain = [[t.replace("S", ".") for t in row] for row in puzzle_input]
    # pprint(only_terrain)
    current_list = puzzle_input
    for _ in range(steps):
        current_list = step(only_terrain, current_list)
        # pprint(only_terrain)
        # pprint(["".join(r) for r in current_list])
    return sum(current_list[j].count("O") for j in range(len(current_list)))


print(steps(input_list, 64))
