HEIGHT_MAP = "abcdefghijklmnopqrstuvwxyz"


class Grid:
    def __init__(self, grid, width, height):
        self._grid = grid
        self._width = width
        self._height = height

        self._start = self._get_pos("S")
        self._goal = self._get_pos("E")

    def search_all(self):
        starting_positions = [
            self._to_pos(index) for index, letter in enumerate(self._grid) if letter == 'a' or letter == 'S'
        ]

        results = []
        for i, pos in enumerate(starting_positions):
            try:
                self._start = pos
                path = self.breadth_first_search()
                results.append((pos, path))
            except ValueError:
                continue

        return results

    def breadth_first_search(self):
        open_set = [self._start]
        visited = {self._start}
        came_from = {}

        while open_set:
            current = open_set.pop(0)
            if current == self._goal:
                return self._reconstruct_path(came_from)

            for neighbor in self._get_neighbors(current):
                if neighbor not in visited:
                    came_from[neighbor] = current
                    visited.add(neighbor)
                    open_set.append(neighbor)

        raise ValueError("No path found")

    def _reconstruct_path(self, came_from):
        current = self._goal
        path = [(current, self._get(current))]
        while current in came_from:
            current = came_from[current]
            path.append((current, self._get(current)))

        return list(reversed(path))

    def _get_neighbors(self, point):
        x, y = point
        neighbors = [
            (x + 1, y),  # rechts
            (x, y + 1),  # unten
            (x - 1, y),  # links
            (x, y - 1),  # oben
        ]

        def in_range(p1):
            return 0 <= p1[0] < self._width and 0 <= p1[1] < self._height

        def max_height_dist(p1):
            cur_height = self._get_height(point)
            p_height = self._get_height(p1)
            # entfernung nach unten ist egal, entfernung nach oben max 01
            return cur_height >= p_height or p_height - cur_height <= 1

        return [neighbor for neighbor in neighbors if in_range(neighbor) and max_height_dist(neighbor)]

    def _get(self, point):
        x, y = point
        return self._grid[y * self._width + x]

    def _get_height(self, point):
        value = self._get(point)
        value = "a" if value == "S" else value
        value = "z" if value == "E" else value
        return HEIGHT_MAP.index(value)

    def _get_pos(self, value):
        index = self._grid.index(value)
        return self._to_pos(index)

    def _to_pos(self, index):
        return index % self._width, index // self._width


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    rows = content.split("\n")
    width = len(rows[0])
    height = len(rows)
    return Grid([s for row in rows for s in row], width, height)


def first_puzzle():
    grid = parse_puzzle_input()
    path = grid.breadth_first_search()
    result = len(path) - 1
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    grid = parse_puzzle_input()
    results = grid.search_all()

    result = len(min(results, key=lambda res: len(res[1]))[1]) - 1
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 01 Answer: 447
    second_puzzle()  # Puzzle 02 Answer: 446
