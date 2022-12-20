import itertools


class Register:
    def __init__(self):
        self._x = 1

    def add(self, value):
        self._x += value

    def get(self):
        return self._x

    def __repr__(self):
        return f"Register(X={self._x})"


class Noop:
    def __init__(self):
        self._finished = False

    def on_cycle(self, register):
        self._finished = True

    def is_finished(self):
        return self._finished

    def __repr__(self):
        return "Noop()"


class AddX:
    REQUIRED_CYCLES = 2

    def __init__(self, value):
        self._value = value
        self._cycles = 0
        self._finished = False

    def on_cycle(self, register):
        self._cycles += 1

        if self._cycles == AddX.REQUIRED_CYCLES:
            register.add(self._value)
            self._finished = True

    def is_finished(self):
        return self._finished

    def __repr__(self):
        return f"AddX(value={self._value})"


class PointsOfInterestEval:
    def __init__(self):
        self._points_of_interest = iter(itertools.count(20, 40))
        self._next_point_of_interest = next(self._points_of_interest)
        self._values_of_interest = []

    def eval(self, cycle, register):
        if cycle == self._next_point_of_interest:
            self._values_of_interest.append((cycle, register.get()))
            self._next_point_of_interest = next(self._points_of_interest)

    def get(self):
        return self._values_of_interest


class GraphicsEval:
    def eval(self, cycle, register):
        cycle_horizontal_screen_position = (cycle % 40) - 1
        if register.get() - 1 <= cycle_horizontal_screen_position <= register.get() + 1:
            print("##", end="")
        else:
            print("  ", end="")

        if cycle % 40 == 0:
            print()


class Cpu:
    def __init__(self, instructions, evaluation):
        self._register = Register()
        self._instructions = instructions
        self._evaluation = evaluation

    def run(self):
        instructions = iter(self._instructions)
        current_instruction = next(instructions)
        cycle = 1

        try:
            while True:
                self._evaluation.eval(cycle, self._register)

                current_instruction.on_cycle(self._register)

                if current_instruction.is_finished():
                    current_instruction = next(instructions)

                cycle += 1

        except StopIteration:
            return


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


def build_instructions(input_string):
    return [
        AddX(int(inst[5:])) if inst.startswith("addx") else Noop()
        for inst in input_string.split("\n")
    ]


def first_puzzle():
    puzzle_input = get_puzzle_input()
    instructions = build_instructions(puzzle_input)
    evaluation = PointsOfInterestEval()
    cpu = Cpu(instructions, evaluation)

    cpu.run()

    values = evaluation.get()
    result = sum(cycle * register for cycle, register in values)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    puzzle_input = get_puzzle_input()
    instructions = build_instructions(puzzle_input)
    evaluation = GraphicsEval()
    cpu = Cpu(instructions, evaluation)

    print("Puzzle 02 Answer: ")
    cpu.run()


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
