#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from itertools import combinations
# from pprint import pprint

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def empty_row(row):
    """Return True if the row contains no galaxy"""
    return row == len(row)*"."


def empty_column(i, unparsed_list):
    """Return True if the column contains no galaxy"""
    for line in unparsed_list:
        if line == "\n":
            continue
        if line[i] == "#":
            return False
    return True


def space_expension(unparsed_list, times_larger: int = 2):
    list_to_return = []
    lines_count = 0
    galaxy_count = 0
    galaxies = []
    for i, r in enumerate(unparsed_list):
        if r == "\n":
            continue
        r = r[:-1]
        rows_count = 0

        for j, char in enumerate(r):
            if char == "#":
                galaxy_count += 1
                galaxies.append((galaxy_count, lines_count, rows_count))
            if empty_column(j, unparsed_list):
                rows_count += times_larger - 1
            rows_count += 1
        if empty_row(r):
            lines_count += times_larger - 1
        lines_count += 1
    return galaxies


def calculate_len(pair):
    """Return the length between the pair"""
    a = pair[0]
    b = pair[1]
    xA = a[1]
    yA = a[2]
    xB = b[1]
    yB = b[2]
    return abs(xB-xA) + abs(yB-yA)


def get_sum(galaxies):
    # pprint(galaxies)
    pairs = combinations(galaxies, 2)
    sum_ = 0
    for pair in pairs:
        length = calculate_len(pair)
        # print(pair[0][0], pair[1][0], length)
        sum_ += length
    return sum_


galaxies = space_expension(input_list)
print(get_sum(galaxies))
# print("===============================")
galaxies_part2 = space_expension(input_list, 1_000_000)
print(get_sum(galaxies_part2))

