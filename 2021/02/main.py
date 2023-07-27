import functools
import math


def parse_puzzle_input():
    def to_tuple(line):
        command, x = tuple(line.split())
        if command == "forward":
            return int(x), 0
        if command == "down":
            return 0, int(x)
        if command == "up":
            return 0, int(x) * -1
        raise ValueError(f"unknown command '{line}'")

    with open("input.txt", "r") as file:
        return [to_tuple(l) for l in file.readlines()]


def first_puzzle():
    def move(a, b):
        return a[0] + b[0], a[1] + b[1]

    commands = parse_puzzle_input()
    result = math.prod(functools.reduce(move, commands, (0, 0)))
    print("Puzzle 1 Answer: ", result)


def second_puzzle():
    def move(current, command):
        pos, depth, aim = current
        forward, down = command

        return pos + forward, depth + (forward * aim), aim + down

    commands = parse_puzzle_input()
    final = functools.reduce(move, commands, (0, 0, 0))
    result = final[0] * final[1]
    print("Puzzle 2 Answer: ", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 2019945
    second_puzzle()  # Puzzle 2 Answer: 1599311480
