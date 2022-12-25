import math

to_dec_lookup = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}
to_snafu_lookup = {
    0: (0, "0"),
    1: (0, "1"),
    2: (0, "2"),
    3: (1, "="),
    4: (1, "-"),
    5: (1, "0")
}


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().strip().split("\n")


def snafu_to_dec(number):
    return sum(int(math.pow(5, i) * to_dec_lookup[c]) for i, c in enumerate(reversed(number)))


def dec_to_snafu(number):
    result = ""
    carry = 0

    while number > 0:
        remainder = (number % 5) + carry
        carry, symbol = to_snafu_lookup[remainder]
        result = symbol + result

        number //= 5

    return result


def first_puzzle():
    result = dec_to_snafu(sum(snafu_to_dec(number) for number in parse_puzzle_input()))
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    # the elves managed to find a single starfruit on this month-long journey.
    # thank you little elves!
    print("Puzzle 2 Answer: We start the blender and deliver the smoothie to the waiting reindeer!")


if __name__ == "__main__":
    first_puzzle()  # 2---0-1-2=0=22=2-011
    second_puzzle()
