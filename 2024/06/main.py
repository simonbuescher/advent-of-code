from collections import defaultdict

width, height = 0, 0
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def get_puzzle_input():
    global width, height
    with open("input.txt", "r") as file:
        lines = [line.strip() for line in file.readlines()]

        width, height = len(lines[0]), len(lines)
        obstacles = {(x, y) for x in range(width) for y in range(height) if lines[y][x] == "#"}
        guard = [(x, y) for x in range(width) for y in range(height) if lines[y][x] == "^"][0]

        return obstacles, guard


def tadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def run(obstacles, guard):
    current = guard
    direction = (0, -1)

    visited = {guard}
    direction_on_visit = defaultdict(list, {current: [direction]})

    while 0 <= current[0] < width and 0 <= current[1] < height:
        next_pos = tadd(current, direction)
        while next_pos in obstacles:
            direction = directions[(directions.index(direction) + 1) % len(directions)]
            next_pos = tadd(current, direction)

        # loop detection
        if direction in direction_on_visit[next_pos]:
            return True, None

        current = next_pos
        visited.add(current)
        direction_on_visit[current].append(direction)

    return False, len(visited) - 1


def first_puzzle():
    obstacles, guard = get_puzzle_input()
    _, result = run(obstacles, guard)
    print("Puzzle 1:", result)


def second_puzzle():
    obstacles, guard = get_puzzle_input()
    result = sum(run(obstacles | {(x, y)}, guard)[0] for x in range(width) for y in range(height))
    print("Puzzle 2:", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 4580
    second_puzzle()  # Puzzle 2: 1480
