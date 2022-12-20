import math


class Head:
    def __init__(self):
        self._x = 0
        self._y = 0

    def move(self, instruction):
        if instruction == "R":
            self._x += 1
        elif instruction == "D":
            self._y += 1
        elif instruction == "L":
            self._x -= 1
        elif instruction == "U":
            self._y -= 1

    def get_pos(self):
        return self._x, self._y


class Knot:
    def __init__(self, parent):
        self._x = 0
        self._y = 0
        self._parent = parent

    def move(self, instruction):
        p_x, p_y = self._parent.get_pos()
        dist = math.sqrt(math.pow(p_x - self._x, 2) + math.pow(p_y - self._y, 2))
        if dist >= 2:
            x_off = math.ceil(p_x - self._x)
            y_off = math.ceil(p_y - self._y)

            self._x += x_off // (abs(x_off) if x_off else 1)
            self._y += y_off // (abs(y_off) if y_off else 1)

    def get_pos(self):
        return self._x, self._y


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    unparsed = [row.split(" ") for row in content.split("\n")]
    return [(d, int(n)) for d, n in unparsed]


def run_puzzle(knots):
    instructions = parse_puzzle_input()
    tail_visited = set()
    for instruction, n in instructions:
        for _ in range(n):
            for knot in knots:
                knot.move(instruction)

            tail_visited.add(knot.get_pos())

    return len(tail_visited)


def first_puzzle():
    head = Head()
    tail = Knot(head)

    result = run_puzzle([head, tail])

    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    knots = [Head()]
    for _ in range(9):
        knots.append(Knot(knots[-1]))

    result = run_puzzle(knots)

    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 01 Answer: 5683
    second_puzzle()  # Puzzle 02 Answer: 2372
