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


def solve_puzzle(garden: list[str]) -> tuple[int, int]:
    """Solves puzzle."""
    already_checked: list[tuple[int, int]] = []
    regions: list[list[tuple[int, int]]] = []
    n = len(garden)
    for i, line in enumerate(garden):
        print(f"ligne {i}/{n}")
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
        checked_up: list[tuple[int, int]] = []
        checked_down: list[tuple[int, int]] = []
        checked_left: list[tuple[int, int]] = []
        checked_right: list[tuple[int, int]] = []
        for i, j in region:
            if (i, j) not in checked_up and ((i-1 >= 0 and (i-1, j) not in region) or i-1 < 0):
                checked_up.append((i, j))
                sides += 1
                # negatives j
                check_j = j
                while check_j >= 0:
                    check_j -= 1
                    if (i, check_j) in region:
                        if i-1 < 0 or (i-1, check_j) not in region:
                            checked_up.append((i, check_j))
                            continue
                    break
                # positives j
                check_j = j
                while check_j < len(garden[0]):
                    check_j += 1
                    if (i, check_j) in region:
                        if i-1 < 0 or (i-1, check_j) not in region:
                            checked_up.append((i, check_j))
                            continue
                    break

            if (i, j) not in checked_down and ((i+1 < len(garden) and (i+1, j) not in region) or i+1 >= len(garden)):
                checked_down.append((i, j))
                sides += 1
                # negatives j
                check_j = j
                while check_j >= 0:
                    check_j -= 1
                    if (i, check_j) in region:
                        if i+1 >= len(garden) or (i+1, check_j) not in region:
                            checked_down.append((i, check_j))
                            continue
                    break
                # positives j
                check_j = j
                while check_j < len(garden[0]):
                    check_j += 1
                    if (i, check_j) in region:
                        if i+1 >= len(garden) or (i+1, check_j) not in region:
                            checked_down.append((i, check_j))
                            continue
                    break

            if (i, j) not in checked_left and ((j-1 >= 0 and (i, j-1) not in region) or j-1 < 0):
                checked_left.append((i, j))
                sides += 1
                # negatives i
                check_i = i
                while check_i >= 0:
                    check_i -= 1
                    if (check_i, j) in region:
                        if j-1 < 0 or (check_i, j-1) not in region:
                            checked_left.append((check_i, j))
                            continue
                    break
                # positives i
                check_i = i
                while check_i < len(garden):
                    check_i += 1
                    if (check_i, j) in region:
                        if j-1 < 0 or (check_i, j-1) not in region:
                            checked_left.append((check_i, j))
                            continue
                    break

            if (i, j) not in checked_right and ((j+1 < len(garden[0]) and (i, j+1) not in region) or j+1 >= len(garden[0])):
                checked_right.append((i, j))
                sides += 1
                # negatives i
                check_i = i
                while check_i >= 0:
                    check_i -= 1
                    if (check_i, j) in region:
                        if j+1 >= len(garden[0]) or (check_i, j+1) not in region:
                            checked_right.append((check_i, j))
                            continue
                    break
                # positives i
                check_i = i
                while check_i < len(garden):
                    check_i += 1
                    if (check_i, j) in region:
                        if j+1 >= len(garden[0]) or (check_i, j+1) not in region:
                            checked_right.append((check_i, j))
                            continue
                    break

        total2 += area*sides
    return total, total2


puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle(parsed_input))

