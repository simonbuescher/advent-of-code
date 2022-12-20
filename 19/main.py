import math
import re


def parse_puzzle_input():
    with open("input.txt", "r") as file:
        content = file.read().strip()

    def parse_blueprint(blueprint_string):
        number_regex = re.compile(r"\d+")
        numbers = list(int(n) * -1 for n in number_regex.findall(blueprint_string))

        return (
            numbers[0] * -1,
            {
                (1, 0, 0, 0): (numbers[1], 0, 0, 0),
                (0, 1, 0, 0): (numbers[2], 0, 0, 0),
                (0, 0, 1, 0): (numbers[3], numbers[4], 0, 0),
                (0, 0, 0, 1): (numbers[5], 0, numbers[6], 0)
            }
        )

    return {blueprint_id: robots for blueprint_id, robots in [parse_blueprint(row) for row in content.split("\n")]}


def add_tuple(*tuples):
    return tuple(sum(items) for items in zip(*tuples))


def mul_tuple(*tuples):
    return tuple(math.prod(items) for items in zip(*tuples))


def can_afford(resources, robot_costs):
    return all(i >= 0 for i in add_tuple(resources, robot_costs))


def should_build(robot, all_robots, all_robot_blueprints):
    if robot == (0, 0, 0, 1):
        # always build geode robots
        return True

    # amount of this robot we already have
    robot_amount = max(mul_tuple(robot, all_robots))
    # max resource cost of resource this robot provides (prices are negative)
    max_robot_costs = min(min(mul_tuple(robot, costs)) for costs in all_robot_blueprints.values())

    return robot_amount + max_robot_costs < 0


def solve(robot_blueprints, start_minutes):
    open_set = [(0, start_minutes, (1, 0, 0, 0), (0, 0, 0, 0))]
    visited = {}

    best_score = 0

    while open_set:
        current = open_set.pop()
        score, minutes, robots, resources = current

        # times up, kill this state
        if minutes == 0:
            if score > best_score:
                best_score = score
            continue

        # check if this state can be better than the best score if it would be able to buy a new geode robot every round
        # way to optimistic, but im to lazy to do the real calculations
        if score + (sum(range(minutes))) + (robots[3] * minutes) <= best_score:
            continue

        # if we reached this state before but with a better score, do not continue the current state
        # it will not be better
        if (minutes, robots, resources) in visited:
            old_score = visited[(minutes, robots, resources)]
            if old_score >= score:
                continue

        visited[(minutes, robots, resources)] = score

        # add "do nothing" as a next state
        new_score = score + robots[3]  # current score plus amount of geode robots
        new_minutes = minutes - 1
        new_resources = add_tuple(resources, robots)  # every robot adds 1 resource
        open_set.append((new_score, new_minutes, robots, new_resources))

        # add "buy this robot" for every possible robot that we can afford as next states
        for robot_index, robot_costs in robot_blueprints.items():
            # if we already have x ore robots and the most expensive robot ore price x, we don't need more ore robots
            # as we have the production capabilities to create a new robot every minute
            if not should_build(robot_index, robots, robot_blueprints):
                continue

            if not can_afford(resources, robot_costs):
                continue

            new_robots = add_tuple(robots, robot_index)  # add our new robot
            new_resources = add_tuple(resources, robots, robot_costs)  # add all new resources and subtract robot price
            open_set.append((new_score, new_minutes, new_robots, new_resources))

    return best_score


def first_puzzle():
    blueprints = parse_puzzle_input()

    result = sum(blueprint * solve(robot_blueprints, 24) for blueprint, robot_blueprints in blueprints.items())
    print(f"Puzzle 1 Answer: {result}")


def second_puzzle():
    blueprints = parse_puzzle_input()

    result = math.prod(
        solve(robot_blueprints, 32)
        for robot_blueprints in [blueprints[1], blueprints[2], blueprints[3]]
    )
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 1147
    second_puzzle()  # Puzzle 2 Answer: 3080
