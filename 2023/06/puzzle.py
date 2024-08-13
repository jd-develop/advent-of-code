#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list: list[str] = input_f.readlines()

time: list[str] = input_list[0][:-1].split()[1:]
distance: list[str] = input_list[1][:-1].split()[1:]


def how_many_ways_to_win(allowed_time: int, win_distance: int) -> int:
    """Returns the number of ways to win, with given time and distance."""
    ways_to_win = 0
    for t in range(allowed_time):
        speed: int = t
        time_remaining: int = allowed_time - t
        distance = speed * time_remaining
        if distance > win_distance:
            ways_to_win += 1
    return ways_to_win


assert len(time) == len(distance)
margin_of_error = 1
for i, t_ in enumerate(time):
    margin_of_error *= how_many_ways_to_win(int(t_), int(distance[i]))
print(margin_of_error)


# part 2
time_part2 = int("".join(time))
distance_part2 = int("".join(distance))

print(time_part2, distance_part2)
print(how_many_ways_to_win(time_part2, distance_part2))
# that worked in 10 seconds :)

