def read_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


def get_packet_starts(string, n):
    return [i for i in range(n - 1, len(string)) if len(set(string[i - n + 1:i + 1])) == n]


def first_puzzle():
    puzzle_input = read_input()
    indices = get_packet_starts(puzzle_input, 4)
    print(f"Puzzle 1 Answer: {indices[0] + 1}")


def second_puzzle():
    puzzle_input = read_input()
    indices = get_packet_starts(puzzle_input, 14)
    print(f"Puzzle 2 Answer: {indices[0] + 1}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
