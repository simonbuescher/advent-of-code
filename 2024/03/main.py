import re


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read()


def calc_mul(instruction):
    split = instruction.split(',')
    return int(split[0][4:]) * int(split[1][:-1])


def first_puzzle():
    line = get_puzzle_input()

    matches = re.findall(r"mul\(\d+,\d+\)", line)
    result = sum(calc_mul(instruction) for instruction in matches)

    print("Puzzle 1:", result)


def second_puzzle():
    line = get_puzzle_input()
    matches = re.findall(r"(mul\(\d+,\d+\)|do\(\)|don\'t\(\))", line)

    result = 0
    active = True
    for instruction in matches:
        if instruction in ['do()', 'don\'t()']:
            active = instruction == 'do()'
        elif active:
            result += calc_mul(instruction)

    print("Puzzle 2:", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 175700056
    second_puzzle()  # Puzzle 2: 71668682
