translate = {
    (".", 0): [0],
    (".", 1): [1],
    (".", 2): [2],
    (".", 3): [3],
    ("/", 0): [1],
    ("/", 1): [0],
    ("/", 2): [3],
    ("/", 3): [2],
    ("\\", 0): [3],
    ("\\", 1): [2],
    ("\\", 2): [1],
    ("\\", 3): [0],
    ("-", 0): [1, 3],
    ("-", 1): [1],
    ("-", 2): [1, 3],
    ("-", 3): [3],
    ("|", 0): [0],
    ("|", 1): [0, 2],
    ("|", 2): [2],
    ("|", 3): [0, 2],
}
gx, gy = 0, 0


def get_puzzle_input():
    global gx, gy
    with open("input.txt", "r") as file:
        grid = [line.strip() for line in file.readlines()]
        gx, gy = len(grid[0]), len(grid)
        return grid


def get_next(x, y, d):
    if d == 0 and y > 0:
        return x, y - 1
    elif d == 1 and x < gx - 1:
        return x + 1, y
    elif d == 2 and y < gy - 1:
        return x, y + 1
    elif d == 3 and x > 0:
        return x - 1, y
    return None


def run(start):
    grid = get_puzzle_input()
    open_set = {start}
    visited = set()

    while open_set:
        (x, y), d = open_set.pop()
        if ((x, y), d) in visited:
            continue

        visited.add(((x, y), d))

        for nd in translate[(grid[y][x], d)]:
            n = get_next(x, y, nd)
            if n:
                open_set.add((n, nd))

    return len({pos for pos, _ in visited})


def first_puzzle():
    print(f"Puzzle 1: {run(((0, 0), 1))}")


def second_puzzle():
    starting_pos = [
        pos
        for s in [[((i, 0), 2), ((i, gy - 1), 0)] for i in range(gx)] + [[((0, i), 1), ((gx - 1, i), 3)] for i in range(gy)]
        for pos in s
    ]
    result = max(run(start) for start in starting_pos)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 8323
    second_puzzle()  # Puzzle 2: 8491
