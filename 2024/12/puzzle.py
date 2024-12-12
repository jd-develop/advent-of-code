#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[str]:
    """Parses the input"""
    parsed = puzzle_input.split("\n")
    if parsed[-1] == "":
        parsed = parsed[:-1]
    return parsed


def solve_puzzle(garden: list[str]) -> int:
    """Solves puzzle."""
    already_checked: list[tuple[int, int]] = []
    regions: list[list[tuple[int, int]]] = []
    for i, line in enumerate(garden):
        print(f"ligne {i}")
        for j, tile in enumerate(line):
            if (i, j) in already_checked: continue
            regions.append([(i, j)])
            already_checked.append((i, j))
            still_to_check: list[tuple[int, int]] = [(i+1, j), (i, j+1)]
            while len(still_to_check) != 0:
                check_i, check_j = still_to_check.pop(0)
                if (check_i, check_j) in already_checked: continue
                if check_i < 0 or check_i >= len(garden): continue
                if check_j < 0 or check_j >= len(garden[0]): continue
                if garden[check_i][check_j] == tile:
                    regions[-1].append((check_i, check_j))
                    already_checked.append((check_i, check_j))
                    if (check_i+1, check_j) not in already_checked and (check_i+1, check_j) not in still_to_check:
                        still_to_check.append((check_i+1, check_j))
                    if (check_i-1, check_j) not in already_checked and (check_i-1, check_j) not in still_to_check:
                        still_to_check.append((check_i-1, check_j))
                    if (check_i, check_j+1) not in already_checked and (check_i, check_j+1) not in still_to_check:
                        still_to_check.append((check_i, check_j+1))
                    if (check_i, check_j-1) not in already_checked and (check_i, check_j-1) not in still_to_check:
                        still_to_check.append((check_i, check_j-1))

    print("calcul des périmètres")
    total = 0
    for region in regions:
        area = len(region)
        perimeter = 0
        for i, j in region:
            if i-1 >= 0:
                if (i-1, j) not in region:
                    perimeter += 1
            else:
                perimeter += 1
            if i+1 < len(garden):
                if (i+1, j) not in region:
                    perimeter += 1
            else:
                perimeter += 1
            if j-1 >= 0:
                if (i, j-1) not in region:
                    perimeter += 1
            else:
                perimeter += 1
            if j+1 < len(garden):
                if (i, j+1) not in region:
                    perimeter += 1
            else:
                perimeter += 1
        total += area*perimeter

    print("calcul de la partie 2")
    total2 = 0
    for region in regions:
        area = len(region)
        sides = 0
        checked: list[tuple[int, int]] = []
        for i, j in region:
            if (i, j) in checked: continue
            if i-1 >= 0:
                if (i-1, j) not in region:
                    sides += 1
            else:
                sides += 1
            if i+1 < len(garden):
                if (i+1, j) not in region:
                    sides += 1
            else:
                sides += 1
            if j-1 >= 0:
                if (i, j-1) not in region:
                    sides += 1
            else:
                sides += 1
            if j+1 < len(garden):
                if (i, j+1) not in region:
                    sides += 1
            else:
                sides += 1
        total2 += area*sides
    return total



puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle(parsed_input))

