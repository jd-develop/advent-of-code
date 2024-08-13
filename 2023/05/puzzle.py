#!/usr/bin/env python3
# -*- coding:utf-8 -*-

with open("input", "r+", encoding="utf-8") as input_f:
    input_list = input_f.readlines()


def parse(list_to_parse) -> tuple[list[int], dict[str: list[str, list[int, int, int]]]]:
    """Returns a list and a dict.
    The list is just the list of the seeds (int).
    The dict is under this form:
    {
        "source": ["destination", [destination_range_start, source_range_start, range_lenght], ...],
        ...
    }
    """
    dict_to_return = {}
    current_source = ""
    current_destination = ""
    parse_seeds = True
    seeds = []
    for line in list_to_parse:
        if line == "\n":
            continue
        if parse_seeds:
            line = line[:-1].split()
            line = line[1:]
            seeds = list(map(int, line))
            parse_seeds = False
            continue
        if "map" in line:
            line = line.split()
            
            source_and_destination = line[0].split("-")
            source = source_and_destination[0]
            destination = source_and_destination[2]

            dict_to_return[source] = [destination]
            current_source = source
            current_destination = destination

            continue
        line = line[:-1].split()
        destination_range_start = int(line[0])
        source_range_start = int(line[1])
        range_lenght = int(line[2])
        dict_to_return[current_source].append([destination_range_start, source_range_start, range_lenght])
    return seeds, dict_to_return


def find_destination_number(current_number, ranges):
    """Return the destination number of a given number for a given source-to-destination."""
    for r in ranges[1:]:
        if r[1] <= current_number <= r[1]+r[2]-1:
            shift = current_number - r[1]
            destination_number = r[0] + shift
            return destination_number
    return current_number


def find_location_number(seed: int, ranges_dict) -> int:
    """Returns the location number of the given seed."""
    source = "seed"
    destination = ranges_dict[source][0]
    current_number = seed
    while source != "location":
        ranges = ranges_dict[source]
        current_number = find_destination_number(current_number, ranges)
        source = destination
        if source == "location":
            break
        destination = ranges_dict[source][0]
    return current_number


# def shifts_for_one_destination(ranges):
#     """Returns all the cases under the form [[start, end, shift], ...]"""
#     shifts = []
#     for r in ranges[1:]:
#         start_value = r[1]
#         end_value = r[1]+r[2]
#         shift = r[0] - r[1]
#         shifts.append([start_value, end_value, shift])
#     print(shifts)
#     return shifts


# def total_shift(seed_ranges, ranges_dict):
#     """Returns a list of lists, which are under the form [start, end, shift]"""
#     source = "seed"
#     destination = ranges_dict[source][0]
#     cases = [[seed_range[0], seed_range[0] + seed_range[1]] for seed_range in seed_ranges]
#     print(cases)
#     while source != "location":
#         print(f"{source}->{destination}")
#         ranges = ranges_dict[source]
#         current_shifts = shifts_for_one_destination(ranges)
#         new_cases = []
#         for case in cases:
#             shifts_to_apply = []
#             no_apply_shifts = False
#             for shift in current_shifts:
#                 print(shift, case, end=" ")
#                 case_start_in_shift_interval = shift[0] <= case[0] <= shift[1]
#                 case_end_in_shift_interval = shift[0] <= case[1] <= shift[1]
#                 shift_interval_in_case = case[0] <= shift[0] <= shift[1] <= case[1]
#                 # 4 possibilities:
#                 if case_start_in_shift_interval and case_end_in_shift_interval:
#                     print("all_case_in_shift_interval")
#                     new_case_start = case[0] + shift[2]
#                     new_case_end = case[1] + shift[2]
#                     new_case = [new_case_start, new_case_end]
#                     new_cases.append(new_case)
#                     print(f"    so new case is {new_case}")
#                     no_apply_shifts = True
#                     break
#                 elif shift_interval_in_case:
#                     print("all shift interval in case")
#                     shifts_to_apply.append((shift[0], shift[1], shift[2]))
#                 elif case_start_in_shift_interval:
#                     print("start of case in shift interval")
#                     shifts_to_apply.append((case[0], shift[1], shift[2]))
#                 elif case_end_in_shift_interval:
#                     print("end of case in shift interval")
#                     shifts_to_apply.append((shift[0], case[1], shift[2]))
#                 else:
#                     print("nothing")
#             if no_apply_shifts:
#                 print("no apply shifts")
#                 continue
#             print("===== case, shifts_to_apply, new_cases =============")
#             print(case, shifts_to_apply, new_cases)
#             if len(shifts_to_apply) == 0:
#                 new_cases.append(case)
#                 continue
#             shifts_to_apply.sort(key=lambda x: x[0])
#             if shifts_to_apply[0][0] != case[0]:
#                 new_cases.append([case[0], shifts_to_apply[0][0]])
#             last_shift_end_number = shifts_to_apply[0][0]
#             for shift_to_apply in shifts_to_apply:
#                 if shift_to_apply[0] != last_shift_end_number:
#                     new_cases.append([last_shift_end_number, shift_to_apply[0]])
#                 new_cases.append([shift_to_apply[0] + shift_to_apply[2], shift_to_apply[1] + shift_to_apply[2]])
#             if shifts_to_apply[-1][1] != case[1]:
#                 new_cases.append([shifts_to_apply[-1][1], case[1]])
#             print("applied shifts, new_cases")
#             print(new_cases)
#             print("=========")
#         cases = new_cases
#         print(cases)
#         source = destination
#         if source == "location":
#             break
#         destination = parsed_dict[source][0]
#         print()
#     return cases

  
seeds, parsed_dict = parse(input_list)
location_numbers = [find_location_number(seed, parsed_dict) for seed in seeds]
print(min(location_numbers))
# i’m too lazy to code, so i’m gonna make the *bruteforce* algorithm
seed_ranges = []
sum_things_to_check = 0
for i, seed in enumerate(seeds):
    if i%2 == 0:
        continue
    seed_ranges.append((seeds[i-1], seed))
    sum_things_to_check += seed


minimum_seed = seed_ranges[0][0]
minimum = find_location_number(seed_ranges[0][0], parsed_dict)
already_checked = 0
for range_ in seed_ranges:
    for seed in range(range_[0], range_[0]+range_[1]):
        current = find_location_number(seed, parsed_dict)
        if current < minimum:
            minimum = current
            minimum_seed = seed
            print("0"*(10-len(str(already_checked))) + f"{already_checked}/{sum_things_to_check} <-- {minimum}")
        elif already_checked % 10000 == 0:
            print("0"*(10-len(str(already_checked))) + f"{already_checked}/{sum_things_to_check}")
        already_checked += 1
print(minimum_seed, minimum)

# cases = total_shift(seed_ranges, parsed_dict)
# minimum = cases[0][0]
# for case in cases:
#     if case[0] < minimum:
#         minimum = case[0]

# print(minimum)
# OPTIMISED PART 2 DOES’NT WORK
