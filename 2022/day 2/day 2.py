#!/usr/bin/env python3
# coding:utf-8

with open("input.txt", "r+", encoding="UTF-8") as input_file:
    raw = input_file.readlines()


letters = {
    "A": "pierre",
    "B": "papier",
    "C": "ciseaux",
    "X": "pierre",
    "Y": "papier",
    "Z": "ciseaux",
}

total_score_1 = 0
total_score_me = 0
for line in raw:
    player1 = letters[line[0]]
    me = letters[line[2]]

    result = None
    if player1 == "pierre":
        total_score_1 += 1
        if me == "ciseaux":
            total_score_me += 3
            result = "1"
        elif me == "papier":
            total_score_me += 2
            result = "me"
        else:
            total_score_me += 1
            result = "draw"
    elif player1 == "papier":
        total_score_1 += 2
        if me == "ciseaux":
            total_score_me += 3
            result = "me"
        elif me == "pierre":
            total_score_me += 1
            result = "1"
        else:
            total_score_me += 2
            result = "draw"
    elif player1 == "ciseaux":
        total_score_1 += 3
        if me == "pierre":
            total_score_me += 1
            result = "me"
        elif me == "papier":
            total_score_me += 2
            result = "1"
        else:
            total_score_me += 3
            result = "draw"
    if result == "1":
        total_score_1 += 6
    elif result == "me":
        total_score_me += 6
    else:
        total_score_1 += 3
        total_score_me += 3


print(total_score_me)
print(total_score_1)

# second part
letters = {
    "A": "pierre",
    "B": "papier",
    "C": "ciseaux",
    "X": "perdre",
    "Y": "égalité",
    "Z": "gagner",
}

total_score_1 = total_score_me = 0
for line in raw:
    player1 = letters[line[0]]
    expectation = letters[line[2]]

    me = None
    if player1 == "pierre":
        if expectation == "perdre":
            me = "ciseaux"
        elif expectation == "gagner":
            me = "papier"
        else:
            me = "pierre"
    elif player1 == "papier":
        if expectation == "perdre":
            me = "pierre"
        elif expectation == "gagner":
            me = "ciseaux"
        else:
            me = "papier"
    else:
        if expectation == "perdre":
            me = "papier"
        elif expectation == "gagner":
            me = "pierre"
        else:
            me = "ciseaux"
    result = None
    if player1 == "pierre":
        total_score_1 += 1
        if me == "ciseaux":
            total_score_me += 3
            result = "1"
        elif me == "papier":
            total_score_me += 2
            result = "me"
        else:
            total_score_me += 1
            result = "draw"
    elif player1 == "papier":
        total_score_1 += 2
        if me == "ciseaux":
            total_score_me += 3
            result = "me"
        elif me == "pierre":
            total_score_me += 1
            result = "1"
        else:
            total_score_me += 2
            result = "draw"
    elif player1 == "ciseaux":
        total_score_1 += 3
        if me == "pierre":
            total_score_me += 1
            result = "me"
        elif me == "papier":
            total_score_me += 2
            result = "1"
        else:
            total_score_me += 3
            result = "draw"
    if result == "1":
        total_score_1 += 6
    elif result == "me":
        total_score_me += 6
    else:
        total_score_1 += 3
        total_score_me += 3

print(total_score_me)
print(total_score_1)
