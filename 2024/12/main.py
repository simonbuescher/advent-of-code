import itertools

width, height = 0, 0


def get_puzzle_input():
    with open("input.txt", "r") as file:
        grid = [[i for i in n] for n in file.read().split("\n")]

        global width, height
        width, height = len(grid[0]), len(grid)

        return grid


def run(calc):
    grid = get_puzzle_input()

    visited = set()
    result = 0
    for x, y in itertools.product(range(width), range(height)):
        if (x, y) not in visited:
            size, borders, area = flood_fill((x, y), grid)

            visited |= area
            result += calc(size, borders, area)

    return result


def flood_fill(start, grid):
    open_set = {start}

    size = 0
    borders = 0
    area = set()

    while open_set:
        current = open_set.pop()

        size += 1
        borders += count_borders(current, grid)
        area.add(current)

        for n in neighbors_in_grid(current, grid):
            if n not in area:
                open_set.add(n)

    return size, borders, area


def count_borders(pos, grid):
    return 4 - len(neighbors_in_grid(pos, grid))


def count_sides(area):
    return sum(count_corners(pos, area) for pos in sorted(area))


def count_corners(pos, area):
    ns = neighbors_in_area(pos, area)

    if len(ns) == 4:
        # 4 direct neighbors => has corner in every direction if diagonal is not in area
        return sum(add(pos, off) not in area for off in [(1, 1), (1, -1), (-1, 1), (-1, -1)])

    elif len(ns) == 3:
        # 3 direct neighbors => half of case above, off is the direction opposite of the missing neighbor
        off = add(sub(ns[0], pos), add(sub(ns[1], pos), sub(ns[2], pos)))
        return sum(add(n, off) not in area for n in ns if n != add(pos, off))

    elif len(ns) == 2:
        # 2 direct neighbors
        in_line = any((
            all((add(pos, n) in ns) for n in ((-1, 0), (1, 0))),
            all((add(pos, n) in ns) for n in ((0, -1), (0, 1)))
        ))
        if in_line:
            # neighbors are in a straight line => no corners
            return 0
        else:
            # neighbors are in a L shape => 1 outside corner and 1 inside corner if the diagonal is not in the area
            return 1 + int(add(pos, add(sub(ns[0], pos), sub(ns[1], pos))) not in area)

    elif len(ns) == 1:
        # 1 direct neighbor => dead end, 180 degree turn equals 2 corners
        return 2

    else:
        # 0 direct neighbors => single element with 4 corners
        return 4


def neighbors_in_grid(pos, grid):
    px, py = pos
    neighbors = [add(pos, (nx, ny)) for (nx, ny) in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] == grid[py][px]]


def neighbors_in_area(pos, area):
    return [add(pos, (nx, ny)) for (nx, ny) in [(1, 0), (0, 1), (-1, 0), (0, -1)] if add(pos, (nx, ny)) in area]


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


if __name__ == "__main__":
    print("Puzzle 1:", run(lambda size, border, area: size * border))  # Puzzle 1: 1415378
    print("Puzzle 2:", run(lambda size, border, area: size * count_sides(area)))  # Puzzle 2: 862714
