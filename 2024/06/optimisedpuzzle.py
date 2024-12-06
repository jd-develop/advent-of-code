#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> list[str]:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str.split("\n")


def solve_puzzle_1(map_: list[str], new_obstacle: tuple[int, int],
                   guard_position: tuple[int, int], facing: int) -> tuple[int, list[list[int]]]:
    """Solves puzzle 1. Returns -1 if a loop is detected"""

    visited_tiles: list[list[set[int]]] = [[set() for _ in map_[0]] for _ in map_]
    visited_tiles_first_time: list[list[int]] = [[-1 for _ in map_[0]] for _ in map_]
    do_not_append_next = False
    next_position: tuple[int, int]

    count = 0
    while True:
        if facing in visited_tiles[guard_position[0]][guard_position[1]]:
            return -1, []

        if not do_not_append_next:
            visited_tiles[guard_position[0]][guard_position[1]].add(facing)

            if visited_tiles_first_time[guard_position[0]][guard_position[1]] == -1:
                visited_tiles_first_time[guard_position[0]][guard_position[1]] = facing
                count += 1
        else:
            do_not_append_next = False

        # instead of if/elif/elif/else, just do some maths
        next_position = (guard_position[0] + (2-facing)*(facing%2),
                         guard_position[1] + (1-facing)*(1-facing%2))

        if next_position[0] < 0 or next_position[0] >= len(map_):
            break
        elif next_position[1] < 0 or next_position[1] >= len(map_[0]):
            break

        if map_[next_position[0]][next_position[1]] == "#" or (next_position[0], next_position[1]) == new_obstacle:
            facing += 1
            facing %= 4
            do_not_append_next = True
            continue

        guard_position = next_position

    return count, visited_tiles_first_time

def solve_puzzle_2(map_: list[str], visited_tiles: list[list[int]]) -> int:
    """Solves puzzle 2"""
    # yay, bruteforce!
    total_other_solutions = 0
    visited_tiles_bool = [[tile != -1 for tile in line] for line in visited_tiles]
    for (i, line) in enumerate(map_):
        for (j, tile) in enumerate(line):
            if not visited_tiles_bool[i][j] or tile in "^#":
                continue
            facing = visited_tiles[i][j]
            if facing == 3:
                new_guard_pos = (i+1, j)
            elif facing == 1:
                new_guard_pos = (i-1, j)
            elif facing == 0:
                new_guard_pos = (i, j-1)
            else:
                new_guard_pos = (i, j+1)
            if solve_puzzle_1(map_, (i, j), new_guard_pos, facing)[0] == -1:
                total_other_solutions += 1
    return total_other_solutions


puzzle_input = open_input()
for i in range(len(puzzle_input)):
    if puzzle_input[i] == "":
        puzzle_input.pop(i)

guard_position = (-1, -1)
facing = -1
for (i, line) in enumerate(puzzle_input):
    if "^" in line:
        guard_position = (i, line.index("^"))
        facing = 3
        break
    elif ">" in line:
        guard_position = (i, line.index(">"))
        facing = 0
        break
    elif "<" in line:
        guard_position = (i, line.index("<"))
        facing = 2
        break
    elif "v" in line:
        guard_position = (i, line.index("v"))
        facing = 1
        break
assert guard_position != (-1, -1)
assert facing != -1

sol1, visited_tiles = solve_puzzle_1(puzzle_input, (-1, -1), guard_position, facing)
print(sol1)
print(solve_puzzle_2(puzzle_input, visited_tiles))

