# Description: This program implements the Bellman-Ford algorithm to find the shortest path from a source node to all other nodes in a graph.
from pprint import pprint


class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbors_distance: dict[str:int] = dict()

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'

    def __lt__(self, other):
        return self.name < other.name


class Edge:
    def __init__(self, source: Node, destination: Node, weight: int):
        self.source = source
        self.destination = destination
        self.weight = weight

    def __str__(self):
        return f'{self.source} -> {self.destination} ({self.weight})'


class Graph:
    def __init__(self):
        self.edges = []

    @property
    def nodes(self):
        nodes = []
        for edge in self.edges:
            nodes.extend([edge.source, edge.destination])
        return list(set(nodes))

    def add_edge(self, edge: Edge):
        self.edges.append(edge)

    def build_graph(self):
        for node in self.nodes:
            for neighbor in self.nodes:
                if neighbor != node:
                    node.neighbors_distance[neighbor] = float('inf')
            node.neighbors_distance = dict(sorted(node.neighbors_distance.items()))
        for edge in self.edges:
            edge.source.neighbors_distance[edge.destination] = edge.weight
            # edge.destination.neighbors_distance[edge.source] = edge.weight # Uncomment this line for undirected graphs


if __name__ == '__main__':
    a = Node('A')
    b = Node('B')
    c = Node('C')
    d = Node('D')
    e = Node('E')
    f = Node('F')

    graph = Graph()
    graph.add_edge(Edge(a, b, 6))
    graph.add_edge(Edge(a, c, 7))
    graph.add_edge(Edge(b, c, 8))
    graph.add_edge(Edge(b, d, 5))
    graph.add_edge(Edge(b, e, 1))
    graph.add_edge(Edge(c, e, 9))
    graph.add_edge(Edge(e, f, 2))
    graph.add_edge(Edge(d, f, 3))

    pprint(f'Nodes: {graph.nodes}')

    graph.build_graph()
    for node in graph.nodes:
        pprint(f"{node} -> {node.neighbors_distance}")

