import functools

numeric_keypad = {
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "0": (1, 3),
    "A": (2, 3),
}

directional_keypad = {
    "^": (1, 0),
    "v": (1, 1),
    "<": (0, 1),
    ">": (2, 1),
    "A": (2, 0),
}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().split("\n")


def split(code):
    current = ""
    results = []

    for c in code:
        current += c
        if c == "A":
            results.append(current)
            current = ""

    return results


def move_on_keypad(code, keypad):
    y_empty_space = keypad["A"][1]
    result = ""
    pos = "A"

    for target in code:
        x, y = keypad[pos]
        tx, ty = keypad[target]
        ox, oy = tx - x, ty - y

        horizontal = (">" * ox if ox >= 0 else "<" * abs(ox))
        vertical = ("v" * oy if oy >= 0 else "^" * abs(oy))

        if y == y_empty_space and tx == 0:
            presses = vertical + horizontal
        elif (x == 0 and ty == y_empty_space) or ox < 0:
            presses = horizontal + vertical
        else:
            presses = vertical + horizontal

        result += presses + "A"
        pos = target

    return result


@functools.cache
def move_on_numerical_pad(code):
    return move_on_keypad(code, numeric_keypad)


@functools.cache
def move_on_directional_pad(code):
    return move_on_keypad(code, directional_keypad)


@functools.cache
def count(code, num_robots):
    if not num_robots:
        return len(code)

    return sum(count(part, num_robots - 1) for part in split(move_on_directional_pad(code)))


def run(num_robots):
    codes = get_puzzle_input()
    return sum(count(move_on_numerical_pad(code), num_robots) * int(code[:-1]) for code in codes)


if __name__ == "__main__":
    print("Puzzle 1:", run(2))  # Puzzle 1: 203814
    print("Puzzle 2:", run(25))  # Puzzle 2: 248566068436630
