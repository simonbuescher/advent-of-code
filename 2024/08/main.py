import itertools

width, height = 0, 0


def get_puzzle_input():
    global width, height
    with open("input.txt", "r") as file:
        lines = file.read().split("\n")
        width, height = len(lines[0]), len(lines)
        nodes = [(lines[y][x], (x, y)) for x in range(width) for y in range(height) if lines[y][x] != "."]
        nodes.sort(key=lambda n: n[0])
        return {k: list(i[1] for i in v) for k, v in itertools.groupby(nodes, lambda n: n[0])}


def first_pattern(a, diff):
    new = (a[0] + diff[0], a[1] + diff[1])
    return {new} if 0 <= new[0] < width and 0 <= new[1] < height else set()


def second_pattern(a, diff):
    if not (0 <= a[0] < width and 0 <= a[1] < height):
        return set()

    return {a} | second_pattern((a[0] + diff[0], a[1] + diff[1]), diff)


def run(pattern):
    nodes = get_puzzle_input()
    antinodes = set()

    for freq, positions in nodes.items():
        for a, b in itertools.permutations(positions, 2):
            diff = a[0] - b[0], a[1] - b[1]
            antinodes.update(pattern(a, diff))

    return len(antinodes)


if __name__ == "__main__":
    print("Puzzle 1:", run(first_pattern))  # Puzzle 1: 265
    print("Puzzle 2:", run(second_pattern))  # Puzzle 1: 962
