#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import functools


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[int]:
    """Parses the input into a list of ints (strs)"""
    stones: list[int] = []
    for stone in puzzle_input.split():
        if stone == "": continue
        if stone.endswith("\n"): stone = stone[:-1]
        stones.append(int(stone))

    return stones


@functools.cache  # the AoC recursion cheatcode :)
def how_many_stones(stone: int, blinks: int = 25) -> int:
    """Returns how many stones this particular stone generates"""
    if blinks == 0:
        return 1
    if stone == 0:
        return how_many_stones(1, blinks-1)
    if len(str(stone))%2 == 0:
        stone_str = str(stone)
        stone1 = stone_str[:len(stone_str)//2]
        stone2 = stone_str[len(stone_str)//2:]
        return how_many_stones(int(stone1), blinks-1) + how_many_stones(int(stone2), blinks-1)
    return how_many_stones(stone*2024, blinks-1)


def solve_puzzle1(stones: list[int], blinks: int = 25) -> int:
    """Solves puzzle 1."""
    if blinks == 0:
        return len(stones)
    total = 0
    for stone in stones:
        total += how_many_stones(stone, blinks)
    return total


puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle1(parsed_input))
print(solve_puzzle1(parsed_input, 75))

