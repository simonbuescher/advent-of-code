import copy

TOWERS = [
    list("QFMRLWCV"),
    list("DQL"),
    list("PSRGWCNB"),
    list("LCDHBQG"),
    list("VGLFZS"),
    list("DGNP"),
    list("DZPVFCW"),
    list("CPDMS"),
    list("ZNWTVMPC"),
]


def get_instruction(line):
    parts = line.split(" ")
    return int(parts[1]), int(parts[3]) - 1, int(parts[5]) - 1


def first_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    towers = copy.deepcopy(TOWERS)
    for line in puzzle_input.split("\n"):
        n, start, end = get_instruction(line)
        for _ in range(n):
            towers[end].append(towers[start].pop())

    result = "".join([tower.pop() for tower in towers])
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    towers = copy.deepcopy(TOWERS)
    for line in puzzle_input.split("\n"):
        n, start, end = get_instruction(line)
        block = towers[start][-n:]
        towers[start] = towers[start][:len(towers[start])-n]
        towers[end].extend(block)

    result = "".join([tower.pop() for tower in towers])
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
