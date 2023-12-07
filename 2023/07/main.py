import functools

card_order = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
joker_card_order = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
type_order = {
    1: lambda hand: len(set(hand)) == 5,  # high card
    2: lambda hand: len(set(hand)) == 4,  # one pair
    3: lambda hand: sorted(hand.count(i) for i in set(hand)) == [1, 2, 2],  # two pair
    4: lambda hand: sorted(hand.count(i) for i in set(hand)) == [1, 1, 3],  # three of a kind
    5: lambda hand: sorted(hand.count(i) for i in set(hand)) == [2, 3],  # full house
    6: lambda hand: sorted(hand.count(i) for i in set(hand)) == [1, 4],  # four of a kind
    7: lambda hand: sorted(hand.count(i) for i in set(hand)) == [5],  # five of a kind
}


def get_puzzle_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()
    return [(list(line.split()[0]), int(line.split()[1])) for line in lines]


def get_type(hand):
    return max(order_key for order_key, checker_func in type_order.items() if checker_func(hand))


def direct_hand_comparator(first, second, lookup):
    return [lookup.index(f) - lookup.index(s) for f, s in zip(first, second) if f != s][0]


def hand_comparator(first, second):
    first_hand, second_hand = first[0], second[0]
    type_first, type_second = get_type(first_hand), get_type(second_hand)

    if type_first == type_second:
        return direct_hand_comparator(first_hand, second_hand, card_order)
    else:
        return type_first - type_second


def get_all_joker_replacements(hand):
    if "J" not in hand:
        # no joker to replace
        return [hand]

    if len(set(hand)) == 1:
        # hand is all jokers, best type is five aces
        return [["A", "A", "A", "A", "A"]]

    results = [list("".join(hand).replace("J", card, 1)) for card in set(c for c in hand if c != "J")]
    return [new_hand for result in results for new_hand in get_all_joker_replacements(result)]


def hand_comparator_with_joker(first, second):
    first_hand, second_hand = first[0], second[0]

    first_max_type = max(get_type(hand) for hand in get_all_joker_replacements(first_hand))
    second_max_type = max(get_type(hand) for hand in get_all_joker_replacements(second_hand))

    if first_max_type == second_max_type:
        return direct_hand_comparator(first_hand, second_hand, joker_card_order)
    else:
        return first_max_type - second_max_type


def run(comparator):
    hands_and_bids = get_puzzle_input()
    hands_and_bids.sort(key=functools.cmp_to_key(comparator))
    return sum(i * bid for i, (_, bid) in enumerate(hands_and_bids, start=1))


if __name__ == "__main__":
    print(f"Puzzle 1: {run(hand_comparator)}")  # Puzzle 1: 253910319
    print(f"Puzzle 2: {run(hand_comparator_with_joker)}")  # Puzzle 2: 254083736
