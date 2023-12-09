def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [[int(i) for i in line.strip().split()] for line in file.readlines()]


def get_next(derivations, i):
    if i == len(derivations) - 1:
        return 0

    return derivations[i][-1] + get_next(derivations, i + 1)


def get_next_front(derivations, i):
    if i == len(derivations) - 1:
        return 0

    return derivations[i][0] - get_next_front(derivations, i + 1)


def run(get_next_func):
    functions = get_puzzle_input()

    results = []
    for function in functions:
        derivations = [function]
        while True:
            derivation = [b - a for a, b in zip(derivations[-1], derivations[-1][1:])]
            derivations.append(derivation)
            if len(set(derivation)) == 1:
                # add zero line
                derivations.append(list(0 for _ in range(len(derivation) - 1)))
                break

        results.append(get_next_func(derivations, 0))

    return sum(results)


if __name__ == "__main__":
    print(f"Puzzle 1: {run(get_next)}")  # 1974913025
    print(f"Puzzle 2: {run(get_next_front)}")  # 884
