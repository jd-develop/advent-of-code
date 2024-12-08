#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[list[str]]:
    """Parses the input"""
    result: list[list[str]] = []
    for line in puzzle_input.split("\n"):
        if line == "": continue
        result.append([c for c in line])
    return result


def solve_puzzle1(antennas: list[list[str]]) -> int:
    """Solves puzzle 1."""
    n, m = len(antennas), len(antennas[0])

    antennas_coords: dict[str, list[tuple[int, int]]] = {}
    antinodes_location: set[tuple[int, int]] = set()
    for (i, line) in enumerate(antennas):
        for (j, antenna) in enumerate(line):
            if antenna == ".":
                continue
            if antenna not in antennas_coords:
                antennas_coords[antenna] = [(i, j)]
            else:
                antennas_coords[antenna].append((i, j))

    for antenna in antennas_coords:
        done: list[tuple[int, int]] = []
        for i, (l, c) in enumerate(antennas_coords[antenna]):
            for (l2, c2) in antennas_coords[antenna]:
                if (l2, c2) == (l, c): continue
                if (l2, c2) in done: continue

                diffl = l2-l
                diffc = c2-c
                antinode_1 = (l-diffl, c-diffc)
                antinode_2 = (l2+diffl, c2+diffc)
                if not (antinode_1[0] < 0 or antinode_1[0] >= n or antinode_1[1] < 0 or antinode_1[1] >= m):
                    antinodes_location.add(antinode_1)
                if not (antinode_2[0] < 0 or antinode_2[0] >= n or antinode_2[1] < 0 or antinode_2[1] >= m):
                    antinodes_location.add(antinode_2)
            done.append((l, c))

    return len(antinodes_location)


def solve_puzzle2(antennas: list[list[str]]) -> int:
    """Solves puzzle 1."""
    n, m = len(antennas), len(antennas[0])
    antennas_coords: dict[str, list[tuple[int, int]]] = {}
    antinodes_location: set[tuple[int, int]] = set()
    for (i, line) in enumerate(antennas):
        for (j, antenna) in enumerate(line):
            if antenna == ".":
                continue
            if antenna not in antennas_coords:
                antennas_coords[antenna] = [(i, j)]
            else:
                antennas_coords[antenna].append((i, j))

    for antenna in antennas_coords:
        done: list[tuple[int, int]] = []
        for i, (l, c) in enumerate(antennas_coords[antenna]):
            for (l2, c2) in antennas_coords[antenna]:
                if (l2, c2) == (l, c): continue
                if (l2, c2) in done: continue

                diffl = l2-l
                diffc = c2-c
                negativel, negativec = l, c
                while (negativel >= 0 and negativel < n and negativec >= 0 and negativec < m):
                    antinodes_location.add((negativel, negativec))
                    negativel -= diffl
                    negativec -= diffc
                positivel, positivec = l, c
                while (positivel >= 0 and positivel < n and positivec >= 0 and positivec < m):
                    antinodes_location.add((positivel, positivec))
                    positivel += diffl
                    positivec += diffc
            done.append((l, c))

    return len(antinodes_location)

puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle1(parsed_input))
print(solve_puzzle2(parsed_input))

