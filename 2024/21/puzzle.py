#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import itertools
import functools


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[str]:
    return puzzle_input.splitlines()


def tile_to_coord(tile: str, door_code: bool) -> tuple[int, int]:
    return {
        "A": (3, 2),
        "0": (3, 1),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2)
    }[tile] if door_code else {
        "A": (0, 2),
        "^": (0, 1),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2)
    }[tile]


def all_movement_possibilities(startx: int, starty: int, endx: int, endy: int, gap: tuple[int, int]):
    diffx = endx - startx
    diffy = endy - starty
    possibility = ""
    if diffx < 0:
        possibility += -diffx*"^"
    else:
        possibility += diffx*"v"
    if diffy < 0:
        possibility += -diffy*"<"
    else:
        possibility += diffy*">"

    all_possibilities = itertools.permutations(possibility, len(possibility))

    real_possibilities: list[str] = []
    for p in all_possibilities:
        px, py = startx, starty
        gap_found = False
        for c in p:
            if c == "<": py -= 1
            elif c == ">": py += 1
            elif c == "^": px -= 1
            elif c == "v": px += 1
            if (px, py) == gap:
                gap_found = True
                break
        if gap_found: continue
        real_possibilities.append("".join(p))

    if len(real_possibilities) == 0:
        return ["A"]
    return [res+"A" for res in real_possibilities]


@functools.cache
def min_len(code: str, robot: int, number_of_robots: int, door_code: bool) -> int:
    current_pos = tile_to_coord("A", door_code)
    gap = (3, 0) if door_code else (0, 0)
    lenght = 0
    for char in code:
        target_pos = tile_to_coord(char, door_code)
        all_moves = all_movement_possibilities(*current_pos, *target_pos, gap)
        if robot == number_of_robots:
            lenght += len(min(all_moves, key=len))
        else:
            new_min_lenght = -1
            for move in all_moves:
                cur_len = min_len(move, robot+1, number_of_robots, False)
                if new_min_lenght == -1 or cur_len < new_min_lenght:
                    new_min_lenght = cur_len
            assert new_min_lenght != -1
            lenght += new_min_lenght
        current_pos = target_pos
    return lenght


def solve_puzzle1(codes: list[str], part2: bool = False) -> int:
    """Solves puzzle 1"""
    result = 0
    for code in codes:
        result += min_len(code, 0, 2+part2*23, True)*int(code[:-1])
    return result


puzzle_input = open_input()
parsed_input = parse(puzzle_input)

print(solve_puzzle1(parsed_input))
print(solve_puzzle1(parsed_input, True))

