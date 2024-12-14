#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[tuple[int, int, int, int]]:
    """Parses the input into a list of robots"""
    res: list[tuple[int, int, int, int]] = []
    lines = puzzle_input.splitlines()
    for line in lines:
        if line == "": continue
        line = line.split(" ")
        x, y = tuple(map(int, line[0][2:].split(",")))
        vx, vy = tuple(map(int, line[1][2:].split(",")))
        res.append((x, y, vx, vy))
    return res


def print_grid(bounds: tuple[int, int], new_positions: list[tuple[int, int]], seconds: int):
    #founds_lines: list[int] = []
    #for j in range(bounds[1]):
    #    found_in_a_row = 0
    #    last_row = -1
    #    for i in range(bounds[0]):
    #        if (i, j) not in new_positions: continue
    #        if last_row+1 == i:
    #            last_row += 1
    #            found_in_a_row += 1
    #        else:
    #            found_in_a_row = 0
    #    founds_lines.append(found_in_a_row)
    #if max(founds_lines) <= 5:
    #    return
    if len(set(new_positions)) < len(new_positions):
        return False

    print(seconds)
    for j in range(bounds[1]):
        for i in range(bounds[0]):
            count = new_positions.count((i, j))
            print("#" if count != 0 else ".", end="")
        print()
    return True


def solve_puzzle1(robots: list[tuple[int, int, int, int]],
                  bounds: tuple[int, int] = (101, 103),
                  seconds: int = 100, verbose: bool = False) -> int:
    """Solves puzzle 1."""
    new_positions: list[tuple[int, int]] = []
    for robot in robots:
        x, y, vx, vy = robot
        x += seconds*vx
        y += seconds*vy
        x %= bounds[0]
        y %= bounds[1]
        new_positions.append((x, y))

    if verbose:
        return int(print_grid(bounds, new_positions, seconds))

    quadrants_x = bounds[0] // 2
    quadrants_y = bounds[1] // 2

    quadrant_1 = 0
    for i in range(quadrants_x):
        for j in range(quadrants_y):
            quadrant_1 += new_positions.count((i, j))

    quadrant_2 = 0
    for i in range(bounds[0] - quadrants_x, bounds[0]):
        for j in range(quadrants_y):
            quadrant_2 += new_positions.count((i, j))

    quadrant_3 = 0
    for i in range(quadrants_x):
        for j in range(bounds[1] - quadrants_y, bounds[1]):
            quadrant_3 += new_positions.count((i, j))

    quadrant_4 = 0
    for i in range(bounds[0] - quadrants_x, bounds[0]):
        for j in range(bounds[1] - quadrants_y, bounds[1]):
            quadrant_4 += new_positions.count((i, j))

    # print(quadrant_1, quadrant_2, quadrant_3, quadrant_4)
    return quadrant_1*quadrant_2*quadrant_3*quadrant_4


#def solve_puzzle2(files: list[tuple[int, int]]) -> int:
#    """Solves puzzle 2."""


puzzle_input = open_input()
parsed_input = parse(puzzle_input)

print(solve_puzzle1(parsed_input))
for s in range(10000):
    if solve_puzzle1(parsed_input, seconds=s, verbose=True):
        break
#print(solve_puzzle2(parsed_input))

