import itertools

width, height = 0, 0


def get_puzzle_input():
    global width, height
    with open("input.txt", "r") as file:
        trail_map = [[int(i) for i in line] for line in file.read().split("\n")]
        width, height = len(trail_map[0]), len(trail_map)
        trail_heads = [(x, y) for x in range(width) for y in range(height) if trail_map[y][x] == 0]
        return trail_heads, trail_map


def neighbors(node):
    x, y = node
    return [n for n in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)] if 0 <= n[0] < width and 0 <= n[1] < height]


def search_endings(node, trail_map):
    cx, cy = node
    if trail_map[cy][cx] == 9:
        return {node}

    return set(itertools.chain.from_iterable(
        search_endings((nx, ny), trail_map)
        for nx, ny in neighbors(node)
        if trail_map[ny][nx] == trail_map[cy][cx] + 1
    ))


def search_unique(start, trail_map):
    cx, cy = start
    if trail_map[cy][cx] == 9:
        return 1

    return sum(
        search_unique((nx, ny), trail_map)
        for nx, ny in neighbors(start)
        if trail_map[ny][nx] == trail_map[cy][cx] + 1
    )


def run(search_strategy, result_calc):
    trail_heads, trail_map = get_puzzle_input()
    return result_calc(search_strategy(head, trail_map) for head in trail_heads)


if __name__ == "__main__":
    print("Puzzle 1:", run(search_endings, lambda rs: sum(len(r) for r in rs)))  # Puzzle 1: 794
    print("Puzzle 2:", run(search_unique, sum))  # Puzzle 2: 1706
