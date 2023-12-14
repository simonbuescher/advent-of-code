import functools


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def tilt_north(grid):
    def tilt_north_single(tx, ty):
        for i in reversed(range(ty)):
            if grid[i][tx] in ("#", "O"):
                return tx, i + 1
        return tx, 0

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "O":
                nx, ny = tilt_north_single(x, y)
                grid[y][x] = "."
                grid[ny][x] = "O"


def tilt_west(grid):
    def tilt_west_single(tx, ty):
        for i in reversed(range(tx)):
            if grid[ty][i] in ("#", "O"):
                return i + 1, ty
        return 0, ty

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "O":
                nx, ny = tilt_west_single(x, y)
                grid[y][x] = "."
                grid[ny][nx] = "O"


def tilt_south(grid):
    def tilt_south_single(tx, ty):
        for i in range(ty + 1, len(grid)):
            if grid[i][tx] in ("#", "O"):
                return tx, i - 1

        return tx, len(grid) - 1

    for y in reversed(range(len(grid))):
        for x in range(len(grid[y])):
            if grid[y][x] == "O":
                nx, ny = tilt_south_single(x, y)
                grid[y][x] = "."
                grid[ny][nx] = "O"


def tilt_east(grid):
    def tilt_east_single(tx, ty):
        for i in range(tx + 1, len(grid[ty])):
            if grid[ty][i] in ("#", "O"):
                return i - 1, ty
        return len(grid[ty]) - 1, ty

    for y in reversed(range(len(grid))):
        for x in reversed(range(len(grid[y]))):
            if grid[y][x] == "O":
                nx, ny = tilt_east_single(x, y)
                grid[y][x] = "."
                grid[ny][nx] = "O"


def get_positions(grid):
    return {(x, y) for y in range(len(grid)) for x in range(len(grid[y])) if grid[y][x] == "O"}


def calculate_result(grid):
    return sum(len(grid) - y for _, y in get_positions(grid))


def first_puzzle():
    grid = get_puzzle_input()

    tilt_north(grid)
    result = calculate_result(grid)

    print(f"Puzzle 1: {result}")


def second_puzzle():
    grid = get_puzzle_input()

    visited = {}
    i = 0

    while i < 1000000000:
        tilt_north(grid)
        tilt_west(grid)
        tilt_south(grid)
        tilt_east(grid)

        key = tuple(sorted(get_positions(grid)))
        if key in visited:
            loop_size = i - visited[key]
            remaining_loop_iterations = (1000000000 - i) // loop_size
            if remaining_loop_iterations:
                print(f"loop found at {i}, skipping {remaining_loop_iterations * loop_size} iterations to {i + remaining_loop_iterations * loop_size}")
                i += remaining_loop_iterations * loop_size
        else:
            visited[key] = i

        i += 1

    result = calculate_result(grid)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 105208
    second_puzzle()  # Puzzle 2: 102943
