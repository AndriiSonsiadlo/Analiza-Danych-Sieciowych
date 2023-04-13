class Graph:

    def __init__(self, vertices):

        self.V = vertices  # całkowita liczba wierzchołków w grafie

        self.graph = []  # lista wierzchołków

    # Dodanie krawędzi między wierzchołkami a i b o wadze c.
    def add_edge(self, a, b, c):

        self.graph.append([a, b, c])

    # Wyprintowanie rozwiązania

    def solution(self, distance):

        print("Odległość wierzchołka od źródła")

        for i in range(self.V):
            print("{0}\t\t{1}".format(i, distance[i]))

    def bellman_ford(self, src):

        distance = [float("Inf")] * self.V  # lista distance, która przechowuje odległość wierzchołka src od każdego innego wierzchołka w grafie

        distance[src] = 0  # Odległość od wierzchołka src do samego siebie

        for _ in range(self.V - 1):

            for a, b, c in self.graph:

                if distance[a] != float("Inf") and distance[a] + c < distance[b]:
                    distance[b] = distance[a] + c

        # sprawdzenie, czy istnieje ujemny cykl w grafie
        for a, b, c in self.graph:

            if distance[a] != float("Inf") and distance[a] + c < distance[b]:
                print("Graph contains negative weight cycle")

                return

        self.solution(distance)


# graf o 4 wierzchołkach z 5 krawędziami

'''
W tym przykładzie, graf ma 4 wierzchołki (oznaczone liczbami 0-3), a krawędzie między nimi mają różne wagi. Pierwsza krawędź ma wagę 5 i łączy wierzchołki 0 i 1. Druga krawędź ma wagę 3 i łączy wierzchołki 0 i 2. Krawędź między wierzchołkami 1 i 2 ma wagę 2, a krawędź między wierzchołkami 1 i 3 ma wagę 6. Ostatnia krawędź ma wagę 7 i łączy wierzchołki 2 i 3.
'''

g = Graph(4)

g.add_edge(0, 1, 5)

g.add_edge(0, 2, 3)

g.add_edge(1, 2, 2)

g.add_edge(1, 3, 6)

g.add_edge(2, 3, 7)

# bellman ford z wierzchołka 0
print(g.bellman_ford(0))
