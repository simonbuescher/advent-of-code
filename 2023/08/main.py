import itertools
import math


def get_puzzle_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()
    return list(lines[0].strip()), {line[0:3]: (line[7:10], line[12:15]) for line in lines[2:]}


def run(instructions, graph, start, end):
    current = start
    for i, instruction in enumerate(itertools.cycle(instructions), start=1):
        current = graph[current][list("LR").index(instruction)]
        if end(current):
            return i


if __name__ == "__main__":
    inst, g = get_puzzle_input()
    print(f"Puzzle 1: {run(inst, g, 'AAA', lambda x: x == 'ZZZ')}")  # Puzzle 1: 13301
    print(f"Puzzle 2: {math.lcm(*[run(inst, g, n, lambda x: x.endswith('Z')) for n in g.keys() if n.endswith('A')])}")  # Puzzle 2: 7309459565207
