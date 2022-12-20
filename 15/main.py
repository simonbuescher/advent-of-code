def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    return [
        (
            (int(line[2][2:-1]), int(line[3][2:-1])),
            (int(line[8][2:-1]), int(line[9][2:]))
        )
        for line in [line.split(" ") for line in content.split("\n")]
    ]


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_blocked_range(sensor, beacon, row):
    max_dist = dist(sensor, beacon)
    if dist(sensor, (sensor[0], row)) > max_dist:
        return -1, -1

    _remove = abs(row - sensor[1])
    _range = (sensor[0] - max_dist + _remove, sensor[0] + max_dist - _remove)
    return _range


def merge_ranges(ranges):
    ranges.sort()

    i = 0
    while i < len(ranges) - 1:
        left_start, left_end = ranges[i]
        right_start, right_end = ranges[i + 1]

        if left_end >= right_start:
            ranges.pop(i)
            ranges.pop(i)
            ranges.insert(i, (left_start, max(left_end, right_end)))
        else:
            i += 1

    return ranges


def get_blocked_ranges(positions, row):
    ranges = [get_blocked_range(sensor, beacon, row) for sensor, beacon in positions]
    return merge_ranges(ranges)


def first_puzzle():
    row = 2000000
    positions = parse_puzzle_input()

    ranges = get_blocked_ranges(positions, row)
    result = sum(range_end - range_start for range_start, range_end in ranges)

    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    min_x = 0
    max_x = 4000000
    positions = parse_puzzle_input()

    # iterate backwards because previous brute force tries showed that the result is not in the first part
    for row in reversed(range(min_x, max_x + 1)):
        ranges = get_blocked_ranges(positions, row)
        # open position could be in x = 0 or x = 4000000, but this case can be ignored for my input
        if len(ranges) == 2:
            x, y = ranges[0][1] + 1, row
            print(f"Puzzle 2 Answer: {x * max_x + y}")
            return

        elif len(ranges) > 2:
            raise ValueError("Row with too many open positions, this has to be a bug in the code")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 01 Answer: 5144286
    second_puzzle()  # Puzzle 02 Answer: 10229191267339
