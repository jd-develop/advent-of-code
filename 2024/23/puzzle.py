#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import itertools
from pprint import pprint


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[tuple[str, str]]:
    """Parses the input into tuples of two computers"""
    res: list[tuple[str, str]] = []
    for line in puzzle_input.splitlines():
        if line == "": continue
        two_computers = line.split("-")
        res.append((two_computers[0], two_computers[1]))
    return res


def solve_puzzle1(links: list[tuple[str, str]]) -> int:
    """Solves puzzle 1"""
    computers: dict[str, list[str]] = {}
    for c1, c2 in links:
        if c1 not in computers:
            computers[c1] = []
        if c2 not in computers:
            computers[c2] = []

        if c2 not in computers[c1]:
            computers[c1].append(c2)
        if c1 not in computers[c2]:
            computers[c2].append(c1)

    triplets: set[tuple[str, str, str]] = set()
    for c in computers:
        for c1, c2 in itertools.combinations(computers[c], 2):
            if c not in computers[c1]: continue
            if c not in computers[c2]: continue
            if c1 not in computers[c2]: continue
            if c2 not in computers[c1]: continue
            triplet_sorted = sorted((c, c1, c2))
            # i looove pyright
            _1, _2, _3 = tuple(triplet_sorted)
            triplets.add((_1, _2, _3))

    count = 0
    for c1, c2, c3 in triplets:
        if c1.startswith("t") or c2.startswith("t") or c3.startswith("t"):
            count += 1
    return count


def solve_puzzle2(links: list[tuple[str, str]]) -> str:
    """Solves puzzle 2"""
    computers: dict[str, list[str]] = {}
    for c1, c2 in links:
        if c1 not in computers:
            computers[c1] = []
        if c2 not in computers:
            computers[c2] = []

        if c2 not in computers[c1]:
            computers[c1].append(c2)
        if c1 not in computers[c2]:
            computers[c2].append(c1)

    sets: list[list[str]] = []
    for c in computers:
        for other_computers in itertools.combinations(computers[c], len(computers[c])-1):
            set_sorted = sorted([c] + list(other_computers))
            if set_sorted in sets: continue

            loop_should_continue = False
            for other_computer in other_computers:
                if any(
                    linked not in computers[other_computer]
                    for linked in other_computers
                    if linked != other_computer
                ):
                    loop_should_continue = True
                    break
            if loop_should_continue:
                continue
            sets.append(set_sorted)

    biggest = max(sets, key=len)
    return ",".join(biggest)


puzzle_input = open_input()
parsed_input = parse(puzzle_input)

print(solve_puzzle1(parsed_input))
print(solve_puzzle2(parsed_input))

