import functools

rocks = set()
slopes = {}
empty = set()
start, goal = (), ()

translate = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}


def load_puzzle_input():
    global rocks, slopes, empty, start, goal
    with open("input.txt", "r") as file:
        grid = [list(line.strip()) for line in file.readlines()]
        gx, gy = len(grid[0]), len(grid)

        rocks = {(x, y) for x in range(gx) for y in range(gy) if grid[y][x] == "#"} | {(1, 0), (gx - 2, gy - 1)}
        slopes = {(x, y): grid[y][x] for x in range(gx) for y in range(gy) if grid[y][x] in translate}
        empty = {(x, y) for x in range(gx) for y in range(gy) if grid[y][x] == "."}

        start = (1, 1)
        goal = (gx - 2, gy - 2)


@functools.cache
def neighbors_with_slopes(pos):
    x, y = pos

    if (x, y) in slopes:
        ox, oy = translate[slopes[(x, y)]]
        return [(x + ox, y + oy)]

    return [(x + ox, y + oy) for ox, oy in translate.values() if (x + ox, y + oy) not in rocks]


@functools.cache
def neighbors_without_slopes(pos):
    x, y = pos
    return [(x + ox, y + oy) for ox, oy in translate.values() if (x + ox, y + oy) not in rocks]


def get_reachable_nodes(start_pos, goals, neighbors_func):
    results = []

    open_set = [(start_pos, set())]
    while open_set:
        pos, pres_path = open_set.pop()

        if pos != start_pos and pos in goals:
            results.append(((start_pos, pos), len(pres_path)))
            continue

        for n in neighbors_func(pos):
            if n not in pres_path:
                open_set.append((n, pres_path | {pos}))

    return results


def build_graph(neighbors_func):
    nodes = {pos for pos in (empty | slopes.keys()) if len(neighbors_func(pos)) > 2} | {start, goal}
    edges = []
    for node in nodes:
        edges.extend(get_reachable_nodes(node, nodes, neighbors_func))

    graph = {node: {} for node in nodes}
    for (a, b), weight in edges:
        graph[a][b] = weight

    return graph


def run(neighbor_func):
    graph = build_graph(neighbor_func)

    open_set = [(start, [])]
    results = []

    while open_set:
        pos, pres_path = open_set.pop()

        if pos == goal:
            dist = sum(graph[a][b] for a, b in zip(pres_path, pres_path[1:] + [pos])) + 2
            results.append(dist)
            continue

        for n in graph[pos].keys():
            if n not in pres_path:
                open_set.append((n, pres_path + [pos]))

    return max(results)


if __name__ == "__main__":
    load_puzzle_input()
    print(f"Puzzle 1: {run(neighbors_with_slopes)}")  # Puzzle 1: 2130
    print(f"Puzzle 2: {run(neighbors_without_slopes)}")  # Puzzle 2: 6710
