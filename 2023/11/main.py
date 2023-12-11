import itertools


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [list(line.strip()) for line in file.readlines()]


def get_galaxies(grid):
    return [(i, pos) for i, pos in enumerate((x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == "#")]


def get_empty(grid):
    empty_rows = {i for i in range(len(grid)) if all(c == "." for c in grid[i])}
    empty_cols = {i for i in range(len(grid[0])) if all(grid[x][i] == "." for x in range(len(grid)))}
    return empty_rows, empty_cols


def dist(a, b):
    ax, ay = a
    bx, by = b
    return abs(ax - bx) + abs(ay - by)


def crossed_empties(a, b, empty_rows, empty_cols):
    ax, ay = a
    bx, by = b
    return len(set(range(min(ax, bx), max(ax, bx))) & empty_cols) + len(set(range(min(ay, by), max(ay, by))) & empty_rows)


def run(expand):
    grid = get_puzzle_input()
    galaxies = get_galaxies(grid)

    empty_rows, empty_cols = get_empty(grid)

    return sum(
        dist(pos_a, pos_b) + (crossed_empties(pos_a, pos_b, empty_rows, empty_cols) * (expand - 1))
        for (_, pos_a), (_, pos_b) in itertools.combinations(galaxies, 2)
    )


if __name__ == "__main__":
    print(f"Puzzle 1: {run(2)}")  # Puzzle 1: 9543156
    print(f"Puzzle 2: {run(1000000)}")  # Puzzle 2: 625243292686
