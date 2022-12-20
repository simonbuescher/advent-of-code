def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    rock_endpoints = [
        [(int(x), int(y)) for x, y in [pos.split(",") for pos in line.split(" -> ")]]
        for line in content.split("\n")
    ]

    def build_rocks(start, end):
        return {
            (x, y)
            for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1)
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1)
        }

    rock_positions = [
        build_rocks(line[i - 1], line[i])
        for line in rock_endpoints for i in range(1, len(line))
    ]

    return {pos for line_pos in rock_positions for pos in line_pos}


def run_puzzle(rocks, exit_predicate):
    blocked_positions = rocks
    total = 0

    while True:
        sand = (500, 0)

        while True:
            if exit_predicate(sand, blocked_positions):
                return total

            x, y = sand
            possible_next_pos = [p for p in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)] if p not in blocked_positions]
            if possible_next_pos:
                sand = possible_next_pos[0]
            else:
                blocked_positions.add(sand)
                total += 1
                break


def first_puzzle():
    result = run_puzzle(parse_puzzle_input(), lambda sand, blocked_positions: sand[1] >= 1000)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    rocks = parse_puzzle_input()
    max_y = max(y for _, y in rocks)
    rocks.update({(i, max_y + 2) for i in range(0, 1000)})

    result = run_puzzle(rocks, lambda sand, blocked_positions: (500, 0) in blocked_positions)
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 01 Answer: 638
    second_puzzle()  # Puzzle 02 Answer: 31722
