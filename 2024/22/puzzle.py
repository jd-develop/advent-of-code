#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def open_input(input_f: str = "input") -> str:
    """Open the input and return the list of lines (without newlines)"""
    with open(input_f, "r", encoding="utf-8") as input_fp:
        input_str = input_fp.read()
    return input_str


def parse(puzzle_input: str) -> list[int]:
    """Parses the input into a list of secret numbers"""
    return list(map(int, puzzle_input.splitlines()))


def next_secret_number(secret_number: int) -> int:
    secret_number = ((secret_number*64)^secret_number)%16777216
    secret_number = ((secret_number//32)^secret_number)%16777216
    secret_number = ((secret_number*2048)^secret_number)%16777216
    return secret_number


def solve_puzzle1(secret_numbers: list[int]) -> int:
    """Solves puzzle 1"""
    result = 0
    for number in secret_numbers:
        for _ in range(2000):
            number = next_secret_number(number)
        result += number
    return result


def best_sequences_for_buyer(prices: list[int]) -> set[tuple[int, int, int, int]]:
    maximum = max(prices[4:])
    result: set[tuple[int, int, int, int]] = set()

    for i in range(4, len(prices)):
        if prices[i] == maximum:
            last_changes = (prices[i-3]-prices[i-4], prices[i-2]-prices[i-3], prices[i-1]-prices[i-2], prices[i]-prices[i-1])
            result.add(last_changes)

    return result


def how_many_bananas_for_sequence(sequence: tuple[int, int, int, int], all_prices: list[list[int]], all_changes: list[list[tuple[int, int, int, int]]]):
    total = 0
    for i, prices in enumerate(all_prices):
        if sequence in all_changes[i]:
            total += prices[all_changes[i].index(sequence)]
    return total


def solve_puzzle2(secret_numbers: list[int]) -> int:
    """Solves puzzle 2"""
    overall_best_sequences: set[tuple[int, int, int, int]] = set()
    all_prices: list[list[int]] = []
    for secret_number in secret_numbers:
        prices = [secret_number%10]
        for _ in range(2000):
            secret_number = next_secret_number(secret_number)
            prices.append(secret_number%10)
        all_prices.append(prices)

    for prices in all_prices:
        overall_best_sequences = overall_best_sequences.union(best_sequences_for_buyer(prices))

    all_changes: list[list[tuple[int, int, int, int]]] = []
    for prices in all_prices:
        changes = [(99, 99, 99, 99)]
        for i in range(1, len(prices)):
            last_change = changes[-1]
            change = (last_change[1], last_change[2], last_change[3], prices[i]-prices[i-1])
            changes.append(change)
        all_changes.append(changes)

    max_overall_bananas = 0
    for_wich_seq: tuple[int, int, int, int] = (0, 0, 0, 0)
    for i, seq in enumerate(overall_best_sequences):
        print(f"séquence {i}/{len(overall_best_sequences)}")
        total = how_many_bananas_for_sequence(seq, all_prices, all_changes)
        if total > max_overall_bananas:
            max_overall_bananas = total
            for_wich_seq = seq

    print(for_wich_seq)
    return max_overall_bananas


puzzle_input = open_input()
parsed_input = parse(puzzle_input)

print(solve_puzzle1(parsed_input))
# part2 takes 26 minutes on my machine – but that’s fiiiiiiiine, we’re sunday:
# we have plenty of time
print(solve_puzzle2(parsed_input))

