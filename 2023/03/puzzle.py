#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from pprint import pprint

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse_line(line_to_parse):
    """Take a single line and return a list of the number and symbols (see docstring for `parse`)"""
    list_to_return = []
    current_num = ""
    start_index = 0
    current_len = 0

    for i, char in enumerate(line_to_parse):
        if char.isnumeric():
            if current_num == "":
                start_index = i
            current_num += char
            current_len += 1
            continue
        if current_num != "":
            num_to_append = int(current_num)
            tuple_to_append = (num_to_append, start_index, current_len, len(line_to_parse))
            list_to_return.append(tuple_to_append)
            current_len = 0
            current_num = ""
        if char in ".\n":
            continue
        list_to_return.append((char, i, len(line_to_parse)))
    return list_to_return



def parse(list_to_parse):
    """Take a whole list and return a list of as many lists as there are lines.
       A line list is under the form: [number, symbol, number, number, symbol, symbol, etc.]
       where number is the tuple (number: int, index: int, lenght: int, line_lenght: int)
       and   symbol is the tuple (symbol: str, index: int)
    """
    list_to_return = []
    for i, line in enumerate(list_to_parse):
        if line == "\n":
            continue
        list_to_return.append(parse_line(line))
    return list_to_return


def find_numbers(lines_list):
    """Take a parsed list and return a list of all numbers with the indexes to check."""
    numbers_to_check = []
    for i, line in enumerate(lines_list):
        for number_or_symbol in line:
            if len(number_or_symbol) == 3:
                continue
            number, start_index, lenght, line_lenght = number_or_symbol
            before = start_index != 0
            after = start_index + lenght != line_lenght
            adjacent_indexes = []
            if before:
                adjacent_indexes.append((i, start_index-1))
            if after:
                adjacent_indexes.append((i, start_index+lenght))

            if before:
                range_start = start_index-1
            else:
                range_start = start_index
            if after:
                range_end = start_index + lenght + 1
            else:
                range_end = start_index + lenght

            if i != 0:
                adjacent_indexes.extend([(i-1, j) for j in range(range_start, range_end)])
            if i+1 != len(lines_list):
                adjacent_indexes.extend([(i+1, j) for j in range(range_start, range_end)])
            
            # print(number, adjacent_indexes)
            numbers_to_check.append((number, adjacent_indexes))
    # pprint(numbers_to_check)
    return numbers_to_check


def check_num(adjacent_indexes, parsed_list_):
    """Return True if the number is adjacent to a symbol"""
    for i, j in adjacent_indexes:
        line = parsed_list_[i]
        for num_or_symbol in line:
            if len(num_or_symbol) != 3:
                continue
            if num_or_symbol[1] == j:
                return True
    return False


def find_gears(lines_list):
    """Return all the gears and their adjacent indexes."""
    gears_to_check = []
    for i, line in enumerate(lines_list):
        for number_or_symbol in line:
            if len(number_or_symbol) != 3:
                continue
            symbol, index, line_lenght = number_or_symbol
            if symbol != "*":
                continue
            before = index != 0
            after = index + 1 != line_lenght
            adjacent_indexes = []
            if before:
                adjacent_indexes.append((i, index-1))
            if after:
                adjacent_indexes.append((i, index+1))

            if before:
                range_start = index - 1
            else:
                range_start = index
            if after:
                range_end = index + 2
            else:
                range_end = index + 1

            if i != 0:
                adjacent_indexes.extend([(i-1, j) for j in range(range_start, range_end)])
            if i+1 != len(lines_list):
                adjacent_indexes.extend([(i+1, j) for j in range(range_start, range_end)])
            
            # print(symbol, adjacent_indexes)
            gears_to_check.append(adjacent_indexes)
    return gears_to_check


def check_gear(adjacent_indexes, parsed_list_):
    """Return True if the gear have exactly 2 numbers around"""
    numbers_around = 0
    gear_ratio = 1
    already_counted = []
    for i, j in adjacent_indexes:
        for num_or_symbol in parsed_list_[i]:
            if len(num_or_symbol) == 3:
                continue
            number, start_index, lenght, linge_lenght = num_or_symbol
            if (i, start_index) in already_counted:
                # print("oui", number)
                continue
            if start_index <= j <= start_index+lenght-1:
                numbers_around += 1
                gear_ratio *= number
                already_counted.append((i, start_index))
    # print(numbers_around, gear_ratio)
    return numbers_around == 2, gear_ratio



parsed_list = parse(input_list)
# pprint(parsed_list)
num_to_check = find_numbers(parsed_list)

valid_numbers = []
for num in num_to_check:
    num_is_valid = check_num(num[1], parsed_list)
    # print(num[0], num_is_valid)
    if num_is_valid:
        valid_numbers.append(num[0])

print(sum(valid_numbers))

gears_to_check_ = find_gears(parsed_list)

valid_gears_ratios = []
for gear in gears_to_check_:
    gear_is_valid, ratio = check_gear(gear, parsed_list)
    if gear_is_valid:
        valid_gears_ratios.append(ratio)

print(sum(valid_gears_ratios))

