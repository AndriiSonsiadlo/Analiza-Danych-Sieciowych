import collections
import functools

import haversine

from Heap import Heap, HeuristicHeap
from models import Route
from src.utils import timeit


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
    def load(cls, flights, airports, n: int = 1_000_000):
        """Return a populated Graph object with real airports and routes."""

        world = cls()

        flights

        for i, flight in enumerate(flights):

            try:
                origin = airports[flight.origin]
                destination = airports[flight.destination]
                world.connect(origin, destination)
                if i == n:
                    break
                # Ignore flights to or from an unknown airport
            except KeyError:
                continue
        return world

    @staticmethod
    @functools.lru_cache()
    def get_distance(origin, destination):
        # Haversine distance, in kilometers
        point1 = origin.latitude, origin.longitude,
        point2 = destination.latitude, destination.longitude
        distance = haversine.haversine(point1, point2)
        return distance

    @staticmethod
    def get_price(distance, cents_per_km=0.1):
        return distance * cents_per_km

    @timeit
    def dijkstra(self, origin, destination):
        """Use Dijkstra's algorithm to find the cheapest path."""

        print(f"{' Dijkstra algorithm ':-^40}")

        routes = Heap()
        for neighbor in self.neighbors(origin):
            distance = self.get_distance(origin, neighbor)
            routes.push(Route(distance=distance, path=[origin, neighbor]))

        visited = set()
        visited.add(origin)

        number_of_checks = 0
        while routes:
            number_of_checks += 1
            # Find the nearest yet-to-visit airport
            distance, path = routes.pop()
            airport = path[-1]
            if airport in visited:
                continue

            # We have arrived! Wo-hoo!
            if airport is destination:
                return distance, path, number_of_checks

            # Tentative distances to all the unvisited neighbors
            for neighbor in self.neighbors(airport):
                if neighbor not in visited:
                    # Total spent so far plus the distance of getting there
                    new_distance = distance + self.get_distance(airport, neighbor)
                    new_path = path + [neighbor]
                    routes.push(Route(new_distance, new_path))

            visited.add(airport)
        return float('infinity'), None, 0

    @timeit
    def a_star(self, origin, destination):
        """Use A* algorithm to find the cheapest path."""

        print(f"{' A* algorithm ':-^40}")

        routes = HeuristicHeap()
        for neighbor in self.neighbors(origin):
            distance = self.get_distance(origin, neighbor)
            routes.push(Route(distance=distance, path=[origin, neighbor]), destination=destination)

        visited = set()
        visited.add(origin)

        checks_number = 0
        while routes:
            checks_number += 1

            # Find the nearest yet-to-visit airport
            distance, path = routes.pop()
            airport = path[-1]
            if airport in visited:
                continue

            # We have arrived! Wo-hoo!
            if airport is destination:
                return distance, path, checks_number

            # Tentative distances to all the unvisited neighbors
            for neighbor in self.neighbors(airport):
                if neighbor not in visited:
                    # Total spent so far plus the price of getting there
                    new_distance = distance + self.get_distance(airport, neighbor)
                    new_path = path + [neighbor]
                    routes.push(Route(new_distance, new_path), destination=destination)
            visited.add(airport)

        return float('infinity'), None, 0
