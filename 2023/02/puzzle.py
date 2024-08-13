#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


# PUZZLE 1
puzzle1_valid_ids = []
for i, line in enumerate(input_list.copy()):
    if line == "\n":
        continue
    game_id = i+1
    line = line[:-1].split("; ")
    line[0] = line[0].split(": ")[1]
    for j, set_of_cubes in enumerate(line):
        line[j] = set_of_cubes.split(", ")
        for k in range(len(line[j])):
            line[j][k] = line[j][k].split()
    # print(line)
    valid_line = True
    for set_of_cubes in line:
        valid_set = True
        for cube_type in set_of_cubes:
            colour = cube_type[1]
            if colour == "red":
                max_cubes = 12
            elif colour == "green":
                max_cubes = 13
            elif colour == "blue":
                max_cubes = 14
            else:
                raise Exception(f"parse error: {colour} is not a valid colour")
            if int(cube_type[0]) > max_cubes:
                valid_set = False
                break
        if not valid_set:
            valid_line = False
            break
    if valid_line:
        puzzle1_valid_ids.append(game_id)
        # print("VALID")
    # else:
    #     print("INVALID")



# PUZZLE 2
powers = []
for i, line in enumerate(input_list.copy()):
    if line == "\n":
        continue
    game_id = i+1
    line = line[:-1].split("; ")
    line[0] = line[0].split(": ")[1]
    for j, set_of_cubes in enumerate(line):
        line[j] = set_of_cubes.split(", ")
        for k in range(len(line[j])):
            line[j][k] = line[j][k].split()
    # print(line)
    maximums = {
        "green": 0,
        "red": 0,
        "blue": 0
    }
    for set_of_cubes in line:
        for cube_type in set_of_cubes:
            colour = cube_type[1]
            if maximums[colour] < int(cube_type[0]):
                maximums[colour] = int(cube_type[0])
    # print(f"max_red  : {maximums['red']}")
    # print(f"max_green: {maximums['green']}")
    # print(f"max_blue : {maximums['blue']}")
    power = maximums['red'] * maximums['green'] * maximums['blue']
    # print(f"power    : {power}")
    powers.append(power)

print(sum(puzzle1_valid_ids))
print(sum(powers))
