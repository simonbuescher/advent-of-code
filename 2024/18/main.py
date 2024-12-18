width, height = 71, 71


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [tuple(int(i) for i in l.split(",")) for l in file.read().split("\n")]


def find_path(walls):
    open_set = [((0, 0), [(0, 0)])]
    visited = {(0, 0)}

    while open_set:
        current, path = open_set.pop(0)
        if current == (width - 1, height - 1):
            return path

        for ox, oy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            nx, ny = current[0] + ox, current[1] + oy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls and (nx, ny) not in visited:
                open_set.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))


def first_puzzle():
    walls = get_puzzle_input()
    path = find_path(walls[:1024])
    return len(path) - 1


def second_puzzle():
    walls = get_puzzle_input()
    last_path = find_path([])

    for i, wall in enumerate(walls):
        if wall in last_path:
            last_path = find_path(walls[:i + 1])
            if not last_path:
                return wall


if __name__ == "__main__":
    print("Puzzle 1:", first_puzzle())  # Puzzle 1: 506
    print("Puzzle 2:", second_puzzle())  # Puzzle 2: 62,6
