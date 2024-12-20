#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import copy


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    """Returns the maze (1 for wall, 0 for path), the start position, and the
       end position"""
    maze: list[list[int]] = []
    start = (-1, -1)
    end = (-1, -1)

    for i, line in enumerate(puzzle_input.splitlines()):
        if line == "": continue
        line_list: list[int] = []
        for j, row in enumerate(line):
            if row == "#":
                line_list.append(1)
            elif row == "S":
                start = (i, j)
                line_list.append(0)
            elif row == "E":
                end = (i, j)
                line_list.append(0)
            elif row == ".":
                line_list.append(0)
        maze.append(line_list)

    assert start != (-1, -1)
    assert end != (-1, -1)
    return maze, start, end


def cost_of_tiles(
        maze: list[list[int]], start: tuple[int, int], end: tuple[int, int],
):
    """Determine the cost of each tile and return a 2D list where -1 are walls
       and other are normal tiles, from 0 (start) to the end"""
    new_maze = [[-j for j in line] for line in maze]

    i, j = start
    cost = 0
    path: list[tuple[int, int]] = [(i, j)]
    while (i, j) != end:
        neighbours = [(i-1, j), (i+1, j), (i, j+1), (i, j-1)]
        for ni, nj in neighbours:
            if new_maze[ni][nj] == -1: continue
            if (ni, nj) in path: continue
            i, j = ni, nj
            break
        cost += 1
        new_maze[i][j] = cost
        path.append((i, j))

    return new_maze, path


def solve_puzzle1(new_maze: list[list[int]], start: tuple[int, int], end: tuple[int, int], path: list[tuple[int, int]]) -> int:
    """Solves puzzle 1"""
    for (i, j) in path:
        # TODO: find the walls, check if tiles behind the walls are in path,
        # substract

    total = 0
    for solution in all_solutions.keys():
        if solution < 100: continue
        total += all_solutions[solution]

    return total


#def solve_puzzle2(maze: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> int:
#    """Solves puzzle 2"""

puzzle_input = open_input("example1.input")
maze, start, end = parse(puzzle_input)
new_maze, path = cost_of_tiles(maze, start, end)

# part1 takes 3:54 to run :)
# print(solve_puzzle1(maze, start, end))

