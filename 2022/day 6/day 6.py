#!/usr/bin/env python3
# coding:utf-8

with open("input.txt", 'r+', encoding="UTF-8") as input_file:
    raw_input = input_file.read()

raw_input.replace('\n', '')
for i, char in enumerate(raw_input):
    if i >= 4:
        current_analyze = raw_input[i-4:i]
        # print(current_analyze)
        # print(set(current_analyze))
        if len(set(list(current_analyze))) == 4:
            print(i)
            break

for i, char in enumerate(raw_input):
    if i >= 14:
        current_analyze = raw_input[i-14:i]
        # print(current_analyze)
        # print(set(current_analyze))
        if len(set(list(current_analyze))) == 14:
            print(i)
            break
