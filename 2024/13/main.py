import re


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [parse_machine(m) for m in file.read().split("\n\n")]


def parse_machine(s):
    return tuple(((int(p[1][2:]), int(p[2][2:])) for p in [re.split(": |, ", line) for line in s.split("\n")]))


def run(offset=0):
    machines = get_puzzle_input()

    game_results = [play(machine, offset) for machine in machines]
    result = sum(can_be_won * (3 * amount_a + amount_b) for can_be_won, (amount_a, amount_b) in game_results)

    return result


def play(machine, offset):
    (ax, ay), (bx, by), (px, py) = machine
    px, py = px + offset, py + offset

    # formeln aufstellen
    # ax * a + bx * b = px
    # ay * a + by * b = py

    # umstellen nach a
    # a = (px - (bx * b)) / ax
    # a = (py - (by * b)) / ay

    # gleichsetzen und umstellen nach b
    # (px - (bx * b)) / ax = (py - (by * b)) / ay
    b = (px * ay - py * ax) / (bx * ay - by * ax)

    # einsetzen
    a = (px - (bx * b)) / ax

    amount_a, amount_b = int(a), int(b)
    if not ax * amount_a + bx * amount_b == px or not ay * amount_a + by * amount_b == py:
        return False, (0, 0)

    return True, (amount_a, amount_b)


if __name__ == "__main__":
    print("Puzzle 1:", run())  # Puzzle 1: 26299
    print("Puzzle 2:", run(offset=10000000000000))  # Puzzle 2: 107824497933339
