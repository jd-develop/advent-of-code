#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from functools import cache

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse(input_list):
    """Return a list of rows, where each row is a tuple of one str and a list of numbers"""
    list_to_return = []
    for line in input_list:
        if line == "\n":
            continue
        line = line.split()
        hot_springs = line[0]
        numbers = list(map(int, line[1].split(",")))
        list_to_return.append((hot_springs, numbers))
    return list_to_return


@cache
def count_possibilities(springs, numbers, springs_i, numbers_i, current_num):
    if springs_i == len(springs):
        if numbers_i+1 == len(numbers) and numbers[numbers_i] == current_num:
            return 1
        if numbers_i == len(numbers) and current_num == 0:
            return 1
        return 0

    result = 0
    if springs[springs_i] in "?#":
        result += count_possibilities(springs, numbers, springs_i+1, numbers_i, current_num+1)
    if springs[springs_i] in "?.":
        if current_num == 0:
            result += count_possibilities(springs, numbers, springs_i+1, numbers_i, 0)
        elif numbers_i < len(numbers) and current_num == numbers[numbers_i]:
            # here we stop a group only if we’re done with this group
            result += count_possibilities(springs, numbers, springs_i+1, numbers_i+1, 0)
    return result


def unfold(parsed_list):
    """Return part2 input"""
    list_to_return = []
    for row, numbers in parsed_list:
        new_row = ((row+"?")*5)[:-1]
        new_numbers = numbers * 5
        list_to_return.append((new_row, new_numbers))
    return list_to_return


parsed_list = parse(input_list)
print(sum(count_possibilities(row[0], tuple(row[1]), 0, 0, 0) for row in parsed_list))

list_part2 = unfold(parsed_list)
sum_2 = 0
for row in list_part2:
    possibilities = count_possibilities(row[0], tuple(row[1]), 0, 0, 0)
    sum_2 += possibilities
print(sum_2)

