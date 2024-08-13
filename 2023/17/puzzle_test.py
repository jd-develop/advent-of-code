#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from typing import Self
import numpy as np
import numpy.typing as npt

with open("input_test1", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()

input_list = [r[:-1] if r.endswith("\n") else r for r in input_list if r != "\n"]
input_list = [list(map(int, list(r))) for r in input_list]

total = sum([sum(r) for r in input_list])
mean = total // len(input_list)*len(input_list[0])

input_array = np.array(input_list)


class Node:
    def __init__(self, pos: tuple[int, int], g_cost: int, h_cost: int, cost_on_grid: int) -> None:
        self.pos = pos
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.cost_on_grid = cost_on_grid

        self.parent = None

    def __lt__(self, other: Self):
        return self.f_cost < other.f_cost


class AStar:
    def __init__(self, grid: npt.NDArray[np.int_]):
        self.open: list[Node] = []
        self.closed: list[Node] = []
        self.grid = grid

    def search(self, start_node: Node, goal_node: Node):
        self.open.append(start_node)
        while len(self.open) != 0:
            self.open.sort()  # this is possible because Node has __lt__
            current_node = self.open.pop(0)
            
            self.closed.append(current_node)
            if current_node == goal_node:
                return self.recontruct_path(goal_node)

            neighbours: list[Node] = self.check_neighbours(current_node)

            for neighbour in neighbours:
                if neighbour in self.closed:
                    continue
                g_cost = current_node.g_cost + neighbour.cost_on_grid
                h_cost = self.heuristic(neighbour, goal_node)
                f_cost = g_cost + h_cost

                if neighbour in self.open:
                    if neighbour.f_cost > f_cost:
                        self.update_node(neighbour, g_cost, h_cost)
                else:
                    self.update_node(neighbour, g_cost, h_cost)
        
        return None
    
    def get_neighbors(self, node: Node) -> list[tuple[int, int]]:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        neighbors: list[tuple[int, int]] = []

        for x, y in directions:
            neighbor_position = (node.pos[0] + x, node.pos[1] + y)

            if (0 <= neighbor_position[0] < self.grid.shape[0] and 0 <= neighbor_position[1] < self.grid.shape[1]):
                neighbors.append(neighbor_position)
        return neighbors

    def heuristic(self, node: Node, goal: Node):
        manhattan_distance = abs(node.pos[0] - goal.pos[0]) + abs(node.pos[1] - goal.pos[1])
        heuristic_distance = manhattan_distance * mean
        return heuristic_distance

    def reconstruct_path(self, goal_node: Node):
        pass #follow parents back to start

    def update_node(self, node: Node, g_cost: int, h_cost: int):
        pass #update if we find better path
