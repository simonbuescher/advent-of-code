def get_puzzle_input():
    with open('input.txt', 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        width = len(lines[0])
        return width, lines


def get_most_common(numbers, bit_pos):
    bits = [n[bit_pos] for n in numbers]
    return max(('1', '0'), key=lambda x: bits.count(x))


def get_least_common(numbers, bit_pos):
    bits = [n[bit_pos] for n in numbers]
    return min(('0', '1'), key=lambda x: bits.count(x))


def filter_numbers(numbers, width, bit_criteria):
    numbers = list(numbers)

    for bit_pos in range(width):
        criteria = bit_criteria(numbers, bit_pos)
        numbers = [n for n in numbers if n[bit_pos] == criteria]
        if len(numbers) == 1:
            break

    return numbers[0]


def first_puzzle():
    width, numbers = get_puzzle_input()

    gamma_bits = [get_most_common(numbers, i) for i in range(width)]
    gamma = int(''.join(gamma_bits), 2)

    epsilon = gamma ^ int('1' * width, 2)

    print('Puzzle 1 Answer:', gamma * epsilon)


def second_puzzle():
    width, numbers = get_puzzle_input()

    oxygen_generator = int(filter_numbers(numbers, width, get_most_common), 2)
    co2_scrubber = int(filter_numbers(numbers, width, get_least_common), 2)

    print('Puzzle 2 Answer:', oxygen_generator * co2_scrubber)


if __name__ == '__main__':
    first_puzzle()  # Puzzle 1 Answer: 3813416
    second_puzzle()  # Puzzle 2 Answer: 2990784
