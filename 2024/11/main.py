import functools

stone_map = {}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [int(n) for n in file.read().split()]


@functools.cache
def expand(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        return [int(str(stone)[:len(str(stone)) // 2]), int(str(stone)[len(str(stone)) // 2:])]
    else:
        return [stone * 2024]


@functools.cache
def size(stone, remaining):
    if remaining == 0:
        return 1

    if stone not in stone_map:
        stone_map[stone] = expand(stone)

    return sum(size(child, remaining - 1) for child in stone_map[stone])


def run(iterations):
    return sum(size(stone, iterations) for stone in get_puzzle_input())


if __name__ == "__main__":
    print("Puzzle 1:", run(25))  # Puzzle 1: 229043
    print("Puzzle 2:", run(75))  # Puzzle 2: 272673043446478
