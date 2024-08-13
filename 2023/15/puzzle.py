#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()

input_list = input_list[0].split(",")
if input_list[-1].endswith("\n"):
    input_list[-1] = input_list[-1][:-1]


def hash(ascii_str: str):
    current_hash = 0
    for char in ascii_str:
        current_hash += ord(char)
        current_hash *= 17
        current_hash %= 256
    return current_hash


def label_in_box(label: str, box: list[tuple[str, int]]):
    for i, lens in enumerate(box):
        if lens[0] == label:
            return True, i
    return False, None


def part2(input_list: list[str]):  # this works
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]
    for step in input_list:
        if "=" in step:
            equals = True
            label_and_focal_len = step.split("=")
            label = label_and_focal_len[0]
        else:
            label_and_focal_len = [None, None]
            equals = False
            label = step[:-1]
        box = hash(label)
        if not equals:
            _, idx = label_in_box(label, boxes[box])
            if idx is not None:
                del boxes[box][idx]
        else:
            in_box, idx = label_in_box(label, boxes[box])
            assert label_and_focal_len[1] is not None
            if not in_box:
                boxes[box].append((label, int(label_and_focal_len[1])))
            else:
                assert idx is not None
                boxes[box][idx] = (label, int(label_and_focal_len[1]))
    return boxes


def calc_focusing_power_lens(lens: tuple[str, int], idx_in_box: int, box_idx: int):
    box_number = box_idx+1
    slot = idx_in_box+1
    focal_length = lens[1]
    value_to_return = box_number * slot * focal_length
    # print(lens, box_number, slot, focal_length, value_to_return)
    return value_to_return


def calc_focusing_power_box(box: list[tuple[str, int]], box_idx: int):
    focusing_power = 0
    for lens_idx, lens in enumerate(box):
        focusing_power += calc_focusing_power_lens(lens, lens_idx, box_idx)
    return focusing_power


def calc_focusing_power_boxes(boxes: list[list[tuple[str, int]]]):
    focusing_power = 0
    for box_idx, box in enumerate(boxes):
        focusing_power += calc_focusing_power_box(box, box_idx)
    return focusing_power


print(sum([hash(a) for a in input_list]))
print(calc_focusing_power_boxes(part2(input_list)))
