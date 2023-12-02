REPLACEMENTS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [line.strip() for line in file.readlines()]


def run(get_digits_func):
    lines = get_puzzle_input()
    cleaned = [get_digits_func(line) for line in lines]
    return sum(int(line[0] + line[-1]) for line in cleaned)


def get_digits(line):
    return "".join(c for c in line if c.isdigit())


def get_digits_with_replacements(line: str):
    current = 0
    result = ""
    while current < len(line):
        if line[current].isdigit():
            result += line[current]
        else:
            for key, value in REPLACEMENTS.items():
                if current + len(key) <= len(line) and line[current: current + len(key)] == key:
                    result += str(value)
        current += 1
    return result


def first_puzzle():
    result = run(get_digits)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    result = run(get_digits_with_replacements)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 54081
    second_puzzle()  # Puzzle 2: 54649
