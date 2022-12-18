def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    return {(int(x), int(y), int(z)) for x, y, z in [row.split(",") for row in content.split("\n")]}


def get_neighbors(cube):
    x, y, z = cube
    return [
        (x + _x, y + _y, z + _z)
        for _x, _y, _z in [(0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0)]
    ]


def is_outside_of_grid(cube, mins, maxs):
    return any((
        not (mins[0] <= cube[0] <= maxs[0]),
        not (mins[1] <= cube[1] <= maxs[1]),
        not (mins[2] <= cube[2] <= maxs[2]),
    ))


def has_outside_connection(cube, cubes, mins, maxs):
    if cube in cubes:
        return False

    open_set = [cube]
    visited = set()
    while open_set:
        current = open_set.pop(0)
        if is_outside_of_grid(current, mins, maxs):
            return True

        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor in cubes or neighbor in visited or neighbor in open_set:
                continue

            open_set.append(neighbor)

    return False


def first_puzzle():
    cubes = parse_puzzle_input()

    visible_sides = sum((neighbor not in cubes) for cube in cubes for neighbor in get_neighbors(cube))

    print(f"Puzzle 1 Answer: {visible_sides}")


def second_puzzle():
    cubes = parse_puzzle_input()

    mins = min(cube[0] for cube in cubes), min(cube[1] for cube in cubes), min(cube[2] for cube in cubes)
    maxs = max(cube[0] for cube in cubes), max(cube[1] for cube in cubes), max(cube[2] for cube in cubes)
    visible = sum(
        has_outside_connection(neighbor, cubes, mins, maxs) for cube in cubes for neighbor in get_neighbors(cube)
    )

    print(f"Puzzle 2 Answer: {visible}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 4322
    second_puzzle()  # Puzzle 2 Answer: 2516
