import itertools


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    rows = content.split("\n")
    blizzards = {
        (c, x - 1, y - 1)
        for y, row in enumerate(rows) for x, c in enumerate(row)
        if
        c in (">", "v", "<", "^")
    }
    start = (rows[0].index(".") - 1, -1)
    end = (rows[-1].index(".") - 1, len(rows) - 2)
    width = len(rows[0]) - 2
    height = len(rows) - 2

    return blizzards, (start, end), (width, height)


def build_blizzard_maps(blizzards, dimensions):
    width, height = dimensions

    direction_map = {
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
        "^": (0, -1),
    }
    offset_map = {(x, y): direction_map[direction] for direction, x, y in blizzards}

    blizzard_map = {}
    for i in itertools.count():
        blizzard_positions = {
            ((x + (ox * i)) % width, (y + (oy * i)) % height)
            for (x, y), (ox, oy) in offset_map.items()
        }

        if blizzard_positions in blizzard_map.values():
            break

        blizzard_map[i] = blizzard_positions

    return blizzard_map


def get_neighbors(pos, minute, blizzard_map, goals, dimensions):
    x, y = pos
    start, end = goals
    width, height = dimensions

    if pos == start:
        if y == -1:
            neighbors = [(x, y + 1), start]
        else:
            neighbors = [(x, y - 1), start]
    else:
        neighbors = [(x + ox, y + oy) for ox, oy in ((1, 0), (0, 1), (-1, 0), (0, -1))]
        neighbors = [(nx, ny) for nx, ny in neighbors if 0 <= nx < width and 0 <= ny < height]

        neighbors.append(pos)

        ex, ey = end
        if (ey == height and pos == (ex, ey - 1)) or (ey == -1 and pos == (ex, ey + 1)):
            neighbors.append(end)

    neighbors = [neighbor for neighbor in neighbors if neighbor not in blizzard_map[(minute + 1) % len(blizzard_map)]]

    return neighbors


def search(blizzard_map, goals, dimensions, starting_minutes=0):
    start, end = goals

    open_set = [(starting_minutes, start)]
    visited = set()
    cache = set()

    while open_set:
        minute, current = open_set.pop(0)

        visited.add((current, minute))
        cache.add((current, minute % len(blizzard_map)))

        if current == end:
            return minute

        for neighbor in get_neighbors(current, minute, blizzard_map, goals, dimensions):
            in_open_set = (minute + 1, neighbor) in open_set
            in_visited = (minute + 1, neighbor) in visited
            in_cache = (current, ((minute + 1) % len(blizzard_map))) in cache
            if not in_open_set and not in_visited and not in_cache:
                open_set.append((minute + 1, neighbor))


def first_puzzle(blizzard_map, goals, dimensions):
    result = search(blizzard_map, goals, dimensions)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle(blizzard_map, goals, dimensions):
    start, end = goals

    first_trip_end = search(blizzard_map, (start, end), dimensions)
    second_trip_end = search(blizzard_map, (end, start), dimensions, starting_minutes=first_trip_end)
    third_trip_end = search(blizzard_map, (start, end), dimensions, starting_minutes=second_trip_end)
    print(f"Puzzle 2 Answer: {third_trip_end}")


def run_puzzles():
    # precalculate the blizzard map for every possible minute
    blizzards, goals, dimensions = parse_puzzle_input()
    blizzard_map = build_blizzard_maps(blizzards, dimensions)

    first_puzzle(blizzard_map, goals, dimensions)  # Puzzle 1 Answer: 308
    second_puzzle(blizzard_map, goals, dimensions)  # Puzzle 2 Answer: 908


if __name__ == "__main__":
    run_puzzles()
