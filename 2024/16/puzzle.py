#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import functools


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    """Returns a 2D list representing the labyrinth, where 0 represents free
       paths and 1 represents walls, as well as two tuples of coordinates
       (start and end position)
    """
    result: list[list[int]] = []
    start_pos: tuple[int, int] = (-1, -1)
    end_pos: tuple[int, int] = (-1, -1)

    for (i, line) in enumerate(puzzle_input.splitlines()):
        if line == "": continue
        line_list: list[int] = []
        for (j, tile) in enumerate(line):
            if tile == "#":
                line_list.append(1)
            elif tile == ".":
                line_list.append(0)
            elif tile == "S":
                start_pos = (i, j)
                line_list.append(0)
            elif tile == "E":
                end_pos = (i, j)
                line_list.append(0)
        result.append(line_list)

    assert start_pos != (-1, -1)
    assert end_pos != (-1, -1)
    return result, start_pos, end_pos


def solve_puzzle1(maze: list[list[int]], start_pos: tuple[int, int], end_pos: tuple[int, int]) -> tuple[int, int]:
    """Solves puzzle 1. Returns the number of forward moves, and the numbers of
       90° turns"""
    maze_height = len(maze)
    maze_width = len(maze[0])

    # Dijkstra!
    tiles_to_visit = [(start_pos, "e", 0, 0)]
    known_tiles = [(start_pos, 0, 0)]
    while len(tiles_to_visit) > 0:
        tiles_to_visit.sort(key=lambda x: x[2]+x[3]*1000)
        (i, j), facing, forward_moves, turns = tiles_to_visit.pop(0)
        neighbours = [(i-1, j, "n"), (i+1, j, "s"), (i, j+1, "e"), (i, j-1, "w")]
        found_end = False
        for ni, nj, new_facing in neighbours:
            if ni < 0 or nj < 0: continue
            if ni >= maze_height: continue
            if nj >= maze_width: continue
            if maze[ni][nj] == 1: continue  # wall
            should_continue = False
            for (ti, tj), _, _ in known_tiles:
                if (ti, tj) == (ni, nj):
                    should_continue = True
                    break
            if should_continue: continue

            new_forward_moves = forward_moves+1
            if new_facing != facing:
                new_turns = turns+1
            else:
                new_turns = turns
            known_tiles.append(((ni, nj), new_forward_moves, new_turns))

            if (ni, nj) == end_pos:
                found_end = True
                break
            tiles_to_visit.append(((ni, nj), new_facing, new_forward_moves, new_turns))
        if found_end:
            break

    for (i, j), forward_moves, turns in known_tiles:
        if (i, j) == end_pos:
            return forward_moves, turns
    assert False, "No end tile was found…"


puzzle_input = open_input()
parsed_maze, start_pos, end_pos = parse(puzzle_input)


# unoptimised
@functools.cache
def solve_puzzle2(start_pos: tuple[int, int], end_pos: tuple[int, int], facing: str,
                  forward_moves_left: int, turns_left: int) -> set[tuple[int, int]]:
    """Solves puzzle 2 recursively."""
    if start_pos == end_pos:
        return {start_pos}
    if forward_moves_left == 0:
        return set()
    i, j = start_pos
    maze = parsed_maze
    neighbours = [(i-1, j, "n"), (i+1, j, "s"), (i, j+1, "e"), (i, j-1, "w")]
    maze_height = len(maze)
    maze_width = len(maze[0])
    total_visited_tiles: set[tuple[int, int]] = set()
    for ni, nj, nf in neighbours:
        if (facing, nf) in [("n", "s"), ("s", "n"), ("e", "w"), ("w", "e")]:
            continue
        if ni < 0 or nj < 0: continue
        if ni >= maze_height: continue
        if nj >= maze_width: continue
        if maze[ni][nj] == 1: continue  # wall

        new_forward_moves_left = forward_moves_left - 1
        if (facing in "sn" and nf in "ew") or (facing in "ew" and nf in "ns"):
            if turns_left == 0: continue
            new_turns_left = turns_left - 1
        else:
            new_turns_left = turns_left

        new_visited_tiles = solve_puzzle2(
            (ni, nj), end_pos, nf, new_forward_moves_left, new_turns_left
        )
        if len(new_visited_tiles) == 0:
            continue
        total_visited_tiles = total_visited_tiles.union(new_visited_tiles)
        total_visited_tiles.add((ni, nj))

    return total_visited_tiles


forward_moves, turns = solve_puzzle1(parsed_maze, start_pos, end_pos)
print(forward_moves + 1000*turns)
print(len(solve_puzzle2(start_pos, end_pos, "e", forward_moves, turns))+1)

