from collections import defaultdict
from heapq import heappush, heappop

grid = []
width, height = 0, 0
dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def get_puzzle_input():
    with open("input.txt", "r") as file:
        global grid, width, height
        grid = file.read().split("\n")
        width, height = len(grid[0]), len(grid)

        start = [(x, y) for x in range(width) for y in range(height) if grid[y][x] == "S"][0]
        end = [(x, y) for x in range(width) for y in range(height) if grid[y][x] == "E"][0]
        return start, end


def search(start, end):
    open_set = [(0, start, (1, 0), {start})]
    visited = defaultdict(lambda: float("inf"), {start: 0})

    min_dist = float("inf")
    tiles = set()

    while open_set:
        dist, current, direction, path = heappop(open_set)

        if current == end:
            min_dist = dist
            tiles |= path
            continue

        if dist > min_dist:
            continue

        visited[current] = dist

        for ox, oy in dirs:
            nx, ny = current[0] + ox, current[1] + oy
            if grid[ny][nx] == "#":
                continue

            next_dist = dist + (1001 if (ox, oy) != direction else 1)
            if next_dist > visited[(nx, ny)] + 1000:
                continue

            heappush(open_set, (next_dist, (nx, ny), (ox, oy), {(nx, ny)} | path))

    return min_dist, len(tiles)


if __name__ == "__main__":
    best_path_score, num_tiles = search(*get_puzzle_input())
    print("Puzzle 1:", best_path_score)  # Puzzle 1: 102460
    print("Puzzle 2:", num_tiles)  # Puzzle 2: 527
