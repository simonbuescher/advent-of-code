import math


def get_puzzle_input(create_rule_func):
    with open("input.txt", "r") as file:
        workflows_str, parts_str = file.read().split("\n\n")

    def parse_rule(rule_str):
        if ":" in rule_str:
            condition, target = rule_str.split(":")
            (attr, op, value) = condition[0], condition[1], int(condition[2:])
            return create_rule_func(attr, op, value, target)
        else:
            return None, rule_str

    def parse_workflow(workflow_str):
        name = workflow_str[:workflow_str.index("{")]
        rules_str = workflow_str[workflow_str.index("{") + 1: -1]
        rules = [parse_rule(rule_str) for rule_str in rules_str.split(",")]
        return name, rules

    def parse_part(part_str):
        values = part_str[1:-1].split(",")
        return {v[0]: int(v[2:]) for v in values}

    workflows = {name: rules for name, rules in [parse_workflow(ws) for ws in workflows_str.split("\n")]}
    parts = [parse_part(ps) for ps in parts_str.split("\n")]
    return workflows, parts


def create_rule_first(attr, op, value, target):
    comparator = int.__gt__ if op == ">" else int.__lt__
    return lambda part: comparator(part[attr], value), target


def create_rule_second(attr, op, value, target):
    comparator = range_greater if op == ">" else range_less
    return lambda part: comparator(part, value, attr), target


def range_greater(part, value, attr):
    low, high = part[attr]
    if value < low:
        return None, part
    elif value >= high:
        return part, None
    else:
        npart = dict(part)
        npart[attr] = (value + 1, high)

        opart = dict(part)
        opart[attr] = (low, value)

        return opart, npart


def range_less(part, value, attr):
    low, high = part[attr]
    if value > high:
        return None, part
    elif value <= low:
        return part, None
    else:
        npart = dict(part)
        npart[attr] = (low, value - 1)

        opart = dict(part)
        opart[attr] = (value, high)

        return opart, npart


def first_puzzle():
    workflows, parts = get_puzzle_input(create_rule_first)

    accepted = []
    for part in parts:
        current = "in"
        while True:
            for rule, target in workflows[current]:
                if not rule:
                    current = target
                    break
                else:
                    if rule(part):
                        current = target
                        break

            if current == "A":
                accepted.append(part)
                break
            elif current == "R":
                break

    result = sum(sum(part.values()) for part in accepted)
    print(f"Puzzle 1: {result}")


def second_puzzle():
    workflows, parts = get_puzzle_input(create_rule_second)

    accepted = []
    open_set = [({"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000), }, "in")]

    while open_set:
        part, current_workflow = open_set.pop(0)

        new_states = []
        for rule, target in workflows[current_workflow]:
            if not rule:
                new_states.append((part, target))
                break
            else:
                opart, npart = rule(part)

                if npart:
                    new_states.append((npart, target))
                if opart:
                    part = opart
                else:
                    break

        for new_state in new_states:
            new_part, new_target = new_state
            if new_target == "A":
                accepted.append(new_part)
                continue
            elif new_target == "R":
                continue

            open_set.append(new_state)

    result = sum(math.prod((h + 1) - l for l, h in part.values()) for part in accepted)
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 368523
    second_puzzle()  # Puzzle 2: 124167549767307
