import functools


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    pairs = [pair.split("\n") for pair in content.split("\n\n")]
    return [(eval(left), eval(right)) for left, right in pairs]


def compare_ints(left, right):
    diff = left - right
    return diff // (abs(diff) if diff else 1)


def compare_lists(left, right):
    if isinstance(left, list) and not isinstance(right, list):
        right = [right]
    elif not isinstance(left, list) and isinstance(right, list):
        left = [left]

    zipped_list = list(zip(left, right))
    for l, r in zipped_list:
        if isinstance(l, list) or isinstance(r, list):
            compare_result = compare_lists(l, r)
        else:
            compare_result = compare_ints(l, r)

        if compare_result != 0:
            return compare_result
    else:
        if len(left) == len(right) == len(zipped_list):
            return 0
        elif len(left) == len(zipped_list):
            return -1
        else:
            return 1


def first_puzzle():
    pairs = parse_puzzle_input()

    correct_ordered_pairs = []
    for i, (left, right) in enumerate(pairs, start=1):
        compare_result = compare_lists(left, right)
        if compare_result == -1:
            correct_ordered_pairs.append(i)

    result = sum(correct_ordered_pairs)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    pairs = parse_puzzle_input()
    items = [item for pair in pairs for item in pair]
    items.extend([[[2]], [[6]]])

    items.sort(key=functools.cmp_to_key(compare_lists))

    index_1 = items.index([[2]]) + 1
    index_2 = items.index([[6]]) + 1
    result = index_1 * index_2
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 6272
    second_puzzle()  # Puzzle 2 Answer: 22288
