#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[list[int]]:
    """Parses the input into a nice 2D list"""
    res: list[list[int]] = []
    for (i, line) in enumerate(puzzle_input.split("\n")):
        if line == "": continue
        res.append([])
        for c in line:
            if c == ".":
                res[i].append(-1)
                continue
            res[i].append(int(c))
    return res


def find_hiking_trails(map_: list[list[int]], i: int, j: int, next_tile: int = 1) -> list[tuple[int, int]]:
    if next_tile == 10:
        return [(i, j)]
    score: list[tuple[int, int]] = []
    if 0 <= i-1 < len(map_):
        # up: i-1, j
        if map_[i-1][j] == next_tile:
            score.extend(find_hiking_trails(map_, i-1, j, next_tile+1))
    if 0 <= i+1 < len(map_):
        # down: i+1, j
        if map_[i+1][j] == next_tile:
            score.extend(find_hiking_trails(map_, i+1, j, next_tile+1))
    if 0 <= j-1 < len(map_[0]):
        # left: i, j-1
        if map_[i][j-1] == next_tile:
            score.extend(find_hiking_trails(map_, i, j-1, next_tile+1))
    if 0 <= j+1 < len(map_[0]):
        # right: i, j+1
        if map_[i][j+1] == next_tile:
            score.extend(find_hiking_trails(map_, i, j+1, next_tile+1))
    return score


def solve_puzzle(map_: list[list[int]], part2: bool = False) -> int:
    """Solves puzzle"""
    total_scores = 0
    for i, line in enumerate(map_):
        for j, tile in enumerate(line):
            if tile != 0: continue
            all_9 = find_hiking_trails(map_, i, j)
            if not part2:  # I actually accidentally did part2 before part1 so this was trivially easy to implement
                all_9 = set(all_9)  # to remove duplicates
            total_scores += len(all_9)
    return total_scores


puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle(parsed_input))
print(solve_puzzle(parsed_input, True))

