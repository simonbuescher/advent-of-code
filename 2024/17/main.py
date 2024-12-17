class State:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        self._pc = 0
        self._output = []

    def exec(self, command, operand):
        if command == 0:
            self._a = self._a // (2 ** self._eval_operand(operand))
            self._pc += 2

        elif command == 1:
            self._b = self._b ^ operand
            self._pc += 2

        elif command == 2:
            self._b = self._eval_operand(operand) % 8
            self._pc += 2

        elif command == 3:
            if self._a == 0:
                self._pc += 2
            else:
                self._pc = operand

        elif command == 4:
            self._b = self._b ^ self._c
            self._pc += 2

        elif command == 5:
            self._output.append(self._eval_operand(operand) % 8)
            self._pc += 2

        elif command == 6:
            self._b = self._a // (2 ** self._eval_operand(operand))
            self._pc += 2

        elif command == 7:
            self._c = self._a // (2 ** self._eval_operand(operand))
            self._pc += 2

        else:
            raise ValueError(f"illegal command {command}")

    def pc(self):
        return self._pc

    def output(self):
        return self._output

    def _eval_operand(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self._a
        elif operand == 5:
            return self._b
        elif operand == 6:
            return self._c
        else:
            raise ValueError(f"illegal combo operant {operand}")


def get_puzzle_input():
    with open("input.txt", "r") as file:
        registers_str, program_str = file.read().split("\n\n")
        registers = tuple(int(l.split()[2]) for l in registers_str.split("\n"))
        program = [int(i) for i in program_str.split()[1].split(",")]
        return registers, program


def run(registers, program):
    state = State(*registers)
    while 0 <= state.pc() < len(program):
        command, operand = program[state.pc()], program[state.pc() + 1]
        state.exec(command, operand)

    return state.output()


def first_puzzle():
    return ",".join(str(i) for i in run(*get_puzzle_input()))


def second_puzzle():
    _, program = get_puzzle_input()

    a = 0
    while True:
        result = run((a, 0, 0), program)

        if result == program:
            return a

        for i in reversed(range(len(result))):
            program_i = len(program) - len(result) + i
            if result[i] != program[program_i]:
                a += 8 ** program_i
                break


if __name__ == "__main__":
    print("Puzzle 1:", first_puzzle())  # Puzzle 1: 1,3,7,4,6,4,2,3,5
    print("Puzzle 2:", second_puzzle())  # Puzzle 2: 202367025818154
