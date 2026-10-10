"""Day 5 solution."""

from typing import Literal

DAY = "5"

def solve(part: Literal["1", "2"]):
    """Day 5 solution implementation"""
    print(f"Solving day {DAY} part {part}...")
    puzzle_input = get_input()
    solution = _solve_1(puzzle_input) if part == "1" else _solve_2(puzzle_input)
    print(f"Day {DAY}, part {part} solution: {solution}")

def get_input(path: str = f"day_{DAY}/day_{DAY}.txt") -> list[tuple[str, str], list[str]]:
    """Parse input into list of fresh ingredient ranges and list of ingredient ids."""

    ranges = []
    ingredients = []
    # Use blank flag to anticipate a single blank line.
    blank = False

    with open(path, "r", encoding="UTF-8") as f:

        while True:

            line = f.readline().strip("\n")

            # If line empty (i.e. "") either middle line or end of file.
            if not line:
                if blank:
                    break
                blank = True

            if "-" in line:
                ranges.append(tuple(line.split(sep="-")))
            elif line:
                ingredients.append(line)

    return ranges, ingredients

def _solve_1(puzzle_input: list[tuple[str, str], list[str]]):

    fresh_ingredients = []

    for ingredient in puzzle_input[1]:
        for min_id, max_id in puzzle_input[0]:
            if int(min_id) <= int(ingredient) <= int(max_id):
                fresh_ingredients.append(ingredient)
                # If in any range, exit immediately
                break

    return len(fresh_ingredients)

def _solve_2(puzzle_input: list[tuple[str, str], list[str]]):

    # Convert ranges to ints
    ranges = [[int(r[0]), int(r[1])] for r in puzzle_input[0]]

    condensed_ranges = _condense(ranges)

    # Given condensed ranges, determine total number of items.
    total = 0
    for ran in condensed_ranges:

        total += (ran[1] + 1) - ran[0]

    return total

def _condense(ranges: list[list[int, int]]):
    """Given a list of integer ranges, return a condensed list of unique, non-overlapping ranges."""

    condensed_ranges = ranges

    while True:

        overlap = _any_overlap(condensed_ranges)     

        if not overlap:
            break

        range_1, range_2 = overlap

        # Remove from main list and merge
        condensed_ranges.pop(range_1[1])
        condensed_ranges.pop(range_2[1] - 1)

        values = [*range_1[0], *range_2[0]]
        condensed_ranges.append([min(values), max(values)])

    return condensed_ranges

def _any_overlap(ranges: list[list[int, int]]):
    """Return the first overlapping items, else None."""

    for range_1_idx, range_1 in enumerate(ranges):

        for range_2_idx, range_2 in enumerate(ranges):

            if range_1_idx == range_2_idx:
                continue

            range_1_min, range_1_max = range_1
            range_2_min, range_2_max = range_2

            if range_1_min > range_2_max or range_1_max < range_2_min:
                continue

            return (range_1, range_1_idx), (range_2, range_2_idx)

    return None

if __name__ == "__main__":
    solve("1")
    solve("2")
