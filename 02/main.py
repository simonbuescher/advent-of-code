GAME_LOOKUP = {
    "A": {
        "X": 1 + 3,
        "Y": 2 + 6,
        "Z": 3 + 0
    },
    "B": {
        "X": 1 + 0,
        "Y": 2 + 3,
        "Z": 3 + 6
    },
    "C": {
        "X": 1 + 6,
        "Y": 2 + 0,
        "Z": 3 + 3
    },
}

# x = loose, y = draw, z = win
CHOICE_LOOKUP = {
    "A": {
        "X": "Z",
        "Y": "X",
        "Z": "Y"
    },
    "B": {
        "X": "X",
        "Y": "Y",
        "Z": "Z"
    },
    "C": {
        "X": "Y",
        "Y": "Z",
        "Z": "X"
    },
}


def first_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    def get_game_points(line):
        enemy_choice, my_choice = line.split(" ")
        return GAME_LOOKUP[enemy_choice][my_choice]

    total = sum(get_game_points(line) for line in puzzle_input.split("\n"))
    print(f"Puzzle 1 Anwser: {total}")


def second_puzzle():
    with open("input.txt", "r") as file:
        puzzle_input = file.read().strip()

    def get_game_points(line):
        enemy_choice, result = line.split(" ")
        my_choice = CHOICE_LOOKUP[enemy_choice][result]
        return GAME_LOOKUP[enemy_choice][my_choice]

    total = sum(get_game_points(line) for line in puzzle_input.split("\n"))
    print(f"Puzzle 2 Answer: {total}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()
