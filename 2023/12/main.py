import functools


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [(line.split()[0], tuple(int(i) for i in line.split()[1].split(","))) for line in file.readlines()]


@functools.cache
def count(pattern, string, in_pattern, pattern_ended_before):
    if not string:
        # return 1 if string is empty and pattern is empty
        return not pattern

    if not pattern:
        # return 1 if no pattern left and no # in remaining string
        return "#" not in string

    result = 0
    if string[0] in ("#", "?"):
        if not pattern_ended_before:
            remain_in_pattern = pattern and pattern[0] > 1
            new_pattern = ((pattern[0] - 1,) if remain_in_pattern else ()) + pattern[1:]
            result += count(new_pattern, string[1:], remain_in_pattern, not remain_in_pattern)

    if string[0] in (".", "?") and not in_pattern:
        result += count(pattern, string[1:], False, False)

    return result


def first_puzzle():
    lines = get_puzzle_input()
    result = sum(count(pattern, string, False, False) for string, pattern in lines)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    lines = get_puzzle_input()
    result = sum(count(pattern * 5, "?".join([string] * 5), False, False) for string, pattern in lines)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 7653
    second_puzzle()  # Puzzle 2: 60681419004564
