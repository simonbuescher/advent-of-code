import math


def get_puzzle_input():
    with open("input.txt", "r") as file:
        content = [line.strip() for line in file.readlines()]
    return content


def get_neighbors(pos, bounds):
    x, y = pos
    bx, by = bounds
    return [(x + xoff, y + yoff) for xoff in (-1, 0, 1) for yoff in (-1, 0, 1) if 0 <= x + xoff < bx and 0 <= y + yoff < by]


def get_digit(line, x, y):
    start = x
    end = x
    while start >= 0 and line[start].isdigit():
        start -= 1
    else:
        start += 1

    while end < len(line) and line[end].isdigit():
        end += 1
    else:
        end -= 1

    return int(line[start:end + 1]), start, end, y


def first_puzzle():
    content = get_puzzle_input()
    bounds = (len(content[0]), len(content))

    numbers = set()
    for y in range(len(content)):
        for x in range(len(content[y])):
            if content[y][x].isdigit():
                numbers.add(get_digit(content[y], x, y))

    results = []
    for n, xs, xe, y in numbers:
        has_symbol = any(
            any(content[ny][nx] != "." and not content[ny][nx].isdigit() for nx, ny in get_neighbors((xc, y), bounds)) for xc in range(xs, xe + 1)
        )
        if has_symbol:
            results.append(n)

    result = sum(results)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    content = get_puzzle_input()
    bounds = (len(content[0]), len(content))

    results = []
    for y in range(bounds[1]):
        for x in range(bounds[0]):
            if content[y][x] == "*":
                numbers = {get_digit(content[ny], nx, ny) for nx, ny in get_neighbors((x, y), bounds) if content[ny][nx].isdigit()}
                if len(numbers) == 2:
                    results.append(math.prod(n[0] for n in numbers))

    result = sum(results)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 554003
    second_puzzle()  # Puzzle 2: 87263515
