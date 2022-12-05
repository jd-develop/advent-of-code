#!/usr/bin/env python3
# coding:utf-8

def void(*args):
    return args


with open("input.txt", 'r+', encoding="UTF-8") as input_file:
    raw_input = input_file.readlines()

stacks: list[list] = []
for line in raw_input:
    line = line.replace('\n', '')
    if "[" in line:  # stacks configuration
        readable_line = []
        for i in range(1, len(line), 4):
            readable_line.append(line[i])
        for index, item in enumerate(readable_line):
            if item != " ":
                try:
                    stacks[index].insert(0, item)
                except IndexError:
                    stacks.append([item])
            else:
                try:
                    void(stacks[index])
                except IndexError:
                    stacks.append([])

for line in raw_input:
    if line.startswith("move"):  # we made our stacks, we can parse moves
        line_l = line.split()
        quantity = int(line_l[1])
        origin = int(line_l[3]) - 1
        destination = int(line_l[5]) - 1
        for i in range(quantity):
            stacks[destination].append(stacks[origin].pop(-1))

result = ""
for i in stacks:
    result += i[-1]

print(result)

stacks: list[list] = []
for line in raw_input:
    line = line.replace('\n', '')
    if "[" in line:  # stacks configuration
        readable_line = []
        for i in range(1, len(line), 4):
            readable_line.append(line[i])
        for index, item in enumerate(readable_line):
            if item != " ":
                try:
                    stacks[index].insert(0, item)
                except IndexError:
                    stacks.append([item])
            else:
                try:
                    void(stacks[index])
                except IndexError:
                    stacks.append([])

for line in raw_input:
    if line.startswith("move"):
        line_l = line.split()
        quantity = int(line_l[1])
        origin = int(line_l[3]) - 1
        destination = int(line_l[5]) - 1
        crates_to_move = stacks[origin][-quantity:]
        stacks[destination].extend(crates_to_move)
        del stacks[origin][-quantity:]


result = ""
for i in stacks:
    result += i[-1]

print(result)
