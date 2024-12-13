#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import math
import sympy


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[tuple[(int, int, int, int, int, int)]]:  # A(x), A(y), B(x), B(y), P(x), P(y)
    """parses the input"""
    res: list[tuple[(int, int, int, int, int, int)]] = []
    for machine in puzzle_input.split("\n\n"):
        machine = machine.split("\n")

        a = machine[0].split(", ")
        a_x = int(a[0][12:])
        a_y = int(a[1][2:])

        b = machine[1].split(", ")
        b_x = int(b[0][12:])
        b_y = int(b[1][2:])

        p = machine[2].split(", ")
        p_x = int(p[0][9:])
        p_y = int(p[1][2:])

        res.append((a_x, a_y, b_x, b_y, p_x, p_y))
    return res


def solve_puzzle1(machines: list[tuple[(int, int, int, int, int, int)]]) -> int:
    """Solves puzzle 1."""
    total = 0
    for a_x, a_y, b_x, b_y, p_x, p_y in machines:
        x, y = sympy.symbols("x, y", integers=True)
        solutions: set[tuple[sympy.Add, sympy.Add]] = sympy.solvers.diophantine(a_x*x + b_x*y - p_x)

        #print(solutions)
        if len(solutions) == 0:
            continue
        add_1, add_2 = solutions.pop()
        both_solutions = sympy.solvers.solve(add_1*a_y + add_2*b_y - p_y)
        if len(both_solutions) == 0:
            continue

        # times_a = p+kq
        # times_b = p'+kq'
        if isinstance(add_1, sympy.core.symbol.Symbol):
            pa = 0
            qa = 1
            t0 = add_1
        else:
            pa = int(add_1.args[0])
            if isinstance(add_1.args[1], sympy.core.symbol.Symbol):
                qa = 1
                t0 = add_1.args[1]
            else:
                qa = int(add_1.args[1].args[0])
                t0 = add_1.args[1].args[1]
        if isinstance(add_2, sympy.core.symbol.Symbol):
            pb = 0
            qb = 1
        else:
            pb = int(add_2.args[0])
            if isinstance(add_2.args[1], sympy.core.symbol.Symbol):
                qb = 1
            else:
                qb = int(add_2.args[1].args[0])

        minimum = -1
        for sol in both_solutions:
            times_a = pa+sol*qa
            times_b = pb+sol*qb
            if times_a < 0: continue
            if times_b < 0: continue

            assert times_a*a_x + times_b*b_x == p_x
            assert times_a*a_y + times_b*b_y == p_y

            cost = times_a*3 + times_b
            if cost < minimum or minimum == -1:
               minimum = cost

        minimum_working = -1
        for i in range(100):
            for j in range(100):
                if i*a_x + j*b_x != p_x: continue
                if i*a_y + j*b_y != p_y: continue
                cost = i*3 + j
                if cost < minimum_working or minimum_working == -1:
                   minimum_working = cost

        if minimum != minimum_working:
            print(minimum, minimum_working, both_solutions, pa+both_solutions[0]*qa, pb+both_solutions[0]*qb, pa, qa, pb, qb)

        total += minimum if minimum != -1 else 0

    return total

#def solve_puzzle2() -> int:
#    """Solves puzzle 2."""


puzzle_input = open_input()
parsed_input = parse(puzzle_input)
print(solve_puzzle1(parsed_input))
#print(solve_puzzle2(parsed_input))

