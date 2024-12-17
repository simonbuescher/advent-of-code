moves_lookup = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        grid_str, moves_str = file.read().split("\n\n")
        grid = [list(l) for l in grid_str.split("\n")]
        moves = "".join(moves_str.split("\n"))

        return grid, moves, [(x, y) for x in range(len(grid[0])) for y in range(len(grid)) if grid[y][x] == "@"][0]


def move_robot(pos, move, grid):
    moved = move_tile(pos, move, grid)
    if moved:
        dx, dy = moves_lookup[move]
        return pos[0] + dx, pos[1] + dy
    else:
        return pos


def move_tile(pos, move, grid, check_neighbor=True):
    x, y = pos

    if grid[y][x] == "#":
        return False
    elif grid[y][x] == ".":
        return True
    elif grid[y][x] in "[]" and move in "^v" and check_neighbor:
        neighbor = (x + 1) if grid[y][x] == "[" else (x - 1), y
        copy = copy_grid(grid)
        if move_tile(pos, move, copy, False) and move_tile(neighbor, move, copy, False):
            return move_tile(pos, move, grid, False) and move_tile(neighbor, move, grid, False)
        else:
            return False
    else:
        dx, dy = moves_lookup[move]
        nx, ny = x + dx, y + dy
        if move_tile((nx, ny), move, grid):
            grid[ny][nx] = grid[y][x]
            grid[y][x] = "."
            return True
        else:
            return False


def widen_grid(grid):
    replace_map = {
        "#": "##",
        ".": "..",
        "O": "[]",
        "@": "@.",
    }
    return [list("".join([replace_map[c] for c in line])) for line in grid]


def copy_grid(grid):
    return [list("".join(line)) for line in grid]


def first_puzzle():
    grid, moves, robot = get_puzzle_input()

    for move in moves:
        robot = move_robot(robot, move, grid)

    result = sum(y * 100 + x for y, line in enumerate(grid) for x, c in enumerate(line) if c == "O")
    print("Puzzle 1:", result)


def second_puzzle():
    grid, moves, robot = get_puzzle_input()

    grid = widen_grid(grid)
    robot = (robot[0] * 2, robot[1])

    for move in moves:
        robot = move_robot(robot, move, grid)

    result = sum(y * 100 + x for y, line in enumerate(grid) for x, c in enumerate(line) if c == "[")
    print("Puzzle 2:", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 1430536
    second_puzzle()  # Puzzle 2: 1452348
