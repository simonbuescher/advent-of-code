def get_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().strip().split(",")


def get_puzzle_input_parsed():
    def parse_minus(string: str):
        if "-" not in string:
            return None
        return "-", string[:string.index("-")], None

    def parse_equals(string: str):
        if "=" not in string:
            return None
        return "=", string[:string.index("=")], int(string[string.index("=") + 1:])

    return [parse_minus(s) or parse_equals(s) for s in get_puzzle_input()]


def hash(string):
    current = 0
    for c in string:
        current += ord(c)
        current *= 17
        current %= 256
    return current


def first_puzzle():
    result = sum(hash(string) for string in get_puzzle_input())
    print(f"Puzzle 1: {result}")


def second_puzzle():
    boxes = [[] for _ in range(256)]

    for op, lens, focal in get_puzzle_input_parsed():
        box = hash(lens)
        box_lenses = [l for l, _ in boxes[box]]

        if op == "-" and lens in box_lenses:
            boxes[box].pop(box_lenses.index(lens))
        elif op == "=" and lens in box_lenses:
            boxes[box][box_lenses.index(lens)] = (lens, focal)
        elif op == "=":
            boxes[box].append((lens, focal))

    result = sum((i + 1) * (j + 1) * focal for i, box in enumerate(boxes) for j, (_, focal) in enumerate(box))
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 515974
    second_puzzle()  # Puzzle 2: 265894
