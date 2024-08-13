#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.read().split("\n")


def find_start(input_list):
    """Return the tuple of indexes of the start point"""
    for i, line in enumerate(input_list):
        if "S" not in line:
            continue
        return (i, line.index("S"))


def find_start_nex_hop(input_list: list[str], start_index: tuple[int, int]):
    """Return the coordinates of the next hop after start"""
    s_i, s_j = start_index
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not 0 <= s_i + i < len(input_list):
                continue
            if not 0 <= s_j + j < len(input_list[0]):
                continue
            pipe = input_list[s_i+i][s_j+j]
            if pipe == "." or pipe == "S":
                continue
            
            condition1 = pipe == "-" and i == 0
            condition2 = pipe == "|" and j == 0
            condition3 = pipe in "J7" and i == 0 and j == 1
            condition4 = pipe in "LF" and i == 0 and j == -1
            condition5 = pipe in "JL" and i == 1 and j == 0
            condition6 = pipe in "7F" and i == -1 and j == 0
            if condition1 or condition2 or condition3 or condition4 or condition5 or condition6:
                return s_i+i, s_j+j
    assert False, "error"


def find_start_type(input_list):
    """Return -, |, J, L, F or 7 depending on start’s type"""
    s_i, s_j = find_start(input_list)
    start_surroundings = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not 0 <= s_i + i < len(input_list):
                continue
            if not 0 <= s_j + j < len(input_list[0]):
                continue
            pipe = input_list[s_i+i][s_j+j]
            if pipe == "." or pipe == "S":
                continue
            
            condition1 = pipe == "-" and i == 0
            condition2 = pipe == "|" and j == 0
            condition3 = pipe in "J7" and i == 0 and j == 1
            condition4 = pipe in "LF" and i == 0 and j == -1
            condition5 = pipe in "JL" and i == 1 and j == 0
            condition6 = pipe in "7F" and i == -1 and j == 0
            if condition1 or condition2 or condition3 or condition4 or condition5 or condition6:
                start_surroundings.append((i, j))
    assert len(start_surroundings) == 2, "error"
    i, j = start_surroundings[0]
    k, l = start_surroundings[1]
    if (i, j) == (0, -1) and (k, l) == (0, 1):
        return "-"
    elif (i, j) == (-1, 0) and (k, l) == (1, 0):
        return "|"
    elif (i, j) == (-1, 0) and (k, l) == (0, 1):
        return "L"
    elif (i, j) == (-1, 0) and (k, l) == (0, -1):
        return "J"
    elif (i, j) == (0, 1) and (k, l) == (1, 0):
        return "F"
    elif (i, j) == (0, -1) and (k, l) == (1, 0):
        return "7"
    else:
        assert False, "error"


def find_lenght(input_list: list[str]):
    """Find the total lenght of the loop"""
    part2list = [["."]*len(input_list[0]) for i in range(len(input_list))]

    start_index = find_start(input_list)
    part2list[start_index[0]][start_index[1]] = find_start_type(input_list)
    next_hop = find_start_nex_hop(input_list, start_index)

    current = input_list[next_hop[0]][next_hop[1]]
    last_index = start_index
    current_index = next_hop

    counter = 1

    while current != "S":
        counter += 1

        i, j = current_index
        part2list[i][j] = current
        if current == "-":
            possible_indexes = [(i, j-1), (i, j+1)]
        elif current == "|":
            possible_indexes = [(i-1, j), (i+1, j)]
        elif current == "L":
            possible_indexes = [(i-1, j), (i, j+1)]
        elif current == "J":
            possible_indexes = [(i-1, j), (i, j-1)]
        elif current == "7":
            possible_indexes = [(i+1, j), (i, j-1)]
        elif current == "F":
            possible_indexes = [(i+1, j), (i, j+1)]

        if possible_indexes[0] == last_index:
            last_index = current_index
            current_index = possible_indexes[1]
            current = input_list[possible_indexes[1][0]][possible_indexes[1][1]]
        else:
            last_index = current_index
            current_index = possible_indexes[0]
            current = input_list[possible_indexes[0][0]][possible_indexes[0][1]]
    
    return counter, part2list


def how_many_inside_the_loop(part2list):
    """Returns how may tiles are inside the loop"""
    # for line in part2list:
    #     print("".join(line))
    how_many = 0
    for line in part2list:
        line_count = 0
        for char in line:
            if char in "|LJ":
                # print(f"\033[94m{char}\033[0m", end="")
                line_count += 1
            elif char == ".":
                if line_count%2 == 1:
                    # print(f"\033[91m{char}\033[0m", end="")
                    how_many += 1
                # else:
                #     print(char, end="")
            # else:
            #     print(char, end="")
        # print()
    return how_many


lenght, part2list = find_lenght(input_list)
print(lenght//2)
print(how_many_inside_the_loop(part2list))

