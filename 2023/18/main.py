translate = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [(line.split()[0], int(line.split()[1])) for line in file.readlines()]


def get_puzzle_input_hex():
    with open("input.txt", "r") as file:
        return [("RDLU"[int(line.split()[2][-2])], int(line.split()[2][2:-2], 16)) for line in file.readlines()]


def find_area(commands):
    current = (0, 0)
    length = 0

    loop = [current]
    for command in commands:
        direction, n = command

        offset = translate[direction]
        current = (current[0] + (offset[0] * n), current[1] + (offset[1] * n))

        loop.append(current)
        length += n

    return shoelace(loop) + (length // 2 + 1)


def shoelace(points):
    # https://en.wikipedia.org/wiki/Shoelace_formula
    return int(0.5 * sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(points, points[1:])))


if __name__ == "__main__":
    print(f"Puzzle 1: {find_area(get_puzzle_input())}")  # Puzzle 1: 35401
    print(f"Puzzle 2: {find_area(get_puzzle_input_hex())}")  # Puzzle 2: 48020869073824
