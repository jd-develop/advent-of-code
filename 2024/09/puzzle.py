#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[int], list[tuple[int, int]]]:
    """Parses the input into a list of ints (IDs). ID is -1 for a free space"""
    res1: list[int] = []
    res2: list[tuple[int, int]] = []
    for i, c in enumerate(puzzle_input):
        if c == "\n": continue
        if i%2 == 0:
            res2.append((i//2, int(c)))
            for _ in range(int(c)):
                res1.append(i//2)
        else:
            res2.append((-1, int(c)))
            for _ in range(int(c)):
                res1.append(-1)
    return res1, res2


def solve_puzzle1(files: list[int]) -> int:
    """Solves puzzle 1."""
    for i in range(len(files)-1, -1, -1):
        if files[i] == -1:
            continue
        first_available_space = files.index(-1)
        if first_available_space == i+1:
            break
        files[first_available_space] = files[i]
        files[i] = -1
    return sum(i*files[i] for i in range(len(files)) if files[i] != -1)


def move_block_and_clean_mess(files: list[tuple[int, int]], already_seen: set[int]) -> tuple[list[tuple[int, int]], set[int]]:
    id_seen = -1
    for i in range(len(files)-1, -1, -1):
        #print(files[i])
        if files[i][0] == -1: continue
        if files[i][0] in already_seen: continue
        file_len = files[i][1]
        id_seen = files[i][0]
        for j in range(len(files)):
            #print("  ", files[j])
            if j > i: continue
            if files[j][0] != -1: continue
            if files[j][1] >= file_len:
                space_len = files[j][1]
                files.insert(j, files[i])
                files[j+1] = (-1, space_len-file_len)
                files[i+1] = (-1, file_len)
                break
        break
    #print(id_seen)
    if id_seen == -1:
        return files, already_seen

    already_seen.add(id_seen)
    new_files: list[tuple[int, int]] = []
    for id_, len_ in files:
        #print(id_, len_)
        if len_ == 0: continue
        #print(id_, len_)
        if id_ == -1:
            #print(new_files[-1])
            if len(new_files) != 0 and new_files[-1][0] == -1:
                new_files[-1] = (-1, new_files[-1][1]+len_)
                continue
        new_files.append((id_, len_))
    if new_files[-1][0] == -1:
        new_files.pop(-1)
    #print(f"we have {new_files}")
    return new_files, already_seen


def solve_puzzle2(files: list[tuple[int, int]]) -> int:
    """Solves puzzle 1."""
    print("je commence la partie 2")
    already_seen: set[int] = set()
    while 0 not in already_seen:
        #print(files, already_seen)
        files, already_seen = move_block_and_clean_mess(files, already_seen)

    #print(files)
    #for id_, len_ in files:
    #    if id_ == -1: print("."*len_, end="")
    #    else: print(int(id_)*len_, end="")
    #print()

    total = 0
    i = 0
    for id_, len_ in files:
        if id_ == -1:
            i += len_
            continue
        for _ in range(len_):
            total += i*id_
            i += 1

    return total


puzzle_input = open_input()
parsed_input1, parsed_input2 = parse(puzzle_input)
print(solve_puzzle1(parsed_input1))
print(solve_puzzle2(parsed_input2))

