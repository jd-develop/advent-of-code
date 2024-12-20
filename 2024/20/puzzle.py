#!/usr/bin/env python3
# -*- coding:utf-8 -*-


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


def find_best_way(
        maze: list[list[int]], start: tuple[int, int], end: tuple[int, int],
        nowall: tuple[int, int],
        allowed_to_tp: tuple[tuple[int, int], tuple[int, int]] = ((-1, -1), (-1, -1)),
        cheat_cost: int = 0
):
    """Dijkstra"""
    tiles_to_visit: list[tuple[int, int, int]] = [(*start, 0)]
    known_tiles: dict[tuple[int, int], int] = {start: 0}
    maze_h = len(maze)
    maze_w = len(maze[0])

    while len(tiles_to_visit) > 0:
        tiles_to_visit.sort(key=lambda x: x[2])
        i, j, cost = tiles_to_visit.pop(0)
        neighbours = [(i-1, j, 1), (i+1, j, 1), (i, j+1, 1), (i, j-1, 1)]

        if (i, j) == allowed_to_tp[0]:
            neighbours.append(allowed_to_tp[1]+(cheat_cost,))
        if (i, j) == allowed_to_tp[1]:
            neighbours.append(allowed_to_tp[0]+(cheat_cost,))
        found_end = False

        for ni, nj, ncost in neighbours:
            if ni < 0 or nj < 0: continue
            if ni >= maze_h: continue
            if nj >= maze_w: continue
            if maze[ni][nj] == 1 and (ni, nj) != nowall: continue  # wall
            if (ni, nj) in known_tiles: continue

            known_tiles[(ni, nj)] = cost+ncost

            if (ni, nj) == end:
                found_end = True
                break
            tiles_to_visit.append((ni, nj, cost+ncost))
        if found_end:
            break

    assert end in known_tiles
    return known_tiles[end]


def solve_puzzle1(maze: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> int:
    """Solves puzzle 1"""
    normal_solution = find_best_way(maze, start, end, (-1, -1))
    all_solutions: dict[int, int] = {0: 1}
    for i, line in enumerate(maze):
        for j, row in enumerate(line):
            if row != 1: continue
            solution_without_wall = normal_solution-find_best_way(maze, start, end, (i, j))
            if solution_without_wall not in all_solutions:
                all_solutions[solution_without_wall] = 0
            all_solutions[solution_without_wall] += 1

    total = 0
    for solution in all_solutions.keys():
        if solution < 100: continue
        total += all_solutions[solution]

    return total


#def solve_puzzle2(maze: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> int:
#    """Solves puzzle 2"""

puzzle_input = open_input("example1.input")
maze, start, end = parse(puzzle_input)

# part1 takes 3:54 to run :)
# print(solve_puzzle1(maze, start, end))

