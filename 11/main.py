class Operation:
    def __init__(self, operation_string):
        self._str = operation_string
        tokens = operation_string.split(" ")
        math_op = tokens[3]
        val = tokens[4]

        base_func = (lambda x, y: x + y) if math_op == "+" else (lambda x, y: x * y)
        self._func = (lambda x: base_func(x, x)) if val == "old" else (lambda x: base_func(x, int(val)))

    def apply(self, value):
        return self._func(value)

    def __repr__(self):
        return f"Op('{self._str}')"


class Monkey:
    def __init__(self, monkey_string):
        monkey_lines = monkey_string.split("\n")
        self._index = int(monkey_lines[0][7:-1])
        self._items = [int(item) for item in monkey_lines[1][18:].split(", ")]
        self._operation = Operation(monkey_lines[2][13:])
        self._test_divisible_by = int(monkey_lines[3][21:])
        self._test_if_true = int(monkey_lines[4][29:])
        self._test_if_false = int(monkey_lines[5][30:])

        self._total_inspections = 0

    def get_index(self):
        return self._index

    def play_round(self, other_monkeys, worry_reducer):
        for item in self._items:
            self._total_inspections += 1

            worrying_value = self._operation.apply(item)
            new_item_value = worry_reducer(worrying_value)
            if new_item_value % self._test_divisible_by == 0:
                other_monkeys[self._test_if_true].catch(new_item_value)
            else:
                other_monkeys[self._test_if_false].catch(new_item_value)

        self._items.clear()

    def catch(self, item):
        self._items.append(item)

    def get_total_inspections(self):
        return self._total_inspections

    def __repr__(self):
        return f"Monkey(index={self._index}, items={self._items}, op={self._operation}, test='{self._test_divisible_by} ? {self._test_if_true} : {self._test_if_false}')"


class Game:
    def __init__(self, monkeys, rounds, worry_reducer):
        self._monkeys = {monkey.get_index(): monkey for monkey in monkeys}
        self._rounds = rounds
        self._worry_reducer = worry_reducer

    def run(self):
        for current_round in range(self._rounds):
            for _, monkey in self._monkeys.items():
                monkey.play_round(self._monkeys, self._worry_reducer)


def read_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


def parse_puzzle_input(puzzle_input):
    return [Monkey(monkey_string) for monkey_string in puzzle_input.split("\n\n")]


def run_puzzle(rounds, worry_reducer):
    puzzle_input = read_puzzle_input()
    monkeys = parse_puzzle_input(puzzle_input)
    game = Game(monkeys, rounds, worry_reducer)

    game.run()

    total_inspections = [monkey.get_total_inspections() for monkey in monkeys]
    first, second = list(reversed(sorted(total_inspections)))[:2]
    return first * second


def first_puzzle():
    result = run_puzzle(20, lambda x: x // 3)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    result = run_puzzle(10000, lambda x: x % (5 * 17 * 7 * 13 * 19 * 3 * 11 * 2))  # monkey divisible tests
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 54054
    second_puzzle()  # Puzzle 2 Answer: 14314925001
