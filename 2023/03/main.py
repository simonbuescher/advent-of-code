alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def first_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    total = 0
    for line in puzzle_input.split("\n"):
        first, second = set(line[:len(line) // 2]), set(line[len(line) // 2:])
        common = first & second
        total += alph.index(common.pop()) + 1

    print(f"Puzzle 1 Answer: {total}")


def second_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    lines = puzzle_input.split("\n")
    total = 0
    while lines:
        a, b, c = lines[:3]
        common = set(a) & set(b) & set(c)
        total += alph.index(common.pop()) + 1
        lines = lines[3:]

    print(f"Puzzle 2 Answer: {total}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
