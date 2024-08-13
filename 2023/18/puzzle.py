#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse(puzzle_input: list[str]):
    """Return a list of tuples (str, int, str), for instance ("R", 6, "#70c710")"""
    list_to_return = []
    for line in puzzle_input:
        if line == "\n":
            continue
        line = line.split()
        direction = line[0]
        meters = int(line[1])
        color = line[2]
        if color.endswith("\n"):
            color = color[:-1]
        color = color[1:-1]
        list_to_return.append((direction, meters, color))
    return list_to_return


def area(parsed_input):
    """Return the area"""
    list_of_points = [(0, 0)]
    current_point = (0, 0)
    perimeter = 0
    shoelace_area = 0
    for direction, meters, _ in parsed_input:
        perimeter += meters
        x, y = current_point
        last_point = current_point
        x1, y1 = last_point
        if direction == "U":
            x -= meters
        elif direction == "D":
            x += meters
        elif direction == "L":
            y -= meters
        elif direction == "R":
            y += meters
        current_point = (x, y)
        list_of_points.append(current_point)
        shoelace_area += (x1*y-y1*x)/2
    return int(abs(shoelace_area) + (perimeter/2) + 1)


def parse_for_part2(parsed_input):
    """Return the parsed input for part2"""
    list_to_return = []
    for _, __, color in parsed_input:
        color = color[1:]
        distance = color[:5]
        direction = color[-1]
        true_direction = "RDLU"[int(direction)]
        list_to_return.append((true_direction, int(distance, base=16), color))
    return list_to_return


parsed_list = parse(input_list)
print(area(parsed_list))
parsed_for_part2 = parse_for_part2(parsed_list)
print(area(parsed_for_part2))

