class Op:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def calc(self):
        left_result, right_result = self.left.calc(), self.right.calc()

        if isinstance(left_result, Leaf) and isinstance(right_result, Leaf):
            if self.op == "+":
                return Leaf(left_result.value + right_result.value)
            elif self.op == "-":
                return Leaf(left_result.value - right_result.value)
            elif self.op == "*":
                return Leaf(left_result.value * right_result.value)
            elif self.op == "/":
                return Leaf(left_result.value // right_result.value)
            else:
                raise ValueError(f"unknown op {self.op} in node {self}")

        else:
            return Op(self.op, left_result, right_result)

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"


class Leaf:
    def __init__(self, value):
        self.value = value

    def calc(self):
        return self

    def __repr__(self):
        return repr(self.value)


class Var:
    def __init__(self, name):
        self.name = name

    def calc(self):
        return self

    def __repr__(self):
        return self.name


def parse_puzzle_input(ignore_human=True):
    with open("input.txt", "r") as file:
        content = file.read().strip()

    def parse_line(line):
        name, calc = line.split(": ")
        calc_parts = calc.split(" ")

        if name == "humn" and not ignore_human:
            return name, Var(name)

        if len(calc_parts) == 1:
            return name, Leaf(int(calc_parts[0]))
        else:
            return name, Op(calc_parts[1], Var(calc_parts[0]), Var(calc_parts[2]))

    nodes = [parse_line(row) for row in content.split("\n")]
    op_nodes = [(name, node) for name, node in nodes if isinstance(node, Op)]
    interests = {name: [] for name, _ in nodes}
    for _, op_node in op_nodes:
        interests[op_node.left.name].append(op_node)
        interests[op_node.right.name].append(op_node)

    for name, node in nodes:
        interested_nodes = interests[name]
        for interested_node in interested_nodes:
            if isinstance(interested_node.left, Var) and interested_node.left.name == name:
                interested_node.left = node
            else:
                interested_node.right = node

    root_node = [node for name, node in nodes if name == "root"][0]
    return root_node


def calculate_human_value(current, value):
    reverse_ops = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*"
    }

    while not isinstance(current, Var):
        leaf_is_left = isinstance(current.left, Leaf)
        leaf = current.left if leaf_is_left else current.right

        # division and subtraction are not commutative and need special treatment
        if current.op == "/" and leaf_is_left:
            value = Op("/", leaf, value).calc()

        elif current.op == "-" and leaf_is_left:
            value = Op("-", leaf, value).calc()

        else:
            value = Op(reverse_ops[current.op], value, leaf).calc()

        current = current.right if leaf_is_left else current.left

    return value


def first_puzzle():
    root = parse_puzzle_input()
    print(f"Puzzle 1 Answer: {root.calc()}")


def second_puzzle():
    root = parse_puzzle_input(ignore_human=False)
    root = root.calc()

    current_node = root.left if isinstance(root.left, Op) else root.right
    current_value = root.left if isinstance(root.left, Leaf) else root.right

    result = calculate_human_value(current_node, current_value)
    print(f"Puzzle 2 Answer: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1 Answer: 331120084396440
    second_puzzle()  # Puzzle 2 Answer: 3378273370680
