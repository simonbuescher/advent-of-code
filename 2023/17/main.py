def get_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


class Piece:
    def __init__(self, pattern, position=None):
        self._pattern = pattern
        self._width = 4
        self._height = max(i for i, row in enumerate(pattern) if "#" in row) + 1

        if position:
            self._x = position[0]
            self._y = position[1]

        self._rests = False

    def rests(self):
        return self._rests

    def height(self):
        return self._height

    def move_to_next_position(self, wind, tower):
        if wind == "<" and not self.collides_at((self._x - 1, self._y), tower):
            self._x = self._x - 1
        elif wind == ">" and not self.collides_at((self._x + 1, self._y), tower):
            self._x = self._x + 1

        if self.collides_at((self._x, self._y + 1), tower):
            self._rests = True
        else:
            self._y = self._y + 1

    def collides_at(self, point, tower):
        px, py = point
        for y in range(self._height):
            for x in range(self._width):
                if self._pattern[y][x] == "#" and tower[py + y][px + x] == "#":
                    return True
        return False

    def new_at(self, position):
        return Piece(self._pattern, position)

    def put_into_tower(self, tower):
        for y in range(self._height):
            for x in range(self._width):
                if self._pattern[y][x] == "#":
                    tower[self._y + y][self._x + x] = "#"


def get_tower():
    return [list("#########")]


def get_pieces():
    return [
        Piece(["####", "    ", "    ", "    ", ]),
        Piece([" #  ", "### ", " #  ", "    ", ]),
        Piece(["  # ", "  # ", "### ", "    ", ]),
        Piece(["#   ", "#   ", "#   ", "#   ", ]),
        Piece(["##  ", "##  ", "    ", "    ", ]),
    ]


def prepare_tower_for_next_piece(tower, piece):
    tower_top_diff = (piece.height() + 3) - get_y_of_last_piece(tower)
    if tower_top_diff < 0:
        for _ in range(abs(tower_top_diff)):
            tower.pop(0)
    else:
        for _ in range(tower_top_diff):
            tower = [list("#       #")] + tower

    return tower


def get_current_score(tower):
    return len(tower) - get_y_of_last_piece(tower) - 1


def get_y_of_last_piece(tower):
    for i in range(len(tower)):
        if "#" in tower[i][1:-1]:
            return i
    raise ValueError("tower does not contain any piece or a floor, this is wrong")


def get_ground_shape(tower):
    def col_ground_shape(col):
        for i in range(len(tower)):
            if tower[i][col] == "#":
                return i

    return tuple(col_ground_shape(col) for col in range(1, 8))


def run_simulation(cycles):
    wind = get_puzzle_input()
    tower = get_tower()
    pieces = get_pieces()

    seen_states = {}
    cycle_result = 0

    i = cycles
    wind_i = 0
    piece_i = 0
    while i > 0:
        i -= 1

        piece = pieces[piece_i].new_at((3, 0))
        piece_i = (piece_i + 1) % len(pieces)

        tower = prepare_tower_for_next_piece(tower, piece)

        while not piece.rests():
            piece.move_to_next_position(wind[wind_i], tower)
            wind_i = (wind_i + 1) % len(wind)

        piece.put_into_tower(tower)
        current_score = get_current_score(tower)

        key = (piece_i, wind_i, get_ground_shape(tower))
        if key in seen_states:
            old_i, old_score = seen_states[key]
            diff_i = old_i - i
            diff_score = current_score - old_score

            if diff_i < i:
                cycle_result += diff_score * (i // diff_i)
                i = i % diff_i

        seen_states[key] = (i, current_score)

    return get_current_score(tower) + cycle_result


def first_puzzle():
    result = run_simulation(2022)
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    result = run_simulation(1000000000000)
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 3130
    second_puzzle()  # Puzzle 2 Answer: 1556521739139
