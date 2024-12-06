#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> list[str]:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str.split("\n")


def solve_puzzle_1(map_: list[str]) -> int:
    """Solves puzzle 1. Returns -1 if a loop is detected"""
    guard_position = (-1, -1)
    facing = "nowhere"
    for (i, line) in enumerate(map_):
        if "^" in line:
            guard_position = (i, line.index("^"))
            facing = "up"
            break
        elif ">" in line:
            guard_position = (i, line.index(">"))
            facing = "right"
            break
        elif "<" in line:
            guard_position = (i, line.index("<"))
            facing = "left"
            break
        elif "v" in line:
            guard_position = (i, line.index("v"))
            facing = "down"
            break
    assert guard_position != (-1, -1)
    assert facing != "nowhere"

    visited_tiles: list[list[list[str]]] = [[[] for _ in map_[0]] for _ in map_]
    while True:
        if facing in visited_tiles[guard_position[0]][guard_position[1]]:
            return -1
        visited_tiles[guard_position[0]][guard_position[1]].append(facing)
        if facing == "right":
            next_position = (guard_position[0], guard_position[1]+1)
        elif facing == "left":
            next_position = (guard_position[0], guard_position[1]-1)
        elif facing == "down":
            next_position = (guard_position[0]+1, guard_position[1])
        else:
            next_position = (guard_position[0]-1, guard_position[1])

        if next_position[0] < 0 or next_position[0] >= len(map_):
            break
        elif next_position[1] < 0 or next_position[1] >= len(map_[0]):
            break

        if map_[next_position[0]][next_position[1]] == "#":
            if facing == "right":
                facing = "down"
            elif facing == "down":
                facing = "left"
            elif facing == "left":
                facing = "up"
            else:
                facing = "right"
            continue

        guard_position = next_position

    count = 0
    for line in visited_tiles:
        for tile in line:
            count += 1 if len(tile) != 0 else 0

    return count

def solve_puzzle_2(map_: list[str]) -> int:
    """Solves puzzle 2"""
    # yay, bruteforce!
    total_other_solutions = 0
    for (i, line) in enumerate(map_):
        for (j, tile) in enumerate(line):
            if tile in "^><v#":
                continue
            print(i, j)
            new_map = map_.copy()
            new_line = list(line)
            new_line[j] = "#"
            new_map[i] = "".join(new_line)
            if solve_puzzle_1(new_map) == -1:
                total_other_solutions += 1
    return total_other_solutions


puzzle_input = open_input()
for i in range(len(puzzle_input)):
    if puzzle_input[i] == "":
        puzzle_input.pop(i)

print(solve_puzzle_1(puzzle_input))
print(solve_puzzle_2(puzzle_input))

