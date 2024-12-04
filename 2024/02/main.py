def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [[int(i) for i in line.split()] for line in file.readlines()]


def is_safe(report):
    return all([
        report == list(sorted(report)) or report == list(reversed(sorted(report))),
        all(1 <= abs(a - b) <= 3 for a, b in zip(report, report[1:]))
    ])


def first_puzzle():
    reports = get_puzzle_input()
    result = sum(is_safe(report) for report in reports)
    print("Puzzle 1:", result)


def second_puzzle():
    reports = get_puzzle_input()
    result = sum(any(is_safe(report[:i] + report[i + 1:]) for i in range(len(report))) for report in reports)
    print("Puzzle 2:", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 252
    second_puzzle()  # Puzzle 2: 324
