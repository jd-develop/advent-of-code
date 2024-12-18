#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str, width: int, height: int, octets: int) -> list[list[int]]:
    """Returns the 2D list representing the memory (0 for safe, 1 for corrupted)"""
    memory: list[list[int]] = [[0 for _ in range(width+1)] for _ in range(height+1)]
    for i, octet in enumerate(puzzle_input.splitlines()):
        if octet == "": continue
        if i >= octets: break

        x, y = tuple(map(int, octet.split(",")))
        memory[x][y] = 1
    return memory


def solve_puzzle1(memory: list[list[int]], end: tuple[int, int]) -> int:
    """Solves puzzle 1"""

    tiles_to_visit: list[tuple[int, int, int]] = [(0, 0, 0)]
    known_tiles: dict[tuple[int, int], int] = {(0, 0): 0}
    while len(tiles_to_visit) > 0:
        tiles_to_visit.sort(key=lambda x: x[2])
        i, j, cost = tiles_to_visit.pop(0)
        neighbours = [(i-1, j), (i+1, j), (i, j+1), (i, j-1)]
        found_end = False
        for ni, nj in neighbours:
            if ni < 0 or nj < 0: continue
            if ni > end[0]: continue
            if nj > end[1]: continue
            if memory[ni][nj] == 1: continue  # corrupted byte
            if (ni, nj) in known_tiles: continue

            known_tiles[(ni, nj)] = cost+1

            if (ni, nj) == end:
                found_end = True
                break
            tiles_to_visit.append((ni, nj, cost+1))
        if found_end:
            break

    if end not in known_tiles:
        return -1
    return known_tiles[end]


puzzle_input = open_input()
parsed_input = parse(puzzle_input, 70, 70, 1024)
# parsed_input = parse(puzzle_input, 6, 6, 12)

print(solve_puzzle1(parsed_input, (70, 70)))
# print(solve_puzzle1(parsed_input, (6, 6)))

# that is ONLY a 21 seconds bruteforce :)
i = 1024
# i = 12
puzzle_input = puzzle_input.splitlines()
len_input = len(puzzle_input)
while True:
    x, y = tuple(map(int, puzzle_input[i].split(",")))
    parsed_input[x][y] = 1
    # if solve_puzzle1(parsed_input, (6, 6)) == -1:
    if solve_puzzle1(parsed_input, (70, 70)) == -1:
        print(f"{x},{y}")
        break
    i += 1

