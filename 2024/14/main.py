import functools
import operator

width, height = 101, 103


def get_puzzle_input():
    with open("input.txt", "r") as file:
        lines = file.read().split("\n")
        robots = []
        for line in lines:
            pos_str, vel_str = line.split()
            pos, vel = pos_str[2:].split(","), vel_str[2:].split(",")
            robots.append(((int(pos[0]), int(pos[1])), (int(vel[0]), int(vel[1]))))

        return robots


def simulate(robots, seconds):
    return [((vel[0] * seconds + pos[0]) % width, (vel[1] * seconds + pos[1]) % height) for pos, vel in robots]


def first_puzzle():
    robots = get_puzzle_input()

    positions = simulate(robots, 100)
    parts = []
    quadrants = [
        (0, width // 2, 0, height // 2),
        (width // 2 + 1, width, 0, height // 2),
        (0, width // 2, height // 2 + 1, height),
        (width // 2 + 1, width, height // 2 + 1, height)
    ]
    for xs, xe, ys, ye in quadrants:
        parts.append(sum(xs <= rx < xe and ys <= ry < ye for rx, ry in positions))

    result = functools.reduce(operator.mul, parts)
    print("Puzzle 1:", result)


# the christmas tree probably has a large amount of robots in a straight line from top to bottom
# search for the iteration with the largest amount of robots in a straight line
def second_puzzle():
    robots = get_puzzle_input()

    amounts = []
    for i in range(width * height):
        positions = simulate(robots, i)
        amounts.append(max(len({ry for rx, ry in positions if rx == x}) for x in range(width)))

    result = amounts.index(max(amounts))
    print("Puzzle 2:", result)


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 222062148
    second_puzzle()  # Puzzle 2: 7520
