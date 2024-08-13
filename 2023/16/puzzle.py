#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()

if input_list[-1] == "\n":
    input_list = input_list[:-1]

input_list = [r[:-1] if r.endswith("\n") else r for r in input_list]


def move_pointer(
        puzzle_input: list[str],
        pointer: tuple[int, int, str],
    ) -> list[tuple[int, int, str]]:
    """Return a list of new pointers"""
    i, j, direction = pointer
    tile = puzzle_input[i][j]
    if tile == ".":
        if direction == "up":
            new_i, new_j = i-1, j
        elif direction == "down":
            new_i, new_j = i+1, j
        elif direction == "right":
            new_i, new_j = i, j+1
        else:  # left
            new_i, new_j = i, j-1
        if new_i < 0 or new_i+1 > len(puzzle_input):
            return []
        elif new_j < 0 or new_j+1 > len(puzzle_input[new_i]):
            return []
        return [(new_i, new_j, direction)]
    elif tile == "/":
        if direction == "up":
            new_direction = "right"
            new_i, new_j = i, j+1
        elif direction == "down":
            new_direction = "left"
            new_i, new_j = i, j-1
        elif direction == "right":
            new_direction = "up"
            new_i, new_j = i-1, j
        else:  # left
            new_direction = "down"
            new_i, new_j = i+1, j
        if new_i < 0 or new_i+1 > len(puzzle_input):
            return []
        elif new_j < 0 or new_j+1 > len(puzzle_input[new_i]):
            return []
        return [(new_i, new_j, new_direction)]
    elif tile == "\\":
        if direction == "up":
            new_direction = "left"
            new_i, new_j = i, j-1
        elif direction == "down":
            new_direction = "right"
            new_i, new_j = i, j+1
        elif direction == "right":
            new_direction = "down"
            new_i, new_j = i+1, j
        else:  # left
            new_direction = "up"
            new_i, new_j = i-1, j
        if new_i < 0 or new_i+1 > len(puzzle_input):
            return []
        elif new_j < 0 or new_j+1 > len(puzzle_input[new_i]):
            return []
        return [(new_i, new_j, new_direction)]
    elif tile == "|":
        if direction in ["up", "down"]:
            if direction == "up":
                new_i, new_j = i-1, j
            else:
                new_i, new_j = i+1, j
            if new_i < 0 or new_i+1 > len(puzzle_input):
                return []
            elif new_j < 0 or new_j+1 > len(puzzle_input[new_i]):
                return []
            return [(new_i, new_j, direction)]
        else:  # left and right
            new_i1, new_j1, new_direction1 = i-1, j, "up"
            new_i2, new_j2, new_direction2 = i+1, j, "down"
            new_pointers: list[tuple[int, int, str]] = []
            if new_i1 < 0 or new_i1+1 > len(puzzle_input):
                pass
            elif new_j1 < 0 or new_j1 > len(puzzle_input[new_i1]):
                pass
            else:
                new_pointers.append((new_i1, new_j1, new_direction1))
            if new_i2 < 0 or new_i2+1 > len(puzzle_input):
                pass
            elif new_j2 < 0 or new_j2+1 > len(puzzle_input[new_i2]):
                pass
            else:
                new_pointers.append((new_i2, new_j2, new_direction2))
            return new_pointers
    else:  # -
        if direction in ["left", "right"]:
            if direction == "left":
                new_i, new_j = i, j-1
            else:
                new_i, new_j = i, j+1
            if new_i < 0 or new_i+1 > len(puzzle_input):
                return []
            elif new_j < 0 or new_j+1 > len(puzzle_input[new_i]):
                return []
            return [(new_i, new_j, direction)]
        else:  # up and down
            new_i1, new_j1, new_direction1 = i, j-1, "left"
            new_i2, new_j2, new_direction2 = i, j+1, "right"
            new_pointers: list[tuple[int, int, str]] = []
            if new_i1 < 0 or new_i1+1 > len(puzzle_input):
                pass
            elif new_j1 < 0 or new_j1 > len(puzzle_input[new_i1]):
                pass
            else:
                new_pointers.append((new_i1, new_j1, new_direction1))
            if new_i2 < 0 or new_i2+1 > len(puzzle_input):
                pass
            elif new_j2 < 0 or new_j2+1 > len(puzzle_input[new_i2]):
                pass
            else:
                new_pointers.append((new_i2, new_j2, new_direction2))
            return new_pointers


def move_pointers(
        puzzle_input: list[str],
        beam_pointers: list[tuple[int, int, str]],
        energised_tiles: list[tuple[int, int]],
        puzzle_memory: list[list[list[str]]]
    ) -> tuple[list[tuple[int, int, str]], list[tuple[int, int]], list[list[list[str]]]]:
    """Returns the new pointers and energised tiles lists"""
    new_beam_pointers: list[tuple[int, int, str]] = []
    new_energised_tiles: list[tuple[int, int]] = energised_tiles.copy()

    for pointer in beam_pointers:
        if (pointer[0], pointer[1]) not in new_energised_tiles:
            new_energised_tiles.append((pointer[0], pointer[1]))
        if pointer[2] not in puzzle_memory[pointer[0]][pointer[1]]:
            puzzle_memory[pointer[0]][pointer[1]].append(pointer[2])
            new_beam_pointers.extend(move_pointer(puzzle_input, pointer))

    return new_beam_pointers, new_energised_tiles, puzzle_memory


def count_energised(
        puzzle_input: list[str],
        start: tuple[int, int, str] | None = None
    ) -> int:
    """Return the number of energised tiles"""
    if start is None:
        start = (0, 0, "right")
    beam_pointers: list[tuple[int, int, str]] = [start]  # under the form (i, j, direction)
    energised_tiles: list[tuple[int, int]] = []  # under the form (i, j)
    puzzle_memory: list[list[list[str]]] = [
        [[] for _ in range(len(puzzle_input[i]))] for i in range(len(puzzle_input))
    ]
    while len(beam_pointers) != 0:
        # print(beam_pointers)
        beam_pointers, energised_tiles, puzzle_memory = move_pointers(
            puzzle_input, beam_pointers, energised_tiles, puzzle_memory
        )
    return len(energised_tiles)


def part2(puzzle_input: list[str]):
    """Return the max number of energised tiles.
    Warning: this is pure bruteforce. It took 8m40s on my PC"""
    max_ = 0
    for i in range(len(puzzle_input)):
        print(i)
        # rows
        start = (i, 0, "right")
        energised1 = count_energised(puzzle_input, start)
        start2 = (i, len(puzzle_input[i])-1, "left")
        energised2 = count_energised(puzzle_input, start2)
        if energised1 > max_:
            if energised2 > energised1:
                max_ = energised2
            else:
                max_ = energised1
    
    for j in range(len(puzzle_input[0])):
        print(j)
        # columns
        start = (0, j, "down")
        energised1 = count_energised(puzzle_input, start)
        start2 = (len(puzzle_input)-1, j, "up")
        energised2 = count_energised(puzzle_input, start2)
        if energised1 > max_:
            if energised2 > energised1:
                max_ = energised2
            else:
                max_ = energised1
    return max_


print(count_energised(input_list))
print(part2(input_list))
