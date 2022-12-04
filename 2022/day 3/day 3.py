#!/usr/bin/env python3
# coding:utf-8

with open("input.txt", 'r+', encoding="UTF-8") as input_file:
    raw_input = input_file.readlines()

item_priorities_lower = {chr(ord_): ord_-ord("a")+1 for ord_ in range(ord("a"), ord("z") + 1)}
item_priorities_upper = {chr(ord_): ord_-38 for ord_ in range(ord("A"), ord("Z") + 1)}

priorities_sum = 0
for backpack in raw_input:
    first_compartment = backpack[:int(len(backpack)/2)]
    second_compartment = backpack[int(len(backpack)/2):]
    common_letter: str = list(set(first_compartment) & set(second_compartment))[0]
    if common_letter.islower():
        priority = item_priorities_lower[common_letter]
        priorities_sum += priority
    else:
        priority = item_priorities_upper[common_letter]
        priorities_sum += priority

print(priorities_sum)

badge_priorities_sum = 0
for group_index in range(0, len(raw_input), 3):
    backpack1 = raw_input[group_index].replace('\n', '')
    backpack2 = raw_input[group_index+1].replace('\n', '')
    backpack3 = raw_input[group_index+2].replace('\n', '')
    sets = list(set(backpack1) & set(backpack2) & set(backpack3))[0]
    badge: str = sets[0]
    if badge.islower():
        priority = item_priorities_lower[badge]
        badge_priorities_sum += priority
    else:
        priority = item_priorities_upper[badge]
        badge_priorities_sum += priority

print(badge_priorities_sum)

