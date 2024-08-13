#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_text = input_f.readlines()

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
input_numbers = []
input_numbers_part_2 = []
for str_ in input_text:
    num_str = ""
    num_str_part2 = ""
    current_number_made_out_of_letters = ""
    for i, char in enumerate(str_):
        if char.isnumeric():
            num_str += char
            num_str_part2 += char
            current_number_made_out_of_letters = ""
        else:
            for j in range(3, 6):
                try:
                    if str_[i:i+j] in numbers:
                        num_str_part2 += str(numbers.index(str_[i:i+j]) + 1)
                except IndexError:
                    pass
    if len(num_str) == 0:
        num_str = "0"
    elif len(num_str) == 1:
        num_str *= 2
    elif len(num_str) > 2:
        num_str = num_str[0] + num_str[-1]
    if len(num_str_part2) == 0:
        num_str_part2 = "0"
    elif len(num_str_part2) == 1:
        num_str_part2 *= 2
    elif len(num_str_part2) > 2:
        num_str_part2 = num_str_part2[0] + num_str_part2[-1]
    input_numbers.append(int(num_str))
    input_numbers_part_2.append(int(num_str_part2))

print(f"1: {sum(input_numbers)}")
print(f"2: {sum(input_numbers_part_2)}")

