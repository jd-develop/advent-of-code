#!/usr/bin/env python3
# coding:utf-8

with open("input.txt", 'r+', encoding="UTF-8") as input_file:
    raw_input = input_file.readlines()


def check_visibility(trees_, tree_row, tree_column):
    row = check_visibility_row(trees_, tree_row, tree_column)
    column_ = check_visibility_column(trees_, tree_row, tree_column)
    return row or column_


def check_visibility_row(trees_, tree_row, tree_column):
    tree_height = trees_[tree_row][tree_column]
    visible_from_right = True
    visible_from_left = True
    for tree in trees_[tree_row][:tree_column]:
        if tree >= tree_height:
            visible_from_right = False
            break
    for tree in trees_[tree_row][tree_column+1:]:
        if tree >= tree_height:
            visible_from_left = False
            break
    return visible_from_right or visible_from_left


def check_visibility_column(trees_, tree_row, tree_column):
    tree_height = trees_[tree_row][tree_column]
    visible_from_top = True
    visible_from_bot = True
    for row in trees_[:tree_row]:
        if row[tree_column] >= tree_height:
            visible_from_top = False
            break
    for row in trees_[tree_row + 1:]:
        if row[tree_column] >= tree_height:
            visible_from_bot = False
            break
    return visible_from_top or visible_from_bot


def how_many_trees(trees_, tree_row, tree_column):
    row = how_many_trees_row(trees_, tree_row, tree_column)
    column_ = how_many_trees_column(trees_, tree_row, tree_column)
    return row * column_


def how_many_trees_row(trees_, tree_row, tree_column):
    tree_height = trees_[tree_row][tree_column]
    how_many_right = 0
    how_many_left = 0
    at_right: list = trees_[tree_row][:tree_column].copy()
    at_right.reverse()
    for tree in at_right:
        if tree < tree_height:
            how_many_right += 1
        else:
            how_many_right += 1
            break
    for tree in trees_[tree_row][tree_column+1:]:
        if tree < tree_height:
            how_many_left += 1
        else:
            how_many_left += 1
            break
    return how_many_right * how_many_left


def how_many_trees_column(trees_, tree_row, tree_column):
    tree_height = trees_[tree_row][tree_column]
    how_many_top = 0
    how_many_bot = 0
    above = trees_[:tree_row].copy()
    above.reverse()
    for row in above:
        if row[tree_column] < tree_height:
            how_many_top += 1
        else:
            how_many_top += 1
            break
    for row in trees_[tree_row + 1:]:
        if row[tree_column] < tree_height:
            how_many_bot += 1
        else:
            how_many_bot += 1
            break
    return how_many_top * how_many_bot


trees = [[int(tree) for tree in row if tree != '\n'] for row in raw_input]
visible_trees = 0
for i, row in enumerate(trees):
    if i == 0 or i == len(trees)-1:
        visible_trees += len(row)
        continue
    for j, column in enumerate(row):
        if j == 0 or j == len(row)-1:
            visible_trees += 1
            continue
        if check_visibility(trees, i, j):
            visible_trees += 1

print(visible_trees)

# print(how_many_trees(trees, 3, 2))
max_how_many = 0
for i, row in enumerate(trees):
    if i == 0 or i == len(trees)-1:
        continue
    for j, column in enumerate(row):
        if j == 0 or j == len(row)-1:
            continue
        how_many = how_many_trees(trees, i, j)
        if how_many > max_how_many:
            max_how_many = how_many

print(max_how_many)
