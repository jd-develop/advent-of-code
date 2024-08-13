#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse(input_list):
    """Just separate input list into multiple lists, each corresponding to a pattern"""
    list_to_return = []
    current_pattern = []
    for line in input_list:
        if line == "\n":
            list_to_return.append(current_pattern)
            current_pattern = []
            continue
        current_pattern.append(line[:-1])
    if len(current_pattern) != 0:
        list_to_return.append(current_pattern)
    return list_to_return


def is_difference_1(a, b):
    """Find how many characters differs from 1 str to another, and return True if this is 1"""
    correspondances = list(zip(a, b))
    differences = 0
    for char_a, char_b in correspondances:
        if char_a != char_b:
             differences += 1
        if differences >= 2:
            break
    return differences == 1


assert is_difference_1("abc", "ab.")
assert not is_difference_1("abc", "abc")
assert not is_difference_1("abcd", "ab..")


def find_horizontal_symmetry(pattern, impossible_sol=None):
    """Return the number of lines above the horizontal symmetry axis, or 0 if there is none"""
    for i, line in enumerate(pattern):
        if i == 0:
            continue
        is_match = True
        for j in range(1, i+1):
            lower_i = i-j
            upper_i = i+j-1
            if upper_i >= len(pattern):
                break
            if pattern[lower_i] != pattern[upper_i]:
                is_match = False
                break
            # if lower_i == 0 or upper_i+1 == len(pattern):
            #     return i
        if is_match and i != impossible_sol:
            return i
    return 0


def find_vertical_symmetry(pattern, impossible_sol=None):
    """Return the number of lines to the left of the vertical symmetry axis, or 0 if there is none"""
    transposed_list = list(zip(*pattern))  # this swaps lines and columns
    transposed_list2 = []
    for line in transposed_list:
        transposed_list2.append("".join(line))
    return find_horizontal_symmetry(transposed_list2, impossible_sol)


parsed_list = parse(input_list)
sum_ = 0
part1_solutions = []
for p in parsed_list:
    v = find_vertical_symmetry(p)
    h_result = h = 0
    if v == 0:
        h_result = find_horizontal_symmetry(p)
        h = 100*h_result
    part1_solutions.append((v, h_result))
    sum_ += h+v
print(sum_)

# let’s bruteforce
sum2 = 0
for global_i, p in enumerate(parsed_list):
    found_smudge = False
    for i, row in enumerate(p):
        for j, cell in enumerate(row):
            # flip the cell
            new_grid = p.copy()
            new_grid = list(map(list, new_grid))
            new_grid[i][j] = "." if cell == "#" else "#"
            result = find_vertical_symmetry(new_grid, part1_solutions[global_i][0])
            if result == 0:
                result = find_horizontal_symmetry(new_grid, part1_solutions[global_i][1])
                if result != 0:
                    sum2 += 100*result
                    found_smudge = True
                    break
            elif result != part1_solutions[global_i][0]:
                sum2 += result
                found_smudge = True
                break
        if found_smudge:
            break
print(sum2)

