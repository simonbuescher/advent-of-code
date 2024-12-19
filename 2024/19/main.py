import functools
from collections import defaultdict

towels = defaultdict(list)


def get_puzzle_input():
    with open("input.txt", "r") as file:
        towels_str, patterns_str = file.read().split("\n\n")

        for towel in towels_str.split(", "):
            towels[towel[0]].append(towel)

        return patterns_str.split("\n")


@functools.cache
def find_all(text):
    if not text:
        return 1

    if text[0] not in towels:
        return 0

    return sum(find_all(text[len(pattern):]) for pattern in towels[text[0]] if text.startswith(pattern))


if __name__ == "__main__":
    results = [find_all(text) for text in get_puzzle_input()]
    print("Puzzle 1:", len([r for r in results if r]))  # Puzzle 1: 319
    print("Puzzle 2:", sum(results))  # Puzzle 2: 692575723305545
