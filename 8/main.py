class Grid:
    def __init__(self, trees, width, height):
        self._trees = trees
        self._width = width
        self._height = height

    def count_visible_trees(self):
        total = 0
        for x in range(self._width):
            for y in range(self._height):
                tree = self._get_tree(x, y)
                visible = any((
                    self._check_horizontal_heights(tree, range(x - 1, -1, -1), y)[1],  # links
                    self._check_horizontal_heights(tree, range(x + 1, self._width), y)[1],  # rechts
                    self._check_vertical_heights(tree, x, range(y - 1, -1, -1))[1],  # oben
                    self._check_vertical_heights(tree, x, range(y + 1, self._height))[1]  # unten
                ))
                if visible:
                    total += 1

        return total

    def find_best_tree(self):
        all_scores = []
        for x in range(self._width):
            for y in range(self._height):
                tree = self._get_tree(x, y)
                left, _ = self._check_horizontal_heights(tree, range(x - 1, -1, -1), y)
                right, _ = self._check_horizontal_heights(tree, range(x + 1, self._width), y)
                top, _ = self._check_vertical_heights(tree, x, range(y - 1, -1, -1))
                bottom, _ = self._check_vertical_heights(tree, x, range(y + 1, self._height))
                all_scores.append(left * right * top * bottom)

        return max(all_scores)

    def _check_horizontal_heights(self, tree_height, x_range, y):
        reached_end = False
        total_trees_looked_at = 0
        for x in x_range:
            total_trees_looked_at += 1
            if self._get_tree(x, y) >= tree_height:
                break
        else:
            reached_end = True
        return total_trees_looked_at, reached_end

    def _check_vertical_heights(self, tree_height, x, y_range):
        reached_end = False
        total_trees_looked_at = 0
        for y in y_range:
            total_trees_looked_at += 1
            if self._get_tree(x, y) >= tree_height:
                break
        else:
            reached_end = True
        return total_trees_looked_at, reached_end

    def _get_tree(self, x, y):
        return self._trees[y * self._width + x]


def read_puzzle_input():
    with open("input.txt", "r") as file:
        return file.read().strip()


def parse_puzzle_input(puzzle_input):
    lines = puzzle_input.split("\n")
    width = len(lines[0])
    height = len(lines)

    return Grid([int(tree) for row in puzzle_input.split("\n") for tree in row], width, height)


def first_puzzle():
    puzzle_input = read_puzzle_input()
    grid = parse_puzzle_input(puzzle_input)

    result = grid.count_visible_trees()
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    puzzle_input = read_puzzle_input()
    grid = parse_puzzle_input(puzzle_input)

    result = grid.find_best_tree()
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
