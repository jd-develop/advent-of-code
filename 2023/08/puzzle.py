#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import math

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse(list_to_parse) -> tuple[str, dict[str, tuple[str, str]]]:
    """Return a str and a dict of str: (str, str)"""
    directions = ""
    nodes = dict()
    for i, line in enumerate(list_to_parse):
        if line == "\n":
            continue
        if i == 0:
            directions = line[:-1]
            continue
        line = line[:-1].split()
        nodes[line[0]] = (line[2][1:-1], line[3][:-1])
    return directions, nodes


def find_zzz(directions, parsed_dict, current_node="AAA", just_endswith=False) -> int:
    """Return the number of steps required to find ZZZ"""
    counter = 0
    condition = (lambda: current_node != "ZZZ") if not just_endswith else (lambda: not current_node.endswith("Z"))
    while condition():
        for direction in directions:
            counter += 1
            if direction == "R":
                current_node = parsed_dict[current_node][1]
            else:
                current_node = parsed_dict[current_node][0]
    return counter


def find_zzz_part2(directions, parsed_dict) -> int:
    """Return the number of steps required for part 2"""
    current_nodes = [node for node in list(parsed_dict.keys()) if node.endswith("A")]
    nodes_counters = []
    for node in current_nodes:
        nodes_counters.append(find_zzz(directions, parsed_dict, node, True))
    lcm = nodes_counters[0]
    for counter in nodes_counters:
        lcm = math.lcm(lcm, counter)
    return lcm


print(find_zzz(*parse(input_list)))
print(find_zzz_part2(*parse(input_list)))

