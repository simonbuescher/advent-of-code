translate = {
    "|": (True, False, True, False),
    "-": (False, True, False, True),
    "L": (True, True, False, False),
    "J": (True, False, False, True),
    "7": (False, False, True, True),
    "F": (False, True, True, False),
    ".": (False, False, False, False),
    "S": (True, True, True, True),
}

direction_checks = {
    # o X
    # X X
    0: [(1, 0), (0, 1), (1, 1)],
    # X o
    # X X
    1: [(0, 1), (-1, 0), (-1, 1)],
    # X X
    # X o
    2: [(-1, 0), (0, -1), (-1, -1)],
    # X X
    # o X
    3: [(0, -1), (1, 0), (1, -1)],
}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        grid = [list(line.strip()) for line in file.readlines()]

    gx, gy = len(grid[0]), len(grid)
    return [(x, y) for y in range(gx) for x in range(gy) if grid[y][x] == "S"][0], grid, (gx, gy)


def get_neighbors(pos, grid, grid_size):
    x, y = pos
    gx, gy = grid_size
    top, right, bottom, left = translate[grid[y][x]]

    results = []
    if top and y - 1 >= 0 and translate[grid[y - 1][x]][2]:
        results.append(((x, y - 1), 0))
    if right and x + 1 < gx and translate[grid[y][x + 1]][3]:
        results.append(((x + 1, y), 1))
    if bottom and y + 1 < gy and translate[grid[y + 1][x]][0]:
        results.append(((x, y + 1), 2))
    if left and x - 1 >= 0 and translate[grid[y][x - 1]][1]:
        results.append(((x - 1, y), 3))
    return results


def get_loop(start, grid, grid_size):
    gx, gy = grid_size

    open_set = [((start[0], start[1] + 1), 1)]
    visited = {start}

    sample_right_of_loop = {(start[0], start[1] + 1), (start[0] - 1, start[1]), (start[0] - 1, start[1] + 1)}

    while open_set:
        current, direction = open_set.pop(0)

        for x_off, y_off in direction_checks[direction]:
            nx, ny = current[0] + x_off, current[1] + y_off
            if 0 <= nx < gx and 0 <= ny < gy:
                if (nx, ny) not in visited:
                    sample_right_of_loop.add((nx, ny))

        visited.add(current)
        open_set.extend([(n, d) for n, d in get_neighbors(current, grid, grid_size) if n not in visited])

    return visited, sample_right_of_loop - visited


def get_area(pos, grid_size, loop):
    gx, gy = grid_size

    open_set = [pos]
    visited = set()

    while open_set:
        current = open_set.pop(0)
        if current in loop or current in visited:
            continue

        visited.add(current)
        open_set.extend([
            (current[0] + tx, current[1] + ty)
            for tx, ty in ((0, -1), (1, 0), (0, 1), (-1, 0))
            if 0 <= current[0] + tx < gx and 0 <= current[1] + ty < gy
        ])

    return visited


def first_puzzle():
    start, grid, grid_size = get_puzzle_input()

    open_set = [(start, 0)]
    visited = set()

    while open_set:
        current, dist = open_set.pop(0)
        if current in visited:
            print(dist)
            return

        visited.add(current)
        open_set.extend([(n, dist + 1) for n, _ in get_neighbors(current, grid, grid_size) if n not in visited])


def second_puzzle():
    start, grid, grid_size = get_puzzle_input()
    loop, samples_right_of_loop = get_loop(start, grid, grid_size)

    points_right_of_loop = set()
    for point in samples_right_of_loop:
        if point not in points_right_of_loop:
            points_right_of_loop.update(get_area(point, grid_size, set(loop)))

    right_of_loop = len(points_right_of_loop)
    left_of_loop = grid_size[0] * grid_size[1] - len(loop) - right_of_loop
    print(f"Puzzle 2: {right_of_loop} or {left_of_loop}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 6842
    second_puzzle()  # Puzzle 2: 5523 or 393
