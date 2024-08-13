#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input_example1", "r+", encoding="utf-8") as input_file:
    input_list = input_file.readlines()


def parse(puzzle_input):
    """Return a list of parts, under the form (x, m, a, s), and a dict
    of workflows, under the form (("a<2006", "qkq"), ("m>2090", "A"), ("", "rfg"))"""
    workflows = {}
    parts = []
    for line in puzzle_input:
        if line == "\n":
            continue
        if line.startswith("{"):  # part
            if line.endswith("\n"):
                line = line[:-1]
            line = line[1:-1]
            line = line.split(",")
            line = [num[2:] for num in line]
            part = tuple(map(int, line))
            parts.append(part)
        else:  # workflows
            if line.endswith("\n"):
                line = line[:-1]
            line = line[:-1]
            line = line.split("{")
            name = line[0]
            instructions = line[1].split(",")
            instructions[-1] = f":{instructions[-1]}"
            instructions = tuple([tuple(instruct.split(":")) for instruct in instructions])
            workflows[name] = instructions
    return parts, workflows


def test_part(part, test):
    """Returns a boolean"""
    if test == "":
        return True
    x, m, a, s = part
    return eval(test)


def get_part_to_one_workflow(part, workflow):
    """Return the output of the workflow"""
    for instruction in workflow:
        if test_part(part, instruction[0]):
            return instruction[1]
    assert False


def get_part_to_workflows(part, workflows):
    """Return 0 if the part is rejected, and the sum of its values if it is accepted"""
    current_workflow = workflows["in"]
    finish = False
    while not finish:
        res = get_part_to_one_workflow(part, current_workflow)
        if res == "R":
            return 0
        if res == "A":
            return sum(part)
        current_workflow = workflows[res]


parsed_parts, parsed_workflows = parse(input_list)
sum_ = 0
for part in parsed_parts:
    sum_ += get_part_to_workflows(part, parsed_workflows)
print(sum_)

