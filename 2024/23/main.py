import itertools


def get_puzzle_input():
    with open("input.txt", "r") as file:
        edges = {tuple(line.split("-")) for line in file.read().split("\n")}
        return set(itertools.chain.from_iterable((edge, (edge[1], edge[0])) for edge in edges))


def first_puzzle():
    edges = get_puzzle_input()

    results = set()
    for edge in edges:
        for other in edges:
            if edge == other or edge[0] != other[0]:
                continue

            if (edge[1], other[1]) in edges:
                results.add(tuple(sorted((edge[0], edge[1], other[1]))))

    t_results = {c for c in results if any(c[i][0] == "t" for i in range(3))}
    return len(t_results)


def second_puzzle():
    edges = get_puzzle_input()

    max_clique = set()
    max_size = 0

    nodes = {edge[0] for edge in edges}
    for node in nodes:
        clique = {node}
        for other in nodes:
            if node == other:
                continue

            if all((other, node_in_clique) in edges for node_in_clique in clique):
                clique.add(other)

        if len(clique) > max_size:
            max_clique = clique
            max_size = len(clique)

    return ",".join(sorted(max_clique))


if __name__ == "__main__":
    print("Puzzle 1:", first_puzzle())  # Puzzle 1: 1337
    print("Puzzle 2:", second_puzzle())  # Puzzle 2: aw,fk,gv,hi,hp,ip,jy,kc,lk,og,pj,re,sr
