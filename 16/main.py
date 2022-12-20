import re


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    flow_rate = {}
    edges = {}

    matcher = re.compile(r".*(?P<valve>[A-Z]{2}).+(rate=(?P<flow>\d+)).*valve(s)?\s(?P<dest>[A-Z]{2}(,\s[A-Z]{2})*)")
    for line in content.split("\n"):
        match = matcher.match(line)
        valve, flow, dest = match.group("valve"), match.group("flow"), match.group("dest")
        flow_rate[valve] = int(flow)
        edges[valve] = set(dest.split(", "))

    return flow_rate, edges


def first_puzzle():
    flow_rates, edges = parse_puzzle_input()

    states = [(1, "AA", ("zzz",), 0)]
    visited = {}
    best = 0

    while states:
        minutes, valve, opened_valves_state, score = states.pop()
        opened_valves = set(opened_valves_state)

        if visited.get((minutes, valve), -1) >= score:
            continue

        visited[(minutes, valve)] = score

        if minutes == 30:
            best = max(best, score)
            continue

        if flow_rates[valve] > 0 and valve not in opened_valves:
            opened_valves.add(valve)
            new_score = score + sum(flow_rates.get(where, 0) for where in opened_valves)
            new_state = (minutes + 1, valve, tuple(opened_valves), new_score)

            states.append(new_state)
            opened_valves.discard(valve)

        new_score = score + sum(flow_rates.get(where, 0) for where in opened_valves)
        for option in edges[valve]:
            new_state = (minutes + 1, option, tuple(opened_valves), new_score)
            states.append(new_state)

    print(f"Puzzle 1 Answer: {best}")


# copy of first one with all the extra options crammed in
def second_puzzle():
    flow_rates, edges = parse_puzzle_input()

    states = [(1, "AA", "AA", ('zzz',), 0)]
    visited = {}
    best = 0

    while states:
        minutes, valve, elph_valve, opened_valves_state, score = states.pop()
        opened_valves = set(opened_valves_state)

        if visited.get((minutes, valve, elph_valve), -1) >= score:
            continue

        visited[(minutes, valve, elph_valve)] = score

        if minutes == 26:
            best = max(best, score)
            continue

        if flow_rates[valve] > 0 and valve not in opened_valves:
            opened_valves.add(valve)
            new_score = score + sum(flow_rates.get(where, 0) for where in opened_valves)
            new_state = (minutes + 1, valve, elph_valve, tuple(opened_valves), new_score)

            states.append(new_state)

            for elph_option in edges[elph_valve]:
                new_state = (minutes + 1, valve, elph_option, tuple(opened_valves), new_score)
                states.append(new_state)

            opened_valves.discard(valve)

        if flow_rates[elph_valve] > 0 and elph_valve not in opened_valves:
            opened_valves.add(elph_valve)
            new_score = score + sum(flow_rates.get(where, 0) for where in opened_valves)
            new_state = (minutes + 1, valve, elph_valve, tuple(opened_valves), new_score)

            states.append(new_state)

            for option in edges[valve]:
                new_state = (minutes + 1, option, elph_valve, tuple(opened_valves), new_score)
                states.append(new_state)

            opened_valves.discard(elph_valve)

        if flow_rates[valve] > 0 and flow_rates[elph_valve] > 0 and valve not in opened_valves and elph_valve not in opened_valves:
            opened_valves.add(valve)
            opened_valves.add(elph_valve)
            new_score = score + sum(flow_rates.get(where, 0) for where in opened_valves)
            new_state = (minutes + 1, valve, elph_valve, tuple(opened_valves), new_score)

            states.append(new_state)
            opened_valves.discard(valve)
            opened_valves.discard(elph_valve)

        new_score = score + sum(flow_rates.get(where, 0) for where in opened_valves)
        for option in edges[valve]:
            for elph_option in edges[elph_valve]:
                new_state = (minutes + 1, option, elph_option, tuple(opened_valves), new_score)
                states.append(new_state)

    print(f"Puzzle 2 Answer: {best}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 2114
    second_puzzle()  # Puzzle 2 Answer: 2666
