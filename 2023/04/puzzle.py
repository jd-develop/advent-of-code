#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from pprint import pprint

with open("input", "r+", encoding="utf-8") as input_file:
    input_list = input_file.readlines()


def parse(list_to_parse) -> list[tuple[list[int], list[int]]]:
    """Return a list of all the lines, each lines is the tuple of the list of winning numbers
       and the list of the numbers you have
    """
    parsed_list = []
    for line in list_to_parse:
        if line == "\n":
            continue
        line = line.split()
        line = line[2:]
        
        winning_numbers = []
        numbers_you_have = []
        register_win = True
        for token in line:
            if token == "|":
                register_win = False
                continue
            if register_win:
                winning_numbers.append(int(token))
            else:
                numbers_you_have.append(int(token))
        parsed_list.append((winning_numbers, numbers_you_have))
    return parsed_list


def calculate_points(parsed_list):
    """Return the sum of the points of each card"""
    sum_ = 0
    for line in parsed_list:
        winning_numbers = 0
        for number in line[1]:
            if number in line[0]:
                winning_numbers += 1
        if winning_numbers != 0:
            sum_ += 2 ** (winning_numbers - 1)
    return sum_


def calculate_points_part_2(parsed_list):
    """Return the number of scratchcards you end up with at the end"""
    scratchcards = [1]*len(parsed_list)
    for i, line in enumerate(parsed_list):
        winning_numbers = 0
        for number in line[1]:
            if number in line[0]:
                winning_numbers += 1
        if winning_numbers != 0:
            current_card_copies = scratchcards[i]
            for j in range(1, winning_numbers+1):
                try:
                    scratchcards[i+j] += current_card_copies
                except IndexError:
                    pass
    return sum(scratchcards)


parsed = parse(input_list)
pprint(calculate_points(parsed))
pprint(calculate_points_part_2(parsed))

