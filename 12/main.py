import math


class HeightMap:
    HEIGHT_MAP = "abcdefghijklmnopqrstuvwxyz"

    @staticmethod
    def get_height(value):
        if value == "S":
            return 0
        elif value == "E":
            return 25
        else:
            return HeightMap.HEIGHT_MAP.index(value)


class Grid:
    def __init__(self, grid, width, height):
        self._grid = grid
        self._width = width
        self._height = height

        self._start = self._get_pos("S")
        self._start_height = 0
        self._goal = self._get_pos("E")
        self._goal_height = 25

    def a_star_all(self):
        starting_positions = [self._to_pos(index) for index, letter in enumerate(self._grid) if
                              letter == 'a' or letter == 'S']

        results = []
        for i, pos in enumerate(starting_positions):
            print(f"Evaluating {i}/{len(starting_positions)}", end="\r")
            try:
                self._start = pos
                path = self.a_star()
                results.append((pos, path))
            except ValueError:
                continue

        return results

    def a_star(self):
        open_set = {self._start}
        came_from = {}
        g_score = {self._start: 0}
        f_score = {self._start: self._h(self._start)}

        while open_set:
            current = min(open_set, key=lambda n: f_score[n] if n in f_score else float("inf"))
            if current == self._goal:
                return self._reconstruct_path(came_from)

            open_set.remove(current)
            neighbors = self._get_neighbors(current)
            for neighbor in neighbors:
                d = 1  # entfernung zwischen current und neighbor (immer 1 in unserem grid)
                tentative_g_score = g_score[current] + d

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from.update({neighbor: current})
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._h(neighbor)
                    if neighbor not in open_set:
                        open_set.add(neighbor)

        raise ValueError("No path found")

    def _reconstruct_path(self, came_from):
        current = self._goal
        path = [(current, self._get(current))]
        while current in came_from:
            current = came_from[current]
            path.append((current, self._get(current)))

        return list(reversed(path))

    def _h(self, point):
        x1 = math.pow(self._goal[0] - point[0], 2)
        x2 = math.pow(self._goal[1] - point[1], 2)
        x3 = math.pow(self._goal_height - self._get_height(point), 2)
        return math.sqrt(x1 + x2 + x3)

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
            # entfernung nach unten ist egal, entfernung nach oben max 1
            return cur_height >= p_height or p_height - cur_height <= 1

        return [(_x, _y) for _x, _y in neighbors if in_range((_x, _y)) and max_height_dist((_x, _y))]

    def _get(self, point):
        x, y = point
        return self._grid[y * self._width + x]

    def _get_height(self, point):
        return HeightMap.get_height(self._get(point))

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
    path = grid.a_star()
    result = len(path) - 1
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    grid = parse_puzzle_input()
    results = grid.a_star_all()

    result = len(min(results, key=lambda res: len(res[1]))[1]) - 1
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
