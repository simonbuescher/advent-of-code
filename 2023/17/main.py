import math
from collections import defaultdict

gx, gy = 0, 0
ns = {
    0: [((-1, 0), 3, lambda x: 1), ((0, -1), 0, lambda x: x + 1), ((1, 0), 1, lambda x: 1)],
    1: [((0, -1), 0, lambda x: 1), ((1, 0), 1, lambda x: x + 1), ((0, 1), 2, lambda x: 1)],
    2: [((1, 0), 1, lambda x: 1), ((0, 1), 2, lambda x: x + 1), ((-1, 0), 3, lambda x: 1)],
    3: [((0, 1), 2, lambda x: 1), ((-1, 0), 3, lambda x: x + 1), ((0, -1), 0, lambda x: 1)]
}


def get_puzzle_input():
    global gx, gy
    with open("input.txt", "r") as file:
        grid = [[int(i) for i in line.strip()] for line in file.readlines()]
        gx, gy = len(grid[0]), len(grid)
        return grid


def neighbors(pos, dist, direction, steps, grid):
    result = []

    for offset, nd, steps_func in ns[direction]:
        nx, ny = pos[0] + offset[0], pos[1] + offset[1]
        if 0 <= nx < gx and 0 <= ny < gy and steps_func(steps) <= 3:
            result.append(((nx, ny), dist + grid[ny][nx], nd, steps_func(steps)))

    return result


def ultra_neighbors(pos, dist, direction, steps, grid):
    result = []

    for offset, nd, steps_func in ns[direction]:
        nx, ny = pos[0] + offset[0], pos[1] + offset[1]
        if 0 <= nx < gx and 0 <= ny < gy and steps_func(steps) <= 10 and (steps >= 4 or direction == nd):
            result.append(((nx, ny), dist + grid[ny][nx], nd, steps_func(steps)))

    return result


def insert(open_set, pos, dist, direction, steps):
    for i in range(len(open_set)):
        if open_set[i][1] > dist:
            open_set.insert(i, (pos, dist, direction, steps))
            return

    open_set.append((pos, dist, direction, steps))


def run(neighbors_func, target_reached, calc_dist):
    grid = get_puzzle_input()

    open_set = [((0, 0), 0, 1, 0), ((0, 0), 0, 2, 0)]

    visited = set()
    distances = defaultdict(lambda: math.inf)

    while open_set:
        current = open_set.pop(0)
        pos, dist, direction, steps = current

        if target_reached(pos, steps):
            return calc_dist(dist, pos, grid)

        visited.add((pos, direction, steps))

        for npos, ndist, ndir, nsteps in neighbors_func(pos, dist, direction, steps, grid):
            if ndist < distances[(npos, ndir, nsteps)] and (npos, ndir, nsteps) not in visited:
                insert(open_set, npos, ndist, ndir, nsteps)
                distances[(npos, ndir, nsteps)] = ndist

    raise ValueError("target not reached")


def first_puzzle():
    print(f"Puzzle 1: {run(neighbors, lambda pos, steps: pos == (gx - 1, gy - 1), lambda dist, pos, grid: dist)}")


def second_puzzle():
    result = run(
        ultra_neighbors,
        lambda pos, steps: pos in ((gx - 5, gy - 1), (gx - 1, gy - 5)),
        lambda dist, pos, grid: dist + sum(grid[y][x] for y in range(pos[1], gy) for x in range(pos[0], gx) if (x, y) != pos)
    )
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 1004
    second_puzzle()  # Puzzle 2: 1171
