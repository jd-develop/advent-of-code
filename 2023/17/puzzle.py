#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# I’ll try to implement the Dijkstra algorithm.

with open("input_test1", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()

input_list = [r[:-1] if r.endswith("\n") else r for r in input_list if r != "\n"]


def find_neighbours(puzzle_input: list[str], i: int, j: int) -> list[tuple[int, int, int, str]]:
    """Find the neighbours of the cell"""
    neighbours: list[tuple[int, int, int, str]] = []
    for x, y, m in [(i+1, j, "d"), (i-1, j, "u"), (i, j+1, "r"), (i, j-1, "l")]:
        if x >= 0 and x < len(puzzle_input) and y >= 0 and y < len(puzzle_input[x]):
            neighbours.append((x, y, int(puzzle_input[x][y]), m))
    return neighbours


def dijkstra(puzzle_input: list[str], start: tuple[int, int], end: tuple[int, int]):
    """Find the best way to get from start to finish"""
    known_path: dict[tuple[int, int], tuple[int, str]] = {}
    candidate_path: list[tuple[tuple[int, int], int, str]] = [(start, 0, "")]
    while end not in known_path:
        print(known_path)
        print(candidate_path)
        # find smallest candidate
        print("smallest candidate: ")
        candidate = min(candidate_path, key=lambda x: x[1])
        print(candidate)
        candidate_path.pop(candidate_path.index(candidate))
        # find its neighbours
        (i, j), cost, last_moves = candidate
        known_path[(i, j)] = (cost, last_moves)
        if (i, j) == end:
            print(f"it corresponds to the end. Final cost is {cost}")
            return cost
        neighbours = find_neighbours(puzzle_input, i, j)
        print(f"Its neighbours are {neighbours}. Looping…")
        assert len(neighbours) != 0
        for x, y, cost_to_add, new_move in neighbours:
            print(f"Currently on neighbour {x}:{y}")
            if (x, y) in known_path:
                print(" -> Already in known path. Pass")
                continue
            forbidden_moves = [("r", "l"), ("l", "r"), ("u", "d"), ("d", "u")]
            if any((last_moves.endswith(a) and new_move == b) for a, b in forbidden_moves):
                print(" -> Forbidden move. Pass")
                continue
            if last_moves.endswith(new_move*3):
                print(" -> More than 3 times the same movement. Pass")
                continue
            added = False
            for i, ((candidate_x, candidate_y), candidate_cost, _) in enumerate(candidate_path):
                if (candidate_x, candidate_y) == (x, y):
                    print(" -> Already in known list")
                    if candidate_cost < cost+cost_to_add:
                        print(f" -> -> With a better cost (current cost is {candidate_cost}, better cost is {cost+cost_to_add}). Replacing")
                        added = True
                        candidate_path[i] = ((x, y), cost+cost_to_add, last_moves+new_move)
                    break
            if not added:
                print(" -> Not in known list. Appending")
                candidate_path.append(((x, y), cost+cost_to_add, last_moves+new_move))
    print("meh")


end_i = len(input_list) - 1
end_j = len(input_list[end_i]) - 1
print(dijkstra(input_list, (0, 0), (end_i, end_j)))
        