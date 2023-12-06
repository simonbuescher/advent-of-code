import math


def get_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read()
    time_str, dist_str = content.split("\n")
    return [int(t.strip()) for t in time_str.split()[1:]], [int(d.strip()) for d in dist_str.split()[1:]]


def first_puzzle():
    times, distances = get_puzzle_input()
    results = [(sum(((time - x) * x) > goal for x in range(time))) for time, goal in zip(times, distances)]
    result = math.prod(results)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    times, distances = get_puzzle_input()

    time = int("".join(str(i) for i in times))
    goal = int("".join(str(i) for i in distances))

    x_low = math.ceil((time / 2) - math.sqrt(math.pow((time * -1) / 2, 2) - goal))
    x_high = math.floor((time / 2) + math.sqrt(math.pow((time * -1) / 2, 2) - goal))

    result = (x_high - x_low) + 1
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 2344708
    second_puzzle()  # Puzzle 2: 30125202
