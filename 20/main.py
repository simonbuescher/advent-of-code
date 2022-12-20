import collections


# wrap numbers in object to make them unique
class Number:
    def __init__(self, n):
        self._n = n

    def get(self):
        return self._n


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        return [int(line) for line in file.read().strip().split("\n")]


def mix(numbers, times):
    original = [Number(n) for n in numbers]
    current = collections.deque(original)

    for _ in range(times):
        for n in original:
            current_index = current.index(n)

            current.remove(n)
            current.rotate(n.get() * - 1)
            current.insert(current_index, n)

    return [n.get() for n in current]


def get_result(result_list):
    zero_index = result_list.index(0)
    return sum(result_list[(zero_index + offset) % len(result_list)] for offset in [1000, 2000, 3000])


def first_puzzle():
    numbers = parse_puzzle_input()

    result_list = mix(numbers, 1)

    result = get_result(result_list)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    numbers = parse_puzzle_input()
    decryption_key = 811589153

    numbers = [n * decryption_key for n in numbers]
    result_list = mix(numbers, 10)

    result = get_result(result_list)
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 11073
    second_puzzle()  # Puzzle 2 Answer: 11102539613040
