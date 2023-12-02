import collections


def get_sets(string: str):
    sets = string.split("; ")
    return [{part.split()[1]: int(part.split()[0]) for part in cset.split(", ")} for cset in sets]


def get_puzzle_input():
    with open("input.txt", "r") as file:
        content = [line.strip() for line in file.readlines()]

    return [(int(line.split(": ")[0].split()[1]), get_sets(line.split(": ")[1])) for line in content]


def is_possible(sets, compare):
    return all(all(value <= compare[key] for key, value in cset.items()) for cset in sets)


def first_puzzle():
    games = get_puzzle_input()

    compare = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    ids = [gid for gid, sets in games if is_possible(sets, compare)]

    result = sum(ids)
    print(f"Puzzle 1: {result}")


def get_max_values(sets):
    result = collections.defaultdict(lambda: 0)
    for cset in sets:
        for key, value in cset.items():
            if value >= result[key]:
                result[key] = value

    return tuple(result.values())


def second_puzzle():
    games = get_puzzle_input()
    values = [get_max_values(sets) for _, sets in games]
    result = sum(t[0] * t[1] * t[2] for t in values)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 2149
    second_puzzle()  # Puzzle 2: 71274
