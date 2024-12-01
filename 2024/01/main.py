def get_puzzle_input():
    with open("input.txt", "r") as file:
        return zip(*[tuple(int(i) for i in line.split()) for line in file.readlines()])
    

def first_puzzle():
    first, second = get_puzzle_input()
    result = sum(max(a, b) - min(a, b) for a, b in zip(sorted(first), sorted(second)))
    print("Puzzle 1:", result)


def second_puzzle():
    first, second = get_puzzle_input()
    result = sum(a * second.count(a) for a in first)
    print("Puzzle 2:", result)


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()