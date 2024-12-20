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


def solve_puzzle1(new_maze: list[list[int]], path: list[tuple[int, int]]) -> int:
    """Solves puzzle 1"""
    all_solutions: dict[int, int] = {0: 1}
    maze_h = len(new_maze)
    maze_w = len(new_maze[0])
    done: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for (i, j) in path:
        neighbours = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        for ni, nj in neighbours:
            if ni < 0 or nj < 0: continue
            if ni >= maze_h or nj >= maze_w: continue

            if new_maze[ni][nj] != -1: continue
            neighbour_neighbours = [(ni-1, nj), (ni+1, nj), (ni, nj-1), (ni, nj+1)]
            for nni, nnj in neighbour_neighbours:
                if ((i, j), (nni, nnj)) in done: continue
                if nni < 0 or nnj < 0: continue
                if nni >= maze_h or nnj >= maze_w: continue
                if (nni, nnj) == (i, j): continue
                if new_maze[nni][nnj] == -1: continue

                time_save = abs(new_maze[nni][nnj] - new_maze[i][j])-2
                if time_save not in all_solutions.keys():
                    all_solutions[time_save] = 0
                all_solutions[time_save] += 1
                done.add(((i, j), (nni, nnj)))
                done.add(((nni, nnj), (i, j)))

    total = 0
    for solution in all_solutions.keys():
        if solution < 100: continue
        total += all_solutions[solution]

    return total


def all_tiles_with_same_manhattan_distance(
    new_maze: list[list[int]], start_tile: tuple[int, int], distance: int
) -> list[tuple[int, int]]:
    """Return the list of valid tiles that are separated by `distance` from
       `start_tile` (in terms of manhattan distance)"""
    x, y = start_tile
    result: list[tuple[int, int]] = []

    for diffx in range(0, distance+1):
        diffy = distance-diffx
        tiles = [(x+diffx, y+diffy), (x-diffx, y+diffy), (x+diffx, y-diffy), (x-diffx, y-diffy)]
        for ti, tj in tiles:
            if ti < 0 or tj < 0: continue
            if ti >= len(new_maze) or tj >= len(new_maze[0]): continue
            if new_maze[ti][tj] == -1: continue
            result.append((ti, tj))

    return result


def solve_puzzle2(new_maze: list[list[int]], path: list[tuple[int, int]]) -> int:
    """Solves puzzle 2"""
    all_solutions: dict[int, int] = {0: 1}
    done: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for c, (i, j) in enumerate(path):
        print(f"{c+1}/{len(path)}")
        for distance in range(2, 21):
            neighbour_neighbours = all_tiles_with_same_manhattan_distance(new_maze, (i, j), distance)
            for ni, nj in neighbour_neighbours:
                if ((i, j), (ni, nj)) in done: continue
                if (ni, nj) == (i, j): continue

                time_save = abs(new_maze[ni][nj] - new_maze[i][j])-(distance)
                if time_save not in all_solutions.keys():
                    all_solutions[time_save] = 0
                all_solutions[time_save] += 1
                done.add(((i, j), (ni, nj)))
                done.add(((ni, nj), (i, j)))


    #import pprint
    #pprint.pprint(all_solutions)
    total = 0
    for solution in all_solutions.keys():
        if solution < 100: continue
        total += all_solutions[solution]

    return total


puzzle_input = open_input()
maze, start, end = parse(puzzle_input)
new_maze, path = cost_of_tiles(maze, start, end)

print("Finished parsing")
print(solve_puzzle1(new_maze, path))
print(solve_puzzle2(new_maze, path))

