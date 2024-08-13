#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse(list_to_parse: list[str]) -> list[tuple[str, int]]:
    """Parse the input list, returns a list of tuples where ewach tuple is (hand: str, bid: int)."""
    list_to_return: list[tuple[str, int]] = []
    for line in list_to_parse:
        if line == "\n":
            continue
        if line.endswith("\n"):
            line = line[:-1]
        line = line.split()
        hand = line[0]
        bid = int(line[1])
        list_to_return.append((hand, bid))
    return list_to_return


def find_type(hand: tuple[str, int], part2: bool = False) -> int:
    """Return the number corresponding to the type.
    1 for High Card (5 types)
    2 for One Pair (4 types)
    3 for Two Pair (3 types)
    4 for Three of a Kind (3 types)
    5 for Full House (2 types)
    6 for Four of a Kind (2 types)
    7 for Five of a Kind (1 type)
    """
    cards_in_hand = {}
    for card in hand[0]:
        try:
            cards_in_hand[card] += 1
        except KeyError:
            cards_in_hand[card] = 1
    if part2 and hand[0] != "JJJJJ" and "J" in cards_in_hand.keys():
        number_of_jokers = cards_in_hand["J"]
        del cards_in_hand["J"]
        keys = list(cards_in_hand.keys())
        max_card_in_hand = cards_in_hand[keys[0]]
        max_card = keys[0]
        for k in keys:
            if cards_in_hand[k] > max_card_in_hand:
                max_card_in_hand = cards_in_hand[k]
                max_card = k
        cards_in_hand[max_card] += number_of_jokers
    how_may_cards_type = len(cards_in_hand.keys())
    if how_may_cards_type == 5:
        return 1
    elif how_may_cards_type == 4:
        return 2
    elif how_may_cards_type == 3:
        types = sorted(cards_in_hand.values())
        if types == [1, 1, 3]:
            return 4
        else:  # types == [1, 2, 2]:
            return 3
    elif how_may_cards_type == 2:
        types = sorted(cards_in_hand.values())
        if types == [2, 3]:
            return 5
        else:  # types == [1, 4]:
            return 6
    else:
        return 7


def card_to_int(card: str, part2: bool = False) -> int:
    """Return an int corresponding to the card"""
    if card.isnumeric():
        return int(card)
    if card == "T":
        return 10
    elif card == "J":
        return 11 if not part2 else -1
    elif card == "Q":
        return 12
    elif card == "K":
        return 13
    else:
        return 14


def higher_strenght(hand1: tuple[str, int], hand2: tuple[str, int], part2: bool = False) -> bool:
    """Return True if hand1 > hand2"""
    type_hand1 = find_type(hand1, part2)
    type_hand2 = find_type(hand2, part2)
    if type_hand1 > type_hand2:
        return True
    elif type_hand1 < type_hand2:
        return False
    # type_hand1 == type_hand2
    for i in range(5):
        card1 = card_to_int(hand1[0][i], part2)
        card2 = card_to_int(hand2[0][i], part2)
        if card1 > card2:
            return True
        elif card1 < card2:
            return False
    raise ValueError("both hands are equals")


def merge_sort(target_list: list[tuple[str, int]], part2: bool = False):
    target_list_ = target_list.copy()

    if len(target_list_) == 1:
        return target_list_
    middle_i = len(target_list_) // 2
    array_left = merge_sort(target_list_[:middle_i], part2)
    array_right = merge_sort(target_list_[middle_i:], part2)
    target_list_ = merge(array_left, array_right, part2)

    return target_list_


def merge(array1, array2, part2: bool = False):
    array_final = [0]*(len(array1) + len(array2))
    i = j = k = 0  # `i` is index in array1, `j` in array2 and `k` in array_final
    while i < len(array1) and j < len(array2):
        if not higher_strenght(array1[i], array2[j], part2):
            array_final[k] = array1[i]
            i += 1
        else:
            array_final[k] = array2[j]
            j += 1
        k += 1

    while i < len(array1):
        array_final[k] = array1[i]
        i += 1
        k += 1

    while j < len(array2):
        array_final[k] = array2[j]
        j += 1
        k += 1

    return array_final



parsed_list = parse(input_list)
sorted_list = merge_sort(parsed_list)
sum_ = 0
for i, hand in enumerate(sorted_list):
    sum_ += (i+1) * (hand[1])
    print(f"{i+1}\t{hand}\t{''.join(sorted(hand[0]))}\t{find_type(hand)}\t{(i+1) * hand[1]}\t{sum_}")
print(sum_)

sorted_list = merge_sort(parsed_list, True)
sum_ = 0
for i, hand in enumerate(sorted_list):
    sum_ += (i+1) * (hand[1])
    print(f"{i+1}\t{hand}\t{''.join(sorted(hand[0]))}\t{find_type(hand, True)}\t{(i+1) * hand[1]}\t{sum_}")
print(sum_)

