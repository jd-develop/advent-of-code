#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import itertools


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[list[int]], list[list[int]]]:
    """Returns locks and keys"""
    locks: list[list[int]] = []
    keys: list[list[int]] = []
    for thing in puzzle_input.split("\n\n"):
        if thing[0] == ".":  # key
            key: list[int] = []
            for i in range(5):
                key.append(6-([thing[k*6+i] for k in range(7)].index("#")))
            keys.append(key)
        else:
            lock: list[int] = []
            for i in range(5):
                lock.append(([thing[k*6+i] for k in range(7)].index("."))-1)
            locks.append(lock)

    return locks, keys


def solve_puzzle1(locks: list[list[int]], keys: list[list[int]]) -> int:
    """Solves puzzle 1"""
    all_arrangements = itertools.product(locks, keys)
    total = 0
    for lock, key in all_arrangements:
        should_continue = False
        for i in range(len(lock)):
            if lock[i]+key[i] > 5:
                should_continue = True
                break
        if should_continue: continue
        total += 1
    return total


puzzle_input = open_input()
gl_locks, gl_keys = parse(puzzle_input)

print(solve_puzzle1(gl_locks, gl_keys))

# Amazing! this is the first year ever I’ve completed each of the AoC puzzles!
# Merry Christmas!

