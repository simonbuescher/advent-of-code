import itertools
import re


class Grid:
    def __init__(self, grid_strings):
        max_row_width = max(len(row) for row in grid_strings)
        self._grid = [[" " for _ in range(max_row_width)] for _ in range(len(grid_strings))]
        for y in range(len(grid_strings)):
            for x in range(len(grid_strings[y])):
                self._grid[y][x] = grid_strings[y][x]

        self.start = grid_strings[0].index("."), 0
        self.width = len(self._grid[0])
        self.height = len(self._grid)

    def at(self, pos):
        x, y = pos
        return self._grid[y][x]


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().rstrip().split("\n")

    grid_strings, command_string = content[:-2], content[-1]

    commands = re.split("([RL])", command_string)
    commands = itertools.islice(itertools.pairwise([None] + commands), 0, None, 2)
    commands = [(move, int(n)) for move, n in commands]

    return Grid(grid_strings), commands


def add(*tuples):
    return tuple(sum(e) for e in zip(*tuples))


def solve(grid, commands, wrap_function):
    direction = 1
    position = grid.start

    move_vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for turn, steps in commands:
        direction = (direction + (1 if turn == "R" else -1)) % 4

        for _ in range(steps):
            move_vector = move_vectors[direction]

            npos = add(position, move_vector)
            npos, new_direction = wrap_function(npos, direction)

            if grid.at(npos) == "#":
                break
            else:
                position = npos
                direction = new_direction

    fx, fy = position
    return (1000 * (fy + 1)) + (4 * (fx + 1)) + direction


def first_puzzle():
    grid, commands = parse_puzzle_input()

    widths = [
        (min(xs), max(xs))
        for xs in [
            [x for x in range(grid.width) if grid.at((x, y)) in (".", "#")]
            for y in range(grid.height)
        ]
    ]
    heights = [
        (min(ys), max(ys))
        for ys in [
            [y for y in range(grid.height) if grid.at((x, y)) in (".", "#")]
            for x in range(grid.width)
        ]
    ]

    def wrap_function(npos, direction):
        nx, ny = npos
        if direction == 0 or direction == 2:
            w_min, w_max = widths[ny]
            if nx < w_min:
                nx = w_max
            elif nx > w_max:
                nx = w_min

        if direction == 1 or direction == 3:
            h_min, h_max = heights[nx]
            if ny < h_min:
                ny = h_max
            elif ny > h_max:
                ny = h_min

        return (nx, ny), direction

    result = solve(grid, commands, wrap_function)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    grid, commands = parse_puzzle_input()

    horizontal_edges = [
        (49, (0, 50), 0, lambda x, y: (0, 149 - y)),  # H
        (150, (0, 50), 2, lambda x, y: (99, 149 - y)),  # K
        (49, (50, 100), 1, lambda x, y: (y - 50, 100)),  # G
        (100, (50, 100), 3, lambda x, y: (y + 50, 49)),  # J
        (-1, (100, 150), 0, lambda x, y: (50, 149 - y)),  # H
        (100, (100, 150), 2, lambda x, y: (149, 149 - y)),  # K
        (-1, (150, 200), 1, lambda x, y: (y - 100, 0)),  # I
        (50, (150, 200), 3, lambda x, y: (y - 100, 149)),  # F
    ]
    vertical_edges = [
        (99, (0, 50), 0, lambda x, y: (50, x + 50)),  # G
        (200, (0, 50), 1, lambda x, y: (x + 100, 0)),  # L
        (-1, (50, 100), 0, lambda x, y: (0, x + 100)),  # I
        (150, (50, 100), 2, lambda x, y: (49, x + 100)),  # F
        (-1, (100, 150), 3, lambda x, y: (x - 100, 199)),  # L
        (50, (100, 150), 2, lambda x, y: (99, x - 50)),  # J
    ]

    def wrap_function(npos, direction):
        nx, ny = npos
        if direction == 0 or direction == 2:
            for edge_x, (edge_y_min, edge_y_max), new_direction, transform in horizontal_edges:
                if nx == edge_x and edge_y_min <= ny < edge_y_max:
                    return transform(nx, ny), new_direction

        if direction == 1 or direction == 3:
            for edge_y, (edge_x_min, edge_x_max), new_direction, transform in vertical_edges:
                if ny == edge_y and edge_x_min <= nx < edge_x_max:
                    return transform(nx, ny), new_direction

        return npos, direction

    result = solve(grid, commands, wrap_function)
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 123046
    second_puzzle()  # Puzzle 2 Answer: 195032
