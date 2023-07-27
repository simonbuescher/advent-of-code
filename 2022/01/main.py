SPLIT_CHAR = "\n"


def first_puzzle():
    with open("input.txt", "r") as input_file:
        puzzle_input = input_file.read()

    elf_strings = [c.split(SPLIT_CHAR) for c in puzzle_input.split(SPLIT_CHAR + SPLIT_CHAR)]
    elf_totals = [sum(int(s) for s in es if s) for es in elf_strings]
    print(f"Answer 1. Puzzle: {max(elf_totals)}")


def second_puzzle():
    with open("input.txt", "r") as input_file:
        puzzle_input = input_file.read()

    elf_strings = [c.split(SPLIT_CHAR) for c in puzzle_input.split(SPLIT_CHAR + SPLIT_CHAR)]
    elf_totals = [sum(int(s) for s in es if s) for es in elf_strings]
    elf_totals_sorted = list(reversed(sorted(elf_totals)))
    totals = elf_totals_sorted[0:3]
    print(f"Answer 2. Puzzle: {sum(totals)}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
