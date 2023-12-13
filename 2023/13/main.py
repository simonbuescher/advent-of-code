import functools


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [pattern.strip().split("\n") for pattern in file.read().split("\n\n")]


@functools.cache
def find_reflections_in_line(line):
    return {i for i in range(1, len(line)) if all(a == b for a, b in zip(reversed(line[:i]), line[i:]))}


def find_reflection(pattern):
    vertical_reflection = set(range(len(pattern[0])))
    for row in pattern:
        vertical_reflection &= find_reflections_in_line(tuple(row))
        if not vertical_reflection:
            break

    horizontal_reflection = set(range(len(pattern)))
    for col in [[pattern[y][x] for y in range(len(pattern))] for x in range(len(pattern[0]))]:
        horizontal_reflection &= find_reflections_in_line(tuple(col))
        if not horizontal_reflection:
            break

    return vertical_reflection, horizontal_reflection


def all_patterns(pattern):
    n = len(pattern[0]) + 1
    s = "|".join(pattern)
    return [(s[:i] + ("#" if s[i] == "." else ".") + s[i + 1:]).split("|") for i in range(len(s)) if (i + 1) % n]


def first_puzzle():
    patterns = get_puzzle_input()

    result = 0
    for pattern in patterns:
        vertical, horizontal = find_reflection(pattern)
        if vertical:
            result += vertical.pop()
        if horizontal:
            result += horizontal.pop() * 100

    print(f"Puzzle 1: {result}")


def second_puzzle():
    patterns = get_puzzle_input()

    result = 0
    for pattern in patterns:
        vertical, horizontal = find_reflection(pattern)
        for p in all_patterns(pattern):
            v, h = find_reflection(p)
            if v - vertical:
                vertical = v - vertical
                horizontal = set()
                break
            if h - horizontal:
                horizontal = h - horizontal
                vertical = set()
                break

        if vertical:
            result += vertical.pop()
        if horizontal:
            result += horizontal.pop() * 100

    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 34889
    second_puzzle()  # Puzzle 2: 34224
