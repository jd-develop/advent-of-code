#!/usr/bin/env python3
# coding:utf-8

with open("input", 'r+', encoding="UTF-8") as input_file:
    raw_input = input_file.readlines()

elves = [0]
index = 0
for line in raw_input:
    if line == '\n':
        index += 1
        elves.append(0)
    else:
        if line.endswith('\n'):
            line = line[:-1]
        elves[index] += int(line)


print(max(elves))

# find the top three
elves = sorted(elves, reverse=True)
print(elves[0], elves[1], elves[2])
print(sum([elves[0], elves[1], elves[2]]))
