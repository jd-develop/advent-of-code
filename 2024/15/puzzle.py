#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# DIRECTIONS :
# 0 for right
# 1 for down
# 2 for left
# 3 for up

# TILES :
# part 1 :
# 0 for wall
# 1 for box
# 2 for free space
# part 2 :
# 0 for wall
# 1 for the left part of a box
# 2 for the right part of a box
# 3 for free space
import os
import time


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[list[list[int]], tuple[int, int], list[tuple[int, int]]]:
    """Returns the puzzle input under a 2D list of ints (the map), a tuple
       (int, int) (the robot’s starting position) and a list of tuples
       (int, int) (the moves)
    """
    warehouse: list[list[int]] = []
    robot_pos: tuple[int, int] = (-1, -1)
    moves: list[tuple[int, int]] = []

    for i, line in enumerate(puzzle_input.splitlines()):
        if line == "": continue

        if line.startswith("#"):
            new_line: list[int] = []
            for j, c in enumerate(line):
                new_line.append(
                    0 if c == "#" else
                    1 if c == "O" else
                    2
                )
                if c == "@":
                    robot_pos = (i, j)
            warehouse.append(new_line)
            continue

        for c in line:
            moves.append(
                (0, 1) if c == ">" else
                (1, 0) if c == "v" else
                (0, -1) if c == "<" else
                (-1, 0)
            )

    assert robot_pos != (-1, 1)
    return warehouse, robot_pos, moves


def print_warehouse(warehouse: list[list[int]], robot_pos: tuple[int, int]):
    for i, line in enumerate(warehouse):
        for j, tile in enumerate(line):
            print(
                "@" if (i, j) == robot_pos else
                "#" if tile == 0 else
                "O" if tile == 1 else
                ".",
                end=""
            )
        print()


def solve_puzzle1(
        warehouse: list[list[int]],
        robot_pos: tuple[int, int],
        moves: list[tuple[int, int]]
) -> int:
    """Solves puzzle 1."""
    warehouse = [[tile for tile in line] for line in warehouse]
    robotx, roboty = robot_pos

    for movex, movey in moves:
        new_tile = warehouse[robotx+movex][roboty+movey]
        # wall: do nothing
        if new_tile == 0: continue
        # empty tile: go for it
        if new_tile == 2:
            robotx += movex
            roboty += movey
            continue
        # box…
        assert new_tile == 1

        i = 1
        can_move = True
        first_empty_tile = (-1, -1)
        while True:
            checked_tile = warehouse[robotx + i*movex][roboty + i*movey]
            # if there’s a wall in the way, we can’t move
            if checked_tile == 0:
                can_move = False
                break
            # box: fine, we’ll move it
            if checked_tile == 1:
                i += 1
                continue
            # empty space: that’s where we’re moving all those boxes
            if checked_tile == 2:
                first_empty_tile = (robotx+i*movex, roboty + i*movey)
                break
            i += 1

        if not can_move: continue
        assert first_empty_tile != (-1, -1)
        warehouse[robotx + movex][roboty + movey] = 2
        warehouse[first_empty_tile[0]][first_empty_tile[1]] = 1
        robotx += movex
        roboty += movey

    # calculate GPS coordinates
    gps_sum = 0
    for i, line in enumerate(warehouse):
        for j, tile in enumerate(line):
            if tile != 1: continue
            gps_sum += 100*i + j
    return gps_sum


def print_new_warehouse(warehouse: list[list[int]], robot_pos: tuple[int, int]):
    os.system("clear")
    for i, line in enumerate(warehouse):
        for j, tile in enumerate(line):
            print(
                "@" if (i, j) == robot_pos else
                "#" if tile == 0 else
                "[" if tile == 1 else
                "]" if tile == 2 else
                ".",
                end=""
            )
        print()


def check_tile(
    warehouse: list[list[int]],
    pos_to_check: tuple[int, int],
    direction: int,
) -> tuple[bool, list[tuple[int, int]]]:
    """
        Checks recursively if we can move up (-1) or down (1) from the pos to
        check, and returns a bool (whether we can move or not), and a list of
        all the tiles to move (including the pos to check)
    """
    to_check_x, to_check_y = pos_to_check
    new_tile = warehouse[to_check_x+direction][to_check_y]
    if new_tile == 3:
        return True, [(to_check_x, to_check_y)]
    if new_tile == 0:
        return False, list()
    if new_tile == 1:
        # []
        # ^
        left_ok, left_tiles_to_move = check_tile(warehouse, (to_check_x+direction, to_check_y), direction)
        right_ok, right_tiles_to_move = check_tile(warehouse, (to_check_x+direction, to_check_y+1), direction)
    else:
        assert new_tile == 2
        # []
        #  ^
        left_ok, left_tiles_to_move = check_tile(warehouse, (to_check_x+direction, to_check_y-1), direction)
        right_ok, right_tiles_to_move = check_tile(warehouse, (to_check_x+direction, to_check_y), direction)

    if not left_ok or not right_ok:
        return False, list()
    return True, list(set(left_tiles_to_move+right_tiles_to_move+[(to_check_x, to_check_y)]))


def solve_puzzle2(
        warehouse: list[list[int]],
        robot_pos: tuple[int, int],
        moves: list[tuple[int, int]],
        print_things: bool = False
) -> int:
    """Solves puzzle 2."""
    new_warehouse: list[list[int]] = []

    for line in warehouse:
        new_line: list[int] = []
        for tile in line:
            if tile == 0:
                new_line.append(0)
                new_line.append(0)
            elif tile == 1:
                new_line.append(1)
                new_line.append(2)
            elif tile == 2:
                new_line.append(3)
                new_line.append(3)
        new_warehouse.append(new_line)

    robotx, roboty = robot_pos
    roboty *= 2

    for movex, movey in moves:
        if print_things:
            print_new_warehouse(new_warehouse, (robotx, roboty))
            time.sleep(0.1)
        new_tile = new_warehouse[robotx+movex][roboty+movey]
        # wall: do nothing
        if new_tile == 0: continue
        # empty tile: go for it
        if new_tile == 3:
            robotx += movex
            roboty += movey
            continue
        # box…
        assert new_tile in (1, 2)

        if movex == 0:
            # move left or right
            i = 1
            can_move = True
            first_empty_tile = (-1, -1)
            while True:
                checked_tile = new_warehouse[robotx][roboty + i*movey]
                # if there’s a wall in the way, we can’t move
                if checked_tile == 0:
                    can_move = False
                    break
                # box: fine, we’ll move it
                if checked_tile in (1, 2):
                    i += 1
                    continue
                # empty space: that’s where we’re moving all those boxes
                if checked_tile == 3:
                    first_empty_tile = (robotx, roboty + i*movey)
                    break
                i += 1

            if not can_move: continue
            assert first_empty_tile != (-1, -1)
            new_warehouse[robotx][roboty + movey] = 3
            for j in range(roboty + 2*movey, first_empty_tile[1]+movey, movey):
                if (j - roboty - 2*movey)%2 == max(movey, 0):
                    new_warehouse[robotx][j] = 2
                else:
                    new_warehouse[robotx][j] = 1
            roboty += movey
        else:
            # move up or down
            can_move, all_tiles = check_tile(new_warehouse, (robotx, roboty), movex)
            if not can_move: continue
            all_tiles.sort(key=lambda x: x[0], reverse=bool(max(0, movex)))
            for i, j in all_tiles:
                new_warehouse[i+movex][j] = new_warehouse[i][j]
                new_warehouse[i][j] = 3
            robotx += movex

    if print_things:
        print_new_warehouse(new_warehouse, (robotx, roboty))

    # calculate GPS coordinates
    gps_sum = 0
    for i, line in enumerate(new_warehouse):
        for j, tile in enumerate(line):
            if tile != 1: continue
            gps_sum += 100*i + j
    return gps_sum


puzzle_input = open_input()
warehouse, robot_pos, moves = parse(puzzle_input)
print(solve_puzzle1(warehouse.copy(), robot_pos, moves))
print(solve_puzzle2(warehouse.copy(), robot_pos, moves))

