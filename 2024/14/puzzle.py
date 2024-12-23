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
    if len(set(new_positions)) < len(new_positions):
        return False

    print(seconds)
    for j in range(bounds[1]):
        for i in range(bounds[0]):
            if ((i, j)) in new_positions:
                print("#", end="")
            else:
                print(".", end="")
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
    quadrant_2 = 0
    quadrant_3 = 0
    quadrant_4 = 0
    for i, j in new_positions:
        if i < quadrants_x:
            if j < quadrants_y:
                quadrant_1 += 1
            elif j >= bounds[1] - quadrants_y:
                quadrant_2 += 1
        elif i >= bounds[0] - quadrants_x:
            if j < quadrants_y:
                quadrant_3 += 1
            elif j >= bounds[1] - quadrants_y:
                quadrant_4 += 1

    # print(quadrant_1, quadrant_2, quadrant_3, quadrant_4)
    return quadrant_1*quadrant_2*quadrant_3*quadrant_4



puzzle_input = open_input()
parsed_input = parse(puzzle_input)

print(solve_puzzle1(parsed_input))
safety_factors: list[int] = []
for s in range(101*103):
    safety_factors.append(solve_puzzle1(parsed_input, seconds=s))

print(safety_factors.index(min(safety_factors)))

for s in range(101*103):
    if solve_puzzle1(parsed_input, seconds=s, verbose=True):
        break

# from matplotlib import pyplot as plt
# plt.plot(range(101*103), safety_factors, "-")  # type: ignore
# plt.show()  # type: ignore

