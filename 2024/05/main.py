from collections import defaultdict
from functools import cmp_to_key


def get_puzzle_input():
    with open("input.txt", "r") as file:
        rules_str, updates_str = file.read().split("\n\n")

        ordering = defaultdict(list)
        for rule in rules_str.split("\n"):
            first, second = rule.strip().split("|")
            ordering[first].append(second)

        updates = [update_str.strip().split(",") for update_str in updates_str.split("\n")]

        return ordering, updates


def create_sorting_key(ordering):
    return cmp_to_key(lambda a, b: -1 if b in ordering[a] else 1 if a in ordering[b] else 0)


def sort_update(update, ordering):
    before = list(update)
    after = list(sorted(before, key=create_sorting_key(ordering)))
    return before == after, after


def filter_updates(updates, ordering, should_be_sorted):
    sorted_updates = [sort_update(update, ordering) for update in updates]
    return [sorted_update for was_sorted, sorted_update in sorted_updates if was_sorted == should_be_sorted]


def calculate_result(updates):
    return sum(int(update[len(update) // 2]) for update in updates)


def run(should_be_sorted):
    ordering, updates = get_puzzle_input()
    filtered_updates = filter_updates(updates, ordering, should_be_sorted)
    return calculate_result(filtered_updates)


if __name__ == "__main__":
    print("Puzzle 1:", run(True))  # Puzzle 1: 6051
    print("Puzzle 2:", run(False))  # Puzzle 2: 5093
