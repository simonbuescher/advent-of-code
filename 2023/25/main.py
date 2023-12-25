from collections import defaultdict

import matplotlib.pyplot as plt
import networkx


def get_puzzle_input():
    graph = defaultdict(lambda: [])
    with open("input.txt", "r") as file:
        for source, targets in [line.strip().split(": ") for line in file.readlines()]:
            graph[source].extend(targets.split())
    return graph


def draw_graph(graph):
    g = networkx.Graph()
    g.add_nodes_from(graph.keys())
    for node in graph:
        for target in graph[node]:
            g.add_edge(node, target)

    networkx.draw(g, with_labels=True)

    ax = plt.gca()
    ax.margins(0.1)
    plt.axis("off")
    plt.show()


def get_size(graph, start):
    open_set = [start]
    visited = set()

    while open_set:
        current = open_set.pop(0)
        visited.add(current)
        for n in set(graph[current]) | {source for source in graph if current in graph[source]}:
            if n not in visited:
                open_set.append(n)

    return len(visited)


def first_puzzle():
    graph = get_puzzle_input()

    draw_graph(graph)

    remove = [("hrs", "mnf"), ("sph", "rkh"), ("nnl", "kpc")]
    for source, target in remove:
        if target in graph[source]:
            graph[source].remove(target)
        else:
            graph[target].remove(source)

    draw_graph(graph)

    result = get_size(graph, remove[0][0]) * get_size(graph, remove[0][1])
    print(f"Puzzle 1: {result}")


if __name__ == "__main__":
    first_puzzle()  # Puzzle 1: 614655
    # Puzzle 2: some vague figure repaired a machine or something, so we only needed 49 stars.
    # for some reason we still got 50 on the board...
