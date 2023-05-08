import collections
import functools

import haversine

from Heap import Heap, HeuristicHeap
from models import Route


class Graph:
    """ A hash-table implementation of an undirected graph."""

    def __init__(self):
        # Map each node to a set of nodes connected to it
        self._neighbors = collections.defaultdict(set)

    def connect(self, node1, node2):
        self._neighbors[node1].add(node2)
        self._neighbors[node2].add(node1)

    def neighbors(self, node):
        yield from self._neighbors[node]

    @classmethod
    def load(cls, flights, airports):
        """Return a populated Graph object with real airports and routes."""

        world = cls()
        for flight in flights:
            try:
                origin = airports[flight.origin]
                destination = airports[flight.destination]
                world.connect(origin, destination)
            # Ignore flights to or from an unknown airport
            except KeyError:
                continue
        return world

    @staticmethod
    @functools.lru_cache()
    def get_price(origin, destination, cents_per_km=0.1):
        """Return the cheapest flight without stops."""

        # Haversine distance, in kilometers
        point1 = origin.latitude, origin.longitude,
        point2 = destination.latitude, destination.longitude
        distance = haversine.haversine(point1, point2)
        return distance * cents_per_km

    def dijkstra(self, origin, destination):
        """Use Dijkstra's algorithm to find the cheapest path."""

        routes = Heap()
        for neighbor in self.neighbors(origin):
            price = self.get_price(origin, neighbor)
            routes.push(Route(price=price, path=[origin, neighbor]))

        visited = set()
        visited.add(origin)

        while routes:

            # Find the nearest yet-to-visit airport
            price, path = routes.pop()
            airport = path[-1]
            if airport in visited:
                continue

            # We have arrived! Wo-hoo!
            if airport is destination:
                return price, path

            # Tentative distances to all the unvisited neighbors
            for neighbor in self.neighbors(airport):
                if neighbor not in visited:
                    # Total spent so far plus the price of getting there
                    new_price = price + self.get_price(airport, neighbor)
                    new_path = path + [neighbor]
                    routes.push(Route(new_price, new_path))

            visited.add(airport)

        return float('infinity'), None

    def a_star(self, origin, destination):
        """Use Dijkstra's algorithm to find the cheapest path."""

        routes = HeuristicHeap()
        for neighbor in self.neighbors(origin):
            price = self.get_price(origin, neighbor)
            routes.push(Route(price=price, path=[origin, neighbor]), destination=destination)

        visited = set()
        visited.add(origin)

        while routes:

            # Find the nearest yet-to-visit airport
            price, path = routes.pop()
            airport = path[-1]
            if airport in visited:
                continue

            # We have arrived! Wo-hoo!
            if airport is destination:
                return price, path

            # Tentative distances to all the unvisited neighbors
            for neighbor in self.neighbors(airport):
                if neighbor not in visited:
                    # Total spent so far plus the price of getting there
                    new_price = price + self.get_price(airport, neighbor)
                    new_path = path + [neighbor]
                    routes.push(Route(new_price, new_path), destination=destination)

            visited.add(airport)

        return float('infinity'), None
