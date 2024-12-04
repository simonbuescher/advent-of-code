offsets = [
    [(1, 0), (2, 0), (3, 0)],  # right
    [(1, 1), (2, 2), (3, 3)],  # right down
    [(0, 1), (0, 2), (0, 3)],  # down
    [(-1, 1), (-2, 2), (-3, 3)],  # left down
    [(-1, 0), (-2, 0), (-3, 0)],  # left
    [(-1, -1), (-2, -2), (-3, -3)],  # left up
    [(0, -1), (0, -2), (0, -3)],  # up
    [(1, -1), (2, -2), (3, -3)],  # right up
]
width = 0
height = 0


def get_puzzle_input():
    global width, height
    with open("input.txt", "r") as file:
        lines = [l.strip() for l in file.readlines()]
        width, height = len(lines[0]), len(lines)
        return lines


def tadd(t1, t2):
    return tuple(sum(t) for t in zip(t1, t2))


def check_word(lines, start_pos, pos_off):
    for off, c in zip(pos_off, "MAS"):
        x, y = tadd(start_pos, off)
        if not ((0 <= y < height) and (0 <= x < width) and (lines[y][x] == c)):
            return False

    return True


def check_cross(lines, start_pos):
    x, y = start_pos

    top_left = lines[y - 1][x - 1]
    top_right = lines[y - 1][x + 1]
    bottom_left = lines[y + 1][x - 1]
    bottom_right = lines[y + 1][x + 1]

    return all([
        (top_left == "M" and bottom_right == "S") or (top_left == "S" and bottom_right == "M"),
        (top_right == "M" and bottom_left == "S") or (top_right == "S" and bottom_left == "M")
    ])


def first_puzzle():
    lines = get_puzzle_input()

    starting_positions = [(x, y) for x in range(width) for y in range(height) if lines[y][x] == "X"]
    result = sum(check_word(lines, start, off) for start in starting_positions for off in offsets)

    print("Puzzle 1:", result)


def second_puzzle():
    lines = get_puzzle_input()

    starting_positions = [(x, y) for x in range(1, width - 1) for y in range(1, height - 1) if lines[y][x] == "A"]
    result = sum(check_cross(lines, start) for start in starting_positions)

    print("Puzzle 2:", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 2517
    second_puzzle()  # Puzzle 2: 1960
