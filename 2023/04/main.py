import math


def to_int_set(str_list):
    return {int(n) for n in str_list.split()}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        content = [line.strip() for line in file.readlines()]

    strings = [line.split(": ") for line in content]
    return {
        int(game_str.split()[1]): (to_int_set(numbers_str.split(" | ")[0]), to_int_set(numbers_str.split(" | ")[1]))
        for game_str, numbers_str in strings
    }


def first_puzzle():
    games = get_puzzle_input()
    amount_winning_numbers = [len(winning_numbers & my_numbers) for winning_numbers, my_numbers in games.values()]
    points = [int(math.pow(2, x - 1)) for x in amount_winning_numbers if x > 0]
    result = sum(points)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    games = get_puzzle_input()
    results = list(games.items())

    current = 0
    while current < len(results):
        game_id, (winning_numbers, my_numbers) = results[current]
        amount_winning = len(winning_numbers & my_numbers)

        for i in range(game_id + 1, game_id + amount_winning + 1):
            copy_card = games.get(i, None)
            if copy_card:
                results.append((i, copy_card))

        current += 1

    result = len(results)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 22897
    second_puzzle()  # Puzzle 2: 5095824
