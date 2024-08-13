#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import numpy as np
from pprint import pprint

with open("input", "r+", encoding="utf-8") as input_file:
    input_list = input_file.readlines()
    input_list = [list(r) for r in input_list]
    input_list = [r[:-1] if r[-1] == "\n" else r for r in input_list]


def tilt_north_x_lines(input_list: list[list[str]], x: int):
    """Tilt north only the first x lines of the list"""
    if x == 0:
        return input_list.copy()
    list_to_return = [input_list[0].copy()]
    for i in range(1, x):
        list_to_return.append([])
        for j, char in enumerate(input_list[i]):
            if char == "O":
                if list_to_return[i-1][j] == ".":
                    list_to_return[i-1][j] = "O"
                    list_to_return[i].append(".")
                    continue
            list_to_return[i].append(char)
    list_to_return.extend(input_list[x:])
    return list_to_return


def tilt_north(input_list_):
    """Tilt north every rock in the list"""
    list_ = input_list_.copy()
    for i in range(len(list_), -1, -1):
        list_ = tilt_north_x_lines(list_, i)
        # printable = ["".join(r) for r in list_]
        # pprint(printable)
    return list_


def tilt_south(input_list_):
    """Tilt south every rock in the list"""
    list_ = np.rot90(np.rot90(input_list_.copy()))
    tilted = np.array(tilt_north(list_))
    tilted = np.rot90(np.rot90(tilted))
    return tilted


def tilt_east(input_list_: list[list[str]]):
    """Tilt east every rock in the list"""
    list_ = np.rot90(input_list_.copy())
    tilted = np.array(tilt_north(list_))
    tilted = np.rot90(np.rot90(np.rot90(tilted)))
    return tilted


def tilt_west(input_list_: list[list[str]]):
    """Tilt east every rock in the list"""
    list_ = np.rot90(np.rot90(np.rot90(input_list_.copy())))
    tilted = np.array(tilt_north(list_))
    tilted = np.rot90(tilted)
    return tilted


def calculate_load(tilted_list):
    """Return the sum of the load caused by the rocks"""
    tilted_list = list(map(list, tilted_list))
    load = 0
    for i, r in enumerate(tilted_list):
        load += (len(input_list)-i) * r.count("O")
    return load


def cycle(input_list_, cycles):
    """Cycle `cycles` time: north, west, south, east"""
    list_ = input_list_.copy()
    cycles_memory = []
    remaining = 0
    for i in range(cycles):
        # print(i)
        list_ = tilt_north(list_)
        list_ = tilt_west(list_)
        list_ = tilt_south(list_)
        list_ = tilt_east(list_)
        list_to_append_in_memory = "".join(["".join(r) for r in list_])
        if list_to_append_in_memory in cycles_memory:
            from_i = cycles_memory.index(list_to_append_in_memory)
            # print(f"LOOP FOUND from index {from_i} to index {i}")
            # print(f"This is a len of {i-from_i}")
            remaining = (cycles - i - 1) % (i-from_i)
            # print(f"Remaining is {remaining}")
            break
        cycles_memory.append(list_to_append_in_memory)
    for i in range(remaining):
        list_ = tilt_north(list_)
        list_ = tilt_west(list_)
        list_ = tilt_south(list_)
        list_ = tilt_east(list_)

    return list_


input_list = np.array(input_list)
tilted = tilt_north(input_list)
print(calculate_load(tilted))
part2 = cycle(input_list, 1000000000)
pprint(part2)
print(calculate_load(part2))

