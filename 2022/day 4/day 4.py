#!/usr/bin/env python3
# coding:utf-8

with open("input.txt", 'r+', encoding="UTF-8") as input_file:
    raw_input = input_file.readlines()

how_many_full_overlaps = 0
for pair in raw_input:
    pair_list = pair.replace('\n', '').split(',')
    pair1 = pair_list[0].split('-')
    pair2 = pair_list[1].split('-')
    if (int(pair1[0]) <= int(pair2[0]) and int(pair1[1]) >= int(pair2[1])) \
            or (int(pair2[0]) <= int(pair1[0]) and int(pair2[1]) >= int(pair1[1])):
        how_many_full_overlaps += 1

print(how_many_full_overlaps)

how_many_overlaps = 0
for pair in raw_input:
    pair_list = pair.replace('\n', '').split(',')
    pair1 = pair_list[0].split('-')
    pair2 = pair_list[1].split('-')
    range1 = list(range(int(pair1[0]), int(pair1[1])+1))
    range2 = list(range(int(pair2[0]), int(pair2[1])+1))
    if len(list(set(range1) & set(range2))) != 0:
        how_many_overlaps += 1

print(how_many_overlaps)
