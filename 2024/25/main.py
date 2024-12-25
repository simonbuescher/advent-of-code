def get_puzzle_input():
    with open("input.txt", "r") as file:
        grids = file.read().split("\n\n")

        keys = set()
        locks = set()
        for grid_str in grids:
            grid = grid_str.split("\n")
            values = tuple(sum(grid[y][x] == "#" for y in range(7)) for x in range(5))
            if grid[0][0] == "#":
                locks.add(values)
            else:
                keys.add(values)

    return keys, locks


def first_puzzle():
    keys, locks = get_puzzle_input()

    result = 0
    for lock in locks:
        for key in keys:
            fit = all(a + b <= 7 for a, b in zip(lock, key))
            if fit:
                result += 1

    return result


if __name__ == "__main__":
    print("Puzzle 1:", first_puzzle())  # Puzzle 1: 3090
