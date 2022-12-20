import ast
import functools


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    pairs = [pair.split("\n") for pair in content.split("\n\n")]
    return [(ast.literal_eval(left), ast.literal_eval(right)) for left, right in pairs]


def compare_ints(left, right):
    return left - right


def compare_lists(left, right):
    left = [left] if not isinstance(left, list) else left
    right = [right] if not isinstance(right, list) else right

    for left_item, right_item in zip(left, right):
        if isinstance(left_item, list) or isinstance(right_item, list):
            compare_result = compare_lists(left_item, right_item)
        else:
            compare_result = compare_ints(left_item, right_item)

        if compare_result != 0:
            return compare_result
    else:
        return compare_ints(len(left), len(right))


def first_puzzle():
    pairs = parse_puzzle_input()
    result = sum(i for i, (left, right) in enumerate(pairs, start=1) if compare_lists(left, right) < 0)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    pairs = parse_puzzle_input()
    items = [item for pair in pairs for item in pair] + [[[2]], [[6]]]

    items.sort(key=functools.cmp_to_key(compare_lists))

    index_1 = items.index([[2]]) + 1
    index_2 = items.index([[6]]) + 1
    result = index_1 * index_2
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 01 Answer: 6272
    second_puzzle()  # Puzzle 02 Answer: 22288
