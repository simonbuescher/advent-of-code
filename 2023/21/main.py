gx, gy = 0, 0


def get_puzzle_input():
    global gx, gy
    with open("input.txt", "r") as file:
        lines = file.readlines()

    rocks = {(x, y) for y in range(len(lines)) for x in range(len(lines[y].strip())) if lines[y][x] == "#"}
    start = [(x, y) for y in range(len(lines)) for x in range(len(lines[y].strip())) if lines[y][x] == "S"][0]

    gx, gy = len(lines[0].strip()), len(lines)

    return rocks, start


def search(rocks, start, n):
    positions = {start}
    for i in range(n):
        new_positions = set()
        for x, y in positions:
            for neighbor in [(x + ox, y + oy) for ox, oy in ((0, -1), (1, 0), (0, 1), (-1, 0))]:
                if neighbor not in rocks and 0 <= neighbor[0] < gx and 0 <= neighbor[1] < gy:
                    new_positions.add(neighbor)
        positions = new_positions

    return len(positions)


def get_diamond_size(x, even, odd):
    result = odd
    for i in range(int(x)):
        result += 4 * i * [even, odd][(i + 1) % 2]
    return result


def first_puzzle():
    rocks, start = get_puzzle_input()
    result = search(rocks, start, 64)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    rocks, start = get_puzzle_input()

    n = 26501365
    r = n // gx

    diamond_size = get_diamond_size(r, 7490, 7423)  # magic numbers: number of positions on full field after even and odd number of steps
    directions = [search(rocks, start_pos, gx - 1) for start_pos in ((gx // 2, 0), (0, gy // 2), (gx // 2, gy - 1), (gx - 1, gy // 2))]
    first_layer = [search(rocks, start_pos, gx + gx // 2 - 1) for start_pos in ((0, 0), (gx - 1, 0), (gx - 1, gy - 1), (0, gy - 1))]
    second_layer = [search(rocks, start_pos, gx // 2 - 1) for start_pos in ((0, 0), (gx - 1, 0), (gx - 1, gy - 1), (0, gy - 1))]

    result = diamond_size + sum(directions) + sum((r - 1) * v for v in first_layer) + sum(r * v for v in second_layer)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 3687
    second_puzzle()  # Puzzle 2: 610321885082978
