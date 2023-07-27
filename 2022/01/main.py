def parse_puzzle_input():
    with open("input.txt", "r") as file:
        return [int(line.strip()) for line in file.readlines()]


def first_puzzle():
    numbers = parse_puzzle_input()
    result = sum(a < b for (a, b) in zip(numbers, numbers[1:]))
    print("Puzzle 1 Answer: ", result)


def second_puzzle():
    numbers = parse_puzzle_input()

    def create_tuples(offset):
        return zip(numbers[offset:], numbers[offset + 1:], numbers[offset + 2:])

    result = sum(sum(a) < sum(b) for (a, b) in zip(create_tuples(0), create_tuples(1)))
    print("Puzzle 2 Answer: ", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer:  1215
    second_puzzle()  # Puzzle 2 Answer:  1150
