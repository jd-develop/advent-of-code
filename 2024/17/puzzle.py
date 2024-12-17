#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> tuple[int, int, int, list[int]]:
    """Returns tha values of A, B and C then the list of instructions
       (opcodes/operands)"""
    a = -1
    b = -1
    c = -1
    instructions: list[int] = []

    for line in puzzle_input.splitlines():
        if line == "": continue
        if line.startswith("Register A: "):
            a = int(line[12:])
        elif line.startswith("Register B: "):
            b = int(line[12:])
        elif line.startswith("Register C: "):
            c = int(line[12:])
        else:
            instructions = list(map(int, line[9:].split(",")))

    assert a != -1
    assert b != -1
    assert c != -1
    return a, b, c, instructions


def combo(a: int, b: int, c: int, op: int) -> int:
    """Returns the value of the compo operator 'op'"""
    if 0 <= op <= 3:
        return op
    if op == 4:
        return a
    if op == 5:
        return b
    if op == 6:
        return c
    assert False, op


def solve_puzzle1(a: int, b: int, c: int, instructions: list[int], debug: bool = False, p2: bool = False) -> list[int]:
    """Solves puzzle 1"""
    instruction_ptr = 0
    n_op = len(instructions)
    stdout: list[int] = []
    out_ctr = 0

    while instruction_ptr < n_op:
        opcode = instructions[instruction_ptr]
        operand = instructions[instruction_ptr+1]
        if opcode == 0:  # ADV
            if debug: print(f"ADV {operand}")
            numerator = a
            denominator = 2 ** combo(a, b, c, operand)
            a = numerator // denominator
        elif opcode == 1:  # BXL
            if debug: print(f"BXL {operand}")
            b ^= operand
        elif opcode == 2:  # BST
            if debug: print(f"BST {operand}")
            b = combo(a, b, c, operand) % 8
        elif opcode == 3:  # JNZ
            if debug: print(f"JNZ {operand}")
            if a != 0:
                instruction_ptr = operand-2  # -2 because there’s a +2 at the end of the loop
        elif opcode == 4:  # BXC
            if debug: print(f"BXC {operand}")
            b ^= c
        elif opcode == 5:  # OUT
            if debug: print(f"OUT {operand}")
            out = combo(a, b, c, operand)%8
            if p2 and out != instructions[out_ctr]:
                break
            stdout.append(out)
            out_ctr += 1
        elif opcode == 6:  # BDV
            if debug: print(f"BDV {operand}")
            numerator = a
            denominator = 2 ** combo(a, b, c, operand)
            b = numerator // denominator
        elif opcode == 7:  # CDV
            if debug: print(f"CDV {operand}")
            numerator = a
            denominator = 2 ** combo(a, b, c, operand)
            c = numerator // denominator
        else:
            assert False, opcode

        instruction_ptr += 2

    return stdout


def solve_puzzle2(b: int, c: int, instructions: list[int], debug: bool = False) -> int:
    """Solves puzzle 2"""
    i = 0
    while True:
        if solve_puzzle1(i, b, c, instructions, debug) == instructions:
            return i
        i += 1


puzzle_input = open_input()
a, b, c, instructions = parse(puzzle_input)

stdout = solve_puzzle1(a, b, c, instructions)

for i, res in enumerate(stdout):
    if i == len(stdout)-1:
        print(res)
    else:
        print(res, end=",")

print(solve_puzzle2(b, c, instructions))

