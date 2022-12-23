import collections
import itertools

neighbor_moves = [(x, y) for x, y in itertools.product((-1, 0, 1), repeat=2) if (x, y) != (0, 0)]
proposal_moves = collections.deque((
    ((0, -1), ((-1, -1), (0, -1), (1, -1))),
    ((0, 1), ((-1, 1), (0, 1), (1, 1))),
    ((-1, 0), ((-1, -1), (-1, 0), (-1, 1))),
    ((1, 0), ((1, -1), (1, 0), (1, 1))),
))


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    return {(x, y) for y, row in enumerate(content.split("\n")) for x, c in enumerate(row) if c == "#"}


def has_neighbors(elf, elves):
    x, y = elf
    return any(((x + nx, y + ny) in elves) for nx, ny in neighbor_moves)


def get_proposal(elf, elves):
    x, y = elf
    proposals = [
        (x + nx, y + ny) for (nx, ny), checks in proposal_moves
        if all((x + cx, y + cy) not in elves for cx, cy in checks)
    ]

    return proposals[0] if proposals else elf


def get_bounding_box(elves):
    x_vals = {x for x, _ in elves}
    y_vals = {y for _, y in elves}
    return (min(x_vals), max(x_vals)), (min(y_vals), max(y_vals))


def solve(break_at=None):
    elves = parse_puzzle_input()

    # reset rotation of proposal_moves after the 10 rounds from puzzle 1
    while proposal_moves[0][0] != (0, -1):
        proposal_moves.rotate(-1)

    for i in itertools.count():
        if break_at and i == break_at:
            break

        elf_proposals = {(elf, (get_proposal(elf, elves) if has_neighbors(elf, elves) else elf)) for elf in elves}
        proposals = [proposal for _, proposal in elf_proposals]
        decisions = {(proposal if proposals.count(proposal) == 1 else elf) for elf, proposal in elf_proposals}

        moves = elves.difference(decisions)
        if not moves:
            break

        elves = decisions
        proposal_moves.rotate(-1)

    (min_x, max_x), (min_y, max_y) = get_bounding_box(elves)
    result = ((max_x - min_x + 1) * (max_y - min_y + 1)) - len(elves)

    return result, i + 1


def first_puzzle():
    result, _ = solve(break_at=10)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    _, result = solve()
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 4218
    second_puzzle()  # Puzzle 2 Answer: 976
