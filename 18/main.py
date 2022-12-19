def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    return {(int(x), int(y), int(z)) for x, y, z in [row.split(",") for row in content.split("\n")]}


def get_neighbors(cube):
    x, y, z = cube
    return [
        (x + _x, y + _y, z + _z)
        for _x, _y, _z in [(0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0)]
    ]


class Control:
    def __init__(self, cubes):
        self._cubes = cubes
        self._mins = min(cube[0] for cube in cubes), min(cube[1] for cube in cubes), min(cube[2] for cube in cubes)
        self._maxs = max(cube[0] for cube in cubes), max(cube[1] for cube in cubes), max(cube[2] for cube in cubes)

        self._no_outside_connection = set()
        self._outside_connection = set()

    def has_outside_connection(self, cube):
        if cube in self._cubes:
            return False

        return self._bfs(cube)

    def _bfs(self, cube):
        open_set = [cube]
        visited = set()
        while open_set:
            current = open_set.pop(0)
            if current in self._outside_connection:
                return True
            elif current in self._no_outside_connection:
                return False

            if self._is_outside_of_grid(current):
                self._outside_connection.update(visited)
                return True

            visited.add(current)
            for neighbor in get_neighbors(current):
                if neighbor in self._cubes or neighbor in visited or neighbor in open_set:
                    continue

                open_set.append(neighbor)

        self._no_outside_connection.update(visited)
        return False

    def _is_outside_of_grid(self, cube):
        return any((
            not (self._mins[0] <= cube[0] <= self._maxs[0]),
            not (self._mins[1] <= cube[1] <= self._maxs[1]),
            not (self._mins[2] <= cube[2] <= self._maxs[2]),
        ))


def first_puzzle():
    cubes = parse_puzzle_input()

    visible_sides = sum((neighbor not in cubes) for cube in cubes for neighbor in get_neighbors(cube))
    print(f"Puzzle 1 Answer: {visible_sides}")


def second_puzzle():
    cubes = parse_puzzle_input()
    control = Control(cubes)

    visible = sum(control.has_outside_connection(neighbor) for cube in cubes for neighbor in get_neighbors(cube))
    print(f"Puzzle 2 Answer: {visible}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 4322
    second_puzzle()  # Puzzle 2 Answer: 2516
