import operator

operations = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}

with open("input.txt", "r") as file:
    init_str, connections_str = file.read().split("\n\n")

    init_values = {s[:3]: bool(int(s[-1])) for s in init_str.split("\n")}
    connections = {s[-1]: (s[1], s[0], s[2]) for s in [l.split() for l in connections_str.split("\n")]}


def evaluate(operand):
    if operand in init_values:
        return init_values[operand]

    else:
        op, left, right = connections[operand]
        return operations[op](evaluate(left), evaluate(right))


def next_gates_are(node, expected):
    gates = [op for op, left, right in connections.values() if node in (left, right)]
    return sorted(gates) == expected


def first_puzzle():
    outputs = list(sorted(k for k in connections.keys() if k[0] == "z"))
    results = [evaluate(z) for z in outputs]
    result = sum(v * (2 ** i) for i, v in enumerate(results))
    return result


def second_puzzle():
    # gates build this adder: https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Full-adder_logic_diagram.svg
    # search for all connections that do not match this adder format
    wrong_connections = set()
    for k, (op, left, right) in connections.items():
        if any((
                # XOR is either an OUTPUT or has two INPUT as operands and has 2 next gates (AND and XOR)
                op == "XOR" and not (k[0] == "z" or ((left[0] in "xy" and right[0] in "xy") and next_gates_are(k, ["AND", "XOR"]))),
                # OR always as 2 next gates (AND and XOR)
                op == "OR" and not next_gates_are(k, ["AND", "XOR"]),
                # AND always has just one next gate (OR)
                op == "AND" and not next_gates_are(k, ["OR"]),
        )):
            wrong_connections.add(k)

    # first two and last OUTPUT are different from middle ones
    # first carry is different from middle ones
    # remove them from output
    wrong_connections -= {"z00", "z01", "z45", "mjh"}
    return ",".join(sorted(wrong_connections))


if __name__ == "__main__":
    print("Puzzle 1:", first_puzzle())  # Puzzle 1: 45923082839246
    print("Puzzle 2:", second_puzzle())  # Puzzle 2: jgb,rkf,rrs,rvc,vcg,z09,z20,z24
