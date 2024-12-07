def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [(int(l), [int(i) for i in r.split(" ")]) for l, r in [ll.split(": ") for ll in file.read().split("\n")]]


def test_equation(test, values, use_third):
    return test_equation_rec(test, values[1:], values[0], use_third)


def test_equation_rec(test, values, current, use_third):
    if not values:
        return current == test

    return (
            test_equation_rec(test, values[1:], current + values[0], use_third) or
            test_equation_rec(test, values[1:], current * values[0], use_third) or
            (use_third and test_equation_rec(test, values[1:], int(str(current) + str(values[0])), use_third))
    )


def run(use_third=False):
    return sum(test for test, values in get_puzzle_input() if test_equation(test, values, use_third))


if __name__ == "__main__":
    print("Puzzle 1:", run())  # Puzzle 1: 1260333054159
    print("Puzzle 2:", run(use_third=True))  # Puzzle 1: 162042343638683
