from copy import deepcopy
import pickle


def get_puzzle_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()

    bricks = [
        (tuple(int(i) for i in start.split(",")), tuple(int(i) for i in end.split(",")))
        for start, end in [line.strip().split("~") for line in lines]
    ]
    return {
        i: {(x, y, z) for x in range(s[0], e[0] + 1) for y in range(s[1], e[1] + 1) for z in range(s[2], e[2] + 1)}
        for i, (s, e) in enumerate(bricks, start=65)
    }


def overlap(comp, brick):
    a = {(x, y) for x, y, _ in comp}
    b = {(x, y) for x, y, _ in brick}
    return bool(a & b)


def get_touching(brick, bricks):
    below = []
    above = []
    for key, comp in bricks.items():
        if brick == comp:
            continue

        if min(z for _, _, z in comp) - 1 == max(z for _, _, z in brick):
            if overlap(comp, brick):
                above.append(key)

        if max(z for _, _, z in comp) + 1 == min(z for _, _, z in brick):
            if overlap(comp, brick):
                below.append(key)

    return below, above


def fall(bricks):
    falling = set(bricks.keys())
    while falling:
        print(f"{len(falling)} remaining")
        ordered_bricks = sorted([(k, bricks[k]) for k in falling], key=lambda x: min(p[2] for p in x[1]))

        for key, brick in ordered_bricks:
            if min(b[2] for b in brick) == 1:
                falling.remove(key)
                continue

            below, _ = get_touching(brick, bricks)
            if not below:
                bricks[key] = {(x, y, z - 1) for x, y, z in brick}
            else:
                falling.remove(key)


def remove(brick_map, key):
    below, above = brick_map[key]
    brick_map.pop(key)

    for b in below:
        brick_map[b][1].remove(key)

    for a in above:
        brick_map[a][0].remove(key)

    for a in above:
        if not brick_map[a][0]:
            remove(brick_map, a)


def preprocess_falling():
    bricks = get_puzzle_input()

    fall(bricks)
    brick_map = {key: get_touching(brick, bricks) for key, brick in bricks.items()}

    with open("preprocess.pickle", "wb+") as file:
        pickle.dump(brick_map, file)


def first_puzzle():
    with open("preprocess.pickle", "rb") as file:
        brick_map = pickle.load(file)

    # count all bricks where all above bricks have more than one brick below
    result = sum(all(len(brick_map[a][0]) > 1 for a in above) for _, above in brick_map.values())

    print(f"Puzzle 1: {result}")


def second_puzzle():
    with open("preprocess.pickle", "rb") as file:
        brick_map = pickle.load(file)

    result = 0
    for key in brick_map:
        map_copy = deepcopy(brick_map)
        remove(map_copy, key)
        result += len(brick_map) - len(map_copy) - 1

    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    preprocess_falling()
    first_puzzle()  # Puzzle 1: 393
    second_puzzle()  # Puzzle 2: 58440
