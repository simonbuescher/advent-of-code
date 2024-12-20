width, height = 0, 0
walls = set()


def get_puzzle_input():
    with open("input.txt", "r") as file:
        grid = [list(line) for line in file.read().split("\n")]

        global width, height, walls
        width, height = len(grid[0]), len(grid)

        walls = {(x, y) for x in range(width) for y in range(height) if grid[y][x] == "#"}
        start = [(x, y) for x in range(width) for y in range(height) if grid[y][x] == "S"][0]
        end = [(x, y) for x in range(width) for y in range(height) if grid[y][x] == "E"][0]
        return start, end


def bfs(start, end):
    open_set = [(start, [start])]
    visited = {start}

    while open_set:
        current, path = open_set.pop(0)
        if current == end:
            return path

        for ox, oy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            nx, ny = current[0] + ox, current[1] + oy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls and (nx, ny) not in visited:
                open_set.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))


def run(num_cheats, check_bounds):
    start, end = get_puzzle_input()
    path = bfs(start, end)

    results = 0
    for i in range(len(path)):
        pos = path[i]
        for x in range(i + check_bounds + 1, len(path)):
            end_pos = path[x]

            dist = x - i
            dist_cheat = abs(pos[0] - end_pos[0]) + abs(pos[1] - end_pos[1])
            if dist_cheat <= num_cheats and dist > dist_cheat and (dist - dist_cheat) >= check_bounds:
                results += 1

    return results


if __name__ == "__main__":
    print("Puzzle 1:", run(2, 100))  # Puzzle 1: 1422
    print("Puzzle 2:", run(20, 100))  # Puzzle 2:  1009299
