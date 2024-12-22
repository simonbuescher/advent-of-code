import itertools


def get_puzzle_input():
    with open("input.txt", "r") as file:
        return [int(i) for i in file.read().split("\n")]


def calc_next(number):
    current = number * 64
    current = number ^ current
    number = current % 16777216

    current = number // 32
    current = number ^ current
    number = current % 16777216

    current = number * 2048
    current = number ^ current
    number = current % 16777216

    return number


def get_all_numbers(number):
    return [number] + [number := calc_next(number) for _ in range(2000)]


def first_puzzle():
    return sum(get_all_numbers(number)[-1] for number in get_puzzle_input())


def second_puzzle():
    all_sequence_maps = []
    for number in get_puzzle_input():
        prices = [int(str(i)[-1]) for i in get_all_numbers(number)]
        changes = [(b - a) for a, b in zip(prices, prices[1:])]

        sequences = {}
        for i in range(3, len(changes)):
            key = tuple(changes[x] for x in range(i - 3, i + 1))
            if key not in sequences:
                sequences[key] = prices[i + 1]

        all_sequence_maps.append(sequences)

    all_possible_sequences = set(itertools.chain.from_iterable(sequences.keys() for sequences in all_sequence_maps))
    results = {key: sum(sequences.get(key, 0) for sequences in all_sequence_maps) for key in all_possible_sequences}
    result = max(results.items(), key=lambda pair: pair[1])
    return result[1]


if __name__ == "__main__":
    print("Puzzle 1:", first_puzzle())  # Puzzle 1: 14869099597
    print("Puzzle 2:", second_puzzle())  # Puzzle 2: 1717
