#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[str]:
    return puzzle_input.splitlines()


def tile_to_coord(tile: str, door_code: bool) -> tuple[int, int]:
    return {
        "A": (3, 2),
        "0": (3, 1),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2)
    }[tile] if door_code else {
        "A": (0, 2),
        "^": (0, 1),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2)
    }[tile]


def sequence(code: str, door_code: bool) -> str:
    #gap = (3, 0) if door_code else (0, 0)
    current_tile = tile_to_coord("A", door_code)
    result: str = ""
    for char in code:
        char_coords = tile_to_coord(char, door_code)
        if char_coords == current_tile:
            result += "A"
            continue

        diffx = char_coords[0] - current_tile[0]
        diffy = char_coords[1] - current_tile[1]

        #possibility = ""
        #if diffx < 0:
        #    possibility += -diffx*"^"
        #else:
        #    possibility += diffx*"v"
        #if diffy < 0:
        #    possibility += -diffy*"<"
        #else:
        #    possibility += diffy*">"

        #all_possibilities = itertools.permutations(possibility, len(possibility))
        #if care_about_gaps:
        #    real_possibilities: list[str] = []
        #    for p in all_possibilities:
        #        px, py = current_tile
        #        gap_found = False
        #        for c in p:
        #            if c == "<": py -= 1
        #            elif c == ">": py += 1
        #            elif c == "^": px -= 1
        #            elif c == "v": px += 1
        #            if (px, py) == gap:
        #                gap_found = True
        #                break
        #        if gap_found: continue
        #        real_possibilities.append("".join(p))
        #else:
        #    real_possibilities = list(map(lambda x: "".join(x), all_possibilities))

        #assert len(real_possibilities) != 0, (possibility, list(all_possibilities), current_tile, char_coords)

        #if len(result) == 0:
        #    result = real_possibilities
        #    for i in range(len(result)):
        #        result[i] = result[i]+"A"
        #else:
        #    new_result: list[str] = []
        #    for res in result:
        #        for possibility in real_possibilities:
        #            new_result.append(res+possibility+"A")
        #    result = new_result

        if door_code:
            if diffx < 0:
                result += -diffx*"^"
            if diffy < 0:
                result += -diffy*"<"
            else:
                result += diffy*">"
            if diffx > 0:
                result += diffx*"v"
        else:
            if diffx > 0:
                result += diffx*"v"
            if diffy < 0:
                result += -diffy*"<"
            else:
                result += diffy*">"
            if diffx < 0:
                result += -diffx*"^"
        result += "A"
        current_tile = char_coords

    return result


def solve_puzzle1(codes: list[str]) -> int:
    """Solves puzzle 1"""
    result = 0
    for code in codes:
        first_robot_sequence = sequence(code, True)
        second_robot_sequence = sequence(first_robot_sequence, False)
        my_sequence = sequence(second_robot_sequence, False)
        print(my_sequence)
        print(len(my_sequence))

        result += len(my_sequence)*int(code[:-1])
    return result


# def solve_puzzle2() -> int:
#     """Solves puzzle 2"""

puzzle_input = open_input("example1.input")
parsed_input = parse(puzzle_input)

print(solve_puzzle1(parsed_input))
# print(solve_puzzle2(parsed_input))

