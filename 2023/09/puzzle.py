#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse(list_to_parse) -> list[list[int]]:
    """Return a list of lists of numbers"""
    list_to_return = []
    for line in list_to_parse:
        if line == "\n":
            continue
        line_list = line[:-1].split()
        line_list = list(map(int, line_list))
        list_to_return.append(line_list)
    return list_to_return


def find_difference_sequences(sequence: list[int]) -> list[int]:
    """Return the sequence of the differences of the given sequence"""
    differences = []
    for i in range(len(sequence)-1):
        differences.append(sequence[i+1] - sequence[i])
    return differences


def all_zeroes(sequence: list[int]) -> bool:
    for elt in sequence:
        if elt != 0:
            return False
    return True


def extrapolate(line_to_extrapolate: list[int], part2: bool = False) -> int:
    """Return the extrapolation value of the line"""
    sequences = [line_to_extrapolate]
    while not all_zeroes(sequences[-1]):
        sequences.append(find_difference_sequences(sequences[-1]))
    extrapolate_value = 0
    del sequences[-1]
    while len(sequences) != 0:
        if part2:
            extrapolate_value = sequences[-1][0] - extrapolate_value
        else:
            extrapolate_value = sequences[-1][-1] + extrapolate_value
        del sequences[-1]
    return extrapolate_value
    

parsed_list = parse(input_list)
sum_ = 0
sum_part2 = 0
for line in parsed_list:
    extval = extrapolate(line)
    sum_ += extval
    extval2 = extrapolate(line, True)
    sum_part2 += extval2
print(sum_)
print(sum_part2)

