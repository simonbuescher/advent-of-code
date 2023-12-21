import itertools
import math


class Broadcaster:
    def __init__(self, targets):
        self.targets = targets

    def process(self, queue, signal):
        _, pulse, _ = signal
        for target in self.targets:
            queue.append(("broadcaster", pulse, target))


class FlipFlop:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.state = False

    def process(self, queue, signal):
        _, pulse, _ = signal
        if not pulse:
            self.state = not self.state
            for target in self.targets:
                queue.append((self.name, self.state, target))


class Conjunction:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets
        self.source_states = {}

    def process(self, queue, signal):
        source, pulse, _ = signal
        self.source_states[source] = pulse

        send = not all(self.source_states.values())
        for target in self.targets:
            queue.append((self.name, send, target))

    def set_sources(self, sources):
        for source in sources:
            self.source_states[source] = False


def get_puzzle_input():
    with open("input.txt", "r") as file:
        lines = file.readlines()

    modules = {}

    for line in lines:
        module, targets = line.strip().split(" -> ")
        if module == "broadcaster":
            modules["broadcaster"] = Broadcaster(targets.split(", "))
        elif module.startswith("%"):
            modules[module[1:]] = FlipFlop(module[1:], targets.split(", "))
        elif module.startswith("&"):
            modules[module[1:]] = Conjunction(module[1:], targets.split(", "))

    for module in modules.values():
        if isinstance(module, Conjunction):
            sources = [m.name for m in modules.values() if module.name in m.targets]
            module.set_sources(sources)

    return modules


def first_puzzle():
    modules = get_puzzle_input()
    signals = [0, 0]

    for _ in range(1000):
        queue = [("button", False, "broadcaster")]
        while queue:
            source, pulse, target = queue.pop(0)

            signals[int(pulse)] += 1

            if target in modules:
                modules[target].process(queue, (source, pulse, target))

    result = math.prod(signals)
    print(f"Puzzle 1: {result}")


def search(search_signal):
    modules = get_puzzle_input()
    for i in itertools.count(start=1):
        queue = [("button", False, "broadcaster")]
        while queue:
            source, pulse, target = queue.pop(0)

            if (source, pulse, target) == search_signal:
                return i

            if target in modules:
                modules[target].process(queue, (source, pulse, target))


def second_puzzle():
    result = math.lcm(*[search((source, True, "qb")) for source in ("kv", "jg", "rz", "mr")])
    print(f"Puzzle 2: {result}")


if __name__ == "__main__":
    first_puzzle()
    second_puzzle()