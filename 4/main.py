def get_sections(string):
    start, end = string.split("-")
    return set(range(int(start), int(end) + 1))


def first_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    total = 0
    for line in puzzle_input.split("\n"):
        first_str, second_str = line.split(",")
        first, second = get_sections(first_str), get_sections(second_str)
        total += int(first.issubset(second) or second.issubset(first))

    print(f"1. Puzzle Answer: {total}")


def second_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    total = 0
    for line in puzzle_input.split("\n"):
        first_str, second_str = line.split(",")
        first, second = get_sections(first_str), get_sections(second_str)
        total += int(bool(first & second))

    print(f"2. Puzzle Answer: {total}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
